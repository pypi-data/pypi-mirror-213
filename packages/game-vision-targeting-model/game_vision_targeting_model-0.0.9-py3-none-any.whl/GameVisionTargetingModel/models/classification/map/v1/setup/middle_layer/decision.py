from keras.layers \
    import \
    Conv2D, \
    GlobalMaxPooling2D

from GameVisionTargetingModel.variables.model_settings \
    import \
    get_channels


def generate_decision_middle_layer(
        layers: list
):
    decision_layer_size: int = 64
    padding_style: str = 'same'

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        Conv2D(
            decision_layer_size,
            get_channels(),
            padding=padding_style,
            activation='relu'
        )
    )

    layers.append(
        GlobalMaxPooling2D()
    )

