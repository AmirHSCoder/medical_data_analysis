from typing import List
from .base import BaseRepository
from analysis.models import CrossData, LongData, MergedData, RFResult, YProb


class CrossDataRepository(BaseRepository[CrossData]):
    """Repository for :class:`CrossData` model."""
    model = CrossData

    def get_by_gender(self, gender: str) -> List[CrossData]:
        """Return all records matching the given gender."""
        return list(self.filter(gender=gender))


class LongDataRepository(BaseRepository[LongData]):
    """Repository for :class:`LongData` model."""
    model = LongData

    def get_by_subject(self, subject_id: str) -> List[LongData]:
        """Return all records for a specific subject."""
        return list(self.filter(subject_id=subject_id))


class MergedDataRepository(BaseRepository[MergedData]):
    """Repository for :class:`MergedData` model."""
    model = MergedData


class RFResultRepository(BaseRepository[RFResult]):
    """Repository for :class:`RFResult` model."""
    model = RFResult

    def latest(self) -> RFResult | None:
        return self.model.objects.order_by('-created_at').first()


class YProbRepository(BaseRepository[YProb]):
    """Repository for :class:`YProb` model."""
    model = YProb

    def latest(self) -> YProb | None:
        return self.model.objects.order_by('-created_at').first()
