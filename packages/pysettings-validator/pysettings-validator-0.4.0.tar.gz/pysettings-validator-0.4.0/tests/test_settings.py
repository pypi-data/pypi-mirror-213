import pytest
import copy

from pysettings.base import BaseSettings
from pysettings.options import Option
from pysettings.exceptions import OptionNotAvailable, ConfigNotValid


def test_config_constructor():
    """Should contain options registry only for attributes of type Option"""

    class SettingsTest(BaseSettings):
        home = Option()
        url = Option()
        objects = []

    config = SettingsTest()
    assert sorted(config._options) == ["home", "url"]


def test_config_set_value():
    """Should set the underlying Option value"""

    class SettingsTest(BaseSettings):
        home = Option()

    config = SettingsTest()
    config.home = "test"
    option = config._get_option("home")
    assert option.value == "test"


def test_config_get_value():
    """Should get the underlying Option value"""

    class SettingsTest(BaseSettings):
        home = Option()

    config = SettingsTest()
    option = config._get_option("home")
    option.value = "test"
    assert config.home == "test"


def test_config_instance():
    """Should return a new instance of the config and not use the Class options"""

    class SettingsTest(BaseSettings):
        home = Option(default="klass")

    config = SettingsTest()
    config.home = "instance"
    assert SettingsTest.home.value == "klass"
    assert config.home == "instance"


def test_config_set_value_not_available():
    """Should raise an exception if the option is not present"""

    class SettingsTest(BaseSettings):
        pass

    config = SettingsTest()
    with pytest.raises(OptionNotAvailable):
        config.test = "test"


def test_config_get_value_not_available():
    """Should raise an exception if the option is not present"""

    class SettingsTest(BaseSettings):
        pass

    config = SettingsTest()
    with pytest.raises(OptionNotAvailable):
        config.test


def test_config_is_valid_all_options(mocker):
    """Should validate all Option attributes"""

    class SettingsTest(BaseSettings):
        option1 = Option()
        option2 = Option()

    config = SettingsTest()
    option1 = config._get_option("option1")
    option2 = config._get_option("option2")

    # Mock config options
    mocker.patch.object(option1, "_validate", return_value=(True, []))
    mocker.patch.object(option2, "_validate", return_value=(True, []))

    config.is_valid()
    assert option1._validate.call_count == 1
    assert option2._validate.call_count == 1


def test_config_is_valid(mocker):
    """Should return a success if the configuration is valid"""

    class SettingsTest(BaseSettings):
        home = Option()

    config = SettingsTest()
    option = config._get_option("home")

    # Mock config options
    mocker.patch.object(option, "_validate", return_value=(True, []))

    assert config.is_valid() == (True, [])


def test_config_is_not_valid(mocker):
    """Should return a failure if the configuration is not valid and raise_exception is False"""

    class SettingsTest(BaseSettings):
        home = Option()

    config = SettingsTest()
    option = config._get_option("home")

    # Mock config options
    mocker.patch.object(
        option, "_validate", return_value=(False, ["allow_null", "validator"])
    )

    assert config.is_valid(raise_exception=False) == (
        False,
        [{"home": ["allow_null", "validator"]}],
    )


def test_config_is_not_valid_exception(mocker):
    """Should raise an exception if the configuration is not valid and raise_exception is True"""

    class SettingsTest(BaseSettings):
        home = Option()

    config = SettingsTest()
    option = config._get_option("home")

    # Mock config options
    mocker.patch.object(option, "_validate", return_value=(False, ["validator"]))

    with pytest.raises(ConfigNotValid):
        assert config.is_valid()


def test_config_deepcopy():
    """Should clone the configuration when deepcopy() is called"""

    class SettingsTest(BaseSettings):
        home = Option(default="original")

    config = SettingsTest()
    clone_config = copy.deepcopy(config)
    clone_config.home = "clone"
    # Should be different Settings
    assert config != clone_config
    assert config.home == "original"
    assert clone_config.home == "clone"


def test_config_copy():
    """Should clone the configuration when copy() is called"""

    class SettingsTest(BaseSettings):
        home = Option(default="original")

    config = SettingsTest()
    clone_config = copy.copy(config)
    clone_config.home = "shallow-copy"
    # Should be different Settings but same Option (shallow copy)
    assert config != clone_config
    assert config.home == "shallow-copy"
    assert clone_config.home == "shallow-copy"
