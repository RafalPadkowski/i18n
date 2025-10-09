import gettext
from dataclasses import dataclass
from pathlib import Path

from loguru import logger


@dataclass
class Translation:
    default_language = "en"
    default_domain = "messages"

    localedir: Path | None = None
    _language: str = default_language
    _gnutranslations: gettext.GNUTranslations | gettext.NullTranslations = (
        gettext.NullTranslations()
    )

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str) -> None:
        """
        Set the current language.
        Create a Translations object based on the domain, localedir and language.
        """
        self._language = value

        if self._language != self.default_language:
            try:
                assert self.localedir is not None
                self._gnutranslations = gettext.translation(
                    domain=self.default_domain,
                    localedir=self.localedir,
                    languages=[self._language],
                )
            except AssertionError:
                logger.error("localedir is not initialized")
            except OSError:
                logger.error(".mo file is not found")

    def __call__(self, message: str) -> str:
        """
        Return the localized translation of message based on the current language.
        """
        if not message or self._language == self.default_language:
            return message

        return self._gnutranslations.gettext(message)


tr = Translation()
