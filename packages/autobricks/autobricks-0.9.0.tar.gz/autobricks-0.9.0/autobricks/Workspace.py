from .api_service import ApiService, autobricks_logging
from typing import List, Union

from ._decode_utils import (
    base64_encode,
    base64_decode,
)
import os

from enum import Enum

_logger = autobricks_logging.get_logger(__name__)

endpoint = "workspace"


_api_service = ApiService()


class DeployMode(Enum):
    DEFAULT = "DEFAULT"
    MOVE = "MOVE"
    PARENT = "PARENT"
    CHILD = "CHILD"
    ROOT_CHILD = "ROOT_CHILD"


class Extension(Enum):
    py = "py"
    html = "html"
    ipynb = "ipynb"
    dbc = "dbc"
    sql = "sql"


class Format(Enum):
    SOURCE = "SOURCE"
    HTML = "HTML"
    JUPYTER = "JUPYTER"
    DBC = "DBC"
    AUTO = "AUTO"


class Language(Enum):
    SCALA = "SCALA"
    PYTHON = "PYTHON"
    SQL = "SQL"
    R = "R"


class ObjectType(Enum):
    DIRECTORY = "DIRECTORY"
    NOTEBOOK = "NOTEBOOK"
    LIBRARY = "LIBRARY"
    FILE = "FILE"
    REPO = "REPO"


def get_language(extension: Extension):
    if extension == Extension.py:
        return Language.PYTHON
    elif extension == Extension.sql:
        return Language.SQL
    else:
        raise Exception("unknown language for extension")


def workspace_import(
    from_path: str,
    to_path: str,
    format: Format = Format.AUTO,
    language: Language = None,
    overwrite=True,
):
    with open(from_path, "rb") as file:
        content = base64_encode(file.read())

    data = {
        "path": to_path,
        "format": format.name,
        "content": content,
        "overwrite": overwrite,
    }

    if language:
        data["language"] = language.name

    _logger.info(f"workspace import {from_path} to {to_path}")

    return _api_service.api_post(endpoint, "import", data)


def workspace_delete(path: str, recursive: True):
    data = {"path": path, "recursive": recursive}
    _logger.info(f"workspace deleting path {path} recursive {str(recursive)}")
    return _api_service.api_post(endpoint, "delete", data)


def workspace_get_status(path: str):
    data = {"path": path}
    _logger.info(f"workspace getting status path {path}")
    return _api_service.api_get(endpoint, "get-status", data)


def workspace_list(path: str):
    data = {"path": path}
    _logger.info(f"workspace listing path {path}")
    return _api_service.api_get(endpoint, "list", data)


def workspace_mkdirs(path: str):
    data = {"path": path}
    _logger.info(f"workspace making dirs {path}")
    return _api_service.api_post(endpoint, "mkdirs", data)


def workspace_get_folder_id(path: str):
    dir = os.path.basename(path)
    parent = path.replace(dir, "")
    ls = workspace_list(parent)["objects"]
    try:
        gen = (d for d in ls if d["path"] == path)
        dir_data = next(gen)
        object_id = dir_data["object_id"]
    except Exception as e:
        msg = f"Path {path} not found in directory listing {ls}"
        raise Exception(msg) from e

    return object_id


def workspace_find_paths(
    folder_ids: List[str], root_folders: Union[str, List[str]] = None
):
    if not root_folders:
        return _workspace_find_paths(folder_ids)
    if isinstance(root_folders, str):
        return _workspace_find_paths(folder_ids, f"/{root_folders}")
    if isinstance(root_folders, list):
        workpsace_paths = {}
        for folder in root_folders:
            paths = _workspace_find_paths(folder_ids, f"/{folder}")
            workpsace_paths = {**workpsace_paths, **paths}

        return workpsace_paths


