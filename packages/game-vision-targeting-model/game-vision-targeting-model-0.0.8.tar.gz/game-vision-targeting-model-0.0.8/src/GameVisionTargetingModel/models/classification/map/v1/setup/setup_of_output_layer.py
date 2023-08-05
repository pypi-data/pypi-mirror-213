from keras.layers \
    import \
    Flatten, \
    Dense

from GameVisionTargetingModel.variables\
    import \
    get_number_of_labels, \
    get_last_layer_multiplier


def generate_output_layer(
    layers: list
):
    size_of_decision_layer: int = get_number_of_labels() * get_last_layer_multiplier()

    layers.append(
        Flatten()
    )

    layers.append(
        Dense(
            size_of_decision_layer
        )
    )

    layers.append(
        Dense(
            get_number_of_labels()
        )
    )
