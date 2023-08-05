from keras.layers \
    import \
    Rescaling

from GameVisionTargetingModel.variables \
    import                              \
    get_input_set,                      \
    get_rescaling_multiplier


def generate_input_layer(
    layers: list
):
    layers.append(
        Rescaling(
            get_rescaling_multiplier(),
            input_shape=get_input_set()
        )
    )

