# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.devices.softbox.api.schemas.subrack_schemas import *

class ZhoneSubrackSchema(SubrackSchema):
    class Meta:
        model = Subrack
        fields = SubrackSchema.Meta.fields # + ('', '', '', '')