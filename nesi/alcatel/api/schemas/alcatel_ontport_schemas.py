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

from nesi.softbox.api.schemas.ontport_schemas import *


class AlcatelOntPortSchema(OntPortSchema):
    class Meta:
        model = OntPort
        fields = OntPortSchema.Meta.fields + ('admin_state', 'operational_state', 'uni_idx', 'config_indicator',
                                              'link_status', 'speed')
