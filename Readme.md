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
  



## Installation
1. Clone the repository:
``` bash
   git clone https://github.com/A-Quaglia/todoist-obsidian-exporter.git
   cd todoist-obsidian-exporter
```
1. Install dependencies:
``` bash
   pip install -r requirements.txt
```
1. Configure your Todoist API token:
    - Create a `.env` file in the project root directory.
    - Add the following line to the `.env` file:
``` 
     TODOIST_TOKEN=your_api_token
```
Replace `your_api_token` with your actual Todoist API token. You can generate your token from [Todoist Settings](https://todoist.com) under the Integrations tab.


## Usage
### Running the Script
1. Run the script:
``` bash
   python main.py
```
1. Follow the prompts to export tasks based on project ID:
    - **Search for Project ID**:
        - If you don't know the project ID, you can search for it by project name.
        - Enter the name of the project, and the script will display matching project IDs.

    - **Export Tasks**:
        - Enter the project ID.
        - Choose whether to export completed tasks or only active tasks.

    - The tasks and sections will be exported to a Markdown (.md) file organized for Obsidian.

## Example Output
An example Markdown export file will look like this:
``` 
# Project: Work

## Section: To Do
- [ ] Task 1 (Priority: 4) @[Section Name]
- [ ] Task 2 (Priority: 2) @[Section Name]

## Section: Completed
- [x] Task 3 - completed on 2023-04-15
```
