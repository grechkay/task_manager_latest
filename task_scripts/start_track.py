import os
import argparse
from tools import raise_fail_error
from project_manager import ProjectManager

def main(track_target, min_value, max_value, direction, aggregator, units):
    if direction not in ['up', 'down']:
        raise_fail_error("Error. Direction must be in [up, down]. For more info:\n\tpython start_track.py -h")
    if aggregator not in ['mean', 'sum', 'max', 'min']:
        raise_fail_error("Error. Aggregator must be in [mean, sum, max, min]. For more info:\n\tpython start_track.py -h")
    pm = ProjectManager()
    personal_dir = pm.personal_dir
    track_targets_dir = '{}/track_targets'.format(personal_dir)

    all_track_targets = os.listdir(track_targets_dir)
    if '{}.track'.format(track_target) in all_track_targets:
        raise_fail_error("Error. Tracking already exists")

    with open('{}/{}.track'.format(track_targets_dir, track_target), 'w') as _in:
        _in.write('{min},{max},{dir},{agg},{units}\n'.format(
            min=min_value,
            max=max_value,
            dir=direction,
            agg=aggregator,
            units=units,
        ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('track_target', type=str, help='name of target to add to track')
    parser.add_argument('min_value', type=str, help='the min value user wants to assign to be graphically displayed')
    parser.add_argument('max_value', type=str, help='the max value user wants to assign to be graphically displayed')
    parser.add_argument('direction', type=str, help='values: [up, down]. signifies which direction implies improvement')
    parser.add_argument('aggregator', type=str, help='how the data should be aggregated. values: [mean, sum, max, min]')
    parser.add_argument('units', type=str, help='units data values are tracked in')
    args = parser.parse_args()
    main(args.track_target, args.min_value, args.max_value, args.direction, args.aggregator, args.units)
