rescaling_multiplier: float = 1./255


def get_rescaling_multiplier() -> float:
    global rescaling_multiplier
    return rescaling_multiplier


def set_rescaling_multiplier(
        value: float
) -> None:
    global rescaling_multiplier
    rescaling_multiplier = value
