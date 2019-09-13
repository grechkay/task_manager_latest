import argparse
from project_manager import ProjectManager
import os
import pickle as pk
from tools import bcolors, Ignore

def main(trackname):
	# 1. Make sure that this actually exists in my track targets, if not throw an exception
	pm = ProjectManager()
	track_path = pm.personal_dir
	track_targets_path = '{}/track_targets'.format(track_path)
	all_track_targets = sorted(os.listdir(track_targets_path))
	if trackname + '.track' not in all_track_targets:
		raise ValueError("Error, the trackname provided is not a current track target")
	elif trackname in ['weekly_goals', 'monthly_goals', 'quarterly_goals', 'yearly_goals']:
		raise ValueError("Error, cannot ignore {}".format(trackname))
	else:
		ignore = Ignore()
		ignored_tracks = ignore.get_ignored_tracks()
		ignored_tracks.add(trackname)

		# and finally save it
		with open(ignore.ignore_path, 'wb') as f:
			pk.dump(ignored_tracks, f)

		print(bcolors.BOLD + bcolors.OKBLUE + "\n\t" + trackname + " has officially been ignored. \n\tPlease execute unignore_track.py to unignore this track name.\n" + bcolors.ENDC)




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("trackname", help="The name of the track target that you wish to now ignore from all future statistics and showing")
	args = parser.parse_args()
	main(args.trackname)