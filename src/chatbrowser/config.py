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
        print("Schema loaded; browser runtime checks are handled by `chatbrowser doctor`.")

    CHATBROWSER_DEFAULT_BACKEND = EnvField(
        "CHATBROWSER_DEFAULT_BACKEND",
        desc="Default browser backend name, for example chrome-for-testing",
        default="chrome-for-testing",
    )
    CHATBROWSER_REGISTRY_HOME = EnvField(
        "CHATBROWSER_REGISTRY_HOME",
        desc="Optional ChatBrowser metadata root override; normally leave unset to use ChatArch home",
    )


__all__ = ["ChatbrowserConfig"]
