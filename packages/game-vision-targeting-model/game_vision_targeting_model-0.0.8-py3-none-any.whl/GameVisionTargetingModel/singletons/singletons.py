from keras.models \
    import Model

from GameVisionTargetingModel.models.classification \
    import MapClassifierVersion1

map_classifier_model = None


def get_map_classifier_model():
    global map_classifier_model

    if map_classifier_model is None:
        set_map_classifier_model(
            MapClassifierVersion1()
        )

    return map_classifier_model


def set_map_classifier_model(
        value: Model
):
    global map_classifier_model
    map_classifier_model = value


def delete_of_map_classifier() -> None:
    global map_classifier_model
    del map_classifier_model