def _workspace_find_paths(folder_ids: List[str], path="/"):
    folder_ids = list(dict.fromkeys(folder_ids))
    ls = workspace_list(path)
    folder_paths = {}
    if ls:
        ls = ls["objects"]

        folder_paths = {}

        for folder in ls:
            id = folder["object_id"]
            object_type = ObjectType(folder["object_type"])
            path = folder["path"]
            if str(id) in folder_ids:
                folder_paths[str(id)] = folder["path"]
            if object_type == ObjectType.DIRECTORY:
                sub_folder_paths = _workspace_find_paths(folder_ids, path)
                folder_paths = {**folder_paths, **sub_folder_paths}

    return folder_paths


def workspace_export(from_path: str, format: Format, to_path: str):
    data = {"path": from_path, "format": format.name.upper(), "direct_download": False}

    _logger.info(
        f"workspace exporting from path {from_path} format {format.name.upper()}"
    )
    response = _api_service.api_get(endpoint, "export", data)

    file_type = response["file_type"]
    filename = os.path.basename(from_path)
    file_path = f"{to_path}/{filename}.{file_type}"

    content = base64_decode(response["content"])
    with open(file_path, "wb") as file:
        file.write(content)

    if file_type == "py":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.SOURCE.name,
        }

    elif file_type == "html":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.HTML.name,
        }

    elif file_type == "ipynb":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.JUPYTER.name,
        }

    elif file_type == "dbc":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.DBC.name,
        }

    return response


def workspace_dir_exists(path: str):
    try:
        reponse = workspace_get_status(path)
    except Exception:
        return False

    return reponse.get("object_type") == "DIRECTORY" and reponse.get("path") == path


def workspace_notebook_exists(path: str):
    try:
        reponse = workspace_get_status(path)
    except Exception:
        return False

    return reponse.get("object_type") == "NOTEBOOK" and reponse.get("path") == path


def workspace_import_dir(from_path: str, to_path: str, sub_dirs: List[str] = None):
    # automaticall adjust for user entered paths using the wrong separators
    from_path = os.path.abspath(from_path)

    response = {
        "from_path": from_path,
        "to_path": to_path,
        "actions": [],
    }

    _logger.info(f"Start deploying from from_path={from_path} to_path={to_path}")

    if sub_dirs:
        sub_dirs = [f"{to_path}/{d}" for d in sub_dirs]

    workspace_mkdirs(to_path)
    for root, subdirs, files in os.walk(from_path):
        dbx_root = root.replace(from_path, "")
        root_deploy_dir = to_path
        if dbx_root:
            root_deploy_dir = f"{root_deploy_dir}{dbx_root}"

        for dir in subdirs:
            deploy_dir = f"{root_deploy_dir}/{dir}"
            if sub_dirs:
                if from_path == root and deploy_dir in sub_dirs:
                    workspace_mkdirs(deploy_dir)
                else:
                    _logger.info(f"Skipping dir {deploy_dir}")
                if from_path != root:
                    workspace_mkdirs(deploy_dir)
            else:
                workspace_mkdirs(deploy_dir)

        for filename in files:
            from_file_path = os.path.join(root, filename)
            to_file_path = os.path.join(root_deploy_dir, filename)

            if sub_dirs:
                root_path = to_file_path.split("/")[:3]
                root_path = "/".join(root_path)
                if root_path in sub_dirs or "." in root_path:
                    action = _deploy_file(from_file_path, to_file_path)
                    response["actions"].append(action)
                else:
                    _logger.info(f"Skipping file {to_file_path}")
            else:
                action = _deploy_file(from_file_path, to_file_path)
                response["actions"].append(action)

    return response


def _deploy_file(
    from_file_path: str,
    to_file_path: str,
):
    action = {
        "action": "import",
        "from_file_path": from_file_path,
        "to_file_path": to_file_path,
    }

    workspace_import(from_path=from_file_path, to_path=to_file_path)

    return action


def _deploy_dir(deploy_dir: str):
    # make the directory it's not the root
    action = None
    if deploy_dir != "/":
        action = {"action": "mkdirs", "path": deploy_dir}
        workspace_mkdirs(deploy_dir)

    return action
