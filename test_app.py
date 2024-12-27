import unittest
from app import create_app
from models import db, Task


class TestTaskAPI(unittest.TestCase):
    def setUp(self):
        """Set up a temporary test database and Flask test client."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all() 

    def tearDown(self):
        """Clean up the test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_tasks_empty(self):
        """Test GET /tasks when there are no tasks."""
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  

    def test_add_task(self):
        """Test POST /tasks to add a new task."""
        response = self.client.post('/tasks', json={'title': 'Test Task'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], "Task added successfully!")

   
        response = self.client.get('/tasks')
        tasks = response.json
        self.assertEqual(len(tasks), 1)  
        self.assertEqual(tasks[0]['title'], 'Test Task')  

    def test_update_task(self):
        """Test PUT /tasks/<id> to update a task's status."""

        self.client.post('/tasks', json={'title': 'Test Task'})
        task_id = 1


        response = self.client.put(f'/tasks/{task_id}', json={'status': 'Completed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Task updated successfully!")

 
        response = self.client.get('/tasks')
        tasks = response.json
        self.assertEqual(tasks[0]['status'], 'Completed') 

    def test_delete_task(self):
        """Test DELETE /tasks/<id> to delete a task."""

        self.client.post('/tasks', json={'title': 'Test Task'})
        task_id = 1


        response = self.client.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Task deleted successfully!")

 
        response = self.client.get('/tasks')
        self.assertEqual(response.json, [])  

    def test_get_tasks_with_data(self):
        """Test GET /tasks when tasks exist."""

        self.client.post('/tasks', json={'title': 'Task 1'})
        self.client.post('/tasks', json={'title': 'Task 2'})

 
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        tasks = response.json
        self.assertEqual(len(tasks), 2)  # Ensure two tasks are retrieved
        self.assertEqual(tasks[0]['title'], 'Task 1')
        self.assertEqual(tasks[1]['title'], 'Task 2')


if __name__ == '__main__':
    unittest.main()
