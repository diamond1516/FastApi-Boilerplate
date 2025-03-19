from dataclasses import dataclass
from datetime import timedelta, datetime
from functools import cached_property
from typing import Optional, Any, Union, Literal

import jwt

from config import jwt_settings
from .utility import now


@dataclass(frozen=True, slots=True)
class Payload:
    iat: datetime
    exp: datetime
    sub: str
    id: int


def encode_jwt(
        payload: dict,
        algorithm=jwt_settings.ALGORITHM,
        secret_key: str = jwt_settings.JWT_SECRET_KEY,
        expiration: timedelta = jwt_settings.ACCESS_TOKEN_EXPIRE,
):
    payload.update(
        exp=now() + expiration,
        iat=now(),
    )

    return jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm,
    )


def decode_jwt(
        token: str,
        secret_key: str = jwt_settings.JWT_SECRET_KEY,
        algorithm: str = jwt_settings.ALGORITHM,
):
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )


def get_decoded(
        token: str
) -> Union[dict, None]:
    try:
        return decode_jwt(token)
    except (jwt.InvalidTokenError, jwt.DecodeError, jwt.ExpiredSignatureError):
        return None


class JWT:
    def __init__(
            self,
            obj: Optional[Any] = None,
            payload: Optional[dict] = None,
            sub: Optional[str] = 'id',
            payload_fields: Optional[tuple] = jwt_settings.JWT_PAYLOAD_FIELDS,
    ):
        self.payload = self.set_payload(obj, sub, payload, payload_fields)
        self.secret_key = jwt_settings.JWT_SECRET_KEY
        self.algorithm = jwt_settings.ALGORITHM
        self.access_token_expire = jwt_settings.ACCESS_TOKEN_EXPIRE
        self.refresh_token_expire = jwt_settings.REFRESH_TOKEN_EXPIRE

    @classmethod
    def set_payload(cls, obj, sub, payload, payload_fields):
        if payload and payload.get('sub'):
            return payload
        elif obj and sub and payload_fields:
            payload = {field: getattr(obj, field) for field in payload_fields}
            payload['sub'] = str(getattr(obj, sub))
            return payload
        else:
            raise ValueError('payload must have sub or obj')

    @cached_property
    def access(self) -> str:
        return encode_jwt(
            payload=self.payload,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expiration=self.access_token_expire,
        )

    @cached_property
    def refresh(self) -> str:
        return encode_jwt(
            payload=self.payload,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expiration=self.refresh_token_expire,
        )

    def get_tokens(self, which: Literal['refresh', 'access', 'both'] = 'both') -> dict:

        functions = {
            'refresh': lambda: dict(refresh=self.refresh),
            'access': lambda: dict(access=self.access),
            'both': lambda: dict(access=self.access, refresh=self.refresh),
        }

        return functions[which]()
