import os
from typing import TypeVar

from injector import Injector

from src.api.app import create_modules, create_app
from tests.core import HttpClient


def create_test_client():
    def step(context):
        app = context.app
        context.client = HttpClient(app=app)

    return step


def prepare_test_injector_server():
    def step(context):
        context.injector = Injector(modules=create_modules())

    return step


def prepare_api_server(modules=None):
    if modules is None:
        modules = []
    modules = list(modules)

    def step(context):
        initial_modules = create_modules()
        initial_modules.extend(modules)
        app = create_app(modules=initial_modules)
        context.app = app
        context.injector = app.injector

    return step


def prepare_injector(modules=None):
    if modules is None:
        modules = []
    modules = list(modules)

    def step(context):
        initial_modules = create_modules()
        initial_modules.extend(modules)
        context.injector = Injector(modules=initial_modules)

    return step


def prepare_data_for_count_people():
    def step(context):
        video_path = os.path.join(
            os.path.dirname(__file__),
            'test_files/people_inside_bus.mp4'
        )
        context.video = open(video_path, 'rb')

    return step


C = TypeVar("C")
