"""
Facilitating Internationalization and Localization.

This module assists internationalization (i18n) and localization (L10n) processes.
It helps to adapt software to various languages, regional nuances, and technical requirements of a target locale.
This adaptation is achieved by externalizing all strings and marking them for translation, usually by wrapping them in a
function, named simply as an underscore (`_`). The core function in this module is gettext, which returns the hard-coded
translations for these strings.
The function {py:func}`set_language` further enables the selection of the desired language for the application, thus
ensuring smooth multilingual operation.

::::{admonition} Example
:class: example dropdown

Declare a string that is to be translated as follows:
```python
from optool.languages import gettext as _

my_translated_str = _("A sentence to translate")
```
"""

import gettext as _gettext
import locale
from pathlib import Path

from optool.logging import LOGGER

_TRANSLATOR = None


def gettext(message):
    """
    Returns the translation of a given message.

    If no translation is found for the current language, a warning is logged and the original message is returned.

    :param message: The string to be translated.
    :return: The translated string if found in the language catalog, else the original string.
    """

    if _TRANSLATOR is None:
        return _gettext.gettext(message)

    # noinspection PyUnresolvedReferences
    info = _TRANSLATOR.info()
    # noinspection PyProtectedMember,PyUnresolvedReferences
    catalog = _TRANSLATOR._catalog
    if message not in catalog:
        LOGGER.warning("The message {!r} is not present in the catalog of the currently selected language {!r}.",
                       message, info["language"])
    elif catalog[message] == "":
        LOGGER.warning("The translation for the message {!r} for the currently selected language {!r} is missing.",
                       message, info["language"])

    # noinspection PyUnresolvedReferences
    return _TRANSLATOR.gettext(message)


def set_language(language: str, locale_directory: Path):
    """
    Sets the language for the application and loads the corresponding translation catalog.

    :param language: The language to be set. It should correspond to one of the locales available in the locale
        directory.
    :param locale_directory: The path to the directory containing the locale files for different languages.
    """

    locale.setlocale(locale.LC_ALL, language)

    global _TRANSLATOR
    _TRANSLATOR = _gettext.translation('messages', localedir=str(locale_directory), languages=[language])
