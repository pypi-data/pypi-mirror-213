============================
Using the flufl.i18n library
============================

.. currentmodule:: flufl.i18n

There are two ways that your application can set up translations to use
:doc:`flufl.i18n <apiref>`.  The simple initialization will work for most
applications, where there is only one *language context* for the entire run of
the application, such as for a command line tool.  The more complex
initialization works well for applications like servers that may want to use
multiple language contexts during their execution.


Single language contexts
========================

If your applicationonly needs one language context for its entire execution
(such as a command line tool), you can use the simple API to set things up.

    >>> from flufl.i18n import initialize

The library by default uses the ``$LANG`` and ``$LOCPATH`` environment
variables to set things up.

As environment variables, ``$LANG`` sets the language code and ``$LOCPATH``
sets the directory containing containing the translation catalogs with the
language codes as subdirectories.  Python's :mod:`gettext` module provides
more detail about the underlying organization and technology.

.. note::
    In these examples, we're using a faux language with a code of ``xx``.
    For demonstration purposes, the ``xx`` language is just the `rot13
    <https://en.wikipedia.org/wiki/ROT13>`_ of the original source string.
    The faux ``messages`` module referred to in these examples contains these
    language code directories.

::

    >>> import os
    >>> # Import the Python package containing all the translations.
    >>> import messages

    >>> os.environ['LANG'] = 'xx'
    >>> os.environ['LOCPATH'] = os.path.dirname(messages.__file__)

Now you just need to call the :meth:`initialize()` function, passing in the
application's name, and you'll get an object back that you can bind to the
local ``_()`` function for run-time translations.  Note that using ``_()``
isn't required, but it's a widely-used convention, derived from the `GNU
gettext <https://www.gnu.org/software/gettext/>`_ model.

    >>> _ = initialize('flufl')
    >>> print(_('A test message'))
    N grfg zrffntr

It's probably best to just share this function through imports, but it does no
harm to call :meth:`initialize()` again.

    >>> _ = initialize('flufl')
    >>> print(_('A test message'))
    N grfg zrffntr

..
    >>> # Unregister the application domain used earlier.  Also, clear the
    >>> # environment settings from above.
    >>> from flufl.i18n import registry
    >>> registry._registry.clear()
    >>> del os.environ['LANG']
    >>> del os.environ['LOCPATH']


Multiple language contexts
==========================

Some applications, such as servers, are more complex; they need multiple
language contexts during their execution.  To support this, there is a global
registry of catalog searching :doc:`strategies <strategies>`.  When a
particular language code is specified, a strategy is used to find the catalog
that provides that language's translations.

:doc:`flufl.i18n <apiref>` comes with a couple of fairly simple strategies,
and you can implement your own.  A convenient built-in strategy looks up
catalogs from within a directory using GNU gettext conventions, where the
directory is an importable Python package (such as our ``messages`` example).

    >>> from flufl.i18n import PackageStrategy
    >>> strategy = PackageStrategy('flufl', messages)

The first argument is the application name, which must be unique among all
registered strategies.  The second argument is the package under which the
translations can be found.

Once you have the desired strategy, register this with the global registry.
The registration process returns an application object which can be used to
look up language codes.

    >>> from flufl.i18n import registry
    >>> application = registry.register(strategy)

The application object keeps track of the current *translation context*,
essentially a stack of languages.  This object also exports a method which you
can bind to the ``_()`` function, usually in your module globals.  This
underscore function always returns translations in the language at the top of
the stack.  I.e., at run time, ``_()`` will always translate its string
argument to the current context's language.

    >>> _ = application._

By default the application just returns the original source string; i.e. it is
a null translator.

    >>> print(_('A test message'))
    A test message

And it has no language code.

    >>> print(_.code)
    None

You can temporarily *push* a new language context to the top of the stack, so
that the same underscore function will now return translations in the new
language context.

    >>> _.push('xx')
    >>> print(_.code)
    xx
    >>> print(_('A test message'))
    N grfg zrffntr

Pop the current language to return to the default.  Once you're at the bottom
of the stack, more pops will just give you the *default translation*.
Normally, that's the null translation, but as you'll see below, you can change
that too.

    >>> _.pop()
    >>> print(_.code)
    None
    >>> print(_('A test message'))
    A test message
    >>> _.pop()
    >>> print(_.code)
    None
    >>> print(_('A test message'))
    A test message


Context manager
===============

To make all of this more convenient, the underscore method has a context
manager called :meth:`~RuntimeTranslator.using()` which temporarily sets a new
language inside a ``with`` statement.
::

    >>> print(_('A test message'))
    A test message

    >>> with _.using('xx'):
    ...     print(_('A test message'))
    N grfg zrffntr

    >>> print(_('A test message'))
    A test message

