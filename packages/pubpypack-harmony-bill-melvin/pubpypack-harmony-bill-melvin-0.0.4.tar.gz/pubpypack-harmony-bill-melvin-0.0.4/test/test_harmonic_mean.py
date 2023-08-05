import pytest
import sys

from termcolor import colored

from imppkg.harmony import main


@pytest.mark.parametrize(
    "inputs, expected_value",
    [(["1", "4", "4"], 2.0), ([], 0.0), (["badinput"], 0.0)],
)
def test_harmony_inputs(inputs, expected_value, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)
    main()
    assert capsys.readouterr().out.strip() == colored(
        expected_value, "red", "on_yellow", attrs=["bold"]
    )
