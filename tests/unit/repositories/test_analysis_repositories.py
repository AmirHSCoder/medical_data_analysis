from django.test import TestCase

from apps.analysis.models import CrossData, LongData, MergedData, RFResult, YProb
from apps.common.repositories.analysis_repository import (
    CrossDataRepository,
    LongDataRepository,
    MergedDataRepository,
    RFResultRepository,
    YProbRepository,
)


class TestCrossDataRepository(TestCase):

    def setUp(self):
        self.repo = CrossDataRepository()
        CrossData.objects.all().delete()
        self.instance = CrossData.objects.create(
            id="c1",
            gender="M",
            handedness="R",
            age=30,
            delay=0,
        )

    def test_get_by_id(self):
        obj = self.repo.get_by_id("c1")
        self.assertEqual(obj, self.instance)

    def test_get_by_gender(self):
        CrossData.objects.create(id="c2", gender="F", handedness="L", age=25, delay=1)
        males = self.repo.get_by_gender("M")
        self.assertEqual(males, [self.instance])


class TestLongDataRepository(TestCase):

    def setUp(self):
        self.repo = LongDataRepository()
        LongData.objects.all().delete()
        self.instance = LongData.objects.create(
            subject_id="s1",
            mri_id="m1",
            visit=1,
            delay=0,
            gender="M",
            handedness="R",
            age=30,
        )

    def test_get_by_id(self):
        obj = self.repo.get_by_id("m1")
        self.assertEqual(obj, self.instance)

    def test_get_by_subject(self):
        LongData.objects.create(
            subject_id="s1",
            mri_id="m2",
            visit=1,
            delay=5,
            gender="M",
            handedness="R",
            age=31,
        )
        results = self.repo.get_by_subject("s1")
        self.assertEqual(len(results), 2)


class TestMergedDataRepository(TestCase):

    def setUp(self):
        self.repo = MergedDataRepository()
        MergedData.objects.all().delete()
        self.instance = MergedData.objects.create(
            source_id="m1",
            subject_id="s1",
            group="A",
            visit=1,
            delay=0,
            gender="M",
            handedness="R",
            age=30,
        )

    def test_get_by_id(self):
        obj = self.repo.get_by_id(self.instance.id)
        self.assertEqual(obj, self.instance)


class TestRFResultRepository(TestCase):

    def setUp(self):
        self.repo = RFResultRepository()
        RFResult.objects.all().delete()
        self.instance = RFResult.objects.create(report="{}")

    def test_latest(self):
        latest = self.repo.latest()
        self.assertEqual(latest, self.instance)


class TestYProbRepository(TestCase):

    def setUp(self):
        self.repo = YProbRepository()
        YProb.objects.all().delete()
        self.instance = YProb.objects.create(y_prob={"a": 1})

    def test_latest(self):
        latest = self.repo.latest()
        self.assertEqual(latest, self.instance)
