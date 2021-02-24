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

import copy
import logging
from nesi import exceptions

LOG = logging.getLogger(__name__)


class Field:
    """Scalar field of a JSON object.

    :param path: JSON field to fetch the value from. Either a string,
        or a list of strings in case of a nested field.
    :param required: whether this field is required. Missing required
        fields result in MissingAttributeError.
    :param default: the default value to use when the field is missing.
        Only has effect when the field is not required.
    :param converter: a callable to transform and/or validate the received
        value.
    """

    def __init__(self, path, required=False, default=None, converter=None):
        if not isinstance(path, list):
            path = [path]

        elif not path:
            raise exceptions.InvalidInputError(
                error='Path cannot be empty')

        self._path = path
        self._required = required
        self._default = default
        self._converter = converter

    def _load(self, body, resource, nested_in=None):
        """Load a field from a JSON object.

        :param body: parsed JSON body.
        :param resource: `Resource` instance for which the field is
            loaded.
        :param nested_in: parent resource path.
        :raises: MissingAttributeError if a required field is missing.
        :raises: MalformedAttributeError on invalid field value or type.
        :returns: field value.
        """
        name = self._path[-1]
        for path_item in self._path[:-1]:
            body = body.get(path_item, {})

        try:
            item = body[name]

        except KeyError:
            if self._required:
                path = (nested_in or []) + self._path
                raise exceptions.MissingAttributeError(
                    attribute='/'.join(path),
                    resource=resource.path)
            else:
                return self._default

        if self._converter is None:
            return item

        try:
            return self._converter(item)

        except Exception as exc:
            path = (nested_in or []) + self._path
            raise exceptions.MalformedAttributeError(
                attribute='/'.join(path),
                resource=resource.path,
                error=exc)


def _collect_fields(resource):
    """Collect fields from JSON document.

    :param resource: `Resource` instance.
    :returns: generator of tuples (key, field)
    """
    for attr in dir(resource.__class__):
        field = getattr(resource.__class__, attr)
        if isinstance(field, Field):
            yield (attr, field)


class CollectionField(Field):
    """A list of objects field."""

    def __init__(self, *args, **kwargs):
        super(CollectionField, self).__init__(*args, **kwargs)
        self._subfields = dict(_collect_fields(self))

    def _load(self, body, resource, nested_in=None):
        """Load a field from a JSON object.

        :param body: parent JSON body.
        :param resource: parent resource.
        :param nested_in: parent resource name.
        :returns: a new list object containing subfields.
        """
        nested_in = (nested_in or []) + self._path
        values = super(CollectionField, self)._load(body, resource)
        if values is None:
            return

        instances = []
        for value in values:
            instance = copy.copy(self)
            for attr, field in self._subfields.items():
                # Hide the Field object behind the real value
                setattr(instance, attr, field._load(
                    value, resource, nested_in))
            instances.append(instance)

        return instances


class EnumerationField(Field):
    """Enumerated field of a JSON object.

    :param field: JSON field to fetch the value from.
    :param mapping: a `dict` to look up mapped values at.
    :param required: whether this field is required. Missing required
        fields result in MissingAttributeError.
    :param default: the default value to use when the field is missing.
    """

    def __init__(self, field, mapping, required=False, default=None):
        if not isinstance(mapping, dict):
            raise exceptions.InvalidInputError(
                error="%s initializer must be a "
                      "dict" % self.__class__.__name__)

        super(EnumerationField, self).__init__(
            field, required=required, default=default,
            converter=mapping.get)


class Resource:
    """Represent a JSON document.

    JSON document fields are set as object attributes with
    `Field` instances as values.

    Lazily loads hyperlinked JSON documents.

    :param connection: A RestClient instance
    :param path: sub-URI path to the resource.
    """

    def __init__(self, connection, path='', params=None):
        self._conn = connection
        self._path = path
        self._json = None

        self.load(params)

    @classmethod
    def create(cls, connection, path='', **fields):
        """Create new resource.

        Performs a REST API call to create a resource with some initial
        values. In response, REST API can return a redirect to the newly
        created resource. In that case, this method will load and return
        the new resource.

        :param connection: A RestClient instance
        :param path: Path to create the resource (via POST).
        :param fields: required and optional name-value pairs for
            resource fields

        :return: new resource object or `None`
        """
        rsp = connection.post(path=path, data=fields, allow_redirects=False)

        LOG.info(
            'Resource has been created by path %s, status code %s, '
            'new object redirect %s', path, rsp.status_code, rsp.url)

        if rsp.status_code == 201:
            url = rsp.url
            if url:
                return cls(connection, url)

    def update(self, **fields):
        """Update existing resource

        Performs a REST API call to update this resource
        """
        self._conn.put(path=self._path, data=fields)
        self.load()

        LOG.info('Resource %s has been updated', self)

    def delete(self):
        """Delete existing resource.

        Performs a REST API call to delete this resource.
        """
        self._conn.delete(path=self._path)

        LOG.info('Resource %s has been deleted', self)

    def _parse_attributes(self, json_doc):
        """Parse the attributes of a resource.

        Parsed JSON fields are set to `self` as declared in the class.

        :param json_doc: parsed JSON document in form of Python types
        """
        for attr, field in _collect_fields(self):
            setattr(self, attr, field._load(json_doc, self))

    def load(self, params=None):
        """Load and parse JSON document.

        :raises: ResourceNotFoundError
        :raises: NetworkError
        :raises: HTTPError
        """
        data = self._conn.get(path=self._path, params=params)
        self._json = data.json() if data.content else {}

        LOG.debug('Received representation of %(type)s %(path)s: %(json)s',
                  {'type': self.__class__.__name__,
                   'path': self._path, 'json': self._json})
        self._parse_attributes(self._json)

    @property
    def json(self):
        return self._json

    @property
    def path(self):
        return self._path


