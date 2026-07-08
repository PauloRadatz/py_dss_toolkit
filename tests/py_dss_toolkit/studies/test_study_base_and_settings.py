from unittest.mock import MagicMock

import pytest

from py_dss_toolkit.studies.StudySettings import StudySettings


class TestStudyBaseName:
    def test_name_setter_updates_value(self, snapshot_study_13bus):
        snapshot_study_13bus.name = "new_name"
        assert snapshot_study_13bus.name == "new_name"

    def test_name_initial_removes_blanks_and_lowercases(self, snapshot_study_13bus):
        assert " " not in snapshot_study_13bus.name
        assert snapshot_study_13bus.name == snapshot_study_13bus.name.lower()

    def test_name_setter_allows_arbitrary_string(self, snapshot_study_13bus):
        snapshot_study_13bus.name = "WITH SPACES"
        assert snapshot_study_13bus.name == "WITH SPACES"


class TestStudySettingsTimeRegex:
    @staticmethod
    def _make_settings(text_response: str) -> StudySettings:
        fake_dss = MagicMock()
        fake_dss.text.return_value = text_response
        settings = object.__new__(StudySettings)
        settings._dss = fake_dss
        return settings

    def test_parses_standard_format(self):
        settings = self._make_settings("[3.0, 0.0]")
        assert settings.time == (3.0, 0.0)

    def test_parses_integer_format(self):
        settings = self._make_settings("[10, 5]")
        assert settings.time == (10.0, 5.0)

    def test_parses_extra_whitespace(self):
        settings = self._make_settings("[  7.5 ,  12.3  ]")
        assert settings.time == (7.5, 12.3)

    def test_parses_no_whitespace(self):
        settings = self._make_settings("[0.0,0.0]")
        assert settings.time == (0.0, 0.0)

    def test_raises_on_malformed_response(self):
        settings = self._make_settings("unexpected output")
        with pytest.raises(AttributeError):
            _ = settings.time
