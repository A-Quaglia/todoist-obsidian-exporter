# Todoist to Obsidian Exporter
This is a Python utility for exporting tasks and projects from Todoist to Obsidian-friendly Markdown files. 

## Features
- Fetch all **projects** from your Todoist account.
- Retrieve tasks associated with a selected project.
    - **Active tasks**: Tasks that are still incomplete.
    - **Completed tasks**: Tasks marked as done.

- Export tasks with rich metadata (sections, labels, priorities, etc.) to markdown files.
- Retrieve specific **project IDs** by project name (for streamlined workflow).
- Organize tasks by sections in Markdown format for better readability in Obsidian.

## Requirements
- **Python** 3.6+
- Todoist API token
- Libraries:
    - [requests](https://pypi.org/project/requests/)
    - [python-dotenv](https://pypi.org/project/python-dotenv/)
  