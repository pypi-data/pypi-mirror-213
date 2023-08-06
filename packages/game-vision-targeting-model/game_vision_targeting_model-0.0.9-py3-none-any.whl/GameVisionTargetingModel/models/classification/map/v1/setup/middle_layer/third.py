from keras.layers \
    import \
    Conv2D, \
    MaxPooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_third_middle_layer(
        layers: list
):
    third_layer_size: int = 128
    padding_style: str = 'same'

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        MaxPooling2D(
            (2, 2)
        )
    )
