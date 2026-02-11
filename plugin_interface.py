from abc import ABC, abstractmethod

class Plugin(ABC):
    """
    Abstract base class for NL-Terminal plugins.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of what the plugin does"""
        pass

    @property
    @abstractmethod
    def intents(self) -> list:
        """List of intents this plugin handles"""
        pass

    @abstractmethod
    def execute(self, intent: str, entities: dict, os_type: str) -> str:
        """
        Execute the logic for the given intent.
        
        Returns:
            str: The command or output to be displayed/executed.
                 If it returns a string starting with "EXEC:", the terminal will run it as a system command.
                 Otherwise, it returns the string as output.
        """
        pass
