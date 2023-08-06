from GameVisionTargetingModel.setup_package \
    import default_settings

from GameVisionTargetingModel.variables \
    import                      \
    get_width,                  \
    get_height,                 \
    get_channels,               \
    set_width,                  \
    set_height,                 \
    set_channels,               \
    set_number_of_labels,       \
    set_last_layer_multiplier,  \
    get_last_layer_multiplier,  \
    get_number_of_labels


def test_defaults() -> None:
    default_settings()


def test_height() -> None:
    height = 256

    set_height(height)

    assert get_height() == height


def test_width() -> None:
    width = 128

    set_width(width)

    assert get_width() == width


def test_channels() -> None:
    channels = 9

    set_channels(channels)

    assert get_channels() == channels


def test_number_labels() -> None:
    n_labels = 20

    set_number_of_labels(n_labels)

    assert get_number_of_labels() == n_labels


def test_last_layers() -> None:
    multiplier = 2

    set_last_layer_multiplier(multiplier)

    assert get_last_layer_multiplier() == multiplier
