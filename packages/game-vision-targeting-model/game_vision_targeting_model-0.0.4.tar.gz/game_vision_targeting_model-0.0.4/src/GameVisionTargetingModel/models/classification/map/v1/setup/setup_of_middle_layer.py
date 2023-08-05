from src.GameVisionTargetingModel.models.classification.map.v1.setup.middle_layer\
    import                          \
    generate_first_middle_layer,    \
    generate_second_middle_layer,   \
    generate_third_middle_layer,    \
    generate_decision_middle_layer


def generate_middle_layer(
        layers: list
):
    generate_first_middle_layer(
        layers
    )

    generate_second_middle_layer(
        layers
    )

    generate_third_middle_layer(
        layers
    )

    generate_decision_middle_layer(
        layers
    )
