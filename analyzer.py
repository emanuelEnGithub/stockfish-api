import chess
import chess.engine
import chess.pgn
from io import StringIO

ENGINE_PATH = "/usr/games/stockfish"

def classify_cp_loss(cp_loss):
    if cp_loss is None:
        return "Best"
    if cp_loss < 20:
        return "Inaccuracy"
    elif cp_loss < 100:
        return "Mistake"
    else:
        return "Blunder"

def analyze_pgn(pgn_text, depth=15):
    results = []
    pgn = chess.pgn.read_game(StringIO(pgn_text))
    board = pgn.board()

    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
        for move in pgn.mainline_moves():
            info = engine.analyse(board, chess.engine.Limit(depth=depth))
            best = info["pv"][0]
            score_before = info["score"].white().score(mate_score=100000)

            played_move = move
            board.push(move)

            info_after = engine.analyse(board, chess.engine.Limit(depth=depth))
            score_after = info_after["score"].white().score(mate_score=100000)

            cp_loss = None
            if score_before is not None and score_after is not None:
                cp_loss = abs(score_before - score_after)

            results.append({
                "played": played_move.uci(),
                "best": best.uci(),
                "cp_loss": cp_loss,
                "classification": classify_cp_loss(cp_loss)
            })

    avg_loss = round(sum(r["cp_loss"] for r in results if r["cp_loss"] is not None) / len(results), 2)
    accuracy = max(0, 100 - avg_loss / 2)  # Simple estimate

    return {
        "analysis": results,
        "average_centipawn_loss": avg_loss,
        "estimated_accuracy": round(accuracy, 2)
    }
