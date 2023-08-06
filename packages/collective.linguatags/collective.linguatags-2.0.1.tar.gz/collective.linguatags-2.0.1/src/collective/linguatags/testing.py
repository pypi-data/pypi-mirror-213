from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2

import collective.linguatags


COLLECTIVE_LINGUATAGS_FIXTURE = PloneWithPackageLayer(
    bases=(PLONE_APP_CONTENTTYPES_FIXTURE,),
    name="CollectiveLinguatagsLayer:Fixture",
    gs_profile_id="collective.linguatags:default",
    zcml_package=collective.linguatags,
    zcml_filename="configure.zcml",
    additional_z2_products=["collective.linguatags"],
)


COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_LINGUATAGS_FIXTURE,),
    name="CollectiveLinguatagsLayer:IntegrationTesting",
)


COLLECTIVE_LINGUATAGS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_LINGUATAGS_FIXTURE,),
    name="CollectiveLinguatagsLayer:FunctionalTesting",
)
