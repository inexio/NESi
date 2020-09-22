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
from urllib import parse as urlparse
from urllib.request import url2pathname

import requests
from requests import adapters

from nesi import exceptions

LOG = logging.getLogger(__name__)


class LocalFileAdapter(adapters.BaseAdapter):
    """Allow Requests to GET file:// URLs.

    Protocol Adapter to allow Requests to GET file:// URLs.
    """

    @staticmethod
    def _verify_path(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ('put', 'delete'):
            return 501, "Not implemented"

        elif method.lower() not in ('get', 'head'):
            return 405, "Method not allowed"

        elif os.path.isdir(path):
            return 400, "Not a file"

        elif not os.path.isfile(path):
            return 404, "File not found"

        elif not os.access(path, os.R_OK):
            return 403, "Access denied"

        else:
            return 200, "OK"

    def send(self, req, **kwargs):  # pylint: disable=unused-argument
        """Return the file specified by the given request.

        :param req: request object
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._verify_path(
            req.method, path)
        if response.status_code == 200 and req.method.lower() != 'head':
            try:
                response.raw = open(path, 'rb')

            except OSError as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')

        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


class RestClient(object):
    """HTTP method executor.

    Abstracts away HTTP details, exposes high-level CRUD
    methods.

    :param url: The base URL to the REST API server. Should include
        scheme and authority portion of the URL. For example:
        https://example.com
    :param username: Username to use for basic HTTP authentication.
    :param password: Password to use for basic HTTP authentication.
    :param verify: Either a boolean value, a path to a CA_BUNDLE
        file or directory with certificates of trusted CAs.
        Defaults to True.
    """

    def __init__(self, url, username=None, password=None, verify=True):
        self._url = url
        self._session = requests.Session()
        self._session.mount('file://', LocalFileAdapter())
        self._session.auth = (username, password)
        self._session.verify = verify
        self._session.headers['Connection'] = 'close'

    def close(self):
        """Close this connection and the associated HTTP session."""
        self._session.close()

    def _http_call(self, method, path='', data=None, headers=None,
                   timeout=60, **requests_options):
        """Call any HTTP method.

        :param method: The HTTP method to be used, e.g: GET, POST,
            PUT, PATCH, DELETE.
        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        url = path if urlparse.urlparse(path).netloc else urlparse.urljoin(
            self._url, path)

        headers = headers or {}

        LOG.debug('HTTP request: %s %s; headers: %s; body: %s; timeout: %s; '
                  'session arguments: %s;', method, url, headers, data,
                  timeout, requests_options)

        try:
            response = self._session.request(
                method, url, json=data, headers=headers,
                **requests_options)

        except requests.ConnectionError as e:
            raise exceptions.NetworkError(url=url, error=e)

        LOG.debug('HTTP response for %s %s: status code: %s',
                  method, url, response.status_code)

        exceptions.handle_error_response(method, url, response)

        return response

    def get(self, path='', data=None, headers=None,
            timeout=60, **requests_options):
        """Call HTTP GET method.

        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        return self._http_call(
            'GET', path, data=data, headers=headers, timeout=timeout,
            **requests_options)

    def post(self, path='', data=None, headers=None,
             timeout=60, **requests_options):
        """Call HTTP POST method.

        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        return self._http_call(
            'POST', path, data=data, headers=headers, timeout=timeout,
            **requests_options)

    def patch(self, path='', data=None, headers=None,
              timeout=60, **requests_options):
        """Call HTTP PATCH method.

        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        return self._http_call(
            'PATCH', path, data=data, headers=headers, timeout=timeout,
            **requests_options)

    def put(self, path='', data=None, headers=None,
            timeout=60, **requests_options):
        """Call HTTP PUT method.

        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        return self._http_call(
            'PUT', path, data=data, headers=headers, timeout=timeout,
            **requests_options)

    def delete(self, path='', data=None, headers=None,
               timeout=60, **requests_options):
        """Call HTTP DELETE method.

        :param path: Sub-URI or absolute URL path to the resource.
        :param data: JSON data.
        :param headers: HTTP headers as a `dict`.
        :param timeout: Response timeout (seconds).
        :param requests_options: `requests` library options.
        :returns: `requests` library response object.
        :raises: NetworkError
        :raises: HTTPError
        """
        return self._http_call(
            'DELETE', path, data=data, headers=headers, timeout=timeout,
            **requests_options)

    def __enter__(self):
        """Enter into context."""
        return self

    def __exit__(self, *_args):
        """Leave context."""
        self.close()
