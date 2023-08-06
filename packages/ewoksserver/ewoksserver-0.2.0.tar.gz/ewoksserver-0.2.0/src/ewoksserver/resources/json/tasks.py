from typing import List, Dict, Optional

import flask
from flask import current_app

from ewoksjob.client import discover_all_tasks
from ewoksjob.client.local import discover_all_tasks as discover_all_tasks_local
from ewoksjob.client import discover_tasks_from_modules
from ewoksjob.client.local import (
    discover_tasks_from_modules as discover_tasks_from_modules_local,
)

from . import resource
from .. import api


class Task(resource.JsonResource):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["task_identifier"]

    @api.get_resource("task")
    def get(self, identifier: resource.ResourceIdentifierType) -> resource.ResponseType:
        return self.load_resource(identifier)

    @api.put_resource("task")
    def put(
        self, identifier: resource.ResourceIdentifierType, **resource
    ) -> resource.ResponseType:
        return self.save_resource(
            resource, error_on_missing=True, identifier=identifier
        )

    @api.delete_resource("task")
    def delete(
        self, identifier: resource.ResourceIdentifierType
    ) -> resource.ResponseType:
        return self.delete_resource(identifier)


class Tasks(resource.JsonResource):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["task_identifier"]

    @api.list_resource_identifiers("task")
    def get(self) -> resource.ResponseType:
        return self.list_resource_identifiers()

    @api.post_resource("task")
    def post(self, **resource) -> resource.ResponseType:
        return self.save_resource(resource, error_on_exists=True)


class Descriptions(resource.JsonResource):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["task_identifier"]

    @api.list_resource_content("task")
    def get(self):
        return self.list_resource_content()


class DiscoverTasks(resource.JsonResource):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["task_identifier"]

    @api.discover_resources("task")
    def post(self, modules: Optional[List[str]], worker_options: Optional[Dict] = None):
        try:
            tasks = discover_tasks(
                current_app, modules=modules, reload=True, worker_options=worker_options
            )
        except ModuleNotFoundError as e:
            return self.make_response(404, message=str(e))
        for task in tasks:
            response, code = self.save_resource(task)
            if code != 200:
                return response, code
        tasks = [desc["task_identifier"] for desc in tasks]
        return self.make_response(200, identifiers=tasks)


def discover_tasks(
    app: flask.Flask,
    modules: Optional[List[str]] = None,
    reload: Optional[bool] = None,
    worker_options: Optional[Dict] = None,
) -> List[Dict[str, str]]:
    if worker_options is None:
        kwargs = dict()
    else:
        kwargs = dict(worker_options)

    discover_kwargs = dict()
    if modules:
        kwargs["args"] = modules
    if reload is not None:
        discover_kwargs["reload"] = reload
    kwargs["kwargs"] = discover_kwargs

    if app.config.get("CELERY") is None:
        if modules:
            future = discover_tasks_from_modules_local(**kwargs)
        else:
            future = discover_all_tasks_local(**kwargs)
        tasks = future.result()
    else:
        if modules:
            future = discover_tasks_from_modules(**kwargs)
        else:
            future = discover_all_tasks(**kwargs)
        tasks = future.get()

    for task in tasks:
        _default_task_properties(task)
    return tasks


def _default_task_properties(task: dict) -> None:
    if not task.get("icon"):
        task["icon"] = "default.png"
    if not task.get("label"):
        task_identifier = task.get("task_identifier")
        if task_identifier:
            task["label"] = task_identifier.split(".")[-1]
