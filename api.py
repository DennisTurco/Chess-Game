"""HTTP API exposing the Stockfish-backed engine to the React frontend.

Run with: python api.py
The frontend (see frontend/src/lib/api.ts) talks to this over HTTP during
development at http://localhost:5000.
"""

import logging
import threading

import chess
from flask import Flask, jsonify, request
from flask_cors import CORS

from Elo import elo_to_skill
from MoveEmulator import MoveEvaluator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s:%(lineno)d - %(message)s")
logger = logging.getLogger("api")

app = Flask(__name__)
CORS(app)

_engine_lock = threading.Lock()
_engine: MoveEvaluator | None = None


def get_engine() -> MoveEvaluator:
    global _engine
    if _engine is None:
        _engine = MoveEvaluator()
    return _engine


def bad_request(message: str):
    return jsonify({"error": message}), 400


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/best-move")
def best_move():
    data = request.get_json(silent=True) or {}
    fen = data.get("fen")
    elo = data.get("elo", 1200)
    time_limit = float(data.get("timeLimit", 0.5))

    if not fen:
        return bad_request("Missing 'fen'")

    try:
        chess.Board(fen)
    except ValueError:
        return bad_request("Invalid FEN")

    skill = elo_to_skill(int(elo))

    with _engine_lock:
        engine = get_engine()
        engine._set_skill_level(skill)
        try:
            uci_move = engine.get_best_move(fen, time_limit=time_limit)
        except Exception as exc:  # engine/timeout/no-legal-move errors
            logger.error("best-move failed: %s", exc)
            return bad_request(str(exc))

    return jsonify({"uci": uci_move, "skill": skill})


@app.post("/api/move-comment")
def move_comment():
    data = request.get_json(silent=True) or {}
    fen_before = data.get("fenBefore")
    move_uci = data.get("move")
    elo = data.get("elo", 1200)

    if not fen_before or not move_uci:
        return bad_request("Missing 'fenBefore' or 'move'")

    try:
        chess.Board(fen_before)
    except ValueError:
        return bad_request("Invalid FEN")

    skill = elo_to_skill(int(elo))

    with _engine_lock:
        engine = get_engine()
        engine._set_skill_level(skill)
        try:
            comment = engine.get_move_comment(fen_before, move_uci)
        except Exception as exc:
            logger.error("move-comment failed: %s", exc)
            return bad_request(str(exc))

    return jsonify(
        {
            "score": comment.score,
            "quality": comment.quality,
            "comment": comment.comment,
            "best": comment.best,
        }
    )


@app.teardown_appcontext
def _shutdown(_exc):
    pass


def _cleanup_engine():
    global _engine
    if _engine is not None:
        _engine.close()
        _engine = None


if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False, threaded=False)
    finally:
        _cleanup_engine()
