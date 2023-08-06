import typing_extensions

from songtradr_api_client_python.apis.tags import TagValues
from songtradr_api_client_python.apis.tags.allowed_values_api import AllowedValuesApi
from songtradr_api_client_python.apis.tags.party_api import PartyApi
from songtradr_api_client_python.apis.tags.playlist_api import PlaylistApi
from songtradr_api_client_python.apis.tags.recording_api import RecordingApi
from songtradr_api_client_python.apis.tags.user_api import UserApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ALLOWEDVALUES: AllowedValuesApi,
        TagValues.PARTY: PartyApi,
        TagValues.PLAYLIST: PlaylistApi,
        TagValues.RECORDING: RecordingApi,
        TagValues.USER: UserApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ALLOWEDVALUES: AllowedValuesApi,
        TagValues.PARTY: PartyApi,
        TagValues.PLAYLIST: PlaylistApi,
        TagValues.RECORDING: RecordingApi,
        TagValues.USER: UserApi,
    }
)
