Differences with Click-REPL
===========================

`Click-REPL`_ is another Click extension that provides a feature similar
to Incenp.Click-Shell. This page lists the main differences between the
two extensions.


No shell escape
---------------

The interactive shell created by Click-REPL allows the user to invoke
commands from the underlying system shell in addition to the commands
from the application itself, by prefixing them with ``!``.

Incenp.Click-Shell has no such feature.


Setting the shell as the default subcommand
-------------------------------------------

With Incenp.Click-Shell, the interactive shell is automatically started
if the the Click application is invoked without an explicit subcommand.

By contrast, Click-REPL adds a new subcommand to start the shell (named
``repl`` by default), but that command is *not* used by default. If the
program is invoked without a subcommand, the help message is displayed
(as with standard Click). The user has to explicitly invoke the ``repl``
command to get the interactive shell.


Calling the root function only once
-----------------------------------

Consider the following minimal example:

.. code-block:: python

    import click
    from incenp.click_shell import shell

    # @click.group()  # no longer
    @shell(prompt='my-app> ', intro='Starting my app...')
    def my_app():
        print('initializing the application...')

    @my_app.command()
    def testcommand():
        print('testcommand is running')

    # more commands...

    if __name__ == '__main__':
        my_app()

The code inside the ``my_app`` function (if any) will always be called
only once, before the interactive shell is started.

By contrast, with the equivalent code using Click-REPL:

.. code-block:: python

    import click
    from click_repl import register_repl

    @click.group()
    def my_app():
        print('initializing the application...')

    @my_app.command()
    def testcommand():
        print('testcommand is running')

    # more commands...

    if __name__ == '__main__':
        register_repl(my_app)
        my_app()
        
the code inside the ``my_app`` function will not be executed prior to
starting the interactive shell. Instead, once the shell is started that
code will be called before each subcommand invocation.

That difference in behaviour means that, if you are doing anything in
the “root” function of your Click app (``my_app`` in those examples),
then Click-REPL and Incenp.Click-Shell *cannot* be used interchangeably.


.. _Click-REPL: https://github.com/click-contrib/click-repl
