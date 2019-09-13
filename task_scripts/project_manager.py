from subprocess import call
from taskw import TaskWarrior
from pathlib import Path
from jsonpath import jsonpath
import os

class ProjectManager:
    def __init__(self):
        self.home_dir = str(Path.home())
        self.EDITOR = os.environ.get('EDITOR', 'vim')
        PERSONAL_FOLDER = os.environ.get('PERSONAL_DIRECTORY', 'personal')
        self.w = TaskWarrior()
        self.tasks = self.w.load_tasks()
        self.personal_dir = '{}/core/{}'.format(self.home_dir, PERSONAL_FOLDER)

    def project_min(self):
        filedir = '{}/project_notes'.format(self.personal_dir)
        filename = 'MINIMUM'

        self.modify_file(
            filename,
            filedir,
        )


    def project_note(
        self,
        project,
        description,
    ):
        base_dir = '{personal_dir}/project_notes'.format(
            personal_dir=self.personal_dir
        )

        filedir = self.get_full_dir_path(
            base_dir,
            project
        )
        filename = description
        if not filename:
            files = (_file for _file in os.listdir(filedir) if os.path.isfile(os.path.join(filedir, _file)))
            print("Notes for this project:\n")
            for _file in files:
                print(_file)
        else:
            self.modify_file(
                filename,
                filedir,
                filename,
            )


    def project_dev_setup(
        self,
        project,
    ):
        base_dir = '{personal_dir}/projects'.format(
            personal_dir=self.personal_dir
        )

        filedir = self.get_full_dir_path(
            base_dir,
            project
        )

        readme = '{filedir}/README'.format(
            filedir=filedir
        )
        data = '{filedir}/data'.format(
            filedir=filedir
        )
        data_readme = '{filedir}/data/README'.format(
            filedir=filedir
        )
        poc = '{filedir}/poc'.format(
            filedir=filedir
        )
        prod = '{filedir}/prod'.format(
            filedir=filedir
        )
        utils = '{filedir}/utils'.format(
            filedir=filedir
        )
        utils_readme = '{filedir}/utils/README'.format(
            filedir=filedir
        )

        call(['mkdir', data])
        call(['touch', data_readme])
        call(['mkdir', poc])
        call(['mkdir', prod])
        call(['touch', readme])
        call(['mkdir', utils])
        call(['touch', utils_readme])

    def get_task_id(
        self,
        project,
    ):
        project_id = jsonpath(
            self.tasks, 
            "$..[?(@.description=='{project}')].id".format(
                project=project
            )
        )
        return project_id[0]


    def get_full_dir_path(
        self,
        base_dir,
        project,
        final_dir=None,
    ):
        if final_dir:
            full_dir_path = '{project}/{final_dir}'.format(
                project=project,
                final_dir=final_dir,
            )
        else:
            full_dir_path = project

        project_id = jsonpath(
            self.tasks,
            "$..[?(@.description=='{project}')].uuid".format(
                project=project
            )
        )
        current_id = jsonpath(
            self.tasks, 
            "$..[?('{}' in @.depends)].uuid".format(
                project_id[0]
            )
        )
        while current_id:
            parent_project = jsonpath(
                self.tasks,
                "$..[?(@.uuid=='{}')].description".format(
                    current_id[0]
                )
            )
            full_dir_path = '{project}/{path}'.format(
                project=parent_project[0],path=full_dir_path
            )
            current_id = jsonpath(
                self.tasks, "$..[?('{}' in @.depends)].uuid".format(
                    current_id[0]
                )
            )

        full_dir_path = '{base_dir}/{path}'.format(
            base_dir=base_dir,
            path=full_dir_path
        )
        call(['mkdir', '-p', full_dir_path])
        return full_dir_path

    def create_file(
        self,
        filename,
        filedir,
        defaulttext='',
    ):

        filepath = '{0}/{1}'.format(
            filedir,
            filename,
        )
        with open(filepath, 'w') as _in:
            _in.write(defaulttext)
            _in.flush()
            call([self.EDITOR, _in.name])


    def modify_file(
        self,
        filename,
        filedir,
        defaulttext='',
    ):
        filepath = '{0}/{1}'.format(
            filedir,
            filename,
        )
        if filename in os.listdir(filedir):
            with open(filepath, 'r') as _in:
                call([self.EDITOR, _in.name])
        else:
            self.create_file(
                filename,
                filedir,
                defaulttext,
            )
