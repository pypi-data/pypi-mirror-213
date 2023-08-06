.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.linguatags
==============================================================================

Multilingual Tags for Plone

Features
--------

- tags are entered in one canonical language
- a tag is turned into a message id
- collective.linguatags provide an own i18n domain 'linguatags'
- all messages in this domain are translatable ttw with a controlpanel
- view/viewlets showing tags are overridden to show the translated tag


Installation
------------

Install collective.linguatags by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.linguatags


and then running ``bin/buildout``


Contribute
----------

.. image:: https://travis-ci.org/collective/collective.linguatags.svg?branch=master
    :target: https://travis-ci.org/collective/collective.linguatags

.. image:: https://coveralls.io/repos/github/collective/collective.linguatags/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.linguatags?branch=master


- Issue Tracker: https://github.com/collective/collective.linguatags/issues
- Source Code: https://github.com/collective/collective.linguatags


We'd be happy to see many commits, forks and pull-requests to make collective.linguatags even better.

If you are having issues, please let us know. `Open an issue <http://github.com/collective/collective.linguatags/issues>`_ or send us an e-mail to dev@bluedynamics.com.


License
-------

The project is licensed under the GPLv2.
