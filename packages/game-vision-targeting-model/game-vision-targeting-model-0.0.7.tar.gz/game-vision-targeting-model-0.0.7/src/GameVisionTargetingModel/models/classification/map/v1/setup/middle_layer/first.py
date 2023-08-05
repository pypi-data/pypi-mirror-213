from keras.layers \
    import \
    Conv2D, \
    MaxPooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_first_middle_layer(
        layers: list
):
    first_layer_size = 512

    layers.append(
        Conv2D(
            first_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            first_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        MaxPooling2D(
            (2, 2)
        )
    )