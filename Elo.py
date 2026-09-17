"""Maps a human-friendly ELO rating to the Fairy-Stockfish "Skill Level" UCI
option (-5..20), using the reference points from README.md."""

_ELO_TO_SKILL: list[tuple[int, int]] = [
    (400, -5),
    (800, 0),
    (1000, 2),
    (1200, 5),
    (1400, 7),
    (1600, 10),
    (1800, 12),
    (2000, 15),
    (2300, 17),
    (2600, 20),
]


def elo_to_skill(elo: int) -> int:
    if elo <= _ELO_TO_SKILL[0][0]:
        return _ELO_TO_SKILL[0][1]
    if elo >= _ELO_TO_SKILL[-1][0]:
        return _ELO_TO_SKILL[-1][1]

    for (elo_a, skill_a), (elo_b, skill_b) in zip(_ELO_TO_SKILL, _ELO_TO_SKILL[1:]):
        if elo_a <= elo <= elo_b:
            ratio = (elo - elo_a) / (elo_b - elo_a)
            return round(skill_a + ratio * (skill_b - skill_a))

    return 0
