import sys
import subprocess
import time
import logging

from os_detector import get_os
from intent_parser import detect_intent, extract_entities
from local_ai import (
    ai_interpret,
    ai_suggest_options,
    ai_explain,
    ai_teach,
)
from command_mapper import map_command
from executor import execute, is_interactive
from pty_executor import run_interactive
from safety import is_safe, confirm_action
from logger import log_action
from error_intelligence import explain_error
from session import Session
from ui import TerminalUI
from backup_manager import BackupManager
from config import CONFIDENCE_THRESHOLD, LOW_CONFIDENCE_FLOOR, AI_MODEL
from output_formatter import (
    format_output, 
    format_ai_insight, 
    format_ai_explanation, 
    format_ai_lesson
)

# Setup logging
logging.basicConfig(
    filename="nl_terminal.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def is_ollama_running():
    try:
        # Just check if 'ollama list' returns 0, fast check
        subprocess.run(["ollama", "list"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def looks_like_nl(sentence):
    keywords = [
        "create", "delete", "remove", "make", "move", "copy",
        "show", "list", "where", "go", "open",
        "explain", "teach", "how",
        "change", "switch", "set", "read", "check", "what",
        "install", "update", "upgrade"
    ]
    return any(k in sentence.lower() for k in keywords)


def run_ui():
    os_type = get_os()
    session = Session()
    ui = TerminalUI(session.mode, os_type)
    backup_manager = BackupManager()

    ui.welcome_screen()
    
    if not is_ollama_running():
        ui.print_warning("Ollama is not running. AI features will fail.")
        ui.print_info("Please start Ollama in another terminal.")

    # ui.add_output("Type 'exit' to quit") # Included in welcome screen

    while True:
        try:
            user_input = ui.get_input().strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                ui.print_info("Goodbye!")
                break

            lower = user_input.lower()

            # MODE SWITCH
            if (
                lower.startswith("mode")
                or "change mode" in lower
                or "switch" in lower
                or "set mode" in lower
            ):
                for m in ["beginner", "expert", "safe"]:
                    if m in lower:
                        session.set_mode(m)
                        ui.update_mode(session.mode)
                        ui.print_success(f"Switched to {session.mode} mode")
                        break
                else:
                    ui.print_warning("Specify mode: beginner | expert | safe")
                continue

            # EXPLAIN / TEACH
            if lower.startswith("explain"):
                ui.print_ai_thinking()
                topic = user_input.replace("explain", "", 1).strip()
                explanation = ai_explain(topic)
                ui.print_ai_response(format_ai_explanation(explanation))
                continue

            if lower.startswith(("teach me", "learn", "how to")):
                ui.print_ai_thinking()
                topic = lower.replace("teach me", "").replace("learn", "").replace("how to", "")
                lesson = ai_teach(topic.strip())
                ui.print_ai_response(format_ai_lesson(lesson))
                continue

            # INTERACTIVE
            if is_interactive(user_input):
                ui.print_info(f"Launching interactive session: {user_input}")
                run_interactive(user_input)
                continue

            # NL COMMANDS
            if looks_like_nl(user_input):
                intent = detect_intent(user_input)
                entities = extract_entities(user_input)

                if intent == "UNKNOWN":
                    ui.print_ai_thinking()
                    ai_result = ai_interpret(user_input)
                    confidence = ai_result["confidence"]

                    if confidence < LOW_CONFIDENCE_FLOOR:
                        ui.print_warning(f"Too ambiguous (Confidence: {confidence:.2f}). Please rephrase.")
                        continue

                    if confidence < CONFIDENCE_THRESHOLD:
                        options = ai_suggest_options(user_input)
                        ui.stop_ai_thinking()
                        if not options:
                            ui.print_warning("AI was unsure and could not suggest options.")
                            continue
                            
                        ui.print_info("Did you mean:")
                        for i, opt in enumerate(options, 1):
                            ui.stream_output(f"[bold cyan]{i})[/bold cyan] {opt.get('description', 'Unknown action')}")
                        
                        choice = ui.get_input()
                        if not choice.isdigit():
                            continue
                        idx = int(choice) - 1
                        if 0 <= idx < len(options):
                            selected = options[idx]
                            intent = selected["intent"]
                            entities = selected["entities"]
                        else:
                            continue
                    else:
                        intent = ai_result["intent"]
                        entities = ai_result["entities"]
                        ui.stop_ai_thinking()

                # 🛡️ ROLLBACK
                if intent == "ROLLBACK":
                    msg = backup_manager.restore_last()
                    ui.print_success(msg)
                    log_action(user_input, intent, "ROLLBACK", "SUCCESS", msg)
                    continue

                # 🛡️ SAFETY & CONFIRMATION
                if intent in ["DELETE_FILE", "DELETE_FOLDER", "KILL_PROCESS"]:
                    # Check basic safety
                    if not is_safe(entities.get("name")):
                        ui.print_error("Action blocked by strict safety rules (system path protections).")
                        log_action(user_input, intent, "BLOCKED", "FAIL", "Strict safety block")
                        continue
                    
                    # Check user confirmation
                    action_desc = f"{intent} on {entities.get('name')}"
                    if not confirm_action(action_desc, session.mode):
                        ui.print_warning("Action aborted by user.")
                        log_action(user_input, intent, "ABORTED", "CANCEL", "User denied confirmation")
                        continue

                    # 🛡️ AUTO-BACKUP (Files only)
                    if intent == "DELETE_FILE" and entities.get("name"):
                        if backup_manager.backup_file(entities.get("name")):
                             ui.print_success(f"📦 Backup created for {entities.get('name')}")

                command = map_command(intent, os_type, entities)
                if not command:
                    ui.print_error(f"Could not map command for intent: {intent}")
                    continue

                # Handle Plugin Internal Commands
                if command.startswith("INTERNAL:"):
                    response = command.split("INTERNAL:", 1)[1]
                    ui.print_success(response)
                    log_action(user_input, intent, "PLUGIN_EXEC", "SUCCESS", response)
                    continue

                ui.print_command_execution(command)
                out, err = execute(command)
                
                # LOGGING
                status = "SUCCESS" if not err else "ERROR"
                log_action(user_input, intent, command, status, message=err[:100] if err else "OK")

                if out:
                    formatted = format_output(intent, out, os_type)
                    if formatted:
                        ui.stream_output(formatted)
                    else:
                        ui.stream_output(out)

                if err:
                    ui.print_error(err)
                    # ui.print_ai_thinking() # fast check usually
                    ui.print_ai_response(format_ai_insight(explain_error(command, err)))
                continue

            # RAW COMMAND
            ui.print_command_execution(user_input)
            out, err = execute(user_input)
            
            status = "SUCCESS" if not err else "ERROR"
            log_action(user_input, "RAW_COMMAND", user_input, status, message=err[:100] if err else "OK")
            
            if out:
                ui.stream_output(out)
            if err:
                ui.print_error(err)
                ui.print_ai_response(format_ai_insight(explain_error(user_input, err)))

        except KeyboardInterrupt:
            ui.print_info("\nUser terminated session.")
            break
        except Exception as e:
            logging.error("Crash in main loop", exc_info=True)
            ui.print_error(f"An unexpected error occurred: {str(e)}")
            ui.print_info("The error has been logged. The terminal will not crash.")

def main():
    try:
        run_ui()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Critical Startup Error: {e}")
        logging.critical("Startup violation", exc_info=True)

if __name__ == "__main__":
    main()

