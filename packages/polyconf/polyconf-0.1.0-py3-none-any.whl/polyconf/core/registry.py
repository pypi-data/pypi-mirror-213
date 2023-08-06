import importlib
import logging
import pkgutil
import types
from collections.abc import Iterator
from typing import Any, Callable

from polyconf.core.model import Context, Plugin
from polyconf.core.utils import pipe


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def iter_namespace(ns_pkg: types.ModuleType) -> Iterator[pkgutil.ModuleInfo]:
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.

    return pkgutil.iter_modules(ns_pkg.__path__, f"{ns_pkg.__name__}.")

    # ns_pkg_path = ns_pkg.__path__
    # result = pkgutil.walk_packages(ns_pkg_path, f"{ns_pkg.__name__}.")
    # return result


class Registry:
    def __init__(self, selected_plugins: list[str], **kwargs: Plugin) -> None:
        self.selected_plugins: list[str] = selected_plugins
        self._discovered_plugin_modules: dict[str, types.ModuleType] = {}
        self._active_plugin_modules: dict[str, Any] = {}
        self._active_plugins: dict[str, Plugin] = kwargs

    def discover_plugins(self, package: types.ModuleType) -> None:
        # fmt: off
        self._discovered_plugin_modules = {
            name.removeprefix(f"{package.__name__}."): importlib.import_module(f"{name}.plugin")
            for _finder, name, _is_pkg
            in iter_namespace(package)
        }
        # fmt: on

    @property
    def discovered_plugins(self) -> dict[str, types.ModuleType]:
        return self._discovered_plugin_modules

    def init_plugins(self, package: types.ModuleType | None = None, **kwargs: Any) -> None:
        if package is None:
            log.warning("No package specified. Doing nothing.")
            return

        if not self._discovered_plugin_modules:
            self.discover_plugins(package)

        if self.selected_plugins == ["ALL"]:
            self._active_plugin_modules = self._discovered_plugin_modules
        else:
            # fmt: off
            self._active_plugin_modules = {
                k: v
                for k, v in self._discovered_plugin_modules.items()
                if k in self.selected_plugins
            }
            # fmt: on

        # fmt: off
        self._active_plugins = {
            name: module.factory(**kwargs)
            for name, module in self._active_plugin_modules.items()
        }
        # fmt: on

    @property
    def available_plugins(self) -> list[Callable[[Context], Context]]:
        return [plugin.hydrate for plugin in self._active_plugins.values()]

    @property
    def plugins(self) -> list[Callable[[Context], Context]]:
        if not self.selected_plugins:
            return self.available_plugins
        # fmt: off
        return [
            plugin.hydrate
            for plugin in self._active_plugins.values()
            if plugin.name in self.selected_plugins
        ]
        # fmt: on

    @property
    def plugin_map(self) -> dict[str, Plugin]:
        return self._active_plugins

    def register_plugin(self, name: str, plugin: Plugin) -> None:
        self._active_plugins[name] = plugin


class FooPlugin(Plugin):
    name = "foo"

    def hydrate(self, context: Context) -> Context:
        self.logger.info(f'{self.name} says, "hello"')
        return context


class BarPlugin(Plugin):
    name = "bar"

    def hydrate(self, context: Context) -> Context:
        self.logger.info(f'{self.name} says, "hello"')
        self.add_result("zz", "ZZ", context, "fake")
        return context


if __name__ == "__main__":
    registry = Registry(selected_plugins=["bar"], foo=FooPlugin(log))
    registry.register_plugin("bar", BarPlugin(log))

    ctx = Context(app_name="widget", given={"a": "b", "c": "d"})
    result: Context = pipe(ctx, *registry.plugins)
    log.info(f"{result=}")
    # log.info(f"{result.as_obj=}")
