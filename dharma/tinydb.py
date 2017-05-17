# -*- coding: utf-8 -*-
from typing import Callable, Generic, Optional, TypeVar

from dharma.compat.db import tinydb
from dharma.exceptions import DharmaConfigError
from dharma.utils.imports import to_dotted_path
from .base import BaseRepository


T = TypeVar('T')


class TinyDbRepository(BaseRepository, Generic[T]):
    _table_name = None
    _table = None

    def __init__(self,
                 engine_config: dict,
                 serializer: Callable[[T], dict],
                 klass: T = None,
                 factory: Callable[[dict], T] = None
                 ) -> None:
        if not tinydb:
            raise DharmaConfigError
        super(TinyDbRepository, self).__init__(klass=klass, factory=factory)
        self._table_name = to_dotted_path(klass)
        self._engine = tinydb.TinyDB(**engine_config)
        self._table = self._engine.table(self._table_name)
        self.serializer = serializer

    def get(self, id: int) -> T:
        data = self._table.get(eid=id)
        if not data:
            raise self.NotFound
        return self.create(**data)

    def get_or_none(self, id: int) -> Optional[T]:
        data = self._table.get(eid=id)
        return self.create(**data) if data is not None else None

    def exists(self, id: int) -> bool:
        return self._table.contains(eid=id)

    def filter(self, predicate: Predicate) -> List[T]:
        # predicates do quack just like `tinydb.query.QueryImpl` objects
        return self._table.search(predicate)

    def count(self, predicate: Predicate = None) -> int:
        if not Predicate:
            return len(self._table.all())
        return self._table.count(predicate)

    def insert(self, obj: T) -> T:
        super(TinyDbRepository, self).insert(obj)
        data = self.serializer(obj)
        id = self._table.insert(data)
        self._set_id(obj, id)
        return obj
        
    def batch_insert(self, objs: Iterable[T]) -> List[T]:
        super(TinyDbRepository, self).insert(objs)
        payload = (self.serializer(obj) for obj in objs)
        ids = self._table.insert_multiple(obj)
        for id, obj in zip(ids, objs):
            self._set_id(obj, id)
        return objs
        
    def update(self, obj: T) -> T:
        super(TinyDbRepository, self).update(obj)
        payload = self.serializer(obj)
        # TODO
        return obj

    def clear(self) -> None:
        self._table.purge()
