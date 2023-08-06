from __future__ import annotations
import typing as t

from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator
from sqlalchemy import inspect, select

from .session import sqla_session
from .utils import get_primary_columns


__all__ = (
    'ExistsEntity',
    'UniqueEntity',
)


class ExistsEntity(Validator):
    """The validator checks that an entity exists."""

    default_error_messages = {
        'invalid': 'An instance with %(name)s=%(value)s does not exist.',
        'plural': 'An instance with %(attrs)s attributes does not exist.',
    }

    def __init__(
        self,
        model_class: t.Type[t.Any],
        columns: t.Optional[t.Sequence[str]] = None,
        error: str = '',
    ) -> None:
        """
        Arguments:
            model_class:
                Reference to the model class.
            columns (iterable):
                Model attributes that must be unique.
            error (str):
                Error message.
        """
        if columns is None:
            self.columns = get_primary_columns(model_class)
        else:
            ins = inspect(model_class).columns
            self.columns = tuple(ins[c] for c in columns)

        self.error = error

    def __call__(self, *values: t.Any) -> None:
        if not self._validate(*values):
            if len(values) == 1:
                raise self.make_error(
                    'invalid',
                    name=self.columns[0].name,
                    value=values[0],
                )
            else:
                raise self.make_error(
                    'plural',
                    attrs=', '.join(
                        f'{c.name}={v}' for c, v in zip(self.columns, values)
                    )
                )

    def _validate(self, *values: t.Any) -> bool:
        criteria = tuple(c == v for c, v in zip(self.columns, values))
        return bool(sqla_session.scalar(
            select(1).where(*criteria)
        ))

    def make_error(self, key: str, **kwargs: str) -> ValidationError:
        message = self.error or self.default_error_messages[key]
        return ValidationError(message % kwargs)


class UniqueEntity(ExistsEntity):
    """
    The validator checks the attributes of an entity for uniqueness.
    """

    default_error_messages = {
        'invalid': 'An instance with %(name)s=%(value)s already exists.',
        'plural': 'An instance with unique %(attrs)s attributes already exists.',
    }

    def _validate(self, *values: t.Any) -> bool:
        return not super()._validate(*values)
