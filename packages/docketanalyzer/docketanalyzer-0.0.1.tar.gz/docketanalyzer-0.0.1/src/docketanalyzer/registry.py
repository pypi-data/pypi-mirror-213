class BaseRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name, item):
        if name in self._registry:
            raise ValueError(f"'{name}' already exists.")
        self._registry[name] = item

    def get(self, name):
        if name not in self._registry:
            raise ValueError(f"'{name}' does not exist.")
        return self._registry[name]
    
    def all(self):
        return self._registry.values()


class CommandRegistry(BaseRegistry):
    pass


command_registry = CommandRegistry()

