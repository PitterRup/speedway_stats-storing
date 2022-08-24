from tests.random_data import random_rider_scores
from storing.domain.model import Heat


def test_heat_can_contain_only_4_riders():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    heat.save_result(random_rider_scores())

    # then
    assert list(heat.rider_scores.keys()) == ['a', 'b', 'c', 'd']