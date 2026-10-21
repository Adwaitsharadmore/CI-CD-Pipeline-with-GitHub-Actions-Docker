"""Tests deliberately cover normal data and data-quality failures."""
import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from src.analytics import DataQualityError, load_sessions, compute_metrics
from src.app import render_dashboard

COLUMNS = ["session_id", "player_id", "date", "game_mode", "completed", "score", "minutes", "revenue_usd"]

def row(**overrides):
    r = dict(session_id="s1",player_id="p1",date="2026-10-01",game_mode="Arcade",completed="1",score="20",minutes="15",revenue_usd="2.50")
    r.update(overrides)
    return r

class AnalyticsTests(unittest.TestCase):
    def load(self, rows):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"sessions.csv"
            with file.open("w",newline="") as handle:
                writer=csv.DictWriter(handle,fieldnames=COLUMNS)
                writer.writeheader();writer.writerows(rows)
            return load_sessions(file)

    def test_metric_formulas(self):
        rows = self.load([row(),row(session_id="s2",completed="0",score="10",revenue_usd="0.00"),row(session_id="s3",player_id="p2",game_mode="Trivia",score="30")])
        m=compute_metrics(rows)
        self.assertEqual(m["total_sessions"],3)
        self.assertEqual(m["unique_players"],2)
        self.assertEqual(m["repeat_player_rate"],50)
        self.assertEqual(m["completion_rate"],66.7)
        self.assertEqual(m["total_revenue"],Decimal("5.00"))

    def test_duplicate_sessions_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"duplicate session_id"):
            self.load([row(), row(player_id="p2")])

    def test_blank_player_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"must not be blank"):
            self.load([row(player_id="")])

    def test_negative_revenue_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"negative metric"):
            self.load([row(revenue_usd="-5")])

    def test_negative_score_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"negative metric"):
            self.load([row(score="-1")])

    def test_bad_completed_value_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"completed must be 0 or 1"):
            self.load([row(completed="unknown")])

    def test_empty_data_rejected(self):
        with self.assertRaisesRegex(DataQualityError,"No sessions"):
            self.load([])

    def test_dashboard_has_unique_metrics(self):
        m=compute_metrics(self.load([row()]))
        report=render_dashboard(m)
        self.assertIn("Repeat-player rate",report)
        self.assertIn("Game mode breakdown",report)
        self.assertIn("Quality checks completed",report)

if __name__ == "__main__":
    unittest.main()
