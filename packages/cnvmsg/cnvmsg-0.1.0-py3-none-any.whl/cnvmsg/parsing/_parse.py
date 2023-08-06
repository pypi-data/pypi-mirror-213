import re

from cnvmsg.constants import CONDITION_MAX_LEN, STATUS_MAX_LEN
from cnvmsg.enums import MessageStatus, MessageType
from cnvmsg.errors import ReservedOperatorError
from cnvmsg.models import (ConventionalMessage, MessageCondition,
                           MessageModule, MessageProject)
from cnvmsg.parsing._block import Block, TextByBlock
from cnvmsg.parsing.patterns import (CONSECUTIVE_SPACES_PATTERN,
                                     FUTURE_RESERVED_OPERATOR_PATTERNS,
                                     MAIN_PART_PATTERN, TAG_PATTERN)
from cnvmsg.utils.string import replace


def parse(message: str) -> ConventionalMessage:
    """
    Parses a string into Conventional Message.

    Args:
        message:
            String message to be parsed.

    Returns:
        ConventionalMessage:
            Conventional Message object.
    """

    # TODO(ryzhovalex): How to improve this code:
    # - instead of doing custom loops, write better regex (i don't know regex
    #   well enough for this)

    condition: MessageCondition | None = None
    status: MessageStatus | None = None
    project: MessageProject | None = None
    _type: MessageType | None = None
    module: MessageModule | None = None
    is_breaking: bool = False
    text: str = ""
    tags: list[str] | None = None

    # iterate message manually to ensure perfectly correct message
    # nexti: where to continue main iteration
    nexti: int | None = None
    inter_message: str
    should_be_whitespace: bool = False
    completed: list[Block] = []
    for i, c in enumerate(message):
        if nexti is not None and nexti != i:
            continue
        elif should_be_whitespace:
            if c != " ":
                raise ValueError(
                    "expected whitespace between some blocks,"
                    f" got character={c} instead"
                )
            else:
                should_be_whitespace = False
                nexti = None
                continue
        else:
            nexti = None

            if c == "%":
                if len(completed) > 0:
                    raise ValueError(
                        "condition should be the first block to be parsed,"
                        f" instead there are completed={completed}"
                    )
                else:
                    nexti, inter_message = _parse_aux(
                        block=Block.Condition,
                        message=message[i+1:],
                        end_mark="%",
                        max_len=CONDITION_MAX_LEN
                    )
                    # correct the index to the full message length
                    nexti += i + 1
                    condition = MessageCondition(text=inter_message)
                    completed.append(Block.Condition)
                    should_be_whitespace = True
            elif c == "[":
                if len(completed) > 1:
                    raise ValueError(
                        "only 1 block can precede status, instead"
                        f" completed={completed}"
                    )
                else:
                    nexti, inter_message = _parse_aux(
                        block=Block.Status,
                        message=message[i+1:],
                        end_mark="]",
                        max_len=STATUS_MAX_LEN
                    )
                    nexti += i + 1
                    try:
                        status = MessageStatus(inter_message)
                    except ValueError as error:
                        raise ValueError(
                            f"unsupported status={inter_message}"
                        ) from error
                    else:
                        completed.append(Block.Status)
                        should_be_whitespace = True
            else:
                text_by_block: TextByBlock = _parse_main(
                    main_part=message[i:]
                )

                for k, v in text_by_block.items():
                    match k:
                        case Block.Project:
                            project = MessageProject(name=v)
                        case Block.Type:
                            _type = MessageType(v)
                        case Block.Module:
                            module = MessageModule(name=v)
                        case Block.Breaking:
                            is_breaking = v == "1"
                        case Block.Text:
                            text, tags = _parse_tags(v)
                        case _:
                            raise ValueError(
                                f"unsupported block={k} of main part"
                            )

                break

    return ConventionalMessage(
        message=message,
        condition=condition,
        status=status,
        project=project,
        type=_type,
        module=module,
        is_breaking=is_breaking,
        text=text,
        tags=tags
    )


def _parse_aux(
    *,
    block: Block,
    message: str,
    end_mark: str,
    max_len: int,
) -> tuple[int, str]:
    text: str = ""

    for i, c in enumerate(message):
        if c == end_mark:
            if text == "" or text.isspace():
                raise ValueError(f"empty block={block}")
            else:
                text = text.strip()
                return i + 1, text
        else:
            text += c

            if len(text) > max_len:
                raise ValueError(
                    f"max length of block={block} is exceeded for"
                    f" a message={message}"
                )

    raise ValueError(
        f"end_mark={end_mark} never occured for"
        f" block={block.value}, message={message}"
    )


def _parse_main(
    *,
    main_part: str
) -> TextByBlock:
    result: TextByBlock = {}
    rematch: re.Match | None = re.search(MAIN_PART_PATTERN, main_part)
    has_project: bool = False
    has_type: bool = False

    if rematch is None:
        raise ValueError(f"inreadable main_part={main_part}")
    else:
        groups: tuple[str] = rematch.groups()

        for i, g in enumerate(groups):
            if g is not None:
                match i:
                    case 0:
                        continue
                    case 1:
                        result[Block.Project] = g.strip()
                        has_project = True
                    case 2:
                        continue
                    case 3:
                        result[Block.Type] = g.strip()
                        has_type = True
                    case 4:
                        result[Block.Module] = replace(g, "(", ")")
                    case 5:
                        result[Block.Breaking] = "1"
                    case 6:
                        text: str = g.strip()
                        _check_reserved_operators(text)
                        result[Block.Text] = text

    # in the message like `feat: mytext`, the `feat` will be
    # assigned to Project block, so here we check if we can re-assign it to
    # Type block
    if has_project and not has_type:
        candidate: str = result[Block.Project]
        try:
            MessageType(candidate)
        except ValueError:
            # the Project block really has a custom-defined project, do nothing
            pass
        else:
            result[Block.Type] = candidate
            del result[Block.Project]

    return result


def _parse_tags(text: str) -> tuple[str, list[str] | None]:
    """
    Parses text for tags and returns cleared of tags text and list of tags
    (or None if no tags are found).
    """
    tags: list[str] | None = re.findall(TAG_PATTERN, text) or None

    if tags is not None:
        for i, tag in enumerate(tags):
            text = text.replace(tag, "")
            tags[i] = tag.replace("#", "")

    # remove consecutive spaces, also helps to remove two spaces left after
    # the tag cutting
    text = re.sub(CONSECUTIVE_SPACES_PATTERN, " ", text)

    return text.strip(), tags


def _check_reserved_operators(text: str) -> None:
    for pattern in FUTURE_RESERVED_OPERATOR_PATTERNS:
        if len(re.findall(pattern, text)) > 0:
            raise ReservedOperatorError(operator=pattern)
