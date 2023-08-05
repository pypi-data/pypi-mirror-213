import io
from contextlib import redirect_stdout
from unittest import mock

import pytest

from src.packit_deploy import cli
from src.packit_deploy.cli import prompt_yes_no, verify_data_loss
from src.packit_deploy.config import PackitConfig


def test_args_passed_to_start():
    with mock.patch("src.packit_deploy.cli.packit_start") as f:
        cli.main(["start", "config/basic"])

    assert f.called
    assert f.call_args[0][1]["--pull"] is False

    with mock.patch("src.packit_deploy.cli.packit_start") as f:
        cli.main(["start", "config/basic", "--pull"])

    assert f.called
    assert f.call_args[0][1]["--pull"] is True


def test_args_passed_to_stop():
    with mock.patch("src.packit_deploy.cli.packit_stop") as f:
        cli.main(["stop", "config/basic"])

    assert f.called
    assert f.call_args[0][1]["--kill"] is False
    assert f.call_args[0][1]["--network"] is False
    assert f.call_args[0][1]["--volumes"] is False

    with mock.patch("src.packit_deploy.cli.packit_stop") as f:
        cli.main(["stop", "config/basic", "--volumes", "--network"])

    assert f.called
    assert f.call_args[0][1]["--kill"] is False
    assert f.call_args[0][1]["--network"] is True
    assert f.call_args[0][1]["--volumes"] is True


def test_verify_data_loss_called():
    f = io.StringIO()
    with redirect_stdout(f):
        with mock.patch("src.packit_deploy.cli.verify_data_loss") as verify:
            verify.return_value = True
            cli.main(["stop", "config/basic", "--volumes"])

    assert verify.called
    assert verify.call_args[0][0]["--volumes"] is True


def test_verify_data_loss_silent_if_no_loss():
    cfg = PackitConfig("config/basic")
    f = io.StringIO()
    with redirect_stdout(f):
        with mock.patch("src.packit_deploy.cli.prompt_yes_no") as prompt:
            prompt.return_value = True
            verify_data_loss({"--volumes": False}, cfg)

    assert not prompt.called
    assert f.getvalue() == ""


def test_verify_data_loss_warns_if_loss():
    cfg = PackitConfig("config/basic")
    f = io.StringIO()
    with redirect_stdout(f):
        with mock.patch("src.packit_deploy.cli.prompt_yes_no") as prompt:
            prompt.return_value = True
            verify_data_loss({"--volumes": True}, cfg)

    assert prompt.called
    assert "WARNING! PROBABLE IRREVERSIBLE DATA LOSS!" in f.getvalue()


def test_verify_data_loss_throws_if_loss():
    cfg = PackitConfig("config/basic")
    with mock.patch("src.packit_deploy.cli.prompt_yes_no") as prompt:
        prompt.return_value = False
        with pytest.raises(Exception, match="Not continuing"):
            verify_data_loss({"--volumes": True}, cfg)


def test_verify_data_prevents_unwanted_loss():
    cfg = PackitConfig("config/basic")
    cfg.protect_data = True
    msg = "Cannot remove volumes with this configuration"
    with mock.patch("src.packit_deploy.cli.prompt_yes_no"):
        with pytest.raises(Exception, match=msg):
            verify_data_loss({"--volumes": True}, cfg)


def test_prompt_is_quite_strict():
    assert prompt_yes_no(lambda x: "yes")
    assert not prompt_yes_no(lambda x: "no")
    assert not prompt_yes_no(lambda x: "Yes")
    assert not prompt_yes_no(lambda x: "Great idea!")
    assert not prompt_yes_no(lambda x: "")
