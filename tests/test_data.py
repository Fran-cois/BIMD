"""Tests for the eras data loader."""

import datetime

import pytest

from bimd.data import Era, find_era, load_eras
from bimd.i18n import set_lang


@pytest.fixture(autouse=True)
def _force_french():
    set_lang("fr")
    yield
    set_lang("fr")


class TestLoadEras:
    def test_loads_all_eras(self):
        eras = load_eras()
        assert len(eras) >= 10

    def test_loads_english_eras(self):
        eras = load_eras(lang="en")
        names = [e.name for e in eras]
        assert "The Silent Era" in names

    def test_loads_french_eras(self):
        eras = load_eras(lang="fr")
        names = [e.name for e in eras]
        assert "L'Ère Silencieuse" in names

    def test_eras_sorted_by_start_date(self):
        eras = load_eras()
        dates = [e.start_date for e in eras]
        assert dates == sorted(dates)

    def test_every_era_has_required_fields(self):
        for era in load_eras():
            assert era.id
            assert era.name
            assert era.start_date < era.end_date
            assert len(era.top_models) >= 1
            assert era.context_window
            assert era.badge_label
            assert era.badge_color

    def test_no_date_gaps_between_consecutive_eras(self):
        """Adjacent eras should not overlap (start > prev end)."""
        eras = load_eras()
        for i in range(1, len(eras)):
            assert eras[i].start_date > eras[i - 1].start_date

    def test_every_era_has_boomer_comments(self):
        for era in load_eras():
            assert len(era.boomer_comments) >= 1, f"{era.id} has no comments"


class TestFindEra:
    def test_pre_transformer(self):
        era = find_era(datetime.date(2015, 6, 1))
        assert era is not None
        assert era.id == "pre_transformer"

    def test_gpt3_dawn(self):
        era = find_era(datetime.date(2021, 1, 15))
        assert era is not None
        assert era.id == "gpt3_dawn"

    def test_chatgpt_explosion(self):
        era = find_era(datetime.date(2022, 12, 25))
        assert era is not None
        assert era.id == "chatgpt_explosion"

    def test_gpt4_revolution(self):
        era = find_era(datetime.date(2023, 3, 14))
        assert era is not None
        assert era.id == "gpt4_revolution"

    def test_open_source_wave(self):
        era = find_era(datetime.date(2024, 1, 15))
        assert era is not None
        assert era.id == "open_source_wave"

    def test_multimodal_era(self):
        era = find_era(datetime.date(2024, 6, 1))
        assert era is not None
        assert era.id == "multimodal_era"

    def test_reasoning_age(self):
        era = find_era(datetime.date(2024, 11, 1))
        assert era is not None
        assert era.id == "reasoning_age"

    def test_agent_era(self):
        era = find_era(datetime.date(2025, 6, 1))
        assert era is not None
        assert era.id == "agent_era"

    def test_future_unknown(self):
        era = find_era(datetime.date(2027, 5, 8))
        assert era is not None
        assert era.id == "future_unknown"

    def test_exact_boundary_start(self):
        era = find_era(datetime.date(2020, 6, 11))
        assert era is not None
        assert era.id == "gpt3_dawn"

    def test_exact_boundary_end(self):
        era = find_era(datetime.date(2022, 11, 29))
        assert era is not None
        assert era.id == "gpt3_dawn"
