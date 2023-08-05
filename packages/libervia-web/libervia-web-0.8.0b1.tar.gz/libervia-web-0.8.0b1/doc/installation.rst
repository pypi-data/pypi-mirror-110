============
Installation
============

This are the instructions to install Libervia (SàT) using Python.
Note that if you are using GNU/Linux, Libervia may already be present on your distribution.

Libervia is a Salut à Toi frontend, the SàT backend must be installed first (if you
haven't installed it yet, it will be downloaded automatically as it is a dependency of
Libervia). Libervia and SàT backend must always have the same version (Libervia won't
start if the version backend has not the same version).

We recommend to use development version for now, until the release of
0.8 version.

Requirements
------------

- Python 3.7+
- Python 3 "venv", which may be installed with Python 3
- Mercurial

To install them on a Debian distribution or derivative, you can enter::

    sudo apt-get install python3-dev python3-venv python3-wheel mercurial

Development Version
-------------------

*Note for Arch users: a pkgbuild is available for your distribution on
AUR, check sat-libervia-hg (as well as other sat-\* packages).*

You can install the latest development version using Mercurial and pip.

Select the location where you want to install libervia and virtual environment, for
instance your ``$HOME`` directory::

    $ cd

You can use the same virtual environment as the one used for installing the backend.
Otherwise, create a new one (backend will be installed automatically if it's not already
there)::

    $ python3 -m venv libervia_venv
    $ source libervia_venv/bin/activate
    $ pip install -U pip wheel

Then you need to clone the repository::

    $ hg clone https://repos.goffi.org/libervia libervia-web && cd libervia-web

Now you can install the requirements::

    $ pip install -r requirements.txt

If you haven't done it for the backend, you need to install the media::

  $ cd
  $ hg clone https://repos.goffi.org/sat_media

then, create the directory ``~/.config/libervia``::

  $ mkdir -p ~/.config/libervia

and the file ``~/.config/libervia/libervia.conf`` containing:

.. sourcecode:: cfg

  [DEFAULT]
  media_dir = ~/sat_media

Of course, replace ``~/sat_media`` with the actual path you have used.

Please check backend documentation for more details on the settings.

You'll also need the ``yarn`` packager, please check your distribution documentation for
instructions to install it.

.. note::

    On Debian and derivatives, the ``yarn`` packager is installed with the ``yarnpkg``
    package (and not ``yarn`` only), you can install it with ``apt install yarnpkg`` as
    root (or with ``sudo``).

Post Installation
-----------------

Libervia uses its own XMPP account to fetch public data. You need to create a profile
named `libervia` linked to this account to launch Libervia. First create an account
dedicated to this on your XMPP server. For instance with `Prosody`_ you would enter
something like::

  $ prosodyctl adduser libervia@example.net

Where you'll obviously change ``libervia@example.net`` for the JID you want to use, with
your domain name. You'll then be prompted for a password. You can now create the
associated SàT profile::

  $ jp profile create libervia -j libervia@example.net -p <libervia_password>

.. note::

   jp doesn't prompt for password yet, this means that the password is visible to anybody
   looking at your screen and will stay in your shell history, and the password will be
   visible for a few seconds in process list. If this is a concern for you (e.g. you use a
   shared machine), use an other frontend to create the profile, or do the necessary to
   remove the password from history.

Finally, you need to specify to specify the password of this ``libervia`` profile in your
configuration. To do so, edit your ``libervia.conf`` and edit ``[libervia]`` and set the
``passphrase`` option to the profile password you have used in the command above:

.. sourcecode:: cfg

    [libervia_web]
    passphrase = <libervia_password>

You should now be good to run the Libervia Web server.

.. _Prosody: https://prosody.im


Usage
=====

To launch the Libervia Web server, enter::

  $ libervia-web

…or, if you want to launch it in foreground::

  $ libervia-web fg

You can stop it with::

  $ libervia-web stop

To know if backend is launched or not::

  $ libervia-web status


SàT Pubsub
==========

Some functionalities use advanced or experimental features of XMPP PubSub. We recommend to
use the SàT PubSub service that is a side project developed for the needs of Salut à Toi,
and consequently implements everything needed. Please refer to SàT PubSub documentation to
know how to install and use it.
