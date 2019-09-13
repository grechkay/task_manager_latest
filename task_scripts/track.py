import os
import argparse
from tools import get_date_from_string, bcolors, raise_fail_error, get_iso_info, Ignore
from project_manager import ProjectManager
import pandas as pd
from datetime import datetime
import pickle as pk

def show_tracks_for_date(track_date, all_track_targets, track_targets_path, is_all):
    ignore = Ignore()
    ignored_tracks = ignore.get_ignored_tracks()


    for t in all_track_targets:

        trackname = t[: -len('.track')]

        color = ""

        if trackname in ignored_tracks and not is_all:
            # then ignore this one, just continue
            continue

        elif trackname in ignored_tracks and is_all:
            # then show this one, but in red for example
            color = bcolors.FAIL + bcolors.STRIKETHROUGH

        try: # try to read the csv file
            df = pd.read_csv(
                '{}/{}'.format(track_targets_path, t),
                skiprows=1,
                header=None,
                index_col=0
            )
            read_csv = True
        except:
            read_csv = False
            nb_tracked = 0
            print(bcolors.ENDC + bcolors.BOLD, end='')

        if read_csv:
            # count entries for date
            counts = df.groupby(0).aggregate('count')
            try:
                nb_tracked = counts.loc[track_date].values[0]
                print(bcolors.BOLD + bcolors.OKBLUE, end='')
            except KeyError:
                nb_tracked = 0
                print(bcolors.ENDC + bcolors.BOLD, end='')

        # get first line to see the min, max values
        with open('{}/{}'.format(track_targets_path, t)) as f:
            first_line = f.readline()
        low, high, cmap_dir, aggregator, unit = first_line.split(',')
        text = str(nb_tracked) +  " (" + low + "," + high + ")"

        outtext =  '\t' + color + color.join(trackname + ' : \t\t' + text) + color + bcolors.ENDC  # so that the '.track' doesn't appear
        print(outtext)
        # if color:
        #     print('\u0336'.join(text) + '\u0336' + bcolors.ENDC)
        # else:
        #     print(text)

    print()

def main(track_date, track_target, track_value, is_all):
    pm = ProjectManager()
    track_path = pm.personal_dir
    track_targets_path = '{}/track_targets'.format(track_path)
    all_track_targets = sorted([x for x in os.listdir(track_targets_path) if x.endswith('.track')])

    to_show = False

     # today
    if not track_target and not track_date and not track_value: # user just called track.py with no arguments --> show targets for today
        print("\nCurrent track targets for today :")
        track_date, dt = get_date_from_string('t')
        to_show = True

    elif track_date and not track_target and not track_value: # user provided a date but nothing else
        track_date, dt = get_date_from_string(track_date)
        print("\nCurrent track targets for {}".format(track_date))
        to_show = True

    elif not track_target or not track_date or not track_value: # user forgot 1 argument
        raise_fail_error("Error. please execute \n\tpython track.py [YYYY-MM-DD] [target] [value]")

    if not to_show:
        track_date, dt = get_date_from_string(track_date) 

    # adapt all_track_targets for weekly_goals, monthly_goals, quarterly_goals, yearly_goals
    iso_info = get_iso_info(dt)
    for key in ['week', 'month', 'quarter', 'year']:
        key1 = key + 'ly_goals.track'
        key2 = key + '_end'
        # if we are tracking ***ly_goals but we are not on the appropriate day, then just remove it from all_track_targets
        if key1 in all_track_targets and dt != iso_info[key2]:
            all_track_targets.remove(key1) 

    if to_show:
        print('Showing track targets for', track_date)
        show_tracks_for_date(track_date, all_track_targets, track_targets_path, is_all)
        return

    if '{}.track'.format(track_target) not in all_track_targets:
        raise_fail_error("Error. Target is not tracked.")

    ignore = Ignore()
    ignored_tracks = ignore.get_ignored_tracks()
    if track_target in ignored_tracks:
        print(bcolors.FAIL + "\n\tError, this is an ignored track. \n\tPlease unignore it first with unignore_track.py\n" + bcolors.ENDC)
        return

    with open('{}/track_targets/{}.track'.format(track_path, track_target), 'a') as _in:
        _in.write('{ds},{val}\n'.format(ds=track_date, val=track_value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="To view the targets you currently have, call this function without arguments.\n\n")
    parser.add_argument('date', type=str, nargs='?', help='possible values: [t, y, tom, YYYY-MM-DD] (for today, yesterday, tomorrow or a precise date)')
    parser.add_argument('target_name', type=str,  nargs='?', help='name of target to track')
    parser.add_argument('value', type=str, nargs='?', help='value given to the target.')
    parser.add_argument('-a', '--all', action='store_true', dest='ALL')
    args = parser.parse_args()
    main(args.date, args.target_name, args.value, args.ALL)

