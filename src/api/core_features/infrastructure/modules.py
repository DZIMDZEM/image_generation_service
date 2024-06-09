from typing import List, Any

from src.api.core_features.infrastructure.app import AppModule
from src.api.core_features.infrastructure.custom_json import JsonModule
from src.api.core_features.infrastructure.models import ModelModule


def create_modules() -> List[Any]:
    modules = [
        AppModule(),
        JsonModule(),
        ModelModule(),
    ]

    return modules
