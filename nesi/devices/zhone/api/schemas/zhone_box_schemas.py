# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.devices.softbox.api.schemas.box_schemas import *

class ZhoneBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields # + ('', '', '', '')
