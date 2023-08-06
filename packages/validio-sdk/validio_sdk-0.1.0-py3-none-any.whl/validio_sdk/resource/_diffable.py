from abc import abstractmethod
from typing import Optional


class Diffable:
    """
    An abstract class to be implemented by objects that can be diff-ed against the
    server version. All Resource instances implement this by default. And in some
    cases (like filters, thresholds etc.), nested objects of a resource need to be
    diff-ed and require such objects require an implementation of this base.

    NOTE: When adding/removing fields to any resource or object contained
    within a resource be sure to account for how that field should be diffed.
    Every field reachable from a resource, should be returned by exactly one
    of the listed APIs here.
    """

    @abstractmethod
    def _immutable_fields(self) -> set[str]:
        """Returns the fields on the object that do not allow updates."""

    @abstractmethod
    def _mutable_fields(self) -> set[str]:
        """Returns the fields on the object that can be updated."""

    @abstractmethod
    def _nested_objects(self) -> dict[str, Optional["Diffable"]]:
        """Returns any nested objects contained within this object.

        Nested objects will be diff-ed recursively.
        ...
        :returns dict[field, Optional[object]].
        """
