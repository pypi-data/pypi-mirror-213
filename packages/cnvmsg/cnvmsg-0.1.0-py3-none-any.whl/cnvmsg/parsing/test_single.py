from cnvmsg.models import ConventionalMessage
from cnvmsg.parsing._parse import parse


def test_condition():
    inp: str = r"%after lunch% ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition_text == "after lunch"
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_status():
    inp: str = r"[waiting] ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status_text == "waiting"
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_text():
    inp: str = "ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_redundant_spaces_text():
    inp: str = "ability      to             call        a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_tags():
    inp: str = "ability to call a comrad #community #pyatiletka"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags == ["community", "pyatiletka"]


def test_stranded_tags():
    inp: str = "ability #forall to call a comrad #community #pyatiletka"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    # the redundant spaces should be correctly trimmed
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags == ["forall", "community", "pyatiletka"]


def test_breaking():
    inp: str = "!: ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is True
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_module():
    inp: str = "(factory): ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type is None
    assert cnvmsg.module_text == "factory"
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_type():
    inp: str = "feat: ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project is None
    assert cnvmsg.type_text == "feat"
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None


def test_project():
    inp: str = "ussr: ability to call a comrad"

    cnvmsg: ConventionalMessage = parse(inp)

    assert cnvmsg.message == inp
    assert cnvmsg.condition is None
    assert cnvmsg.status is None
    assert cnvmsg.project_text == "ussr"
    assert cnvmsg.type is None
    assert cnvmsg.module is None
    assert cnvmsg.is_breaking is False
    assert cnvmsg.text == "ability to call a comrad"
    assert cnvmsg.tags is None
