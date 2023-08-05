from GameVisionTargetingModel.setup_package \
    import default_settings

from GameVisionTargetingModel.variables \
    import          \
    get_width,      \
    get_height,     \
    get_channels


def test_defaults() -> None:
    default_settings()


def test_height() -> None:
    assert get_height() == 512


def test_width() -> None:
    assert get_width() == 512


def test_channels() -> None:
    assert get_channels() == 3
