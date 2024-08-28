import unittest
from unittest.mock import patch, Mock
from client import RZNClient, ContentRow

class TestRZNClient(unittest.TestCase):
    def setUp(self):
        self.client = RZNClient(host="localhost", port=9928)

    @patch('client.requests.get')
    def test_get_projects_success(self, mock_get):
        # Mock the response for a successful API call
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 1, "name": "Project A"}]

        projects = self.client.get_projects(offset=0, limit=10)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['name'], "Project A")

    @patch('client.requests.get')
    def test_get_projects_failure(self, mock_get):
        # Mock the response for a failed API call
        mock_get.side_effect = Exception("Network error")

        projects = self.client.get_projects(offset=0, limit=10)
        self.assertEqual(projects, [])

    @patch('client.requests.get')
    def test_get_added_folders_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 1, "path": "Folder A"}]

        folders = self.client.get_added_folders()
        self.assertEqual(len(folders), 1)
        self.assertEqual(folders[0]['path'], "Folder A")

    @patch('client.requests.get')
    def test_get_folder_contents_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 1, "name": "File A"}]

        contents = self.client.get_folder_contents("path/to/folder")
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0]['name'], "File A")

    @patch('client.requests.get')
    def test_get_folder_contents_empty_path(self, mock_get):
        contents = self.client.get_folder_contents("")
        self.assertEqual(contents, [])

    @patch('client.requests.post')
    def test_search_success(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = [{"id": 1, "title": "Result A"}]

        results = self.client.search("query", search_type="composite")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Result A")

    @patch('client.requests.post')
    def test_search_invalid_type(self, mock_post):
        with self.assertRaises(ValueError):
            self.client.search("query", search_type="invalid_type")

    @patch('client.requests.post')
    def test_search_empty_query(self, mock_post):
        with self.assertRaises(ValueError):
            self.client.search("", search_type="composite")

    @patch('client.requests.post')
    def test_search_failure(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        results = self.client.search("query", search_type="composite")
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()