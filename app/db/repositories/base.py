import typing

from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.ext.sqlalchemy_future import paginate as test_paginate
from sqlalchemy import desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.session import Session

from app.db import get_session

T = typing.TypeVar("T")  # noqa: WPS111


class BaseRepository(typing.Generic[T]):  # noqa: WPS214
    """Base repository."""

    model_class = None

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    async def list(
        self,
        filters: dict = {},  # noqa: B006
        search_fields: list = [],  # noqa: B006
    ):
        stmt = await self._get_list_query(filters, search_fields)
        query_result = await self._session.execute(stmt)

        return query_result.scalars().all()

    async def paginate(
        self,
        page_params: Params,
        filters: dict = {},  # noqa: B006
        search_fields: list = [],  # noqa: B006
    ) -> Page[T]:
        stmt = await self._get_list_query(filters, search_fields)

        if isinstance(self._session, Session):
            return test_paginate(self._session, stmt, params=page_params)
        return await paginate(self._session, stmt, params=page_params)

    async def first(self, filters: dict) -> T | None:
        stmt = select(self.model_class).filter_by(**filters)
        query_result = await self._session.execute(stmt)
        return query_result.scalars().first()

    async def create(self, attributes: dict) -> T:
        attributes = await self._before_create(attributes)

        model = self.model_class(**attributes)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

        return model

    async def update(self, model: T, attributes: dict) -> T:
        attributes = await self._before_update(model, attributes)

        stmt = update(self.model_class).values(attributes).filter_by(id=model.id)
        await self._session.execute(stmt)
        await self._session.commit()
        return model

    async def _before_create(self, attributes: dict) -> dict:
        return attributes

    async def _before_update(self, model: T, attributes: dict) -> dict:
        return attributes

    async def _get_list_query(
        self,
        filters: dict = {},  # noqa: B006
        fields: list = [],  # noqa: B006
    ):
        query = select(self.model_class)
        if filters and fields:
            query = await self._search_filters_inject(query, filters, fields)

        return query.filter_by(
            **filters,
        ).order_by(
            desc(self.model_class.id),
        )

    async def _search_filters_inject(self, query, filters, fields):
        for field in fields:
            if field in filters:
                search_value = filters.pop(field)
                query = query.filter(
                    self.model_class.name.ilike("%{0}%".format(search_value)),
                )

        return query
