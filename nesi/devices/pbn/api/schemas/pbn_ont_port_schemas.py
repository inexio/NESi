# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.devices.softbox.api.schemas.ontport_schemas import *


class PBNOntPortSchema(OntPortSchema):
    class Meta:
        model = OntPort
        fields = OntPortSchema.Meta.fields + ('operational_state', 'admin_state', 'flow_control', 'duplex', 'speed',
                                              'storm_control')
