# -*- coding: utf-8 -*-
"""题库上下文：在自建题库与 CloudCertPrep 板块间切换。"""

from __future__ import annotations

from data.banks import (
    BANK_CLOUDCERTPREP,
    BANK_CONCEPT_DRILL,
    BANK_KEYWORD_DRILL,
    BANK_NATIVE,
    BANK_WEAK_POINT_DRILL,
    get_bank,
    get_bank_label,
)


class BankContextMixin:
    """为 GUI Mixin 提供当前题库上下文。"""

    def _init_bank_context(self) -> None:
        self.current_bank_id: str = BANK_NATIVE

    def _get_bank(self):
        return get_bank(self.current_bank_id)

    def _bank_label(self) -> str:
        return get_bank_label(self.current_bank_id)

    def _is_cloudcertprep(self) -> bool:
        return self.current_bank_id == BANK_CLOUDCERTPREP

    def _is_keyword_drill(self) -> bool:
        return self.current_bank_id == BANK_KEYWORD_DRILL

    def _is_concept_drill(self) -> bool:
        return self.current_bank_id == BANK_CONCEPT_DRILL

    def _is_weak_point_drill(self) -> bool:
        return self.current_bank_id == BANK_WEAK_POINT_DRILL
