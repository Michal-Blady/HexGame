from __future__ import annotations
from flask import (
    Blueprint, jsonify, render_template,
    request, redirect, url_for
)
from flask_sock import Sock
from core.board    import Cell
from core.engine   import HexEngine
from core.registry import new_game, load, save, _fn
from ai.random_ai  import RandomAI
from typing import Optional

bp   = Blueprint("hex_web", __name__, template_folder="templates", static_folder="static")
sock = Sock()

@bp.record_once
def _init(state):
    sock.init_app(state.app)

ai_white = RandomAI(Cell.WHITE)
peers: dict[str, set] = {}

@bp.route("/")
def index():
    mode = request.args.get("mode", "ai")
    gid  = request.args.get("gid")
    role = request.args.get("role")

    if mode == "online" and not gid:
        return render_template("index.html",
                               size=None, gid=None,
                               mode=mode, role=role)

    if not gid:
        info = new_game(size=11, with_ai=(mode == "ai"))
        return redirect(url_for("hex_web.index",
                                mode=mode,
                                gid=info["id"],
                                role="1"))

    return render_template("index.html",
                           size=11, gid=gid,
                           mode=mode, role=role)



@bp.post("/api/game")
def api_new():
    cfg  = request.get_json(force=True) or {}
    size = int(cfg.get("size", 11))
    ai   = bool(cfg.get("ai", False))
    info = new_game(size, ai)
    return jsonify(info), 201

@bp.get("/api/game/<gid>")
def api_get(gid):
    eng, info = load(gid)
    return jsonify({
        **info,
        "grid":   [[c.value for c in row] for row in eng.board.grid],
        "turn":   eng.turn.value,
        "winner": eng.winner().value if eng.winner() else None,
    })

@bp.patch("/api/game/<gid>/move")
def api_move(gid):
    eng, info = load(gid)
    r, c = map(int, request.json["rc"])
    if eng.board.empty(r, c) and eng.winner() is None:
        eng.play(r, c)
        if info["ai"] and eng.winner() is None:
            ar, ac = ai_white.get_move(eng.board)
            eng.play(ar, ac)
        save(gid, eng, info)
    return api_get(gid)

@bp.delete("/api/game/<gid>")
def api_delete(gid):
    _fn(gid).unlink(missing_ok=True)
    return "", 204


@sock.route("/ws/<gid>")
def ws_room(ws, gid):
    eng, info = load(gid)
    group     = peers.setdefault(gid, set())
    mode      = request.args.get("mode", "ai")
    role      = request.args.get("role")

    if info["ai"]:
        my_color = eng.turn.value
    elif mode == "online":
        my_color = int(role) if role else (1 if len(group) % 2 == 0 else 2)
    else:
        my_color = None

    group.add(ws)
    ws.send(f"assign:{my_color}")

    def push():
        state = {
            "grid":   [[c.value for c in row] for row in eng.board.grid],
            "turn":   eng.turn.value,
            "winner": eng.winner().value if eng.winner() else None
        }
        msg = jsonify(state).get_data(as_text=True)
        for w in list(group):
            try:
                w.send(msg)
            except:
                group.discard(w)

    push()

    try:
        while msg := ws.receive():
            r, c = map(int, msg.split(","))

            if my_color and my_color != eng.turn.value:
                continue

            if eng.board.empty(r, c) and eng.winner() is None:
                eng.play(r, c)
                if info["ai"] and eng.winner() is None:
                    ar, ac = ai_white.get_move(eng.board)
                    eng.play(ar, ac)
                save(gid, eng, info)
                push()
    finally:
        group.discard(ws)
        if not group:
            peers.pop(gid, None)
