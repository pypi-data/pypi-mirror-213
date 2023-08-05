from GameVisionTargetingModel.singletons \
    import get_map_classifier_model


def test_make() -> None:
    classifier = get_map_classifier_model()
    classifier.summary()

