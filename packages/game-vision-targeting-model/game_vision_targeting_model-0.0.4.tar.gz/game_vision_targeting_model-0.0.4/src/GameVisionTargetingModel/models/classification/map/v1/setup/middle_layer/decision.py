from keras.layers \
    import \
    Conv2D, \
    GlobalAveragePooling2D

from src.GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_decision_middle_layer(
        layers: list
):
    decision_layer_size = 64

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding='same',
            activation='relu'
        )
    )

    layers.append(
        GlobalAveragePooling2D()
    )

