import os
from dataclasses import dataclass
from typing import Optional, Any

import requests
from dotenv import load_dotenv


@dataclass
class Project:
    id: str
    name: str
    url: str
    description: str
    is_favorite: bool


@dataclass
class Task:
    id: str
    content: str
    project_id: str
    section_id: Optional[str]
    parent_id: Optional[str]
    labels: list[str]
    is_completed: bool
    due: Optional[dict[str, str]] = None
    completed_at: Optional[str] = None
    priority: Optional[int] = None  # only in active tasks
    created_at: Optional[str] = None # only in active tasks
    url: Optional[str] = None # only in active tasks

    sections_dict: Optional[dict[str, str]] = None



class TodoistToObsidian:

    def __init__(self, api_token: Optional[str] = None):
        if not api_token:
            load_dotenv()
            api_token = os.getenv("TODOIST_TOKEN")

        self.headers = self._generate_header(api_token)
        self.rest_url = "https://api.todoist.com/rest/v2"
        self.sync_url = "https://api.todoist.com/sync/v9"
        self.projects = self.get_all_projects()

    def _generate_header(self, api_token: str) -> dict[str, str]:

        if not api_token:
            raise ValueError("API token cannot be empty")

        return {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def fetch_projects(self) -> dict[str, dict[str, Any]]:
        response = requests.get(f"{self.rest_url}/projects", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_all_projects(self) -> dict[str, Project]:
        projects = dict()
        projects_response = self.fetch_projects()
        for project in projects_response:
            projects[project['name']] = Project(name=project['name'], id=project['id'], url=project['url'],
                                                description=project['description'], is_favorite=project['is_favorite'])
        return projects

    def get_project_sections(self, project_id: str) -> dict[str, str] | None:
        response = requests.get(f"{self.rest_url}/sections", headers=self.headers, params={"project_id": project_id})
        response.raise_for_status()
        resp = response.json()

        if not resp:
            return None

        sections: dict[str, str] = dict()
        for section in resp:
            sections[section['id']] = section['name']
        return sections

    def get_completed_tasks(self, project_id: str, sections_dict: Optional[dict] = None, since: Optional[str] = None,
                            until: Optional[str] = None) -> list[Task]:
        sections = sections_dict
        params = {}
        if project_id:
            params["project_id"] = project_id
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        response = requests.get(
            f"{self.sync_url}/completed/get_all",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()

        tasks = []
        for item in data.get('items', []):
            task = Task(
                id=item['id'],
                content=item['content'],
                project_id=item['project_id'],
                section_id=item.get('section_id'),
                parent_id=item.get('parent_id'),
                labels=item.get('labels', []),
                is_completed=True,  # Completed tasks are always marked as completed
                due=item.get('due'),
                completed_at=item.get('completed_at'),
                sections_dict=sections)
            tasks.append(task)
        return tasks


