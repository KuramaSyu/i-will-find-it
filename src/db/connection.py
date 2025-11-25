import functools
from typing import Awaitable, Callable, Coroutine, Optional
import asyncpg
from asyncpg import Pool

from utils.singleton import SingletonMeta

def aquire(coroutine: Callable):
    """
    Wrapper for a coroutine which injects
    an aquired connection as first parameter
    """
    # aquire pool from DatabaseConnection
    pool = DatabaseConnection.get_instance().pool
    
    @functools.wraps(coroutine)
    async def wrapper(*coro_args, **coro_kwargs):
        async with pool.acquire() as connection:
            # aquired connection
            async with connection.transaction():
                # started transaction
                # -> call coroutine inside the transaction
                # and pass the connection as first arg
                return await coroutine(
                    connection, 
                    *coro_args, 
                    **coro_kwargs
                )
    
    return wrapper


class DatabaseConnection(metaclass=SingletonMeta):
    _instance: Optional["DatabaseConnection"] = None
    def __init__(self, dsn: str):
        self._pool: Optional[Pool] = None
        self._dsn: str = dsn
        self._instance = self
    
    async def init_db(self):
        self._pool = await asyncpg.create_pool(dsn=self._dsn)

    @property
    def pool(self) -> asyncpg.Pool:
        """returns the DB connection pool

        Raises
        -------
        AssertionError:
            when the DB was not initialized with init_db()
        """
        assert self._pool
        return self._pool

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        assert cls._instance
        return cls._instance