"""Setup tests for this package."""
from collective.linguatags.testing import (  # noqa,
    COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING,
)
from plone.browserlayer import utils
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.linguatags is properly installed."""

    layer = COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.linguatags is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.linguatags"))

    def test_browserlayer(self):
        """Test that ICollectiveLinguatagsLayer is registered."""
        from collective.linguatags.interfaces import ICollectiveLinguatagsLayer

        self.assertIn(ICollectiveLinguatagsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product("collective.linguatags")

    def test_product_uninstalled(self):
        """Test if collective.linguatags is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.linguatags"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveLinguatagsLayer is removed."""
        from collective.linguatags.interfaces import ICollectiveLinguatagsLayer

        self.assertNotIn(ICollectiveLinguatagsLayer, utils.registered_layers())
