import argparse

from create_project import ProjectGenerator


def __main__():
    try:
        parser = argparse.ArgumentParser(description='Create a new project')
        parser.add_argument('project_name', help='The name of the project')
        parser.add_argument('project_path', help='The path to the project')
        args = parser.parse_args()

        ProjectGenerator(args.project_name, f'{args.project_path}')
    except Exception as e:
        raise e


if __name__ == '__main__':
    __main__()
