"""
    python wrap of the databricks SQL API. Has the base operations and some more complex higher level workflows
    for devops, local development and source control

    Documented databrick api
    https://docs.databricks.com/sql/api/
"""
from .. import _logging
from .api_service import ApiService
import math
import os
import yaml
import json
from enum import Enum

from typing import Union, List
from .Workspace import (
    workspace_dir_exists,
    workspace_mkdirs,
    workspace_get_folder_id,
    workspace_find_paths,
)
from ._common import MetadataFormat, get_metadata_format, load_format, tags_exist_in


_logger = _logging.get_logger(__name__)
endpoint = "sql"
_PREVIEW = True
_API_VERSION = "2.0"
_FOLDERS = "folders/"

# creates an api service that handles the authentication
_api_service = ApiService()


class PermissionLevel(Enum):
    CAN_VIEW = "CAN_VIEW"
    CAN_RUN = "CAN_RUN"
    CAN_MANAGE = "CAN_MANAGE"


class ObjectType(Enum):
    query = "queries"


class AclCredential(Enum):
    user_acl = "user_name"
    group_acl = "group_name"


def _get_credential_type(name: str):
    """
    name: str   name o the credential

    If it contains an @ sign then determine it's an email address
    and therefore a users. TODO: change to regex pattern match
    """
    if "@" in name:
        return AclCredential.user_acl
    else:
        return AclCredential.group_acl


def queries_delete(query_id: str):
    _logger.info(f"Delete query {query_id}")
    response = _api_service.api_delete(
        endpoint,
        f"queries/{query_id}",
        preview=_PREVIEW,
        api_version=_API_VERSION,
    )

    return response


def queries(page_size: int = 10, order: str = "name", q=None):
    """
    page_size:int=10    Number of queries to return in a single API call
    order:str="name"    The attribute to order the queries by
    q:str=None          Query string for a full text search

    Calls the api endpint tor return a list queries and their details.
    https://docs.databricks.com/sql/api/queries-dashboards.html#operation/sql-analytics-get-queries
    """

    page: int = 1
    params = {"page_size": page_size, "page": page, "order": order, "q": q}
    _logger.info("listing queries")

    current_page_size = page_size
    page = 1
    results = []

    while True:
        params["page"] = page
        current_queries: dict = _api_service.api_get(
            endpoint,
            "queries",
            preview=_PREVIEW,
            params=params,
            api_version=_API_VERSION,
        )
        current_count = current_queries.get("count", 0)
        current_page = current_queries.get("page", 0)
        current_page_size = current_queries.get("page_size", 0)
        _logger.debug(
            f"exported page {current_page} page of {current_page_size} queries out of {current_count} total queries"
        )

        results = results + current_queries.get("results", [])
        _logger.debug(f"collected {len(results)} of {current_count} total queries")

        expected_page_threshold = math.ceil(current_count / current_page_size)
        if page >= expected_page_threshold:
            break

        page += 1

    _logger.debug(f"exported {len(results)}")

    return results


def set_acl(
    acl_name: Union[str, List[str]],
    permission: PermissionLevel,
    object_id: str,
    object_type: ObjectType = ObjectType.query,
):
    """
    acl_name: Union[str, List[str]]                         a string or string list of groups or users for acls that you want add
    permission:PermissionLevel                              the permission level that will be granted
    object_id:str                                           the object id to grant the permission on
    object_type:ObjectType=ObjectType.query                 the type of object to grant the permission on

    grants permission of an object to a list of users or groups.
    """

    if isinstance(acl_name, str):
        acl_name = [acl_name]

    acls = [
        {_get_credential_type(name).value: name, "permission_level": permission.value}
        for name in acl_name
    ]

    function = f"permissions/{object_type.value}/{object_id}"

    # deploy the SQL queries
    _api_service.api_post(
        endpoint,
        function,
        data=acls,
        preview=_PREVIEW,
        api_version=_API_VERSION,
    )


def queries_export_sql(
    page_size: int = 10,
    order: str = "name",
    root_folders: Union[str, List[str], None] = None,
    q: str = None,
    tags: Union[str, List[str], None] = None,
):
    """
    page_size:int=10    Number of queries to return in a single API call
    order:str="name"    The attribute to order the queries by
    q:str=None          Query string for a full text search
    tags: Union[str, List[str], None] = None  only export queries that have this or these tags

    Takes a list of query response dictionaries and writes the name and query into smaller dictionary
    for easier handling if you just want the query and nothing else.
    """

    def _lookup_workspace_path(parent: str, workspace_paths: dict):
        id = parent.replace(_FOLDERS, "")
        path = workspace_paths.get(id, "")
        return path

    sql_queries = queries(page_size, order=order, q=q)
    folder_ids = [
        s["options"]["parent"].replace(_FOLDERS, "")
        for s in sql_queries
        if tags_exist_in(tags, s["tags"])
    ]
    workspace_paths = workspace_find_paths(folder_ids, root_folders)
    name_sql = {
        s["name"]: {
            "id": s["id"],
            "name": s["name"],
            "query": s["query"],
            "options": {"parameters": s["options"].get("parameters")},
            "workspace_path": _lookup_workspace_path(
                s["options"]["parent"], workspace_paths
            ),
            "tags": s["tags"],
        }
        for s in sql_queries
        if tags_exist_in(tags, s["tags"])
    }

    _logger.debug(f"matched {len(name_sql.keys())} queries")
    return name_sql


