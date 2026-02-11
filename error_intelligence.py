from local_ai import run_llm

def explain_error(command, error_output):
    prompt = f"""
You are a terminal expert assistant.

A command was executed and failed.

Command:
{command}

Error output:
{error_output}

Explain:
- What the error means
- Why it happened
- One or two suggestions to fix it

Do NOT suggest dangerous commands.
Do NOT execute anything.
Keep it concise and helpful.
"""

    try:
        return run_llm(prompt)
    except Exception:
        return "AI could not analyze the error."
