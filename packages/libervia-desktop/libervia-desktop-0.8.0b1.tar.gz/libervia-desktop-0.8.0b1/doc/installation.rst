============
Installation
============

This are the instructions to install Cagou (SàT) using Python.
Note that if you are using GNU/Linux, Cagou may already be present on your distribution.

Cagou is a Salut à Toi frontend, the SàT backend must be installed first (if you
haven't installed it yet, it will be downloaded automatically as it is a dependency of
Cagou). Cagou and SàT backend must always have the same version.

We recommend to use development version for now, until the release of 0.7 version which
will be "general public" version.

Also note that Cagou as all SàT ecosystem is still using Python 2 (this will change for
0.8 version which will be Python 3 only), so all instructions below have to be made using
python 2.

Development Version
-------------------

*Note for Arch users: a pkgbuild is available for your distribution on
AUR, check sat-cagou-hg (as well as other sat-\* packages).*

You can install the latest development version using pip. Please check backend documentation
to see the system dependencies needed.

You can use the same virtual environment as the one used for installing the backend. If
you haven't installed it yet, just select a location when you want to install it, for
instance your home directory::

  $ cd

And enter the following commands (note that *virtualenv2* may be named
*virtualenv* on some distributions, just be sure it's Python **2** version)::

  $ virtualenv2 env
  $ source env/bin/activate
  $ pip install hg+https://repos.goffi.org/cagou

If you haven't done it for the backend, you need to install the media::

  $ cd
  $ hg clone https://repos.goffi.org/sat_media

Usage
=====

To launch Cagou enter::

  $ cagou

If you want to connect directly a profile::

  $ cagou -p profile_name

Once started, you can use ``F11`` to switch fullscreen mode.

You can show/hide the menu with ``ALT + M`` and show/hide the notification bar with ``ALT + N``.

In Cagou, notifications appear on the top of the screen, in the *notification bar*. They
appear for a few seconds, but you can click on the left Cagou icon to see them entirely
and take your time to read them.

There is no focus stealing pop-up in Cagou, when some event requires a user action, a Cagou
icon will appear on the right of notification bar, so user can click and interact with it
when it is suitable.

Cagou has a concept of **activities**. An activity is some kind of communication tool
(chat, file sharing, remote control, etc.). On top left of each activity you have an icon
representing the activity selected. Click on it to select something else.

You may have noticed the 3 small dots on top and left border of each activity. You can
click (or touch) them, and drag to the bottom or right to create a new activity. This way
you can do several things on the same screen (e.g. check several chat rooms, or use the
file sharing and the chat at the same time). To close this extra activity, click again on
the 3 dots and drag in the opposite direction until the top or left line become red, then
release your mouse.
