from storing.domain.model import RiderScores, RiderScore, HelmetColor, Score

def random_rider_scores():
    return RiderScores(
        rider_a=RiderScore(
            score=Score.THREE,
            helmet_color=HelmetColor.RED,
            waring=False,
            defect=False,
            fall=False,
            exclusion=False,
        ),
        rider_b=RiderScore(
            score=Score.TWO,
            helmet_color=HelmetColor.BLUE,
            waring=False,
            defect=False,
            fall=False,
            exclusion=False,
        ),
        rider_c=RiderScore(
            score=Score.ONE,
            helmet_color=HelmetColor.WHITE,
            waring=False,
            defect=False,
            fall=False,
            exclusion=False,
        ),
        rider_d=RiderScore(
            score=Score.ZERO,
            helmet_color=HelmetColor.YELLOW,
            waring=False,
            defect=False,
            fall=False,
            exclusion=False,
        ),
    )