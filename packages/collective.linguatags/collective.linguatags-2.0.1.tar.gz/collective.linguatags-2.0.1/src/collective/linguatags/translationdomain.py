from collective.linguatags.storage import get_storage
from plone import api
from zope.component import getUtility
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer


@implementer(ITranslationDomain)
class TagsTranslationDomain:

    domain = "linguatags"

    def translate(
        self,
        msgid,
        mapping=None,
        context=None,
        target_language=None,
        default=None,
        msgid_plural=None,
        default_plural=None,
        number=None,
    ):

        msgkey = msgid
        storage = get_storage()
        translations = storage.get(msgkey, None)

        if translations is None:
            # handle default
            if default is None:
                default = msgid
            return default

        # find out what the target language should be
        if target_language is None and context is not None:
            langs = api.portal.get_registry_record("plone.available_languages")
            negotiator = getUtility(INegotiator)
            target_language = negotiator.getLanguage(langs, context)

        # fetch matching translation or default
        message = translations.get(target_language, default)
        return message
