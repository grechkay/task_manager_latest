import sys
from project_manager import ProjectManager
import argparse

# First argument is the project
# Second argument is the title/description

def main(project, description):
	pm = ProjectManager()

	pm.project_note(
	    project,
	    description,
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('project', type=str, help='name of project (as is defined in TaskWarrior)')
	parser.add_argument('description', type=str, nargs='?', help='note description (can be anything)')
	args = parser.parse_args()
	main(args.project, args.description)
