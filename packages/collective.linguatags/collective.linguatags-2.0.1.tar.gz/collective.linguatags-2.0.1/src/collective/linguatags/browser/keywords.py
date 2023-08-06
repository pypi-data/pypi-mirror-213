from plone.app.layout.viewlets import ViewletBase
from zope.i18nmessageid import MessageFactory


mf = MessageFactory("linguatags")


class KeywordsViewlet(ViewletBase):
    """Return messagestrings for keywords"""

    def display_message_string(self, keyword):
        return mf(keyword)