These ``with`` statements are nestable.

.. note::
    The ``yy`` language is another faux translation, where the source string
    is reversed.

Here we can see that the outer context translates the source string
differently than the inner context.
::

    >>> with _.using('xx'):
    ...     print(_('A test message'))
    ...     with _.using('yy'):
    ...         print(_('A test message'))
    ...     print(_('A test message'))
    N grfg zrffntr
    egassem tset A
    N grfg zrffntr

    >>> print(_('A test message'))
    A test message


The default language context
============================

As mentioned above, the default language context, i.e. the `Yertle`_ at the
bottom of the stack is, by default, the null translation.  The null
translation just returns the source string unchanged.  You can set the default
language context at the bottom of the stack.
::

    >>> _.default = 'xx'
    >>> print(_('A test message'))
    N grfg zrffntr

    >>> _.pop()
    >>> print(_.code)
    xx

    >>> print(_('A test message'))
    N grfg zrffntr

    >>> with _.using('yy'):
    ...     print(_('A test message'))
    egassem tset A

    >>> print(_('A test message'))
    N grfg zrffntr

You can reset the default back to the null context by ``del``-ing the
:data:`~RuntimeTranslator.default` attribute.
::

    >>> del _.default
    >>> print(_.code)
    None


Substitutions and placeholders
==============================

Once you have an underscore function, using the library is very simple.  You
just call ``_()`` passing in the source string you want to translate.  What if
your source strings can't be static literals, because you need them to contain
substitutions calculated at run time?  You need to define some placeholders in
your source string, so that the run time substitutions will be inserted there.
Further complicating matters, some languages need to change the order of
placeholders in their translations.  In general, it's good practice for your
source strings to be complete sentences, because that is easier for all your
human translaters to ... translate!

To support this, you use `PEP 292`_ style ``$``-substitution strings inside
the underscore function.  These strings contain ``$variables`` and when
translated, run time data is inserted into these variables.  The substitutions
are taken from the locals and globals of the function where the translation is
performed, so you don't need to repeat yourself.

Here's a simple example where the variable names are ``$ordinal`` and
``$name``.  See if you can figure out where the values are taken from at
run time.

    >>> ordinal = 'first'
    >>> def print_it(name):
    ...     print(_('The $ordinal test message $name'))

In this example, when ``print_it()`` is called, the ``$ordinal`` placeholder
is taken from globals, while the ``$name`` placeholder is taken from the
function's locals (i.e. its parameters and other local variables).

With no language context in place, the source string is printed unchanged,
except that the substitutions are made.

    >>> print_it('Anne')
    The first test message Anne

When a substitution is missing, rather than raise an exception, the
``$``-variable name itself is used.

    >>> del ordinal
    >>> print_it('Bart')
    The $ordinal test message Bart

When there is a language context in effect, the substitutions happen after
translation.

    >>> ordinal = 'second'
    >>> with _.using('xx'):
    ...     print_it('Cris')
    second si n grfg zrffntr Cris

Our hypothetical ``yy`` language changes the order of the substitution
variables, but of course there is no problem with that.

    >>> ordinal = 'third'
    >>> with _.using('yy'):
    ...     print_it('Dave')
    Dave egassem tset third eht

Locals always take precedence over globals.
::

    >>> def print_it(name, ordinal):
    ...     print(_('The $ordinal test message $name'))

    >>> with _.using('yy'):
    ...     print_it('Elle', 'fourth')
    Elle egassem tset fourth eht


Deferred translations
=====================

Remember that the ``_()`` function has both a run time and a *static* purpose.
Most source string extraction tools look for functions named ``_()`` taking a
single string argument, and the pull those arguments out as the source
strings.  Sometimes however, you want to mark source strings for translation,
but you need to defer the translation of some of them until later.  The way to
do this is with the :meth:`~RuntimeTranslator.defer_translation()`
function.
::

    >>> with _.defer_translation():
    ...     print(_('This gets marked but not translated'))
    This gets marked but not translated

Because the string is wrapped in the ``_()`` function, it will get extracted
and added to the catalog by off-line tools, but it will not get translated
until later.  This is true even if there is a translation context in effect.

    >>> with _.using('xx'):
    ...     with _.defer_translation():
    ...         print(_('A test message'))
    ...     print(_('A test message'))
    A test message
    N grfg zrffntr


.. _`PEP 292`: http://www.python.org/dev/peps/pep-0292/
.. _`Yertle`: https://en.wikipedia.org/wiki/Yertle_the_Turtle_and_Other_Stories
