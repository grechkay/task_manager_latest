import sys
from project_manager import ProjectManager
import argparse

# First argument is the project

def main(project):
	pm = ProjectManager()

	pm.project_dev_setup(
	    project,
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('project', type=str, help='name of project (as is defined in TaskWarrior)')
	args = parser.parse_args()
	main(args.project)
