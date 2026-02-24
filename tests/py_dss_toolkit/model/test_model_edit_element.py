import pytest


def test_edit_element_valid_properties(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100))
    snapshot_study_13bus.model.edit_element("load", "my_load", {"kw": "200", "kvar": "50"})

    df = snapshot_study_13bus.model.element_data("load", "my_load")
    assert df.loc["kw", "my_load"] == "200"
    assert df.loc["kvar", "my_load"] == "50"


def test_edit_element_nonexistent_raises_value_error(snapshot_study_13bus):
    with pytest.raises(ValueError, match="does not exist in the model"):
        snapshot_study_13bus.model.edit_element("load", "nonexistent_load", {"kw": "200"})


def test_edit_element_invalid_property_raises_value_error(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100))

    with pytest.raises(ValueError, match="does not have property"):
        snapshot_study_13bus.model.edit_element("load", "my_load", {"not_a_real_prop": "999"})


def test_edit_element_case_insensitive_property(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100))
    snapshot_study_13bus.model.edit_element("load", "my_load", {"KW": "300"})

    df = snapshot_study_13bus.model.element_data("load", "my_load")
    assert df.loc["kw", "my_load"] == "300"
