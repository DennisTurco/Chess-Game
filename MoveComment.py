class MoveComment:
    score: float
    quality: str
    comment: str
    best: str

    def __init__(self, score: float, quality: str, comment: str, best: str) -> None:
        self.score = score
        self.quality = quality
        self.comment = comment
        self.best = best