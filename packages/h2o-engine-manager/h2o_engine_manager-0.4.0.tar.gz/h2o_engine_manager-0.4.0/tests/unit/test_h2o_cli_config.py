import os

from h2o_engine_manager.clients.h2o_cli_config import CLIConfig


def test_h2o_cli_config():
    path = os.path.join(os.path.dirname(__file__), "test_data", "h2o-cli-config.toml")
    config = CLIConfig(path)
    assert config.token == "TestPlatformToken"
    assert config.url == "http://test.endpoint"
