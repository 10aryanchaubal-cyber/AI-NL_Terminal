from rich.prompt import Confirm

def is_safe(entity=None):
    dangerous = ["C:\\", "C:/", "Windows", "System32", "/"]
    
    # Block root or system folders immediately
    if entity:
        # Check for strict matches or containment
        norm = entity.replace("/", "\\").lower()
        for d in dangerous:
            d_norm = d.replace("/", "\\").lower()
            if d_norm == norm or (len(norm) < 4 and norm.endswith(":")): # Block C: or D:
                return False
            if "windows\\system32" in norm:
                return False

    return True

def confirm_action(action_desc, mode):
    """
    Asks for user confirmation based on mode.
    - Safe: Always ask
    - Beginner: Ask for deletions/modifications
    - Expert: Only ask for very dangerous things (system files) - but here mostly trusting logic
    """
    if mode == "safe":
        return Confirm.ask(f"[bold red]SAFETY CHECK:[/bold red] Are you sure you want to {action_desc}?")
    
    if mode == "beginner":
        return Confirm.ask(f"[yellow]Confirm:[/yellow] Do you want to {action_desc}?")
        
    return True # Expert mode defaults to yes basically, or handled elsewhere