def queries_export_sql_files(
    to_path: str = ".",
    page_size: int = 10,
    order: str = "name",
    root_folders: Union[str, List[str], None] = None,
    q: str = None,
    metadata_type=MetadataFormat.yaml,
    tags: Union[str, List[str], None] = None,
):
    """
    to_path:str="."     Where to write the sql query files to
    page_size:int=10    Number of queries to return in a single API call
    order:str="name"    The attribute to order the queries by
    q:str=None          Query string for a full text search
    tags: Union[str, List[str], None] = None  only export queries that have this or these tags

    Takes a list of query response dictionaries and writes the query
    to a sql file at the at the to_path using the query name.
    """

    sql_queries = queries_export_sql(
        page_size=page_size, order=order, root_folders=root_folders, q=q, tags=tags
    )
    os.makedirs(os.path.abspath(to_path), exist_ok=True)

    for name, details in sql_queries.items():
        # get the workspace patg
        relative_path = details.get("workspace_path", "")
        del details["workspace_path"]

        # figure out the absolute path
        relative_path = f"{to_path}/{relative_path}"
        abs_path = os.path.abspath(relative_path)
        os.makedirs(abs_path, exist_ok=True)

        # save the sql file
        sql_path = os.path.abspath(f"{abs_path}/{name}.sql")
        _logger.info(f"Writing sql query {name} to path {sql_path}")
        query = details["query"]
        query = query.replace("\r", "")
        with open(sql_path, "w", encoding="utf-8") as f:
            f.write(query)

        # save the yaml file
        details["query"] = f"./{name}.sql"
        yaml_path = f"{abs_path}/{name}.{metadata_type.value}"
        _logger.info(f"Writing yaml query details {name} to path {yaml_path}")
        if metadata_type == metadata_type.json:
            metadata_string = json.dumps(details, indent=4)
        elif metadata_type == metadata_type.yaml:
            metadata_string = yaml.safe_dump(details, indent=4)

        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(metadata_string)


def queries_get_query_id(name: str):
    """
    name: str   name of the query

    Returns the query id of a given query object. Many operations are by id
    and id's are different across different workspace environments.
    """

    sql_queries = queries(q=name)
    try:
        query = next(q for q in sql_queries if q.get("name").lower() == name.lower())
    except StopIteration:
        return None

    result = {
        name: {
            "id": query["id"],
            "data_source_id": query.get("data_source_id"),
            "parent": query["options"].get("parent"),
        }
    }

    return result


def queries_import_sql(metadata: dict):
    """
    metadata: dict  Dictionary of information required to create a new or edit and existing query

    Edit the sql definition or create a new query.
    """

    name = metadata["name"]
    # if it's an existing query then update it
    # else create a new one!
    existing_query = queries_get_query_id(name=name)
    if existing_query:
        query_id = existing_query[name].get("id")
        function = f"queries/{query_id}"

        if existing_query[name].get("data_source_id"):
            metadata["data_source_id"] = existing_query[name].get("data_source_id")

        _logger.info(f"Updating query id={query_id} name={name}")

        if existing_query[name]["parent"] != metadata["parent"]:
            _logger.info(f"Moving query id={query_id} name={name}")
            # folders can't be moved so we have to delete the query and rename it.
            queries_delete(query_id)
            existing_query = False

    if not existing_query:
        function = "queries"
        _logger.info(f"Creating query name={name}")

    # deploy the SQL queries
    _api_service.api_post(
        endpoint,
        function,
        data=metadata,
        preview=_PREVIEW,
        api_version=_API_VERSION,
    )


def _get_folder_id(workspace_path: str):
    if not workspace_dir_exists(workspace_path):
        workspace_mkdirs(workspace_path)
    folder_object_id = workspace_get_folder_id(workspace_path)
    return folder_object_id


def queries_import_sql_files(
    from_path: str,
    tags: Union[str, List[str], None] = None,
    share_with: Union[str, List[str], None] = None,
    permission: PermissionLevel = PermissionLevel.CAN_RUN,
):
    """
    from_path:str    Number of queries to return in a single API call
    tags: Union[str, List[str], None] = None  only import queries that have this or these tags
    share_with = Union[str, List[str], None] Once imported to dbx then grant permission to these credentials (groups or users)

    Takes a directory of SQL definitions in metadata and SQL files and uploads them databrick.
    If tags are provided it will only load those queries with those tags.
    If share_with is supplied then it will set ACLS on those groups.
    """

    sql_queries = []
    exceptions = []
    for root, _, files in os.walk(from_path):
        config_files = [f for f in files if get_metadata_format(f)]

        for f in config_files:
            filename = os.path.join(root, f)
            filename = os.path.abspath(filename)
            with open(filename, "r", encoding="utf-8") as f:
                metadata_format = get_metadata_format(filename)
                data: dict = load_format(f, metadata_format)

            in_tags = data["tags"]

            if tags_exist_in(tags, in_tags):
                filename = data["query"]
                sql_file_path = os.path.abspath(root)
                sql_file_path = os.path.join(sql_file_path, filename)
                with open(sql_file_path, "r", encoding="utf-8") as f:
                    data["query"] = f.read()

                workspace_path = root.replace(from_path, "").replace("\\", "/")
                folder_object_id = _get_folder_id(workspace_path)

                data["parent"] = f"{_FOLDERS}{folder_object_id}"
                sql_queries.append(data)

    for metadata in sql_queries:
        try:
            queries_import_sql(metadata)
            if share_with:
                # set the ACL permissions
                name = metadata["name"]
                existing_query = queries_get_query_id(name=name)
                query_id = existing_query[name].get("id")
                set_acl(share_with, permission, query_id, ObjectType.query)

        except Exception as e:
            msg = f"Failed to import query due to - {e}"
            _logger.error(msg)
            # continue trying to import the remaining queries
            exceptions.append(msg)

    # raise any exceptions that occured
    if exceptions:
        raise Exception("\n".join(exceptions))
