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
from http import client as http_client

LOG = logging.getLogger(__name__)


class SoftboxenError(Exception):
    """General Softboxen error."""

    message = None

    def __init__(self, **kwargs):
        if self.message and kwargs:
            self.message = self.message % kwargs

        super(SoftboxenError, self).__init__(self.message)


class InvalidInputError(SoftboxenError):
    """Raise on invalid input."""

    message = 'Invalid input: %(error)s'


class NetworkError(SoftboxenError):
    """Raise on network error."""

    message = 'Unable to connect to %(url)s. Error: %(error)s'


class MissingAttributeError(SoftboxenError):
    """Raise on missing resource attribute."""

    message = ('The attribute %(attribute)s is missing from the '
               'resource %(resource)s')


class MalformedAttributeError(SoftboxenError):
    """Raise on malformed resource attribute."""

    message = ('The attribute %(attribute)s is malformed in the '
               'resource %(resource)s: %(error)s')


class InvalidParameterValueError(SoftboxenError):
    """Raise on invalid parameter."""

    message = ('The parameter "%(parameter)s" value "%(value)s" is invalid. '
               'Valid values are: %(valid_values)s')


class ExtensionNotFoundError(SoftboxenError):
    """Raise if extension package is not found."""

    message = ('Cannot find CLI extension for %(vendor)s, %(model)s, '
               '%(version)s')


class TerminalExitError(SoftboxenError):
    """Raise on terminal connection closure."""

    message = 'Terminal connection closed'

    def __init__(self, **kwargs):
        super(TerminalExitError, self).__init__(**kwargs)
        self._return_to = None

    @property
    def return_to(self):
        return self._return_to

    @return_to.setter
    def return_to(self, return_to):
        self._return_to = return_to


class TemplateError(SoftboxenError):
    """Raise on template rendering error."""

    message = ('Jinja2 template error at command processor %(processor)s '
               'while processing template %(template)s, template root '
               '%(template_root)s: %(error)s')


class CommandSyntaxError(SoftboxenError):
    """Raise on CLI command syntax error."""

    message = 'Command syntax error: %(command)s'

    def __init__(self, **kwargs):
        super(CommandSyntaxError, self).__init__(**kwargs)
        self.command = kwargs.get('command')


class RestApiError(SoftboxenError):
    """Raise on REST API error."""

    message = 'REST API error: %(error)s'


class HTTPError(SoftboxenError):
    """Raise on HTTP errors."""

    status_code = None
    """HTTP status code."""

    body = None
    """Error JSON document, if present."""

    message = 'HTTP %(method)s %(url)s returned code %(code)s. %(error)s'

    def __init__(self, method, url, response):
        self.status_code = response.status_code
        try:
            body = response.json()

        except ValueError:
            LOG.warning('Error response from %(method)s %(url)s '
                        'with status code %(code)s has no JSON body',
                        {'method': method, 'url': url, 'code':
                         self.status_code})
            error = 'unknown error'

        else:
            self.body = body.get('error', {})
            error = body.get('error', 'unknown error')

        kwargs = {'method': method, 'url': url, 'code': self.status_code,
                  'error': error}

        LOG.debug('HTTP response for %(method)s %(url)s: '
                  'status code: %(code)s, error: %(error)s', kwargs)

        super(HTTPError, self).__init__(**kwargs)


class BadRequestError(HTTPError):
    """Raise on bad HTTP request event."""


class ResourceNotFoundError(HTTPError):
    """Raise when HTTP resource has not been found."""

    message = 'Resource %(url)s not found'


class FunctionNotFoundError(SoftboxenError):
    """Raise when base function not initialized"""

    message = 'Invalid function: %(error)s'


class PropertyNotFoundError(SoftboxenError):
    """Raise when base ressource not initialized"""

    message = 'Invalid Property: %(error)s'


class ServerSideError(HTTPError):
    """Raise on server side error."""


class AccessError(HTTPError):
    """Raise on HTTP access error."""


def handle_error_response(method, url, response):
    """Turn HTTP code into raised exception."""
    if response.status_code < http_client.BAD_REQUEST:
        return

    elif response.status_code == http_client.NOT_FOUND:
        raise ResourceNotFoundError(method, url, response)

    elif response.status_code == http_client.BAD_REQUEST:
        raise BadRequestError(method, url, response)

    elif response.status_code in (http_client.UNAUTHORIZED,
                                  http_client.FORBIDDEN):
        raise AccessError(method, url, response)

    elif response.status_code >= http_client.INTERNAL_SERVER_ERROR:
        raise ServerSideError(method, url, response)

    else:
        raise HTTPError(method, url, response)
