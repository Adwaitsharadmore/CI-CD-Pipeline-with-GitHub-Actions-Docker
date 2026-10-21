"""Simple, dependency-free synthetic capstone analytics validation engine."""
import csv
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = {"session_id", "player_id", "date", "game_mode", "completed", "score", "minutes", "revenue_usd"}

class DataQualityError(ValueError):
    pass

def load_sessions(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not FIELDS.issubset(reader.fieldnames):
            raise DataQualityError("Missing fields: " + ", ".join(sorted(FIELDS - set(reader.fieldnames or []))))
        sessions = []
        seen = set()
        for line, row in enumerate(reader, start=2):
            sid = (row["session_id"] or "").strip()
            pid = (row["player_id"] or "").strip()
            if not sid or not pid:
                raise DataQualityError(f"Row {line}: session_id/player_id must not be blank")
            if sid in seen:
                raise DataQualityError(f"Row {line}: duplicate session_id {sid}")
            seen.add(sid)
            if row["completed"] not in {"0", "1"}:
                raise DataQualityError(f"Row {line}: completed must be 0 or 1")
            if not row["date"] or not row["game_mode"]:
                raise DataQualityError(f"Row {line}: date/game_mode must be present")
            try:
                score = int(row["score"])
                minutes = float(row["minutes"])
                revenue = Decimal(row["revenue_usd"])
            except (TypeError, ValueError, InvalidOperation):
                raise DataQualityError(f"Row {line}: invalid numeric value") from None
            if score < 0 or minutes < 0 or revenue < 0:
                raise DataQualityError(f"Row {line}: negative metric")
            sessions.append({"session_id": sid,"player_id": pid,"date": row["date"],
                "game_mode": row["game_mode"],"completed": int(row["completed"]),
                "score": score,"minutes": minutes,"revenue_usd": revenue})
    if not sessions:
        raise DataQualityError("No sessions found")
    return sessions

def compute_metrics(sessions):
    n = len(sessions)
    players = Counter(s["player_id"] for s in sessions)
    by_mode = defaultdict(list)
    by_date = defaultdict(set)
    for s in sessions:
        by_mode[s["game_mode"]].append(s)
        by_date[s["date"]].add(s["player_id"])
    return {
        "total_sessions": n,
        "unique_players": len(players),
        "completion_rate": round(sum(s["completed"] for s in sessions) / n * 100, 1),
        "repeat_player_rate": round(sum(c>1 for c in players.values()) / len(players) * 100, 1),
        "avg_score": round(sum(s["score"] for s in sessions) / n, 1),
        "total_revenue": sum((s["revenue_usd"] for s in sessions), Decimal("0")),
        "modes": [{"name": name, "sessions": len(rows),
                   "completion_rate": round(sum(x["completed"] for x in rows) / len(rows) * 100, 1)}
                  for name, rows in sorted(by_mode.items())],
        "daily_players": [{"date": day, "players": len(pl)} for day, pl in sorted(by_date.items())],
    }
