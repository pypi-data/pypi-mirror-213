import typing_extensions

from songtradr_api_client_python.paths import PathValues
from songtradr_api_client_python.apis.paths.api_v1_user_update_password import ApiV1UserUpdatePassword
from songtradr_api_client_python.apis.paths.api_v1_user_token import ApiV1UserToken
from songtradr_api_client_python.apis.paths.api_v1_user_sign_up import ApiV1UserSignUp
from songtradr_api_client_python.apis.paths.api_v1_user_save_playlist import ApiV1UserSavePlaylist
from songtradr_api_client_python.apis.paths.api_v1_user_referrers_new import ApiV1UserReferrersNew
from songtradr_api_client_python.apis.paths.api_v1_user_me import ApiV1UserMe
from songtradr_api_client_python.apis.paths.api_v1_user_login import ApiV1UserLogin
from songtradr_api_client_python.apis.paths.api_v1_user_forgot_password import ApiV1UserForgotPassword
from songtradr_api_client_python.apis.paths.api_v1_user_file_object_key import ApiV1UserFileObjectKey
from songtradr_api_client_python.apis.paths.api_v1_user_file_name_init_upload import ApiV1UserFileNameInitUpload
from songtradr_api_client_python.apis.paths.api_v1_public_recording_search_granular import ApiV1PublicRecordingSearchGranular
from songtradr_api_client_python.apis.paths.api_v1_public_recording_search_granular_abstraction import ApiV1PublicRecordingSearchGranularAbstraction
from songtradr_api_client_python.apis.paths.api_v1_playlist import ApiV1Playlist
from songtradr_api_client_python.apis.paths.api_v1_user_referrers_username import ApiV1UserReferrersUsername
from songtradr_api_client_python.apis.paths.api_v1_user_folders import ApiV1UserFolders
from songtradr_api_client_python.apis.paths.api_v1_user_folder_folder_name_tagstrengths import ApiV1UserFolderFolderNameTagstrengths
from songtradr_api_client_python.apis.paths.api_v1_user_folder_folder_name_taggrams import ApiV1UserFolderFolderNameTaggrams
from songtradr_api_client_python.apis.paths.api_v1_user_files import ApiV1UserFiles
from songtradr_api_client_python.apis.paths.api_v1_user_files_summary import ApiV1UserFilesSummary
from songtradr_api_client_python.apis.paths.api_v1_user_files_status import ApiV1UserFilesStatus
from songtradr_api_client_python.apis.paths.api_v1_user_files_download import ApiV1UserFilesDownload
from songtradr_api_client_python.apis.paths.api_v1_public_recording_ids_tagstrengths import ApiV1PublicRecordingIdsTagstrengths
from songtradr_api_client_python.apis.paths.api_v1_public_recording_ids_taggrams import ApiV1PublicRecordingIdsTaggrams
from songtradr_api_client_python.apis.paths.api_v1_public_recording_ids_similarities import ApiV1PublicRecordingIdsSimilarities
from songtradr_api_client_python.apis.paths.api_v1_public_recording_ids_musical_features import ApiV1PublicRecordingIdsMusicalFeatures
from songtradr_api_client_python.apis.paths.api_v1_public_recording_search import ApiV1PublicRecordingSearch
from songtradr_api_client_python.apis.paths.api_v1_public_recording_s_ids import ApiV1PublicRecordingSIds
from songtradr_api_client_python.apis.paths.api_v1_public_recording_m_ids import ApiV1PublicRecordingMIds
from songtradr_api_client_python.apis.paths.api_v1_public_recording_l_ids import ApiV1PublicRecordingLIds
from songtradr_api_client_python.apis.paths.api_v1_party import ApiV1Party
from songtradr_api_client_python.apis.paths.api_v1_allowed_values_tag import ApiV1AllowedValuesTag
from songtradr_api_client_python.apis.paths.api_v1_allowed_values_musical_features import ApiV1AllowedValuesMusicalFeatures
from songtradr_api_client_python.apis.paths.api_v1_allowed_values_genre import ApiV1AllowedValuesGenre
from songtradr_api_client_python.apis.paths.api_v1_playlist_songtradr_playlist_guid import ApiV1PlaylistSongtradrPlaylistGuid

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_USER_UPDATEPASSWORD: ApiV1UserUpdatePassword,
        PathValues.API_V1_USER_TOKEN: ApiV1UserToken,
        PathValues.API_V1_USER_SIGNUP: ApiV1UserSignUp,
        PathValues.API_V1_USER_SAVE_PLAYLIST: ApiV1UserSavePlaylist,
        PathValues.API_V1_USER_REFERRERS_NEW: ApiV1UserReferrersNew,
        PathValues.API_V1_USER_ME: ApiV1UserMe,
        PathValues.API_V1_USER_LOGIN: ApiV1UserLogin,
        PathValues.API_V1_USER_FORGOTPASSWORD: ApiV1UserForgotPassword,
        PathValues.API_V1_USER_FILE_OBJECT_KEY: ApiV1UserFileObjectKey,
        PathValues.API_V1_USER_FILE_NAME_INIT_UPLOAD: ApiV1UserFileNameInitUpload,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR: ApiV1PublicRecordingSearchGranular,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR_ABSTRACTION: ApiV1PublicRecordingSearchGranularAbstraction,
        PathValues.API_V1_PLAYLIST: ApiV1Playlist,
        PathValues.API_V1_USER_REFERRERS_USERNAME: ApiV1UserReferrersUsername,
        PathValues.API_V1_USER_FOLDERS: ApiV1UserFolders,
        PathValues.API_V1_USER_FOLDER_FOLDER_NAME_TAGSTRENGTHS: ApiV1UserFolderFolderNameTagstrengths,
        PathValues.API_V1_USER_FOLDER_FOLDER_NAME_TAGGRAMS: ApiV1UserFolderFolderNameTaggrams,
        PathValues.API_V1_USER_FILES: ApiV1UserFiles,
        PathValues.API_V1_USER_FILES_SUMMARY: ApiV1UserFilesSummary,
        PathValues.API_V1_USER_FILES_STATUS: ApiV1UserFilesStatus,
        PathValues.API_V1_USER_FILES_DOWNLOAD: ApiV1UserFilesDownload,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_TAGSTRENGTHS: ApiV1PublicRecordingIdsTagstrengths,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_TAGGRAMS: ApiV1PublicRecordingIdsTaggrams,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_SIMILARITIES: ApiV1PublicRecordingIdsSimilarities,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_MUSICAL_FEATURES: ApiV1PublicRecordingIdsMusicalFeatures,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH: ApiV1PublicRecordingSearch,
        PathValues.API_V1_PUBLIC_RECORDING_S_IDS: ApiV1PublicRecordingSIds,
        PathValues.API_V1_PUBLIC_RECORDING_M_IDS: ApiV1PublicRecordingMIds,
        PathValues.API_V1_PUBLIC_RECORDING_L_IDS: ApiV1PublicRecordingLIds,
        PathValues.API_V1_PARTY: ApiV1Party,
        PathValues.API_V1_ALLOWED_VALUES_TAG: ApiV1AllowedValuesTag,
        PathValues.API_V1_ALLOWED_VALUES_MUSICAL_FEATURES: ApiV1AllowedValuesMusicalFeatures,
        PathValues.API_V1_ALLOWED_VALUES_GENRE: ApiV1AllowedValuesGenre,
        PathValues.API_V1_PLAYLIST_SONGTRADR_PLAYLIST_GUID: ApiV1PlaylistSongtradrPlaylistGuid,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_USER_UPDATEPASSWORD: ApiV1UserUpdatePassword,
        PathValues.API_V1_USER_TOKEN: ApiV1UserToken,
        PathValues.API_V1_USER_SIGNUP: ApiV1UserSignUp,
        PathValues.API_V1_USER_SAVE_PLAYLIST: ApiV1UserSavePlaylist,
        PathValues.API_V1_USER_REFERRERS_NEW: ApiV1UserReferrersNew,
        PathValues.API_V1_USER_ME: ApiV1UserMe,
        PathValues.API_V1_USER_LOGIN: ApiV1UserLogin,
        PathValues.API_V1_USER_FORGOTPASSWORD: ApiV1UserForgotPassword,
        PathValues.API_V1_USER_FILE_OBJECT_KEY: ApiV1UserFileObjectKey,
        PathValues.API_V1_USER_FILE_NAME_INIT_UPLOAD: ApiV1UserFileNameInitUpload,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR: ApiV1PublicRecordingSearchGranular,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH_GRANULAR_ABSTRACTION: ApiV1PublicRecordingSearchGranularAbstraction,
        PathValues.API_V1_PLAYLIST: ApiV1Playlist,
        PathValues.API_V1_USER_REFERRERS_USERNAME: ApiV1UserReferrersUsername,
        PathValues.API_V1_USER_FOLDERS: ApiV1UserFolders,
        PathValues.API_V1_USER_FOLDER_FOLDER_NAME_TAGSTRENGTHS: ApiV1UserFolderFolderNameTagstrengths,
        PathValues.API_V1_USER_FOLDER_FOLDER_NAME_TAGGRAMS: ApiV1UserFolderFolderNameTaggrams,
        PathValues.API_V1_USER_FILES: ApiV1UserFiles,
        PathValues.API_V1_USER_FILES_SUMMARY: ApiV1UserFilesSummary,
        PathValues.API_V1_USER_FILES_STATUS: ApiV1UserFilesStatus,
        PathValues.API_V1_USER_FILES_DOWNLOAD: ApiV1UserFilesDownload,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_TAGSTRENGTHS: ApiV1PublicRecordingIdsTagstrengths,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_TAGGRAMS: ApiV1PublicRecordingIdsTaggrams,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_SIMILARITIES: ApiV1PublicRecordingIdsSimilarities,
        PathValues.API_V1_PUBLIC_RECORDING_IDS_MUSICAL_FEATURES: ApiV1PublicRecordingIdsMusicalFeatures,
        PathValues.API_V1_PUBLIC_RECORDING_SEARCH: ApiV1PublicRecordingSearch,
        PathValues.API_V1_PUBLIC_RECORDING_S_IDS: ApiV1PublicRecordingSIds,
        PathValues.API_V1_PUBLIC_RECORDING_M_IDS: ApiV1PublicRecordingMIds,
        PathValues.API_V1_PUBLIC_RECORDING_L_IDS: ApiV1PublicRecordingLIds,
        PathValues.API_V1_PARTY: ApiV1Party,
        PathValues.API_V1_ALLOWED_VALUES_TAG: ApiV1AllowedValuesTag,
        PathValues.API_V1_ALLOWED_VALUES_MUSICAL_FEATURES: ApiV1AllowedValuesMusicalFeatures,
        PathValues.API_V1_ALLOWED_VALUES_GENRE: ApiV1AllowedValuesGenre,
        PathValues.API_V1_PLAYLIST_SONGTRADR_PLAYLIST_GUID: ApiV1PlaylistSongtradrPlaylistGuid,
    }
)
