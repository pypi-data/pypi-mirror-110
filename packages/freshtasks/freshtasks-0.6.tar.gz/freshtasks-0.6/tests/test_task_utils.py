
import os
from freshtasks.task_utils import TaskUtils
from freshtasks.api import Api

class TestTaskUtils:

    api_key = os.environ["ENV_FRESH_SERVICE_KEY_API_B64"]
    domain = "checkoutsupport-fs-sandbox.freshservice.com"
    ticket = "#CHN-3"

    def test_get_open_tasks_NormalData(self):
        # Arrange
        expected_size = 3

        # Act
        api = Api(self.api_key, self.domain)
        tasks = api.load_tasks(self.ticket)
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_open()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size
    
    def test_get_open_tasks_EmptyData(self):
        # Arrange
        tasks = []
        expected_size = 0

        # Act
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_open()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size

    def test_get_in_progress_tasks(self):
        # Arrange
        expected_size = 0

        # Act
        api = Api(self.api_key, self.domain)
        tasks = api.load_tasks(self.ticket)
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_in_progress()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size
    
    def test_get_in_progress_EmptyData(self):
        # Arrange
        tasks = []
        expected_size = 0

        # Act
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_in_progress()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size

    def test_get_completed_tasks(self):
        # Arrange
        expected_size = 1

        # Act
        api = Api(self.api_key, self.domain)
        tasks = api.load_tasks(self.ticket)
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_completed()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size

    def test_get_completed_EmptyData(self):
        # Arrange
        tasks = []
        expected_size = 0

        # Act
        task_utils = TaskUtils(tasks)
        open_tasks = task_utils.get_completed()
        result = len(open_tasks)
        
        # Assert
        assert result == expected_size