# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import collections
import contextlib
import typing as tp

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from ._00_extra_level import ExtraLevel
from ._02_base import BaseComponent


class SentinelMixin(BaseComponent):
    def __init__(self, *args: tp.Any, **kwgs: tp.Any) -> None:
        super().__init__(*args, **kwgs)
        self._auxcon_entered = False
        self._extra_counter: tp.DefaultDict[ExtraLevel, int] = collections.defaultdict(
            int
        )

    def bake(self) -> None:
        with self.extra():
            super().bake()
            self.writeout()

    @contextlib.contextmanager
    def with_formatted(self) -> tp.Iterator[_ProtoNamespace]:
        level = ExtraLevel.FORMATTED
        if self._extra_counter[level] == 0:
            super().formatted()
        self._extra_counter[level] += 1
        yield self.auxf
        self._extra_counter[level] -= 1
        if self._extra_counter[level] == 0:
            del self.auxf

    @contextlib.contextmanager
    def with_defaulted(self) -> tp.Iterator[_ProtoNamespace]:
        level = ExtraLevel.DEFAULTED
        if self._extra_counter[level] == 0:
            super().defaulted()
        self._extra_counter[level] += 1
        yield self.auxd
        self._extra_counter[level] -= 1
        if self._extra_counter[level] == 0:
            del self.auxd

    @contextlib.contextmanager
    def with_enriched(self) -> tp.Iterator[_ProtoNamespace]:
        level = ExtraLevel.ENRICHED
        if self._extra_counter[level] == 0:
            super().enriched()
        self._extra_counter[level] += 1
        yield self.auxe
        self._extra_counter[level] -= 1
        if self._extra_counter[level] == 0:
            del self.auxe

    @contextlib.contextmanager
    def with_hydrated(self) -> tp.Iterator[_ProtoNamespace]:
        level = ExtraLevel.HYDRATED
        if self._extra_counter[level] == 0:
            super().hydrated()
        self._extra_counter[level] += 1
        yield self.auxh
        self._extra_counter[level] -= 1
        if self._extra_counter[level] == 0:
            del self.auxh

    @contextlib.contextmanager
    def extra(
        self, level: ExtraLevel = ExtraLevel.ENRICHED
    ) -> tp.Iterator[_ProtoNamespace]:
        if self._extra_counter[level] == 0:
            logger.info("enabled %s", level)
        if level == ExtraLevel.TEMPLATED:
            self.templated()
            with self.with_formatted() as aux:
                yield aux
        elif level == ExtraLevel.TEMPLATED_WITH_NEGATIVE:
            self.templated(negative_default=True)
            with self.with_formatted() as aux:
                yield aux
        elif level == ExtraLevel.DEMODATA:
            self.templated()
            self.demodata()
            with self.with_formatted() as aux:
                yield aux
        if level == ExtraLevel.FORMATTED:
            with self.with_formatted() as aux:
                yield aux
        elif level == ExtraLevel.DEFAULTED:
            with self.with_formatted(), self.with_defaulted() as aux:
                yield aux
        elif level == ExtraLevel.ENRICHED:
            with self.with_formatted(), self.with_defaulted(), self.with_enriched() as aux:
                yield aux
        elif level == ExtraLevel.HYDRATED:
            with self.with_formatted(), self.with_defaulted(), self.with_enriched(), self.with_hydrated() as aux:
                yield aux

        if self._extra_counter[level] == 0:
            logger.info("disabled %s", level)
