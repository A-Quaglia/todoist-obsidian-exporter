from src.todoist_exporter import TodoistToObsidian

# Since until format: 2021-4-29T10:13:00
SINCE = None
UNTIL = None


def main():
    todoist_app = None
    get_project_id = input("Do you need to search for project id? [y/n] ")
    if get_project_id.lower() == 'y':
        project_name = input("Enter project name: ")
        print("This are the projects ids found matching the name: ")
        todoist_app = TodoistToObsidian()
        print(f"{todoist_app.get_project_id(search=project_name)}")
        print('---')

    project_id = input("Enter project id to export: ")
    get_completed_tasks = input("Do you want to export completed tasks? [y/n] ")

    if not todoist_app:
        todoist_app = TodoistToObsidian()

    sections = todoist_app.get_project_sections(project_id=project_id)
    tasks = todoist_app.get_active_tasks(project_id=project_id, sections_dict=sections)

    if  get_completed_tasks == 'y':
        completed_tasks = todoist_app.get_completed_tasks(project_id=project_id,
                                                          sections_dict=sections,
                                                          since=SINCE,
                                                          until=UNTIL
                                                          )

        tasks += completed_tasks

    todoist_app.export_tasks_to_markdown(sections, tasks)


if __name__ == '__main__':
    main()

