from enum import Enum


class MessageStatus(Enum):
    """
    Attributes:
        Obsolete:
            just overriden somewhere but generally is not wrong
        Deprecated:
            wrong and no more accepted
        Maybe:
            might not be implemented
        Future:
            for future implementations/versions
        Nopoc:
            no proof of concept, often this is about a problem incident
        Waiting:
            waits for an another factor in order to be implemented
        Designing:
            in process of designing/actualizing
    """
    Obsolete = "obsolete"
    Deprecated = "deprecated"
    Maybe = "maybe"
    Future = "future"
    Nopoc = "nopoc"
    Waiting = "waiting"
    Designing = "designing"


class MessageType(Enum):
    """
    For more details see [Angular Commits](https://gist.github.com/brianclements/841ea7bffdb01346392c).
    """  # noqa: E501
    Feat = "feat"
    Refactor = "refactor"
    Fix = "fix"
    Build = "build"
    Ci = "ci"
    Docs = "docs"
    Perf = "perf"
    Test = "test"
