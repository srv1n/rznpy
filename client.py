import requests
from typing import List, Dict, Optional
from datetime import datetime
from requests.exceptions import RequestException  # Add this import at the top

class RZNClient:
    def __init__(self, host: str = "localhost", port: int = 9928):
        self.base_url = f"http://{host}:{port}"

    def get_projects(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Dict[str, str]]:
        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit
        
        try:
            response = requests.get(f"{self.base_url}/projects", params=params)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error fetching projects: {e}")
            return []

    def get_added_folders(self) -> List[Dict[str, str]]:
        try:
            response = requests.get(f"{self.base_url}/added_folders")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error fetching added folders: {e}")
            return []

    def get_folder_contents(self, parent_path: str) -> List[Dict[str, str]]:
        if not parent_path:
            print("Error: parent_path cannot be empty.")
            return []

        try:
            response = requests.get(f"{self.base_url}/folder_contents/{parent_path}")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error fetching folder contents for '{parent_path}': {e}")
            return []

    def search(self, query: str, search_type: str = "composite", project_id: Optional[int] = None, 
               files: Optional[List[int]] = None, limit: Optional[int] = None, rerank: Optional[bool] = None) -> List[Dict]:
        
        valid_search_types = ["keyword", "bm25", "semantic", "composite"]
        if search_type not in valid_search_types:
            raise ValueError(f"Invalid search type. Must be one of {valid_search_types}")

        if not query:
            raise ValueError("Query cannot be empty.")

        payload = {
            "query": query
        }
        if project_id is not None:
            payload["project_id"] = project_id
        if files is not None:
            payload["files"] = files
        if limit is not None:
            payload["limit"] = limit
        if rerank is not None:
            payload["rerank"] = rerank

        try:
            response = requests.post(f"{self.base_url}/{search_type}_local_search", json=payload)
            response.raise_for_status()
            return [ContentRow(**item) for item in response.json()]
        except RequestException as e:
            print(f"Error during {search_type} search: {e}")
            return []
        except ValueError as e:
            print(f"Error processing response: {e}")
            return []

class ContentRow:
    def __init__(self, id: int, title: str, header: List[str], text: str, path: str,
                 chunk_number: int, metadata: Dict[str, str], hash: str, source_id: int,
                 source_type: str, created_at: Optional[str], updated_at: Optional[str], score: Optional[float] = None):
        self.id = id
        self.title = title
        self.header = header
        self.text = text
        self.path = path
        self.chunk_number = chunk_number
        self.metadata = metadata
        self.hash = hash
        self.source_id = source_id
        self.source_type = source_type
        self.created_at = datetime.fromisoformat(created_at) if created_at else None
        self.updated_at = datetime.fromisoformat(updated_at) if updated_at else None
        self.score = score

    def __repr__(self):
        return f"<ContentRow id={self.id} title='{self.title}' score={self.score}>"
