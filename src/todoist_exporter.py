import os
import re
from dataclasses import dataclass
from datetime import datetime
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
    created_at: Optional[str] = None  # only in active tasks
    url: Optional[str] = None  # only in active tasks

    sections_dict: Optional[dict[str, str]] = None

    def __post_init__(self):
        if self.section_id:
            self.section_name = self.sections_dict[self.section_id]

    def format_to_md(self):
        if self.due:
            due_txt = f" 📅 {self.due}"
        else:
            due_txt = ""

        if self.created_at:
            created_date = datetime.strptime(self.created_at, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            created_text = f" ➕ {created_date}"
        else:
            created_text = ""

        if self.is_completed:
            return f"- [x] {self.content}{due_txt}{created_text}"
        else:
            return f"- [ ] {self.content}{due_txt}{created_text}"



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
        # Since until format: 2021-4-29T10:13:00
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
                due=item.get("due", {}).get("date", "") if item.get("due") else "",
                completed_at=item.get('completed_at'),
                sections_dict=sections)
            tasks.append(task)
        return tasks

    def get_active_tasks(self, project_id: str, sections_dict: Optional[dict] = None) -> list[Task]:
        sections = sections_dict
        response = requests.get(f"{self.rest_url}/tasks", headers=self.headers, params={"project_id": project_id})
        response.raise_for_status()
        resp = response.json()

        tasks = []
        for item in resp:
            task = Task(
                id=item['id'],
                content=item['content'],
                project_id=item['project_id'],
                section_id=item.get('section_id'),
                parent_id=item.get('parent_id'),
                labels=item.get('labels', []),
                is_completed=item.get('is_completed'),
                due=item.get("due", {}).get("date", "") if item.get("due") else "",
                completed_at=item.get('completed_at'),
                priority=item.get('priority'),
                created_at=item.get('created_at'),
                url=item.get('url'),
                sections_dict=sections)
            tasks.append(task)
        return tasks


    def export_tasks_to_markdown(self, sections, tasks, project_name: Optional[str] = None):
        markdown_content = ""

        if project_name:
            markdown_content += f"# {project_name}\n\n"
        else:
            markdown_content += f"# Project\n\n"
        tasks_without_section = [t for t in tasks if not t.section_id]
        if tasks_without_section:
            for task in tasks_without_section:
                markdown_content += task.format_to_md() + "\n"
        if sections:
            for section_id, section_name in sections.items():
                markdown_content += f"## {section_name}"+ "\n"

                # Filter tasks for this section
                section_tasks = [t for t in tasks if t.section_id == section_id]

                for task in section_tasks:
                    markdown_content += task.format_to_md() + "\n"

                markdown_content += "\n"

        markdown_content += "\n"

        # Write to a Markdown file
        with open("todoist_tasks.md", "w", encoding="utf-8") as file:
            file.write(markdown_content)

        return markdown_content

    def get_project_id(self, search: str):
        matching_projects = []
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        for project in self.projects.values():
            if pattern.search(project.name):
                matching_projects.append({"name": project.name, "id": project.id})
        return matching_projects if matching_projects else None

    def get_project_name_by_id(self, search_id: str) -> Optional[str]:
        for name, project in self.projects.items():
            if project.id == search_id:
                return name
        return None  # Return None if no match is found
