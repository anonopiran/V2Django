from __future__ import annotations
from uuid import UUID

from django.db import models
from Upstream import tasks


class Server(models.Model):
    url = models.URLField()

    def user__add(self, uuid: UUID, email, async_=True):
        _kwargs = dict(endpoint=self.url, uuid=uuid, email=email)
        if async_:
            tasks.add_user.delay(**_kwargs)
        else:
            tasks.add_user(**_kwargs)

    def user__rm(self, email, async_=True):
        _kwargs = dict(endpoint=self.url, email=email)
        if async_:
            tasks.rm_user.delay(**_kwargs)
        else:
            tasks.rm_user(**_kwargs)

    @classmethod
    def user__add__many(
        cls,
        uuid: UUID,
        email,
        async_=True,
        queryset: models.QuerySet[Server] = None,
    ):
        queryset = queryset or cls.objects.all()
        for q_ in queryset:
            q_.user__add(uuid=uuid, email=email, async_=async_)

    @classmethod
    def user__rm__many(
        cls, email, async_=True, queryset: models.QuerySet[Server] = None
    ):
        queryset = queryset or cls.objects.all()
        for q_ in queryset:
            q_.user__rm(email=email, async_=async_)

    def __str__(self):
        return self.url
