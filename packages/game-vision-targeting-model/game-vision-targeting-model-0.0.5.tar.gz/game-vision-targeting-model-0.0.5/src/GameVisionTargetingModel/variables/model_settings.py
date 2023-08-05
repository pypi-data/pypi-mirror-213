# By default Settings
width: int = 512
height: int = 512

channels: int = 3

number_of_labels: int = 4
last_layer_multiplier: int = 8


# Accessors
def get_input_set():
    global \
        height, \
        width, \
        channels

    return (
        height,
        width,
        channels
    )


def get_width() -> int:
    global width
    return width


def set_width(
        value: int
) -> None:
    global width
    width = value


def get_height() -> int:
    global height
    return height


def set_height(
        value: int
) -> None:
    global width
    width = value


def get_channels() -> int:
    global channels
    return channels


def set_channels(
        value: int
) -> None:
    global channels
    channels = value


def get_last_layer_multiplier() -> int:
    global last_layer_multiplier
    return last_layer_multiplier


def get_number_of_labels() -> int:
    global number_of_labels
    return number_of_labels


def set_last_layer_multiplier(
        value: int
) -> None:
    global last_layer_multiplier
    last_layer_multiplier = value


def set_number_of_labels(
        value: int
) -> None:
    global number_of_labels
    number_of_labels = value
