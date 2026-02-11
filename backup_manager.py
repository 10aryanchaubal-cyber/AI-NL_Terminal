import os
import shutil
import json
import uuid
from datetime import datetime
from rich.console import Console

console = Console()

BACKUP_DIR = ".backups"
INDEX_FILE = os.path.join(BACKUP_DIR, "index.json")

class BackupManager:
    def __init__(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        if not os.path.exists(INDEX_FILE):
             with open(INDEX_FILE, "w") as f:
                 json.dump([], f)

    def _load_index(self):
        try:
            with open(INDEX_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_index(self, index):
        with open(INDEX_FILE, "w") as f:
            json.dump(index, f, indent=4)

    def backup_file(self, filepath):
        """
        Backs up a specific file before modification/deletion.
        Returns True if successful, False otherwise.
        """
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            return False

        try:
            backup_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            filename = os.path.basename(filepath)
            
            # Save the file content to .backups/<uuid>
            backup_path = os.path.join(BACKUP_DIR, backup_id)
            shutil.copy2(filepath, backup_path)

            # Update index
            index = self._load_index()
            entry = {
                "id": backup_id,
                "original_path": filepath,
                "timestamp": timestamp,
                "filename": filename
            }
            index.append(entry)
            self._save_index(index)
            
            # console.print(f"[dim]Backed up {filename}[/dim]")
            return True
        except Exception as e:
            console.print(f"[red]Backup failed: {e}[/red]")
            return False

    def restore_last(self):
        """
        Restores the last backed up file to its original location.
        """
        index = self._load_index()
        if not index:
            return "No backups found."

        # Get last entry
        last_entry = index.pop()
        backup_id = last_entry["id"]
        original_path = last_entry["original_path"]
        backup_path = os.path.join(BACKUP_DIR, backup_id)

        if not os.path.exists(backup_path):
            self._save_index(index) # Save the popped state anyway
            return "Backup file missing from storage."

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            
            # Restore
            shutil.copy2(backup_path, original_path)
            
            # Clean up backup ?? Or keep it? 
            # Usually strict undo removes the undo stack item, but keeping it is safer.
            # For this "undo" command, let's treat it as a reversion. We can keep the backup file but remove from index or keep history.
            # Let's remove it from index to "undo" the action effectively in the stack sense.
            self._save_index(index)
            
            # Optional: delete the blob to save space?
            # os.remove(backup_path) 
            
            return f"Restored {os.path.basename(original_path)}"
        except Exception as e:
            return f"Restore failed: {e}"
