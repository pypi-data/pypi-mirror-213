from keras.models \
    import Sequential

from tensorflow import compat, get_logger

from src.GameVisionTargetingModel.models.classification.map.v1.layers \
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
    compat.v1.disable_eager_execution()
    get_logger().setLevel(
        ERROR
    )


class MapClassifier(
    Sequential
):
    def __init__(self):
        super().__init__(
            generate_layers_for_map_classifier_v1()
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

