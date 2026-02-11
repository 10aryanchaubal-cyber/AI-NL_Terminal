from datetime import datetime
from plugin_interface import Plugin

class TimePlugin(Plugin):
    @property
    def name(self) -> str:
        return "TimePlugin"

    @property
    def description(self) -> str:
        return "Tells the current date and time."

    @property
    def intents(self) -> list:
        return ["CHECK_TIME", "CHECK_DATE"]

    def execute(self, intent: str, entities: dict, os_type: str) -> str:
        now = datetime.now()
        if intent == "CHECK_TIME":
            return f"INTERNAL:The current time is {now.strftime('%H:%M:%S')}."
        if intent == "CHECK_DATE":
            return f"INTERNAL:Today's date is {now.strftime('%Y-%m-%d')}."
        return "INTERNAL:Unknown intent for TimePlugin."
