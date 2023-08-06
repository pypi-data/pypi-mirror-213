import os
from pathlib import Path
from sidetrek.constants import USER_REPO_DATA_DIRNAME, USER_DATA_BUCKET
from typing import Any, Optional, Dict
from s3fs import S3FileSystem
import cloudpickle
import flytekit
from sidetrek.helpers import get_flyte_exec_id


def get_project_dir(repo_full_name: str) -> str:
    """
    Look for __project_root__.py inside repo dir to get the project dir
    - `__project_root__.py` is created inside generated repo during wf version deployment to denote project root dir

    Defaults to local repo path
    - WHY? `__project_root__.py` is only created after deploy, so if it doesn't exist, default to local repo path to avoid syntax error in wf graph

    """
    local_repo_path = "/" + ("workspace" / "source" / "project" / wf_id_id).as_posix()
    files = [str(p) for p in list(Path(local_repo_path).glob("**/__project_root__.py"))]
    print(f"files in get_project_dir={files}")
    if len(files) > 0:
        return files[0].replace("/__project_root__.py", "")
    else:
        return local_repo_path


def save_custom_objects(key: str, value: Dict[str, Any], test_prefix: Optional[str]) -> None:
    """
    Save any python code to s3 by serializing with cloudpickle.
    NOTE: custom_objects are unique per execution (by being stored under flyte execution id as s3 prefix)
    - key: unique key for custom_objects
    - value: dict of python code to save
    - test_prefix: ONLY used for testing
    """
    pickled_val = cloudpickle.dumps(value)

    # Construct bucket prefix
    flyte_exec_ctx = flytekit.current_context()
    flyte_exec_id = flyte_exec_ctx.execution_id.name
    user_prefix = test_prefix if test_prefix is not None else flyte_exec_id
    bucket_prefix = f"/custom_objects/{user_prefix}"

    s3 = S3FileSystem(anon=False)
    with s3.open(f"{USER_DATA_BUCKET}{bucket_prefix}/{key}", "wb") as f:
        f.write(pickled_val)


def load_custom_objects(bentoml_model_tag: str, key: str, test_prefix: Optional[str]) -> Dict[str, Any]:
    """
    Load cloudpickle serialized python code from save_custom_objects
    - bentoml_model_tag: bentoml model tag
    - key: unique key for custom_objects
    - test_prefix: ONLY used for testing - if provided in save_custom_objects, must be supplied here (overrides bentoml_model_tag)
    """
    # Get bucket prefix
    user_prefix = test_prefix if test_prefix is not None else get_flyte_exec_id(bentoml_model_tag)
    # bucket_prefix = f"/custom_objects/{user_prefix}"

    # s3 = S3FileSystem(anon=False)
    # with s3.open(f"{USER_DATA_BUCKET}{bucket_prefix}/{key}", "rb") as f:
    #     pickled_val = f.read()
    #     val = cloudpickle.loads(pickled_val)
    #     return val

    # Load the custom_objects locally (saved locally from s3 during model build)
    custom_objects_local_path = Path.cwd() / "src/custom_objects" / f"{user_prefix}.cpkl"
    with open(custom_objects_local_path, "rb") as f:
        pickled_val = f.read()
        val = cloudpickle.loads(pickled_val)
        return val