def get_sub_resource_path_by(resource, subresource_name):
    """Find subresource path.

    :param resource: Resource instance on which the name
        gets queried upon.
    :param subresource_name: name of the resource attribute.
    :returns: Resource path.
    """
    if not subresource_name:
        raise exceptions.InvalidInputError(
            error='subresource cannot be empty')

    if not isinstance(subresource_name, list):
        subresource_name = [subresource_name]

    body = resource.json
    for path_item in subresource_name:
        body = body.get(path_item, {})

    if not body:
        raise exceptions.MissingAttributeError(
            attribute='/'.join(subresource_name), resource=resource.path)

    try:
        return get_member_identity(body)

    except (TypeError, KeyError):
        attribute = '/'.join(subresource_name)
        raise exceptions.MissingAttributeError(
            attribute=attribute, resource=resource.path)


def get_member_identity(member):
    """Return member identity.

    Expected JSON document structured like this:

    {
        "_links": {
            "self": "/path/to/member"
        }
    }

    :param member: JSON document containing collection member
    :returns: Member document location
    """
    path = member.get('_links')
    if not path:
        raise exceptions.MissingAttributeError(
            attribute='_links', resource=member)

    path = path.get('self')
    if not path:
        raise exceptions.MissingAttributeError(
            attribute='_links', resource=member)

    return path.rstrip('/')


def get_members_identities(members):
    """Return members identities from a collection.

    Expected JSON document structured like this:

    [
        {
            "_links": {
                "self": "/path/to/member"
            }
        }
    ]

    :param members: A sequence of JSON documents referring to members
    :returns: A sequence of member paths
    """
    members_list = []
    for member in members:
        member = get_member_identity(member)
        if not member:
            continue

        members_list.append(member)

    return members_list


class ResourceCollection(Resource):
    """Represent a collection of references to JSON documents.

    :param connection: A RestClient instance
    :param path: sub-URI path to the resource collection.
    """

    MEMBERS_ATTR = 'members'

    members_identities = Field(
        MEMBERS_ATTR, default=[], converter=get_members_identities)

    def __init__(self, connection, path, params=None):
        super(ResourceCollection, self).__init__(
            connection, path, params)
        LOG.debug('Received %(count)d member(s) for %(type)s %(path)s',
                  {'count': len(self.members_identities),
                   'type': self.__class__.__name__, 'path': self._path})

    @property
    def _resource_type(self):
        """`Resource` subclass that the collection contains."""
        return Resource

    def get_member(self, identity):
        """Return `Resource` object identified by `identity`.

        Lazily pulls `Resource` object from the collection.

        :param identity: The identity of the `Resource` object
            in the collection
        :returns: The `Resource` object
        :raises: ResourceNotFoundError
        """
        return self._resource_type(self._conn, identity)

    def __len__(self):
        """Return the size of the collection."""
        return len(self.members_identities)

    def __iter__(self):
        """Iterate over collection members."""
        for identity in self.members_identities:
            yield self.get_member(identity)

    def find_by_field_value(self, name, value):
        for element in self:
            assigned_value = getattr(element, name, None)
            if assigned_value == value:
                return element

        raise exceptions.InvalidInputError(
            error='Component with field %s and value %s not '
                  'found' % (name, value))

    def find_multiple_by_field_value(self, name, value):
        elements = []
        for element in self:
            assigned_value = getattr(element, name, None)
            if assigned_value == value:
                elements.append(element)

        if len(elements) > 0:
            return elements

        raise exceptions.InvalidInputError(
            error='Component with field %s and value %s not '
                  'found' % (name, value))
