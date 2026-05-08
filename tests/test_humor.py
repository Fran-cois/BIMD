"""Tests for the humor engine."""

import datetime

import pytest

from bimd.data import Era, load_eras
from bimd.humor import get_boomer_comment
from bimd.i18n import set_lang


@pytest.fixture(autouse=True)
def _force_french():
    set_lang("fr")
    yield
    set_lang("fr")


class TestGetBoomerComment:
    def test_returns_string(self):
        for era in load_eras():
            comment = get_boomer_comment(era)
            assert isinstance(comment, str)
            assert len(comment) > 10

    def test_comment_from_era_pool(self):
        eras = load_eras()
        for era in eras:
            comment = get_boomer_comment(era)
            assert comment in era.boomer_comments

    def test_fallback_when_no_comments(self):
        era = Era(
            id="test",
            name="Test",
            start_date=datetime.date(2000, 1, 1),
            end_date=datetime.date(2000, 12, 31),
            top_models=["Test"],
            models=[],
            context_window="0",
            badge_label="Test",
            badge_color="grey",
            boomer_comments=[],
        )
        comment = get_boomer_comment(era)
        assert isinstance(comment, str)
        assert len(comment) > 5

    def test_fallback_english(self):
        set_lang("en")
        era = Era(
            id="test",
            name="Test",
            start_date=datetime.date(2000, 1, 1),
            end_date=datetime.date(2000, 12, 31),
            top_models=["Test"],
            models=[],
            context_window="0",
            badge_label="Test",
            badge_color="grey",
            boomer_comments=[],
        )
        comment = get_boomer_comment(era)
        assert "Stack Overflow" in comment or "kids" in comment or "wrap" in comment
