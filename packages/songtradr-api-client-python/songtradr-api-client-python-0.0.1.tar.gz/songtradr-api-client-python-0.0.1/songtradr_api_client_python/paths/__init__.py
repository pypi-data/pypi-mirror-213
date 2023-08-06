# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from songtradr_api_client_python.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_USER_UPDATEPASSWORD = "/api/v1/user/update-password"
    API_V1_USER_TOKEN = "/api/v1/user/token"
    API_V1_USER_SIGNUP = "/api/v1/user/sign-up"
    API_V1_USER_SAVE_PLAYLIST = "/api/v1/user/savePlaylist"
    API_V1_USER_REFERRERS_NEW = "/api/v1/user/referrers/new"
    API_V1_USER_ME = "/api/v1/user/me"
    API_V1_USER_LOGIN = "/api/v1/user/login"
    API_V1_USER_FORGOTPASSWORD = "/api/v1/user/forgot-password"
    API_V1_USER_FILE_OBJECT_KEY = "/api/v1/user/file/{objectKey}"
    API_V1_USER_FILE_NAME_INIT_UPLOAD = "/api/v1/user/file/{name}/initUpload"
    API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR = "/api/v1/public/recording/searchGranular"
    API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR_ABSTRACTION = "/api/v1/public/recording/searchGranularAbstraction"
    API_V1_PLAYLIST = "/api/v1/playlist"
    API_V1_USER_REFERRERS_USERNAME = "/api/v1/user/referrers/{username}"
    API_V1_USER_FOLDERS = "/api/v1/user/folders"
    API_V1_USER_FOLDER_FOLDER_NAME_TAGSTRENGTHS = "/api/v1/user/folder/{folderName}/tagstrengths"
    API_V1_USER_FOLDER_FOLDER_NAME_TAGGRAMS = "/api/v1/user/folder/{folderName}/taggrams"
    API_V1_USER_FILES = "/api/v1/user/files"
    API_V1_USER_FILES_SUMMARY = "/api/v1/user/filesSummary"
    API_V1_USER_FILES_STATUS = "/api/v1/user/filesStatus"
    API_V1_USER_FILES_DOWNLOAD = "/api/v1/user/filesDownload"
    API_V1_PUBLIC_RECORDING_IDS_TAGSTRENGTHS = "/api/v1/public/recording/{ids}/tagstrengths"
    API_V1_PUBLIC_RECORDING_IDS_TAGGRAMS = "/api/v1/public/recording/{ids}/taggrams"
    API_V1_PUBLIC_RECORDING_IDS_SIMILARITIES = "/api/v1/public/recording/{ids}/similarities"
    API_V1_PUBLIC_RECORDING_IDS_MUSICAL_FEATURES = "/api/v1/public/recording/{ids}/musicalFeatures"
    API_V1_PUBLIC_RECORDING_SEARCH = "/api/v1/public/recording/search"
    API_V1_PUBLIC_RECORDING_S_IDS = "/api/v1/public/recording/s/{ids}"
    API_V1_PUBLIC_RECORDING_M_IDS = "/api/v1/public/recording/m/{ids}"
    API_V1_PUBLIC_RECORDING_L_IDS = "/api/v1/public/recording/l/{ids}"
    API_V1_PARTY = "/api/v1/party"
    API_V1_ALLOWED_VALUES_TAG = "/api/v1/allowedValues/tag"
    API_V1_ALLOWED_VALUES_MUSICAL_FEATURES = "/api/v1/allowedValues/musicalFeatures"
    API_V1_ALLOWED_VALUES_GENRE = "/api/v1/allowedValues/genre"
    API_V1_PLAYLIST_SONGTRADR_PLAYLIST_GUID = "/api/v1/playlist/{songtradrPlaylistGuid}"
