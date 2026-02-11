import json
import re
from plugin_loader import load_plugins

with open("intents.json") as f:
    BASE_INTENTS = json.load(f)

PLUGINS = load_plugins()

def detect_intent(sentence):
    sentence = sentence.lower()

    # Base intents
    for intent, phrases in BASE_INTENTS.items():
        for phrase in phrases:
            if phrase in sentence:
                return intent

    # Plugin intents
    for plugin in PLUGINS:
        for phrase in plugin.get("phrases", []):
            if phrase in sentence:
                return plugin.get("intent")

    return "UNKNOWN"

def extract_entities(sentence):
    """
    Extracts entities using Regex patterns for meaningful capture.
    """
    sentence = sentence.lower()
    entities = {"name": None, "source": None, "destination": None}

    # 1. Movement/Copying (Source -> Destination)
    # create specific patterns first because they are more complex
    
    move_match = re.search(r'(?:move|copy|rename)\s+(.*?)\s+to\s+(.*)', sentence)
    if move_match:
        entities["source"] = move_match.group(1).strip()
        entities["destination"] = move_match.group(2).strip()
        
        # We DO NOT strip quotes here. 
        # If the user typed 'move "folder a" to b', we want source='"folder a"'.
        # This ensures the shell command receives the quotes it needs for spaces.
        
        # Clean up "file"/"folder" prefixes if they were inside the capture (unlikely due to regex greedy, but possible)
        # But we must be careful not to strip "file" from "file.txt"
        # Regex: remove prefix "file " or "folder " ONLY if valid
        
        for key in ["source", "destination"]:
            val = entities[key]
            # optional: clean up "file " prefix if not inside quotes?
            # For now, let's just keep it simple. User input is respected.
            pass
            
        return entities

    # 2. Single Name Operations (Create/Delete/Open)
    
    # Check for quoted name specifically for single-argument commands
    quoted = re.search(r'["\'](.*?)["\']', sentence)
    if quoted:
        # Use group(0) to keep the quotes!
        # "My File" -> "My File"
        start, end = quoted.span()
        # Ensure it's not just a fragment? No, we trust the quote.
        entities["name"] = sentence[start:end] 
        return entities 

    # Fallback: capture last word or phrase after keywords
    # create folder X
    match = re.search(r'(?:file|folder|dir|directory)\s+([a-zA-Z0-9_\-\.]+(?:\.[a-z]+)?)', sentence)
    if match:
        entities["name"] = match.group(1)
    
    # Upgrade/Update Packages
    upgrade_match = re.search(r'(?:upgrade|update|install update)\s+([a-zA-Z0-9_\-\.]+)', sentence)
    if upgrade_match:
        name = upgrade_match.group(1).strip()
        # prevent capturing "pip" here if possible, but command_mapper will prefer UPGRADE_PIP if intent matches
        entities["name"] = name
        return entities

    # Process Killing
    # Match longer phrases first to avoid capturing 'process' as part of the name
    kill_match = re.search(r'(?:kill process|stop program|end task|terminate|kill|stop)\s+(.*)', sentence)
    if kill_match:
        entities["name"] = kill_match.group(1).strip()
        return entities

    return entities
