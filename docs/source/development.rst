
Development
-----------

Command processor class
+++++++++++++++++++++++

NESi `command processor <https://github.com/inexio/NESi/blob/master/nesi/softbox/cli/base.py#L35>`_
is a base class that implements CLI `REPR <https://en.wikipedia.org/wiki/Read–eval–print_loop>`_
loop. As a REPR loop, `command processor` operates along these guidelines:

* Read CLI user input on `stdin` up to <CR>
* Parse user input and try to match it against any known commands, otherwise
  default handler will be picked
* Apply user command to the simulated device model (fetched from REST API server
  by `NESi` core)
* Locate appropriate Jinja2 template and render it in the context of the simulated
  switch

... or

* If this command results in moving down the CLI menu tree, create another
  `command processor` object for the submenu and invoke its own `REPR` loop

The typical CLI implementation will have one or more linked
`command processor` objects. The top-level `command processor` will handle the
initial user interaction. In the example CLI implementation, the first
`PreLoginCommandProcessor <https://github.com/inexio/NESi/blob/master/vendors/Alcatel/7360/Alcatel_7360/main.py#L27>`_
is responsible for login-prompt rendering and collecting the username.

The top-level `processor <https://github.com/inexio/NESi/blob/master/vendors/Alcatel/7360/Alcatel_7360/main.py#L19>`_
class should define the `VENDOR`, `MODEL` and `VERSION` attributes. They are used by NESi core for matching the CLI implementation against
the model at hand.


Chaining command processors
+++++++++++++++++++++++++++

When a command processor needs to go down to the next level, the way to represent
it programmatically is to create a sub-processor. The `_create_subprocessor`
helper function is advised to use.

The new `command processor` will
`inherit <https://github.com/inexio/NESi/blob/master/nesi/softbox/cli/base.py#L302>`_
model, I/O streams and the command history from its parent, the user should only supply the new
"scope" for the template tree:

.. code-block::

    subprocessor = self._create_subprocessor(
        UserViewCommandProcessor, 'login', 'mainloop')

Template tree
+++++++++++++

It is advisable to arrange Jinja2 templates, that command processors use for
CLI dialog rendering, in a tree on the file system. The main reason for that
is that the `NESi` core treats some templates in special ways. All vendor specific templates are in the
`templates <https://github.com/inexio/NESi/tree/master/templates>`_
folder.

To date, the following template file names receive special treatment (if
existing):

* `on_enter.j2` - render this template on command processor entering into
  this directory
* `on_exit.j2` - render this template before command processor leaves this
  directory
* `on_cycle.j2` - render this template upon every <CR> received in the REPR
  loop
* `on_error.j2` - render this template on any error that occurs in the
  command processor while handling the command

Please, refer to
`example templates <https://github.com/inexio/NESi/tree/master/templates/Alcatel/Base/1>`_
for further explanation.

Command handling
++++++++++++++++

In response to user input, the REPR loop in every `command processor` will
try to locate a method name starting with the `do_` prefix followed by the
first word of the user input.

If found, this method will be called and all further command processing should
happen there. If no matching method is found, the magic `on_unknown_command`
method will be invoked instead (if defined).

.. code-block::

    def do_show(self, command, *args, context=None):

        subprocessor = self._create_subprocessor(
            EnableCommandProcessor, 'login', 'mainloop', 'show')

        subprocessor.loop(context=context)


Parsing user input
~~~~~~~~~~~~~~~~~~

CLI commands are frequently composed of a series of instructions interlaced
with references to device properties. For example:

.. code-block::

    $ show xdsl operational-data line 1/1/1/1 detail

`1/1/1/1` is the port identifier, while the rest of the arguments are command instructions.

To simplify command validation, the
`_validate <https://github.com/inexio/NESi/blob/master/nesi/softbox/cli/base.py#L416>`_
method can be used:

.. code-block::

    if self._validate(args, 'xdsl', 'operational-data', 'line', str, 'detail'):
        <code>
    elif ...

This method expects the instructions in the literal form and Python types
(e.g. `str`) in place of the options. Furthermore the result of _validate is a boolean value.

To simplify command parsing, the
`_dissect <https://github.com/inexio/NESi/blob/master/nesi/softbox/cli/base.py#L398>`_
method can be used:

.. code-block::

    port_name, = self._dissect(args, 'xdsl', 'operational-data', 'line', str, 'detail')

This method expects the instructions in the literal form and Python types
(e.g. `str`) in place of the options. Furthermore the result of _dissect is a tuple of one or more elements.

Operating on model properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To every `command processor` object a model of the simulated network-device, as
received from the REST API server, is passed. The command handler in
the `command processor` can create/read/update/delete model properties that
will be reflected on the models in the underlying database.

Generally, reading model attributes can be done just like `self._model.ports`, however
attribute creation/update/deletion typically requires a method call on the
model.

For example, to handle a command like:

.. code-block::

    $ configure bridge port 1/1/1/1

The `self._model.add_service_port` method would be called:

.. code-block::

    def do_port(self, command, *args, context=None):
        port_identifier, = self._dissect(args, str)

        port = self._model.get_port('name', port_identifier)

        self._model.add_service_port(name=port_identifier, conntected_type='port', connected_id=port.id)

Initial models
++++++++++++++

For the CLI simulation to work, a model needs to be created in the database,
and the specific CLI implementation for this model needs to be implemented.

To create a model, a series of REST API calls have to be performed. For example the
following call creates a network device for vendor "Alcatel", model "7360" and version "FX-4".

.. code-block::

    req='{
      "vendor": "Alcatel",
      "model": "7360",
      "version": "FX-4",
    }'
    curl -d "$req" \
        -H "Content-Type: application/json" \
        -X POST \
        http://localhost:5000/nesi/v1/boxen

The switch's ID and UUID will be automatically assigned to the newly created model.
Several shell `scripts <https://github.com/inexio/NESi/tree/master/bootup/conf/bootstraps>`_ with multiple
calls were created for the different vendors. Likewise other resources can be created and associated with models.
