from collective.linguatags import _
from collective.linguatags.storage import get_storage
from persistent.dict import PersistentDict
from plone import api
from plone.i18n.normalizer.base import mapUnicode
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import re


num_sort_regex = re.compile(r"\d+")


def zero_fill(matchobj):
    return matchobj.group().zfill(4)


def sort_func(value):
    if not isinstance(value, str):
        return value
    # Ignore case, normalize accents, strip spaces
    value = mapUnicode(safe_unicode(value)).lower().strip()
    # Replace numbers with zero filled numbers
    value = num_sort_regex.sub(zero_fill, value)
    return value.encode("utf-8")


class LinguaTagsControlPanel(BrowserView):
    """Control panel for the portal actions."""

    template = ViewPageTemplateFile("controlpanel.pt")

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.storage = get_storage(rw=self.request.form.get("submitted", False))

    def available_languages(self):
        return sorted(api.portal.get_registry_record("plone.available_languages"))

    def tags(self):
        catalog = api.portal.get_tool("portal_catalog")
        index = catalog._catalog.getIndex("Subject")
        yield from sorted(index._index, key=sort_func)

    def translation(self, tag, language):
        return self.storage.get(tag, {}).get(language, "")

    def __call__(self):
        if self.request.form.get("submitted", False):
            for tag in self.tags():
                value = self.request.form.get(tag, None)
                if value is None:
                    continue
                translations = self.storage.get(tag, None)
                if translations is None:
                    self.storage[tag] = PersistentDict()
                for lang in value:
                    if lang not in self.available_languages():
                        continue
                    self.storage[tag][lang] = value[lang]
                api.portal.show_message(_("Translations saved"), request=self.request)
        return self.template()
