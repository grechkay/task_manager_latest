import os
from subprocess import call
from project_manager import ProjectManager

pm = ProjectManager()
personal_dir = pm.personal_dir
project_notes_path = '{}/project_notes'.format(personal_dir)
EDITOR = pm.EDITOR

all_note_folders = os.listdir(project_notes_path)

full_note_path = '{}/TEMPTASKDOC'.format(project_notes_path)

if 'TEMPTASKDOC' in os.listdir(project_notes_path):
    with open(full_note_path, 'r') as _in:
        call([EDITOR, _in.name])
else:
    with open(full_note_path, 'w') as _in:
        call([EDITOR, _in.name])

