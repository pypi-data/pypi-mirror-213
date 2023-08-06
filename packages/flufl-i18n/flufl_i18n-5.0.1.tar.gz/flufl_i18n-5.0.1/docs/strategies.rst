==================
Catalog strategies
==================

.. currentmodule:: flufl.i18n

The way :doc:`flufl.i18n <apiref>` finds its catalog for an application is
extensible.  These are called *strategies*.  ``flufl.i18n`` comes with a
couple of fairly simple strategies.  Usually one of the built-in strategies
will be sufficient, but you can write your own strategies for finding your
catalogs.


Python package strategies
=========================

The :class:`PackageStrategy` class locates catalog files from within an
importable Python package's directory.  Inside the package directory, you
still need the `gettext`_ standard filesystem layout of
``<code>/LC_MESSAGES/<application>.mo``.

.. note::
    :doc:`As before <using>` these examples will use the faux ``xx`` language,
    and the faux ``messages`` module referred to in these examples contains the
    language code directories.

First import the Python package containing the message catalogs.

    >>> import messages

By setting the ``$LANG`` environment variable, we can specify that the
application translates into that language automatically.

    >>> import os
    >>> os.environ['LANG'] = 'xx'

Now we can instantiate a package strategy which finds its catalogs in the
``messages`` Python package.  The first argument is the application name,
which must be unique among all registered strategies.

    >>> from flufl.i18n import PackageStrategy
    >>> strategy = PackageStrategy('flufl', messages)

Once you have the strategy you need, register it with the global registry.
The registration process returns an application object which can be used to
look up language codes.

    >>> from flufl.i18n import registry
    >>> application = registry.register(strategy)

The application object keeps track of a current translation context, and
exports a method which you can bind to the underscore function in your module
globals for convenient gettext usage.

    >>> _ = application._

Now at run time, ``_()`` will always translate its string argument to the
current catalog's language.

    >>> print(_('A test message'))
    N grfg zrffntr

..
    >>> # Hack to unregister the previous strategy.
    >>> registry._registry.clear()


Simple strategy
===============

There is also a simpler strategy that uses both the ``$LANG`` environment
variable, and the ``$LOCPATH`` environment variable to set things up.
::

    >>> os.environ['LOCPATH'] = os.path.dirname(messages.__file__)

    >>> from flufl.i18n import SimpleStrategy
    >>> strategy = SimpleStrategy('flufl')
    >>> application = registry.register(strategy)

    >>> _ = application._
    >>> print(_('A test message'))
    N grfg zrffntr


Calling with zero arguments
===========================

Strategies should be prepared to accept zero arguments when called, to produce
a *default* translation (usually the :class:`gettext.NullTranslations`).
::

    >>> def get_gettext(strategy):
    ...     catalog = strategy()
    ...     return catalog.gettext

    >>> print(get_gettext(
    ...     SimpleStrategy('example'))('A test message'))
    A test message

    >>> print(get_gettext(
    ...     PackageStrategy('example', messages))('A test message'))
    A test message


.. _gettext: https://www.gnu.org/software/gettext/manual/gettext.html
