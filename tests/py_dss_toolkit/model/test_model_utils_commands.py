from types import SimpleNamespace

from py_dss_toolkit.model.ModelUtils import ModelUtils


class FakeDSS:
    def __init__(self):
        self.commands = []
        self.circuit = SimpleNamespace(elements_names=[])

    def text(self, command: str):
        self.commands.append(command)
        return ""


def test_disable_elements_type_emits_expected_batchedit_command():
    dss = FakeDSS()
    model_utils = ModelUtils(dss)

    model_utils.disable_elements_type("load")

    assert dss.commands == ["batchedit load..* enabled=false"]


def test_batchedit_emits_expected_property_assignment_command():
    dss = FakeDSS()
    model_utils = ModelUtils(dss)

    model_utils.batchedit("line", "normamps", "400")

    assert dss.commands == ["batchedit line..* normamps=400"]
