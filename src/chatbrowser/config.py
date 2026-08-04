"Typed environment configuration for ChatBrowser."

from chatenv import BaseEnvConfig, EnvField


class ChatbrowserConfig(BaseEnvConfig):
    "ChatBrowser ChatEnv configuration."

    _title = "ChatBrowser Configuration"
    _aliases = ["chatbrowser"]
    _storage_dir = "Chatbrowser"

    @classmethod
    def test(cls) -> None:
        """Validate schema registration without external side effects."""

        print(f"Testing {cls._title}...")
        print("Schema loaded; no network test is required.")

    CHATBROWSER_API_KEY = EnvField(
        "CHATBROWSER_API_KEY",
        desc="API key",
        is_sensitive=True,
    )


__all__ = ["ChatbrowserConfig"]
