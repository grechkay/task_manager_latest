from subprocess import call
from project_manager import ProjectManager
import argparse
from tools import get_date_from_string, get_iso_info, raise_fail_error


def main(goal_date, goal_timeframe):
    pm = ProjectManager()
    personal_dir = pm.personal_dir

    # Everything will be based on the week, so the overlapping
    # days may be put into different quarters/months/years

    goal_date, dt = get_date_from_string(goal_date)
    iso_info = get_iso_info(dt)

    timeframe_dict = {
        'yearly':1,
        'quarterly':2,
        'monthly':3,
        'weekly':4,
        'daily':4,
    }
    if goal_timeframe not in timeframe_dict:
        raise_fail_error("Error. Please use:\n\tpython goals.py [YYYY-MM-DD] [daily,weekly,quarterly,yearly]")
    timeframe_number = timeframe_dict[goal_timeframe]

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
    full_dir_path = '{}/goals'.format(personal_dir)
    for i in range(1,timeframe_number + 1):
        full_dir_path += '/{}'.format(path_additions[i])

    call(['mkdir', '-p', full_dir_path])
    if goal_timeframe == 'daily':
        goal_name = goal_date
    else:
        start_day = iso_info['{}_start'.format(goal_timeframe[:-2])]
        end_day = iso_info['{}_end'.format(goal_timeframe[:-2])]

        goal_name = '{}_goal_{}--{}'.format(goal_timeframe, start_day.date(), end_day.date())

    default_string = \
"""context for the goals:


min_goal:

goal:

stretch_goal:


evaluation of the goals:"""

    pm.modify_file(
        goal_name,
        full_dir_path,
        default_string,
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('date', type=str, help='possible values: [t, y, tom, YYYY-MM-DD] (for today, yesterday, tomorrow or a precise date)')
    parser.add_argument('timeframe', type=str, help='possible values: [daily, weekly, yearly]')
    args = parser.parse_args()
    main(args.date, args.timeframe)
