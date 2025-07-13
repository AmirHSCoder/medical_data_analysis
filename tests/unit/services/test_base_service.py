from django.test import TransactionTestCase
from django.db import connection
from apps.common.repositories.base import BaseRepository
from apps.common.services.base import BaseService
from conftest import TestModel


class TestBaseRepository(BaseRepository[TestModel]):
    model = TestModel


class TestBaseService(BaseService[TestModel]):
    repository_class = TestBaseRepository
    __test__ = False


class TestBaseServiceImplementation(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        connection.disable_constraint_checking()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestModel)
        connection.enable_constraint_checking()

    @classmethod
    def tearDownClass(cls):
        connection.disable_constraint_checking()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestModel)
        connection.enable_constraint_checking()
        super().tearDownClass()

    def setUp(self):
        self.service = TestBaseService()
        TestModel.objects.all().delete()
        self.instance = TestModel.objects.create(name="Test", description="Desc", is_active=True)

    def test_get_by_id(self):
        obj = self.service.get_by_id(self.instance.id)
        self.assertEqual(obj, self.instance)

    def test_create_and_delete(self):
        obj = self.service.create(name="New", description="New", is_active=False)
        self.assertIsNotNone(obj.id)
        self.service.delete(obj)
        self.assertFalse(TestModel.objects.filter(id=obj.id).exists())
