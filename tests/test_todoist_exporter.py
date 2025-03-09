import pytest
from unittest.mock import patch
from src.todoist_exporter import TodoistToObsidian, Project


@pytest.fixture
def todoist_app():
    return TodoistToObsidian()


def test_fetch_projects(todoist_app):
    """
    Test fetching projects from Todoist.
    """
    projects = todoist_app.fetch_projects()
    assert isinstance(projects, list)
    if projects:  # If there are projects, check their structure
        assert "id" in projects[0]
        assert "name" in projects[0]
        assert "color" in projects[0]



def test_get_all_projects():
    # Sample mocked API response from /projects endpoint
    mock_projects_response = [
        {
            "id": "123",
            "name": "Work",
            "url": "https://todoist.com/showProject?id=123",
            "description": "Work-related tasks",
            "is_favorite": True,
        },
        {
            "id": "456",
            "name": "Personal",
            "url": "https://todoist.com/showProject?id=456",
            "description": "Personal to-dos",
            "is_favorite": False,
        },
    ]

    # Expected output
    expected_projects = {
        "Work": Project(
            id="123",
            name="Work",
            url="https://todoist.com/showProject?id=123",
            description="Work-related tasks",
            is_favorite=True,
        ),
        "Personal": Project(
            id="456",
            name="Personal",
            url="https://todoist.com/showProject?id=456",
            description="Personal to-dos",
            is_favorite=False,
        ),
    }

    with patch.object(TodoistToObsidian, 'fetch_projects', return_value=mock_projects_response):
        todoist_to_obsidian = TodoistToObsidian(api_token="dummy_api_token")
        actual_projects = todoist_to_obsidian.get_all_projects()

    # Compare the actual output with the expected one
    assert actual_projects == expected_projects