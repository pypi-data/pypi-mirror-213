from pysettings.test import SettingsWrapper


def test_settings_wrapper_init(test_settings):
    # Verify initial state of the SettingsWrapper object.
    # Internal attributes accessors must work.
    wrapper = SettingsWrapper(test_settings)
    assert wrapper._settings == test_settings
    assert wrapper._to_restore == []


def test_settings_wrapper_get(test_settings):
    # Wrapper API must be the same as the wrapped object.
    wrapper = SettingsWrapper(test_settings)
    assert wrapper.url == "https://example.com"
    assert wrapper.description == "A shiny Website!"


def test_settings_wrapper_set(test_settings):
    # Setting values must be reflected in the wrapped object.
    wrapper = SettingsWrapper(test_settings)
    wrapper.url = "https://www.example.com"
    wrapper.description = "New www.example.com"
    assert wrapper._settings.url == "https://www.example.com"
    assert wrapper._settings.description == "New www.example.com"


def test_settings_wrapper_finalize(test_settings):
    # Finalize restores original values.
    wrapper = SettingsWrapper(test_settings)
    wrapper.url = "https://www.example.com"
    wrapper.description = "New www.example.com"
    assert wrapper._to_restore == [
        ("url", "https://example.com"),
        ("description", "A shiny Website!"),
    ]
    wrapper.finalize()
    assert wrapper.url == "https://example.com"
    assert wrapper.description == "A shiny Website!"
    assert wrapper._to_restore == []


def test_settings_wrapper_finalize_multiple_set(test_settings):
    # Finalize correctly handles multiple assignment to the same attribute.
    wrapper = SettingsWrapper(test_settings)
    wrapper.url = "Assign 1"
    wrapper.url = "Assign 2"
    assert wrapper._to_restore == [
        ("url", "https://example.com"),
        ("url", "Assign 1"),
    ]
    wrapper.finalize()
    assert wrapper.url == "https://example.com"
    assert wrapper._to_restore == []
