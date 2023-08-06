from __future__ import annotations
import typing as t
import re

import sqlalchemy as sa

from .session import sqla_session

if t.TYPE_CHECKING:
    from sqlalchemy import Column
    from sqlalchemy.orm import Session


IdentityArgument = t.Union[t.Any, t.Tuple[t.Any, ...], t.Dict[str, t.Any]]


__all__ = (
    'generate_slug',
    'get_primary_columns',
    'normalize_pk',
)


def generate_slug(
    slug_field: t.Any,
    slug: str,
    session: t.Optional[Session] = None,
) -> str:
    """
    Generates a unique slug based on the passed value.

    Arguments:
        slug_field: Model attribute containing slug.
        slug (str): The desired slug value.
        session (Session): SQLAlchemy session.
    """
    if session is None:
        session = sqla_session

    pattern = r'^%s(?:-([0-9]+))?$' % slug

    stmt = (
        sa.select(slug_field)
          .where(slug_field.regexp_match(pattern))
          .order_by(slug_field.desc())
          .limit(1)
    )
    found = session.scalar(stmt)

    if not found:
        return slug

    match = re.match(pattern, found)

    if match is None:
        raise AssertionError('The query found one result for the regular expression.')

    return '{}-{}'.format(slug, int(match.group(1)) + 1)


def get_primary_columns(
    model_class: t.Type[t.Any],
) -> t.Tuple[Column[t.Any], ...]:
    """Returns the primary key columns."""
    return tuple(
        c for c in sa.inspect(model_class).columns if c.primary_key
    )


def normalize_pk(
    value: IdentityArgument,
    model_class: t.Type[t.Any],
) -> t.Dict[str, t.Any]:
    """Returns the primary key with a cast as a dictionary."""
    columns = get_primary_columns(model_class)

    if not isinstance(value, tuple):
        if isinstance(value, dict):
            value = tuple(value[c.name] for c in columns)
        else:
            value = (value,)

    return {
        c.name: c.type.python_type(v) for c, v in zip(columns, value)
    }
