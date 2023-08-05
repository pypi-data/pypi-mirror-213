from keras.layers \
    import \
    Conv2D, \
    MaxPooling2D

from src.GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_third_middle_layer(
        layers: list
):
    third_layer_size = 128

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            third_layer_size,
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
