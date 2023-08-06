from cnvmsg.models import ConventionalMessage
from cnvmsg.parsing._parse import parse


def test_project_type():
    inp: str = "ussr/feat: ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project_text == "ussr"
    assert cnvmsg.type_text == "feat"
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_project_type_module():
    inp: str = "ussr/feat(factory): ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project_text == "ussr"
    assert cnvmsg.type_text == "feat"
    assert cnvmsg.module_text == "factory"
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_project_type_module_breaking():
    inp: str = "ussr/feat(factory)!: ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project_text == "ussr"
    assert cnvmsg.type_text == "feat"
    assert cnvmsg.module_text == "factory"
    assert cnvmsg.is_breaking is True
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_composite():
    inp: str = \
        r"%after lunch% [waiting] ussr/feat(factory)!: ability to" \
        " call a comrad #community #pyatiletka"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition_text == "after lunch"
    assert cnvmsg.status_text == "waiting"
    assert cnvmsg.project_text == "ussr"
    assert cnvmsg.type_text == "feat"
    assert cnvmsg.module_text == "factory"
    assert cnvmsg.is_breaking is True
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags == ["community", "pyatiletka"]
