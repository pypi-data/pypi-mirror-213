from zope.interface import Attribute
from zope.interface import Interface


class ICollectiveImmediateCreate(Interface):
    """Interface to enable immediate create status tracking.

    Also FTI needs the add information to make this work!
    """

    collective_immediatecreate = Attribute("Was this item initially saved?")
