class Session:
    def __init__(self):
        self.mode = "BEGINNER"

    def set_mode(self, mode):
        mode = mode.upper()
        if mode in ["BEGINNER", "EXPERT", "SAFE"]:
            self.mode = mode
            return True
        return False

    def require_preview(self):
        return self.mode in ["BEGINNER", "SAFE"]

    def require_confirmation(self, destructive=False):
        if self.mode == "EXPERT":
            return destructive
        return True

    def show_ai_insight(self):
        return self.mode != "EXPERT"
