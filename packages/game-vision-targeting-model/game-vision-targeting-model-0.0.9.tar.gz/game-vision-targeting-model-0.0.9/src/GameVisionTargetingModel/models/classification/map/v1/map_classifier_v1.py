from keras.models \
    import Sequential

from tensorflow \
    import get_logger

from GameVisionTargetingModel.models.classification.map.v1.layers \
    import generate_layers_for_map_classifier_v1

from keras.losses \
    import SparseCategoricalCrossentropy

from keras.metrics              \
    import                      \
    Accuracy,                   \
    SparseCategoricalAccuracy

from logging \
    import ERROR


def tensorflow_settings():
    get_logger().setLevel(
        ERROR
    )


class MapClassifier(
    Sequential
):
    def __init__(
            self,
            optional_preprocessing: bool = False
    ):
        super().__init__(
            generate_layers_for_map_classifier_v1(
                optional_preprocessing
            )
        )

        tensorflow_settings()

        self.setup()

    def setup(self):
        self.compile(
            loss=SparseCategoricalCrossentropy(
                from_logits=True,
                ignore_class=None
            ),
            metrics=[
                Accuracy('accuracy'),
            ],
            optimizer='adam',
            jit_compile=True
        )

