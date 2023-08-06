from BTrees.OOBTree import OOBTree
from plone import api
from zope.annotation.interfaces import IAnnotations


STORAGE_KEY = "collective.linguatags"


def get_storage(rw=False):
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    if rw and STORAGE_KEY not in annotations:
        annotations[STORAGE_KEY] = OOBTree()
    return annotations.get(STORAGE_KEY, {})
