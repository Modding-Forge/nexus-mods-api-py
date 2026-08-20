"""Copyright (c) Modding Forge."""

import importlib
import inspect
import pkgutil
from types import ModuleType

from pydantic import BaseModel

import nexusmods_api


class TestPublicModelDocumentation:
    """Tests documentation metadata on public Pydantic models."""

    def test_every_public_model_field_has_a_description(self) -> None:
        """Tests that API reference generators can describe every model field."""

        # given
        missing_descriptions: list[str] = []

        # when
        for module in self.__package_modules():
            for _, model in inspect.getmembers(module, inspect.isclass):
                if model.__module__ != module.__name__:
                    continue
                if not issubclass(model, BaseModel):
                    continue
                for name, field in model.model_fields.items():
                    if field.description is None:
                        missing_descriptions.append(
                            f"{model.__module__}.{model.__name__}.{name}"
                        )

        # then
        assert missing_descriptions == []

    @staticmethod
    def __package_modules() -> list[ModuleType]:
        """Imports every module that belongs to the public distribution.

        Returns:
            list[ModuleType]: Imported modules in deterministic name order.
        """

        module_names: list[str] = sorted(
            item.name
            for item in pkgutil.walk_packages(
                nexusmods_api.__path__,
                prefix=f"{nexusmods_api.__name__}.",
            )
        )
        return [importlib.import_module(name) for name in module_names]
