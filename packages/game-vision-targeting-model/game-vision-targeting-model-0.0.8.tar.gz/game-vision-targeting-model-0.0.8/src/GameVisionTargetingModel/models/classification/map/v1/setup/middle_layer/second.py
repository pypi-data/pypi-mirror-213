from keras.layers \
    import \
    Conv2D, \
    AveragePooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_second_middle_layer(
        layers: list
):
    second_layer_size: int = 256
    padding_style: str = 'same'

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            second_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        AveragePooling2D(
            (2, 2)
        )
    )

