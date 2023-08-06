from .api_service import ApiService, autobricks_logging
from typing import Union
from ._common import get_metadata_format, load_format
import os

_logger = autobricks_logging.get_logger(__name__)

endpoint = "pipelines"
_PIPELINES_API_VERSION = "2.0"
_api_service = ApiService()


class PipelineException(Exception):
    def __init__(self, name: Union[str, int]):
        if isinstance(name, int):
            msg = f"Failed on pipeline job_id={name}"
        else:
            msg = f"Failed on pipeline name={name}"

        self.message = msg
        super().__init__(self.message)


def pipeline_create(pipeline: dict):
    name = pipeline.get("name", "Unknown")
    pipeline["development"] = False
    if "id" in pipeline:
        del pipeline["id"]
    if "pipeline_id" in pipeline:
        del pipeline["pipeline_id"]
    try:
        response = _api_service.api_post(
            endpoint, None, pipeline, api_version=_PIPELINES_API_VERSION
        )
    except Exception:
        raise PipelineException(name)

    return response


def pipeline_update(pipeline: dict):
    pipeline_id = pipeline["id"]
    name = pipeline.get("name", "Unknown")
    pipeline["development"] = False

    try:
        response = _api_service.api_put(
            endpoint, pipeline_id, pipeline, api_version=_PIPELINES_API_VERSION
        )
    except Exception:
        raise PipelineException(name)

    return response


def pipeline_get_by_name(name: str):
    params = {"max_results": 1, "filter": f"name LIKE '{name}'"}
    try:
        response = _api_service.api_get(
            endpoint, None, api_version=_PIPELINES_API_VERSION, params=params
        )
    except Exception:
        raise PipelineException(name)

    pipeline = response.get("statuses")
    if len(pipeline) == 1:
        pipeline = pipeline[0]
    else:
        pipeline = None

    return pipeline


def pipeline_get_id(name: str):
    params = {"max_results": 1, "filter": f"name LIKE '{name}'"}
    try:
        response = _api_service.api_get(
            endpoint, None, api_version=_PIPELINES_API_VERSION, params=params
        )
    except Exception:
        raise PipelineException(name)

    pipeline = response.get("statuses")
    if pipeline is not None:
        pipeline = pipeline[0]
        pipeline = pipeline["pipeline_id"]

    return pipeline


def pipeline_get_by_id(pipeline_id: str):
    try:
        response = _api_service.api_get(
            endpoint, pipeline_id, api_version=_PIPELINES_API_VERSION
        )
    except Exception:
        raise PipelineException(pipeline_id)

    return response


def pipeline_create_or_replace(pipeline: dict):
    try:
        name = pipeline["name"]
    except KeyError as e:
        raise Exception(f"Pipeline definition doesn't have a {e}.")

    pipeline_id = pipeline_get_id(name)

    if pipeline_id is None:
        _logger.info(f"creating new job {name}")
        pipeline_create(pipeline=pipeline)
    else:
        _logger.info(f"updaing job {name} pipeline_id={pipeline_id}")
        pipeline["pipeline_id"] = pipeline_id
        pipeline_update(pipeline=pipeline)


def pipeline_import_pipelines(from_path: str):
    for root, _, files in os.walk(from_path):
        config_files = [f for f in files if get_metadata_format(f)]

        for f in config_files:
            filename = os.path.join(root, f)
            filename = os.path.abspath(filename)
            with open(filename, "r", encoding="utf-8") as f:
                metadata_format = get_metadata_format(filename)
                data: dict = load_format(f, metadata_format)

            pipeline_create_or_replace(data)
