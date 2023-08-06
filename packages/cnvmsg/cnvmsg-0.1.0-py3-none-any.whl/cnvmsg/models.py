from pydantic import BaseModel

from cnvmsg.enums import MessageStatus, MessageType
from cnvmsg.errors import MissingFieldError


class MessageCondition(BaseModel):
    text: str


class MessageProject(BaseModel):
    name: str


class MessageModule(BaseModel):
    name: str


class ConventionalMessage(BaseModel):
    """
    Main conventional message represenation model.
    """
    message: str
    condition: MessageCondition | None = None
    status: MessageStatus | None = None
    project: MessageProject | None = None
    type: MessageType | None = None
    module: MessageModule | None = None
    is_breaking: bool = False
    text: str
    tags: list[str] | None = None

    @property
    def condition_text(self) -> str:
        if self.condition is None:
            raise MissingFieldError(field="condition")
        else:
            return self.condition.text

    @property
    def status_text(self) -> str:
        if self.status is None:
            raise MissingFieldError(field="status")
        else:
            return self.status.value

    @property
    def project_text(self) -> str:
        if self.project is None:
            raise MissingFieldError(field="project")
        else:
            return self.project.name

    @property
    def type_text(self) -> str:
        if self.type is None:
            raise MissingFieldError(field="type")
        else:
            return self.type.value

    @property
    def module_text(self) -> str:
        if self.module is None:
            raise MissingFieldError(field="module")
        else:
            return self.module.name
