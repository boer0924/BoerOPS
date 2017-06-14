#!/usr/local/env python
# -*- coding: utf-8 -*-

from app import db


class Base(object):
    __model__ = None

    def __init__(self):
        self.session = db.session

    def save(self, record):
        self.session.add(record)
        self.session.commit()
        return record

    def find(self, **kwargs):
        query = self.session.query(self.__model__).filter_by(**kwargs)
        return query

    def first(self, **kwargs):
        return self.session.query(self.__model__).filter_by(**kwargs).first()

    def get(self, id):
        self.session.expire_all()
        return self.session.query(self.__model__).get(id)

    def get_or_404(self, id):
        self.session.query(self.__model__).get_or_404(id)

    def count(self, **kwargs):
        return self.session.query(self.__model__).filter_by(**kwargs).count()

    def all(self, offset=None, limit=None, order_by=None, desc=False):
        query = self.session.query(self.__model__)
        if order_by is not None:
            if desc:
                query = query.order_by(db.desc(order_by))
            else:
                query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def create(self, **kwargs):
        return self.save(self.__model__(**kwargs))

    def update(self, record, **kwargs):
        for k, v in kwargs.items():
            setattr(record, k, v)
        self.save(record)
        return record

    def session_commit(self):
        self.session.commit()

    def __del__(self):
        self.session.close()
