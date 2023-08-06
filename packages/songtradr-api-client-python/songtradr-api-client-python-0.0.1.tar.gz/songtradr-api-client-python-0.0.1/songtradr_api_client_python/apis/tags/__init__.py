# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from songtradr_api_client_python.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ALLOWEDVALUES = "allowed-values"
    PARTY = "party"
    PLAYLIST = "playlist"
    RECORDING = "recording"
    USER = "user"
