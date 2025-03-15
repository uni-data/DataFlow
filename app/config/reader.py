import sys

if sys.version_info >= (3, 11):
    import tomllib as toml
else:
    import toml

class ConfigReader:
    def __init__(self, config_path = 'config.toml'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, "rb") as f:
            return toml.load(f)
    def get_model_config(self):
        model_config = self.config.get("model", {})
        return {
            "name": model_config.get("name", "default-model"),
            "temperature": model_config.get("temperature", 0.7),
            "max_tokens": model_config.get("max_tokens", 256)
        }

    def get_api_config(self):
        api_config = self.config.get("api", {})
        return {
            "endpoint": api_config.get("endpoint", ""),
            "api_key": api_config.get("api_key", ""),
            "timeout": api_config.get("timeout", 10.0)
        }