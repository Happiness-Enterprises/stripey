"""Utilities common to Django applications."""
from typing import Any, Callable, List

from happy.utils.exceptions import PermissionCheckError


def check_permission(
    _has_root_: bool,
    _username_: str,
    **success_tests: Callable[[], bool],
) -> None:
    """
    If :param:`has_permission` is True, return immediately. Otherwise, raise an error on the first
    kwarg whose function returns `False`.

    :param _has_root_: Basic permission check for caller; if this is `True`, return immediately.
    :param _username_: The username of the user attempting to perform elevated permission.
    :param success_tests: Field names that have boolean values `True` pass a permissions check.

    Example:
      def authorize(self, username, password):
        check_permission(
            False,
            username,
            username=username_from_database() == username,  # user can only modify their own user
        )
    """
    if _has_root_:
        return

    illegal_fields: List[str] = []
    for field, test in success_tests.items():
        if not test():
            illegal_fields.append(field)

    if illegal_fields:
        raise PermissionCheckError(_username_, illegal_fields)


def default_or_first_not_none(default: Any, *args: Any) -> Any:
    """
    Returns the first item from :param:`args` that is not `None`,
    returning :param:`default` in the case that all of them are `None`.
    """
    return next((item for item in args if item is not None), default)
