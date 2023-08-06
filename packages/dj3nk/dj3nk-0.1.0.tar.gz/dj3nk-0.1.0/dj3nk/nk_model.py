# -*- coding: utf-8 -*-
from django.db import models
from .natural_key_generator import NaturalKeyGenerator

from dj3base.type_hints import DjangoModel


nkg = NaturalKeyGenerator()


def gnk() -> int:
    return nkg.generate_nk()


class NKModel(DjangoModel):
    id = models.BigIntegerField('id', primary_key=True, default=gnk)

    class Meta:
        abstract = True
