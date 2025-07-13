from django.test import TransactionTestCase
from django.db import connection, models
from apps.common.repositories.base import BaseRepository
from conftest import TestModel

class TestBaseRepository(BaseRepository[TestModel]):
    model = TestModel

class TestBaseRepositoryImplementation(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create the table for the test model
        connection.disable_constraint_checking()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestModel)
        connection.enable_constraint_checking()

    @classmethod
    def tearDownClass(cls):
        # Drop the table for the test model
        connection.disable_constraint_checking()
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestModel)
        connection.enable_constraint_checking()
        super().tearDownClass()

    def setUp(self):
        self.repository = TestBaseRepository()
        # Ensure a clean state before each test
        TestModel.objects.all().delete()
        self.test_instance = TestModel.objects.create(
            name="Test Item",
            description="Test Description",
            is_active=True
        )

    def test_get_by_id_existing(self):
        """Test getting an existing item by ID"""
        result = self.repository.get_by_id(self.test_instance.id)
        self.assertEqual(result, self.test_instance)
        self.assertEqual(result.name, "Test Item")
        self.assertEqual(result.description, "Test Description")

    def test_get_by_id_nonexistent(self):
        """Test getting a non-existent item by ID"""
        result = self.repository.get_by_id(999)
        self.assertIsNone(result)

    def test_get_all(self):
        """Test getting all items"""
        # Create additional test items
        TestModel.objects.create(name="Item 2", description="Description 2")
        TestModel.objects.create(name="Item 3", description="Description 3")
        
        results = self.repository.get_all()
        self.assertEqual(len(results), 3)
        self.assertIsInstance(results, list)
        self.assertTrue(all(isinstance(item, TestModel) for item in results))

    def test_create(self):
        """Test creating a new item"""
        data = {
            "name": "New Item",
            "description": "New Description",
            "is_active": False
        }
        result = self.repository.create(**data)
        
        self.assertEqual(result.name, "New Item")
        self.assertEqual(result.description, "New Description")
        self.assertFalse(result.is_active)
        self.assertIsNotNone(result.id)
        self.assertTrue(TestModel.objects.filter(id=result.id).exists())

    def test_update(self):
        """Test updating an existing item"""
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description",
            "is_active": False
        }
        result = self.repository.update(self.test_instance, **update_data)
        
        self.assertEqual(result.name, "Updated Name")
        self.assertEqual(result.description, "Updated Description")
        self.assertFalse(result.is_active)
        self.assertEqual(result.id, self.test_instance.id)

    def test_delete(self):
        """Test deleting an item"""
        item_id = self.test_instance.id
        self.repository.delete(self.test_instance)
        self.assertFalse(TestModel.objects.filter(id=item_id).exists())

    def test_filter(self):
        """Test filtering items"""
        # Create items with different names and states
        TestModel.objects.create(name="Filter Test 1", is_active=True)
        TestModel.objects.create(name="Filter Test 2", is_active=True)
        TestModel.objects.create(name="Other Item", is_active=False)
        
        # Test filtering by name
        results = self.repository.filter(name__startswith="Filter")
        self.assertEqual(len(results), 2)
        
        # Test filtering by is_active
        active_results = self.repository.filter(is_active=True)
        self.assertEqual(len(active_results), 3)  # Including the one from setUp

    def test_exists(self):
        """Test checking if items exist"""
        # Test existing item
        self.assertTrue(self.repository.exists(name="Test Item"))
        
        # Test non-existing item
        self.assertFalse(self.repository.exists(name="Nonexistent Item"))
        
        # Test with multiple conditions
        self.assertTrue(self.repository.exists(name="Test Item", is_active=True))
        self.assertFalse(self.repository.exists(name="Test Item", is_active=False))

    def test_filter_with_ordering(self):
        """Test filtering with ordering"""
        # Create items with different names
        TestModel.objects.create(name="A Item")
        TestModel.objects.create(name="B Item")
        TestModel.objects.create(name="C Item")
        
        # Test ordering by name
        results = self.repository.filter().order_by('name')
        self.assertEqual(results[0].name, "A Item")
        self.assertEqual(results[1].name, "B Item")
        self.assertEqual(results[2].name, "C Item")

    def test_filter_with_select_related(self):
        """Test filtering with select_related"""
        # This test would be more relevant with related models
        results = self.repository.filter(is_active=True)
        self.assertIsInstance(results, models.QuerySet)
        self.assertTrue(all(isinstance(item, TestModel) for item in results))
