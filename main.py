import argparse

from factory.framework_factory import FrameworkFactory


def __main__():
    try:
        parser = argparse.ArgumentParser(description='Create a new project')
        parser.add_argument('framework', help='The desired framework')
        parser.add_argument('project_name', help='The name of the project')
        parser.add_argument('project_path', help='The path to the project')
        args = parser.parse_args()

        factory = FrameworkFactory(args.project_name, args.project_path)
        framework = factory.get_framework(args.framework)
        framework.create_project()
    except Exception as e:
        raise e


if __name__ == '__main__':
    __main__()
