from __future__ import annotations
import typing as t


__all__ = ('trim',)


def trim(
    s: t.Optional[str],
    chars: t.Optional[str] = None,
) -> t.Optional[str]:
    """
    To remove other characters when used as a filter for form fields, you can use `functools.partial`.

    Example:
        from functools import partial

        StringField(filters=[partial(trim, chars='/')])
        StringField(filters=[lambda s: trim(s, chars='/')])
    """
    return s.strip(chars) if isinstance(s, str) else None
