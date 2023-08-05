from src.GameVisionTargetingModel.models.classification.map.v1.setup \
    import                  \
    generate_input_layer,   \
    generate_output_layer,  \
    generate_middle_layer,  \
    generate_preprocessing_layers


def generate_layers_for_map_classifier_v1(
        addition_of_preprocessing: bool = True
) -> list:
    return_layers: list = []

    generate_input_layer(
        return_layers
    )

    if addition_of_preprocessing:
        generate_preprocessing_layers(
            return_layers
        )

    generate_middle_layer(
        return_layers
    )

    generate_output_layer(
        return_layers
    )

    return return_layers
