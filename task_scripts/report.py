import os
from tools import get_iso_info, get_date_from_string
import argparse
from project_manager import ProjectManager

def main(goal_date):
    pm = ProjectManager()
    personal_dir = pm.personal_dir

    goal_date, dt = get_date_from_string(goal_date)
    iso_info = get_iso_info(dt)
    year = iso_info['year']
    quarter = iso_info['quarter']
    month = iso_info['month']
    week = iso_info['week']

    path_additions = {
        1:str(year),
        2:'q{}'.format(str(quarter)),
        3:'m{}'.format(str(month)),
        4:'w{}'.format(str(week)),
    }

    goal_strings = [
        '',
        'yearly goals from {} to {}\n\n'.format(iso_info['year_start'].date(), iso_info['year_end'].date()),
        'quarterly goals from {} to {}\n\n'.format(iso_info['quarter_start'].date(), iso_info['quarter_end'].date()),
        'monthly goals from {} to {}\n\n'.format(iso_info['month_start'].date(), iso_info['month_end'].date()),
        'weekly goals from {} to {}\n\n'.format(iso_info['week_start'].date(), iso_info['week_end'].date())
    ]

    full_dir_path = '{}/goals'.format(personal_dir)
    report_string = ""
    underscore = '_' * 80 + '\n'

    for i in range(1, 5):
        full_dir_path += '/{}'.format(path_additions[i])
        files = os.listdir(full_dir_path)
        for _file in files:
            if _file.startswith('.'):
                continue
            if 'goal' in _file:
                report_string += goal_strings[i]
                file_path = '{}/{}'.format(full_dir_path, _file)
                with open(file_path, 'r') as _in:
                    for line in _in:
                        report_string += line

                report_string += underscore

    files = os.listdir(full_dir_path)
    files = sorted(files)

    if 'goal' in files[-1]:
        files.pop()

    for _file in files:
        if _file.startswith('.'):
            continue
        report_string += '{}\n\n'.format(_file)
        file_path = '{}/{}'.format(full_dir_path, _file)
        with open(file_path, 'r') as _in:
            for line in _in:
                report_string += line

        report_string += underscore

    with open('{}/goal_report.txt'.format(personal_dir),'w') as _out:
        _out.write(report_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('date', type=str, help='This is date you want the report for. Possible values: [t, y, tom, YYYY-MM-DD] (for today, yesterday, tomorrow or a precise date)')
    args = parser.parse_args()
    main(args.date)