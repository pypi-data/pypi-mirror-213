from songtradr_api_client_python.paths.api_v1_user_file_object_key.get import ApiForget
from songtradr_api_client_python.paths.api_v1_user_file_object_key.post import ApiForpost
from songtradr_api_client_python.paths.api_v1_user_file_object_key.delete import ApiFordelete


class ApiV1UserFileObjectKey(
    ApiForget,
    ApiForpost,
    ApiFordelete,
):
    pass
