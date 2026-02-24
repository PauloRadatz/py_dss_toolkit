def test_is_element_in_model_returns_true_for_valid_element(snapshot_study_13bus):
    assert snapshot_study_13bus.model.is_element_in_model("line", "632633") is True


def test_is_element_in_model_returns_false_for_invalid_element(snapshot_study_13bus):
    assert snapshot_study_13bus.model.is_element_in_model("line", "nonexistent_line") is False


def test_is_element_in_model_case_insensitivity(snapshot_study_13bus):
    assert snapshot_study_13bus.model.is_element_in_model("LiNe", "632633") is True
    assert snapshot_study_13bus.model.is_element_in_model("LINE", "632633") is True
    assert snapshot_study_13bus.model.is_element_in_model("line", "632633") is True


def test_is_element_in_model_wrong_class(snapshot_study_13bus):
    # Element name exists but in the wrong class
    assert snapshot_study_13bus.model.is_element_in_model("load", "632633") is False

