import pytest


def test_is_element_in_model_returns_false(snapshot_study_13bus):
    assert (
        snapshot_study_13bus.model.is_element_in_model(
            "load",
            "my_load",
        )
        is False
    )


def test_is_element_in_model_returns_true_after_adding_element(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100))
    assert snapshot_study_13bus.model.is_element_in_model("load", "my_load") is True


def test_is_element_in_model_returns_right_values(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100))

    df = snapshot_study_13bus.model.element_data("load", "my_load")

    assert df.loc["phases", "my_load"] == "3"
    assert "632" in str(df.loc["bus1", "my_load"])
    assert df.loc["kv", "my_load"] == "4.16"
    assert df.loc["kw", "my_load"] == "100"


def test_add_element_invalid_property_raises_with_valid_options(snapshot_study_13bus):
    """add_element raises ValueError with valid property options when given invalid property."""
    with pytest.raises(ValueError) as exc_info:
        snapshot_study_13bus.model.add_element(
            "load", "my_load", dict(phases=3, bus1="632.1.2.3", kv=4.16, kw=100, not_a_real_prop="999")
        )
    assert "does not have property 'not_a_real_prop'" in str(exc_info.value)
    assert "Valid options:" in str(exc_info.value)
