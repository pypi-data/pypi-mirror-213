Adapter API
###########

Adapters are an interface between a collection of music data and metadata and
the Sublime Music UI. An adapter exposes a Subsonic-like API to the UI layer,
but can be backed by a variety of music stores including a Subsonic-compatible
server, data on the local filesystem, or even an entirely different service.

This document is designed to help you understand the Adapter API so that you can
create your own custom adapters. This document is best read in conjunction with
the :class:`sublime_music.adapters.Adapter` documentation. This document is
meant as a guide to tell you a general order in which to implement things.

Terms
=====

**Music Metadata**
  Metadata about a music collection. This includes things like song metadata,
  playlists, artists, albums, filesystem hierarchy, etc.

**Music Data**
  The actual data of a music file. This may be accessed in a variety of
  different ways including via a stream URL, or via the local filesystem.

**Music Source**
  A source of music metadata and music data. This is the most atomic entity that
  the user interacts with. It can be composed of one or two *Adapters*.

**Adapter**
  A module which exposes the Adapter API.

Creating Your Adapter Class
===========================

An adapter is composed of a single Python module. The adapter module can have
arbitrary code, and as many files/classes/functions/etc. as necessary, however
there must be one and only one class in the module which inherits from the
:class:`sublime_music.adapters.Adapter` class. Normally, a single file with a
single class should be enough to implement the entire adapter.

.. warning::

   Your adapter cannot assume that it will be running on a single thread. Due to
   the nature of the GTK event loop, functions can be called from any thread at
   any time. **It is critical that your adapter is thread-safe.** Failure to
   make your adapter thread-safe will result in massive problems and undefined
   behavior.

After you've created the class, you will want to implement the following
functions and properties first:

* ``get_ui_info``: Returns a :class:`sublime_music.adapters.UIInfo` with the
  info for the adapter.
* ``__init__``: Used to initialize your adapter. See the
  :class:`sublime_music.adapters.Adapter.__init__` documentation for the
  function signature of the ``__init__`` function.
* ``ping_status``: Assuming that your adapter requires connection to the
  internet, this property needs to be implemented. (If your adapter doesn't
  require connection to the internet, set
  :class:`sublime_music.adapters.Adapter.is_networked` to ``False`` and ignore
  the rest of this bullet point.)

  This property will tell the UI whether or not the underlying server can be
  pinged.

  .. warning::

     This function is called *a lot* (probably too much?) so it *must* return a
     value *instantly*. **Do not** perform the actual network request in this
     function. Instead, use a periodic ping that updates a state variable that
     this function returns.

* ``get_configuration_form``: This function should return a :class:`Gtk.Box`
  that gets any inputs required from the user and uses the given
  ``config_store`` to store the configuration values.

  The ``Gtk.Box`` must expose a signal with the name ``"config-valid-changed"``
  which returns a single boolean value indicating whether or not the
  configuration is valid.

  If you don't want to implement all of the GTK logic yourself, and just want a
  simple form, then you can use the
  :class:`sublime_music.adapters.ConfigureServerForm` class to generate a form
  in a declarative manner.

.. note::

   The :class:`sublime_music.adapters.Adapter` class is an `Abstract Base Class
   <abc_>`_ and all required functions are annotated with the
   ``@abstractmethod`` decorator. This means that your adapter will fail to
   instantiate if the abstract methods are not implemented.

   .. _abc: https://docs.python.org/3/library/abc.html

Handling Configuration
----------------------

For each configuration parameter you want to allow your adapter to accept, you
must do the following:

1. Choose a name for your configuration parameter. The configuration parameter
   name must be unique within your adapter.

2. Add a new entry to the return value of your
   :class:`sublime_music.adapters.Adapter.get_config_parameters` function with
   the key being the name from (1), and the value being a
   :class:`sublime_music.adapters.ConfigParamDescriptor`. The order of the keys
   in the dictionary matters, since the UI uses that to determine the order in
   which the configuration parameters will be shown in the UI.

3. Add any verifications that are necessary for your configuration parameter in
   your :class:`sublime_music.adapters.Adapter.verify_configuration` function.
   If you parameter descriptor has ``required = True``, then that parameter is
   guaranteed to appear in the configuration.

4. The configuration parameter will be passed into your
   :class:`sublime_music.adapters.Adapter.init` function. It is guaranteed that
   the ``verify_configuration`` will have been called first, so there is no need
   to re-verify the config that is passed.

Implementing Data Retrieval Methods
-----------------------------------

After you've done the initial configuration of your adapter class, you will want
to implement the actual adapter data retrieval functions.

For each data retrieval function there is a corresponding ``can_``-prefixed
property (CPP) which will be used by the UI to determine if the data retrieval
function can be called. If the CPP is ``False``, the UI will never call the
corresponding function (and if it does, it's a UI bug). The CPP can be dynamic,
for example, if your adapter supports many API versions, some of the CPPs may
depend on the API version. However, CPPs should not be dependent on connection
status (there are times where the user may want to force a connection retry,
even if the most recent ping failed).

Here is an example of what a ``get_playlists`` interface for an external server
might look:

.. code:: python

    can_get_playlists = True
    def get_playlists(self) -> List[Playlist]:
        return my_server.get_playlists()

    can_get_playlist_details = True
    def get_playlist_details(self, playlist_id: str) -> PlaylistDetails:
        return my_server.get_playlist(playlist_id)

.. tip::

   By default, all ``can_``-prefixed properties are ``False``, which means that
   you can implement them one-by-one, testing as you go. The UI should
   dynamically enable features as new ``can_``-prefixed properties become
   ``True``.*

   \* At the moment, this isn't really the case and the UI just kinda explodes
   if it doesn't have some of the functions available, but in the future, guards
   will be added around all of the function calls.

Usage Parameters
----------------

There are a few special properties dictate how the adapter can be used. You
probably do not need to use this except for very specific purposes. Read the
"Usage Parameters" section of the source code for details.
