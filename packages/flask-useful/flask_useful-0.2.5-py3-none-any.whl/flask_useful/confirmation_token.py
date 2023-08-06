from __future__ import annotations
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
import hashlib
import secrets
import time
import typing as t

from flask import current_app
from itsdangerous import (
    BadData,
    SignatureExpired,
    URLSafeTimedSerializer,
)


__all__ = (
    'BadToken',
    'ConfirmationToken',
    'ConfirmationTokenSerializer',
    'TokenExpired',
)


class TokenProtocol(t.Protocol):
    @property
    def issued(self) -> int: ...

    @property
    def max_age(self) -> int: ...

    @property
    def value(self) -> str: ...


class TokenError(Exception):
    pass


class BadToken(TokenError):
    """Any error during token validation."""


class TokenExpired(TokenError):
    """Error if the token has expired."""


class ConfirmationToken(metaclass=ABCMeta):
    __slots__ = ('length', 'salt')

    def __init__(
        self,
        *,
        salt: str = '',
        length: int = 0,
    ) -> None:
        """
        Arguments
            salt (str): string for salting the token.
            length (int): the length of the generated token.
        """
        self.salt = salt
        self.length = length

    @abstractmethod
    def authenticate_user(self, token: TokenProtocol) -> t.Any:
        """Returns the authenticated owner of the token."""
        raise NotImplementedError

    @abstractmethod
    def delete_user_tokens(self, user: t.Any) -> None:
        """Removes all tokens owned by the given user."""
        raise NotImplementedError

    @abstractmethod
    def find_token(self, value: str) -> t.Optional[TokenProtocol]:
        """Returns the token found by the hashed value, otherwise None."""
        raise NotImplementedError

    @abstractmethod
    def find_user_tokens(self, user: t.Any) -> t.Sequence[TokenProtocol]:
        """Returns all tokens owned by the given user."""
        raise NotImplementedError

    def generate_token(
        self,
        user: t.Any,
        *,
        max_age: int = 0,
        **generator_kwargs: t.Dict[str, t.Any],
    ) -> str:
        """Returns the generated token string."""
        token_string = ''
        hashed_token = ''
        found = True

        while found:
            token_string = self.generate_token_string(**generator_kwargs)
            hashed_token = self.hash_token(token_string)
            if self.find_token(hashed_token) is None:
                found = False

        self.save_token({
            'user': user,
            'value': hashed_token,
            'issued': int(time.time()),
            'max_age': max_age,
        })

        return token_string

    def generate_token_string(
        self,
        **kwargs: t.Dict[str, t.Any],
    ) -> str:
        """Returns a unique token string."""
        return secrets.token_urlsafe(self.length or None)

    def hash_token(self, token_string: str) -> str:
        """Returns the hashed token string."""
        s = token_string + self.salt
        return hashlib.sha256(s.encode()).hexdigest()

    @abstractmethod
    def save_token(self, token_dict: t.Dict[str, t.Any]) -> None:
        """Saves the token in persistent storage."""
        raise NotImplementedError

    @contextmanager
    def validate_token(self, token_string: str) -> t.Iterator[TokenProtocol]:
        """
        Validates the given token string
        and returns the found token as the value of the context manager.
        """
        hashed_token = self.hash_token(token_string)
        token = self.find_token(hashed_token)
        if token is None:
            raise BadToken

        user = self.authenticate_user(token)
        if user is None:
            raise BadToken

        # Возвращаем и блокируем все токены выданные пользователю.
        tokens = self.find_user_tokens(user)
        if not any(i.value == token.value for i in tokens):
            raise BadToken

        if token.max_age > 0:
            expired_in = token.issued + token.max_age

            if time.time() > expired_in:
                raise TokenExpired

        try:
            # Выполняем действие для найденного пользователя.
            yield token
        except Exception:
            raise
        else:
            # Удаляем все токены выданные пользователю.
            self.delete_user_tokens(user)


class ConfirmationTokenSerializer(ConfirmationToken):
    __slots__ = ('ts',)

    def __init__(
        self,
        *,
        salt: str = '',
    ) -> None:
        super().__init__(salt=salt)
        self.ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    def generate_token_string(self, **kwargs: t.Dict[str, t.Any]) -> str:
        payload = kwargs.get('payload')
        token_string = self.ts.dumps(payload, salt=self.salt or None)
        if isinstance(token_string, bytes):
            token_string = token_string.decode()
        return token_string

    @contextmanager
    def parse_token(self, token_string: str) -> t.Iterator[t.Any]:
        """
        Validates the given token string
        and returns the stored data as the value of the context manager.
        """
        with self.validate_token(token_string) as token:
            try:
                yield self.ts.loads(
                    s=token_string,
                    max_age=token.max_age or None,
                    salt=self.salt or None,
                )
            except SignatureExpired as err:
                raise TokenExpired(str(err)) from err
            except BadData as err:
                raise BadToken(str(err)) from err
