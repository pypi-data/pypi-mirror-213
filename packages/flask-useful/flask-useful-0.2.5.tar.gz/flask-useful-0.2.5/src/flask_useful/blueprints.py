from __future__ import annotations
import typing as t

from flask import Blueprint as _Blueprint
from flask.views import View
from flask.typing import RouteCallable

from .utils import camel_to_snake


__all__ = ('Blueprint',)


class Blueprint(_Blueprint):
    def add_url_rule(
        self,
        rule: str,
        endpoint: t.Optional[str] = None,
        view_func: t.Optional[RouteCallable] = None,
        provide_automatic_options: t.Optional[bool] = None,
        *,
        view_kwargs: t.Dict[str, t.Any] = None,
        **options: t.Any,
    ) -> None:
        if endpoint is None:
            endpoint = camel_to_snake(view_func.__name__)

        if isinstance(view_func, type):
            if not issubclass(view_func, View):
                raise ValueError('view must be a subclass of `View`.')
            view_kwargs = view_kwargs or {}
            view_func = view_func.as_view(endpoint, **view_kwargs)

        super().add_url_rule(
            rule,
            endpoint,
            view_func,
            provide_automatic_options,
            **options,
        )
