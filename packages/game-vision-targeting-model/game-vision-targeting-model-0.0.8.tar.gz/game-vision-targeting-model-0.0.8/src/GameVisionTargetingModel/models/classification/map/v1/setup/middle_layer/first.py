from keras.layers \
    import \
    Conv2D, \
    AveragePooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_first_middle_layer(
        layers: list
):
    first_layer_size: int = 512
    padding_style: str = 'same'

    layers.append(
        Conv2D(
            first_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            first_layer_size,
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
