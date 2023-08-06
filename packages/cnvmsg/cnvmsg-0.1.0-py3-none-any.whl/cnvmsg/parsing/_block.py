from enum import Enum


class Block(Enum):
    Condition = "condition"
    Status = "status"
    Project = "project"
    Type = "type"
    Module = "module"
    Breaking = "breaking"
    Text = "text"


TextByBlock = dict[Block, str]
