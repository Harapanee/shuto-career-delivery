import sys, os, json, tempfile, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "publish"))
from zoneinfo import ZoneInfo
import state

JST = ZoneInfo("Asia/Tokyo")


def test_load_ファイルが無ければ空辞書():
    assert state.load(os.path.join(tempfile.mkdtemp(), "nope.json")) == {}


def test_save_load_往復():
    p = os.path.join(tempfile.mkdtemp(), "state.json")
    state.save(p, {"day01_0600": {"status": "published"}})
    assert state.load(p) == {"day01_0600": {"status": "published"}}


def test_is_published():
    d = {"a": {"status": "published"}, "b": {"status": "prepared"}}
    assert state.is_published(d, "a") is True
    assert state.is_published(d, "b") is False
    assert state.is_published(d, "c") is False


def test_mark_prepared():
    d = state.mark_prepared({}, "k", "CID", "2026-09-01T00:02:41+09:00")
    assert d["k"]["status"] == "prepared"
    assert d["k"]["container_id"] == "CID"
    assert d["k"]["container_created_at"] == "2026-09-01T00:02:41+09:00"


def test_mark_published_既存のcontainer_idを消さない():
    d = state.mark_prepared({}, "k", "CID", "2026-09-01T00:02:41+09:00")
    d = state.mark_published(d, "k", "MID", "2026-09-01T06:03:12+09:00")
    assert d["k"]["status"] == "published"
    assert d["k"]["media_id"] == "MID"
    assert d["k"]["published_at"] == "2026-09-01T06:03:12+09:00"
    assert d["k"]["container_id"] == "CID"


def test_fresh_container_id_23時間以内なら返す():
    d = state.mark_prepared({}, "k", "CID", "2026-09-01T00:00:00+09:00")
    now = datetime.datetime(2026, 9, 1, 18, 0, tzinfo=JST)
    assert state.fresh_container_id(d, "k", now) == "CID"


def test_fresh_container_id_23時間を超えたらNone():
    d = state.mark_prepared({}, "k", "CID", "2026-09-01T00:00:00+09:00")
    now = datetime.datetime(2026, 9, 2, 0, 0, tzinfo=JST)   # 24時間後
    assert state.fresh_container_id(d, "k", now) is None


def test_fresh_container_id_記録が無ければNone():
    now = datetime.datetime(2026, 9, 1, 18, 0, tzinfo=JST)
    assert state.fresh_container_id({}, "k", now) is None
