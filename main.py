from src.todoist_exporter import TodoistToObsidian

# Since until format: 2021-4-29T10:13:00
SINCE = None
UNTIL = None


def main():
    todoist_app = TodoistToObsidian()
    mathing_projects = None
    get_project_id = input("Do you need to search for project id? [y/n] ")
    if get_project_id.lower() == 'y':
        project_name = input("Enter project name: ")
        print("This are the projects ids found matching the name: ")
        mathing_projects = todoist_app.get_project_id(search=project_name)
        print(f"{mathing_projects}")
        print('---')

    project_id = input("Enter project id to export: ")

    # Get project_name
    if mathing_projects:
        project_name = [project for project in mathing_projects if project['id'] == project_id][0]['name']
    else:
        project_name = todoist_app.get_project_name_by_id(search_id=project_id)

    get_completed_tasks = input("Do you want to export completed tasks? [y/n] ")

    sections = todoist_app.get_project_sections(project_id=project_id)
    tasks = todoist_app.get_active_tasks(project_id=project_id, sections_dict=sections)

    if get_completed_tasks == 'y':
        completed_tasks = todoist_app.get_completed_tasks(project_id=project_id,
                                                          sections_dict=sections,
                                                          since=SINCE,
                                                          until=UNTIL
                                                          )

        tasks += completed_tasks

    todoist_app.export_tasks_to_markdown(sections, tasks, project_name=project_name)


if __name__ == '__main__':
    main()
