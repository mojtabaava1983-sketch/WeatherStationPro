import pytest

from plugins import (
    DuplicatePluginError,
    IncompatiblePluginError,
    Plugin,
    PluginContext,
    PluginInfo,
    PluginRegistry,
)
from plugins.example_plugin import ExamplePlugin

class BadVersionPlugin(Plugin):
    @property
    def info(self):
        return PluginInfo(
            plugin_id="bad.version",
            name="Bad Version",
            version="1.0.0",
            api_version="999",
        )

def test_register_plugin():
    registry = PluginRegistry(api_version="1")
    registry.register(ExamplePlugin())
    assert registry.get("example.plugin") is not None

def test_duplicate_plugin_rejected():
    registry = PluginRegistry()
    registry.register(ExamplePlugin())
    with pytest.raises(DuplicatePluginError):
        registry.register(ExamplePlugin())

def test_incompatible_plugin_rejected():
    registry = PluginRegistry()
    with pytest.raises(IncompatiblePluginError):
        registry.register(BadVersionPlugin())

def test_lifecycle():
    registry = PluginRegistry()
    registry.register(ExamplePlugin())

    context = PluginContext()
    registry.initialize_all(context)
    assert context.services["example.plugin"]["initialized"] is True

def test_list_info():
    registry = PluginRegistry()
    registry.register(ExamplePlugin())
    info = registry.list_info()
    assert len(info) == 1
    assert info[0].plugin_id == "example.plugin"
