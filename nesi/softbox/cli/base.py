# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst
import logging
import os
import tty
import termios
import pyperclip

import jinja2

from nesi import exceptions

LOG = logging.getLogger(__name__)


class Context:
    """Turn a dict into an object.

    The intension is to simplify context access in the templates.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class CommandProcessor:
    """Create CLI REPR loop.

    :param model: box model
    :param input: terminal input stream
    :param output: terminal output stream
    :param template_root: location of Jinja2 templates for rendering
        command output by this command processor
    :param scopes: a sequence of names of nesting command processors
        followed by the name of this command processor
    """

    # Identify backend models to load and use
    VENDOR = '?'
    MODEL = '?'
    VERSION = '?'

    def __init__(self, model, input_stream, output_stream, history,
                 template_root=None, scopes=(), daemon=False):
        self._model = model
        self._input = input_stream
        self._output = output_stream
        self._scopes = scopes
        self._template_root = template_root
        self._template_dir = os.path.join(
            template_root, self.VENDOR, self.MODEL, self.VERSION,
            *scopes)

        self._jenv = jinja2.Environment(
            loader=(jinja2.FileSystemLoader(self._template_dir)
                    if template_root else None),
            trim_blocks=True, lstrip_blocks=True, autoescape=True)
        self.daemon = daemon
        self.history_pos = 0
        self.history = history
        self.prompt_end_pos = self.get_prompt_len() - 1
        self.cursor_pos = self.prompt_end_pos + 1
        self.cursor_boundary = self.prompt_end_pos + 1

    class _Getch:
        def __call__(self, input):
            old_settings = []
            try:
                old_settings = termios.tcgetattr(input)
                tty.setraw(input)
                ch = input.read(3)
            finally:
                termios.tcsetattr(input, termios.TCSADRAIN, old_settings)
            return ch

    def history_up(self):
        if self.history_pos - 1 <= 0:
            if len(self.history) > 0:
                entry = self.history[0]
            else:
                entry = ''
            self.history_pos = 0
        else:
            entry = self.history[self.history_pos - 1]
            self.history_pos -= 1
        return entry

    def history_down(self):
        try:
            entry = self.history[self.history_pos + 1]
            self.history_pos += 1
        except IndexError:
            entry = ''
            self.history_pos = len(self.history)
        return entry

    def move_left(self):
        if self.cursor_pos - 1 > self.prompt_end_pos:
            self._output.write('\033[D'.encode('utf-8'))
            self.cursor_pos -= 1

    def move_right(self):
        if self.cursor_pos < self.cursor_boundary:
            self._output.write('\033[C'.encode('utf-8'))
            self.cursor_pos += 1

    def get(self):
        inkey = self._Getch()
        while (1):
            k = inkey(self._input).decode('utf-8')
            if k != '': break
        if k == '\x1b[A':  # up-arrow
            return 'history', self.history_up()
        elif k == '\x1b[B':  # down-arrow
            return 'history', self.history_down()
        elif k == '\x1b[C':  # right-arrow
            self.move_right()
            return None, None
        elif k == '\x1b[D':  # left-arrow
            self.move_left()
            return None, None
        elif k == '\b' or k == '':  # crtl-h or backspace
            if self.cursor_pos - 1 > self.prompt_end_pos:
                return 'backspace', ''
            else:
                return None, None
        elif k == '[3':  # del-key
            return 'del', ''
        elif k == '':  # ctrl-v
            return 'paste', pyperclip.paste()
        elif k == 'OF' or k == '[F':  # command + right-arrow or end-key
            self.cursor_pos = self.cursor_boundary
            return 'cursor', ''
        elif k == 'OH' or k == '[H':  # command + left-arrow or pos1-key
            self.cursor_pos = self.prompt_end_pos + 1
            return 'cursor', ''
        elif k == 'b' or k == 'f':  # ignore all alt + right / left arrow presses
            return None, None
        else:
            return 'character', k

    def updateline(self, line):
        self._write('\r')  # reset cursor to start of line
        self._write('\033[' + str(self.prompt_end_pos + 1) + 'C')  # move cursor to end of prompt
        self._write('\033[K')  # clear rest of line
        self._write(line)  # insert new line contents
        self._write('\r')  # reset cursor to start of line
        self._write('\033[' + str(self.cursor_pos) + 'C')  # move cursor to correct position

    def getline(self):
        char = None
        line = ''
        self.history_pos = len(self.history)
        self.cursor_pos = self.prompt_end_pos + 1
        self.cursor_boundary = self.prompt_end_pos + 1

        while char != '\r':
            option, char = self.get()
            if char is None:
                continue
            elif char == '\r':
                continue
            if option == 'backspace':
                line = line[:self.cursor_pos - self.prompt_end_pos - 2] + line[self.cursor_pos - self.prompt_end_pos - 1:]
                self.cursor_pos -= 1
                self.cursor_boundary -= 1
                self.updateline(line)
                continue
            elif option == 'del':
                line = line[:(self.cursor_pos - self.prompt_end_pos) - 1] + line[(self.cursor_pos - self.prompt_end_pos):]
                self.cursor_boundary -= 1
                self.updateline(line)
                continue
            elif option == 'history':
                self.cursor_pos = self.prompt_end_pos + 1 + len(char)
                self.cursor_boundary = self.prompt_end_pos + 1 + len(char)
                self.updateline(char)
                line = char
            elif option == 'cursor':
                self.updateline(line)
            elif option == 'paste':
                line = line[:(self.cursor_pos - self.prompt_end_pos - 1)] + char + line[(self.cursor_pos - self.prompt_end_pos - 1):]
                self.cursor_boundary = self.cursor_boundary + len(char)
                self.cursor_pos = self.cursor_pos + len(char)
                self.updateline(line)
            elif option == 'character':
                line = line[:(self.cursor_pos - self.prompt_end_pos - 1)] + char + line[(self.cursor_pos - self.prompt_end_pos - 1):]
                self.cursor_pos += 1
                self.cursor_boundary += 1
                self.updateline(line)

        if line != '\r' and line != '':
            self.history += (line.replace('\r', '').rstrip(),)

        self._write('\n')

        return line

    def _render(self, template, *scopes, context=None, ignore_errors=False):
        template_name = '%s.j2' % template

        try:
            if scopes:
                template_dir = os.path.join(
                    self._template_root, self.VENDOR, self.MODEL, self.VERSION,
                    *scopes)
                tmp_jenv = jinja2.Environment(
                    loader=(jinja2.FileSystemLoader(template_dir)
                            if self._template_root else None),
                    trim_blocks=True, lstrip_blocks=True, autoescape=True)
                tmpl = tmp_jenv.get_template(template_name)
            else:
                tmpl = self._jenv.get_template(template_name)

            return tmpl.render(
                scopes=self._scopes,
                model=self._model,
                context=Context(**context))

        except jinja2.exceptions.TemplateError as exc:
            if not ignore_errors:
                raise exceptions.TemplateError(
                    template=template,
                    processor=self.__class__.__name__,
                    template_root=self._template_dir, error=exc)

            LOG.debug('ignoring rendering template %s error: %s', template, exc)
            return

    def _default_command_handler(self, command, *args, context=None):
        try:
            text = self._render(command, *args, context=context)

        except exceptions.TemplateError:
            raise exceptions.CommandSyntaxError(command=command)

        self._write(text)

    def _read(self):
        if self.daemon:
            line = self._input.readline().decode('utf-8')
        else:
            line = self.getline()

        return line

    def _write(self, text):
        self._output.write(text.encode('utf-8'))

    def _get_command_func(self, line):
        if line.startswith(self.comment):
            return (lambda: None), '', []

        args = line.strip().split()
        command = args[0]
        args = args[1:]

        if command == self.negation:
            command += "_" + args.pop(0)

        command = command.replace('-', '_')

        matching = sorted(
            [c for c in dir(self) if c.startswith('do_' + command)])

        if len(matching) >= 1:
            return getattr(self, matching[0]), command, args

        if hasattr(self, 'on_unknown_command'):
            LOG.debug('Using unknown command handler for command '
                      '%s %s', command, args)

            return self.on_unknown_command, command, args

        LOG.debug('Using default command handler for command '
                  '%s %s', command, args)

        return self._default_command_handler, command, args

    def _parse_and_execute_command(self, line, context):
        if line.strip():
            func, command, args = self._get_command_func(line)
            if not func:
                LOG.debug("%s can't process : %s, falling back to "
                          "parent" % (self.__class__.__name__, line))
                return False

            else:
                func(command, *args, context=context)

        return True

    def _create_subprocessor(self, subprocessor, *scopes):
        return subprocessor(
            self._model, self._input, self._output, self.history,
            template_root=self._template_root,
            scopes=scopes, daemon=self.daemon)

    def process_command(self, line, context):
        self._parse_and_execute_command(line, context)

    def loop(self, context=None, return_to=None, command=None):
        if context is None:
            context = {}

        self.set_prompt_end_pos(context)

        if command is None:
            self.on_enter(context)
            self.on_cycle(context)

        while True:
            if command is None:
                line = self._read()
                context['raw_line'] = line
            else:
                line = command
                command = None

            try:
                self.process_command(line, context)

            except exceptions.CommandSyntaxError as exc:
                self.on_error(dict(context, command=exc.command))

            except exceptions.TerminalExitError as exc:
                if not exc.return_to:
                    exc.return_to = return_to

                if not exc.return_to or exc.return_to == 'sysexit' or not isinstance(self, exc.return_to):
                    raise exc

                # This is the first instance of the desired
                # CommandProcessor to unwind to, continuing

            self.on_cycle(context)

        self.on_exit(context)

    def get_prompt_len(self):
        text = self._render('on_cycle', context=dict(), ignore_errors=True)

        if text is None or len(text) == 0:
            text = self._render('on_enter', context=dict(), ignore_errors=True)

        if text is None:
            result = 0
        else:
            result = len(text)

        return result

    def set_prompt_end_pos(self, context):
        text = self._render('on_cycle', context=context, ignore_errors=True)

        if len(text) == 0:
            text = self._render('on_enter', context=context, ignore_errors=True)

        self.prompt_end_pos = len(text) - 1

    def on_cycle(self, context):
        text = self._render('on_cycle', context=context, ignore_errors=True)
        if text is not None:
            self._write(text)

    def on_enter(self, context):
        text = self._render('on_enter', context=context, ignore_errors=True)
        if text is not None:
            self._write(text)

    def on_exit(self, context):
        text = self._render('on_exit', context=context, ignore_errors=True)
        if text is not None:
            self._write(text)

    def on_error(self, context):
        text = self._render('on_error', context=context, ignore_errors=True)
        if text is not None:
            self._write(text)

    @property
    def comment(self):
        return '!'

    @property
    def negation(self):
        return 'no'

    def _dissect(self, args, *tokens):
        values = []

        for idx, token in enumerate(tokens):
            try:
                arg = args[idx]

            except IndexError:
                raise exceptions.CommandSyntaxError(command=' '.join(args))

            if type(token) == type:
                values.append(arg)

            elif not token.startswith(arg):
                raise exceptions.CommandSyntaxError(command=' '.join(args))

        return values

    def _validate(self, args, *tokens):
        if len(args) != len(tokens):
            return False
        for idx, token in enumerate(tokens):

            try:
                arg = args[idx]
            except IndexError:
                return False

            if arg != token and type(token) != type:
                return False

        return True
