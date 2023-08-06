import re
from drb.core.predicate import Predicate


class RegexNamePredicate(Predicate):
    def __init__(self, regex: str):
        self._regex = re.compile(regex)

    def matches(self, node):
        return self._regex.match(node.name) is not None
