from typing import List

from apps.analysis.models import CrossData, LongData, MergedData, RFResult, YProb
from apps.analysis.utils import get_collection
from apps.analysis.utils import CROSS_DATA_COLLECTION, LONG_DATA_COLLECTION, MERGED_DATA, RF_RESULT, Y_RESULT

from .base import BaseRepository



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
    collection = MERGED_DATA

    def __init__(self):
        self.connection = get_collection(self.collection)

    async def all(self) -> RFResult | None:
        data = await self.connection.find({}, {'_id': 0}).to_list()
        return data


class RFResultRepository(BaseRepository[RFResult]):
    """Repository for :class:`RFResult` model."""

    model = RFResult
    collection = RF_RESULT

    def __init__(self):
        self.connection = get_collection(self.collection)

    async def latest(self) -> RFResult | None:
        latest = await self.connection.find_one({'_id':'latest'})
        return latest['report']


class YProbRepository(BaseRepository[YProb]):
    """Repository for :class:`YProb` model."""

    model = YProb
    collection = Y_RESULT

    def __init__(self):
        self.connection = get_collection(self.collection)

    async def latest(self) -> RFResult | None:
        latest = await self.connection.find_one({'_id':'latest'})
        return latest['y_prob']
