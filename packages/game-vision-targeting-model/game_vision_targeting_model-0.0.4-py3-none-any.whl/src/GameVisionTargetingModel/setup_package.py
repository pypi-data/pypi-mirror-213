from src.GameVisionTargetingModel.variables \
    import \
    set_channels, \
    set_width, \
    set_height, \
    set_last_layer_multiplier, \
    set_number_of_labels


def default_settings() -> None:
    setup_input_variables()
    setup_output_variables()


def setup_input_variables(
        width: int = 512,
        height: int = 512,
        channels: int = 3
):
    set_width(
        width
    )

    set_height(
        height
    )

    set_channels(
        channels
    )


def setup_output_variables(
        last_layer_multiplier: int = 8,
        number_of_labels: int = 100,
):
    set_last_layer_multiplier(
        last_layer_multiplier
    )

    set_number_of_labels(
        number_of_labels
    )
