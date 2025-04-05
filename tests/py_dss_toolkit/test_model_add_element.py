def test_is_element_in_model_returns_false(snapshot_study_13bus):
    assert snapshot_study_13bus.model.is_element_in_model("load", "my_load", ) is False

def test_is_element_in_model_returns_true_after_adding_element(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1=1, kv=4.16, kw=100))
    assert snapshot_study_13bus.model.is_element_in_model("load", "my_load") is True

def test_is_element_in_model_returns_right_values(snapshot_study_13bus):
    snapshot_study_13bus.model.add_element("load", "my_load", dict(phases=3, bus1=1, kv=4.16, kw=100))

    df = snapshot_study_13bus.model.element_data("load", "my_load")

    assert df.loc["phases", "my_load"] == '3'
    assert df.loc["bus1", "my_load"] == '1'
    assert df.loc["kv", "my_load"] == '4.16'
    assert df.loc["kw", "my_load"] == '100'
