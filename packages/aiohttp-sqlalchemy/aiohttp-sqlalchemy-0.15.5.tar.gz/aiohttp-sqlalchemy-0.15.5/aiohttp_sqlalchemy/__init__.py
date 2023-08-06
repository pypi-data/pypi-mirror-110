from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, \
    create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import cast, TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY, SA_DEFAULT_KEY
from aiohttp_sqlalchemy.decorators import sa_decorator
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError, \
                                          DuplicateRequestKeyError
from aiohttp_sqlalchemy.middlewares import sa_middleware
from aiohttp_sqlalchemy.utils import init_db, sa_init_db, sa_session
from aiohttp_sqlalchemy.views import SAAbstractView, SABaseView, SAView


if TYPE_CHECKING:
    from aiohttp.web import Application
    from aiohttp_sqlalchemy.typedefs import TBinding, TBindings, TBindTo, \
        TSessionFactory


__version__ = '0.15.5'

__all__ = [
    'bind', 'DuplicateAppKeyError', 'DuplicateRequestKeyError', 'init_db',
    'SAAbstractView', 'SABaseView', 'SA_DEFAULT_KEY', 'sa_decorator',
    'sa_middleware', 'sa_session', 'SAView', 'setup',
    # synonyms
    'DEFAULT_KEY', 'sa_bind', 'sa_init_db',
]


def bind(bind_to: 'TBindTo', key: str = SA_DEFAULT_KEY, *,
         middleware: bool = True) -> 'TBinding':
    """ Session factory wrapper for binding in setup function. """

    if isinstance(bind_to, str):
        bind_to = cast(AsyncEngine, create_async_engine(bind_to))

    if isinstance(bind_to, AsyncEngine):
        bind_to = cast('TSessionFactory', sessionmaker(
            bind=bind_to,
            class_=AsyncSession,
            expire_on_commit=False,
        ))

    if isinstance(bind_to, Engine):
        msg = 'Synchronous  engine is unsupported argument for `sa_bind()`.'
        raise ValueError(msg)

    if not callable(bind_to):
        msg = 'Session factory must be callable.'
        raise ValueError(msg)

    if not isinstance(bind_to(), AsyncSession):
        msg = 'Session factory must returning `AsyncSession` instance.'
        raise ValueError(msg)

    return bind_to, key, middleware


sa_bind = bind  # sa_bind is synonym for bind


def setup(app: 'Application', bindings: 'TBindings') -> None:
    """ Setup function for binding SQLAlchemy engines. """
    for factory, key, middleware in bindings:
        if key in app:
            raise DuplicateAppKeyError(key)

        app[key] = factory

        if middleware:
            app.middlewares.append(sa_middleware(key))
