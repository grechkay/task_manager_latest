import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import numpy as np
from collections import OrderedDict
from tools import get_iso_info, Ignore
import math
import argparse
from project_manager import ProjectManager

fontsize = float(os.environ.get('fontsize', '20'))
SIZE_TITLE = 1.0 * fontsize
SIZE_LABEL = 0.75 * fontsize
SIZE_UNITS = 0.5 * fontsize
SIZE_DAYS_OF_WEEK = 0.5 * fontsize

def main(num_weeks, to_show):
    global SIZE_TITLE, SIZE_LABEL, SIZE_UNITS, SIZE_DAYS_OF_WEEK
    pm = ProjectManager()
    personal_dir = pm.personal_dir
    track_targets_path = '{}/track_targets'.format(personal_dir)

    ignore = Ignore()
    ignored_tracks = ignore.get_ignored_tracks()
    all_track_targets = sorted([x for x in os.listdir(track_targets_path) if x.endswith('.track') and x[:-len(".track")] not in ignored_tracks])

    plot_width = 6
    cmap_dict = {
        'up': 'RdYlGn',
        'down': 'RdYlGn_r'
    }

    titles = []
    dfs = []
    _range = []
    cmaps = []
    aggregators = []
    units = []


    now = datetime.now()
    today = now.date()
    iso_info = get_iso_info(now)
    year = iso_info['year']
    last_year_last_date = get_iso_info(datetime(year-1,6,1))['year_end']
    week_multiplier = get_iso_info(last_year_last_date)['week']

    day_delta = timedelta(days=1)
    days_offset = 0
    temp_day = today - day_delta * days_offset

    special_track_targets = OrderedDict({
        'weekly_goals': [None, week_multiplier, 25, 5, 'week'],
        'monthly_goals': [None, 12, 20, 5, 'month'],
        'quarterly_goals': [None, 4, 15, 5, 'quarter'],
        'yearly_goals': [None, 0, 10, 5, 'year'],
    })

    while temp_day.strftime('%a') != 'Mon':
        days_offset += 1
        temp_day = today - day_delta * days_offset

    days_offset += 7 * (num_weeks - 1)
    first_day = (today - days_offset * day_delta).strftime('%Y-%m-%d')
    day_to_idx = {}
    for i in range(days_offset+1):
        date_str = (today - day_delta * i).strftime('%Y-%m-%d')
        day_to_idx[date_str] = days_offset  - i

    for track_target in sorted(all_track_targets):
        title = track_target.split('.')[0]
        try:
            df = pd.read_csv(
                '{}/{}'.format(track_targets_path, track_target),
                skiprows=1,
                header=None,
                index_col=0
            )
        except:
            continue # only show tracked targets
        if title in special_track_targets:
            special_track_targets[title][0] = df
            continue

        df = df.loc[df.index >= first_day,:]
        if df.shape[0] > 0:
            titles.append(title)


            with open('{}/{}'.format(track_targets_path, track_target)) as f:
                first_line = f.readline()
            low, high, cmap_dir, aggregator, unit = first_line.split(',')
            _range.append((float(low) - 0.1, float(high) + 0.1))
            cmaps.append(cmap_dict[cmap_dir.strip()])
            aggregators.append(aggregator.strip())
            units.append(unit)
            dfs.append(df)

    plt.style.use("dark_background")
    x_tick_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig = plt.figure(figsize=(120 , 45))

    for i in range(len(titles)):
        minrange = _range[i][0]
        maxrange = _range[i][1]
        _ax = fig.add_subplot(math.ceil(len(titles)/plot_width)+2 ,plot_width , i + 1)

        _ax.get_yaxis().set_visible(False)
        _ax.set_title(titles[i], fontsize=SIZE_TITLE)
        _ax.xaxis.set(ticks=np.arange(0.5, 8, 1), ticklabels=x_tick_labels)#, labelsize=40)
        _ax.xaxis.set_tick_params(labelsize=SIZE_DAYS_OF_WEEK)
        nrows = days_offset // 7 + 1

        status_array = [np.nan] * nrows * 7
        status_array = np.array(status_array).reshape(nrows, 7)

        data = dfs[i].groupby(by=lambda x:x).agg(aggregators[i])
        zipped_data = zip(data.index.values, data[1].values)

        for date, val in zipped_data:
            idx = day_to_idx[date]
            status_array[nrows - 1 - idx // 7, idx % 7] = val

        pcm = _ax.pcolormesh(
            status_array,
            edgecolors='grey',
            linewidths=4,
            cmap=cmaps[i],
            vmin=minrange,
            vmax=maxrange
        )

        cbar = fig.colorbar(pcm, ax=_ax, orientation='horizontal',cmap=cmaps[i])
        cbar.ax.tick_params(labelsize=SIZE_UNITS) 
        cbar.set_label(units[i], size=SIZE_LABEL, color='lightgray')

    for c, item in enumerate(special_track_targets.items()):
        k,v = item
        df, multiplier, size, n_cols, primary = v
        status_array = [np.nan] * size

        if df is not None:
            data = df.groupby(by=lambda x:x).mean()
            zipped_data = zip(data.index.values, data[1].values)
            period_end = iso_info['{}_end'.format(primary)].date()

            today_idx = iso_info['year'] * multiplier + iso_info[primary] - 1
            for ds,val in zipped_data:
                dt = datetime.strptime(ds, '%Y-%m-%d')
                local_iso = get_iso_info(dt)
                local_idx = local_iso['year'] * multiplier + local_iso[primary] - 1
                if period_end == today:
                    if today_idx - local_idx > size - 1:
                        continue
                    status_array[local_idx - today_idx - 1] = val
                else:
                    if local_idx == today_idx:
                        continue
                    if today_idx - local_idx > size:
                        continue
                    status_array[local_idx - today_idx] = val

        _status_array = np.array(status_array).reshape(size // n_cols, n_cols)
        status_array = np.zeros(_status_array.shape)
        for i in range(_status_array.shape[0]):
            status_array[i] = _status_array[size // n_cols - i - 1]

        _ax = fig.add_subplot(math.ceil(len(titles)/plot_width)+2 ,plot_width , (math.ceil(len(titles) / plot_width) + 1)*plot_width + c + 1)
        _ax.get_xaxis().set_visible(False)
        _ax.get_yaxis().set_visible(False)
        _ax.set_title(k, fontsize=SIZE_TITLE)
        pcm = _ax.pcolormesh(
            status_array,
            edgecolors='grey',
            linewidths=4,
            cmap='RdYlGn',
            vmin=-0.1,
            vmax=10.1
        )
        #pcm.tick_params(labelsize=100) 

        cbar = fig.colorbar(pcm, ax=_ax, orientation='horizontal',cmap='RdYlGn')
        cbar.ax.tick_params(labelsize=SIZE_UNITS) 
        cbar.set_label('points', size=SIZE_LABEL, color='lightgray')

    plt.tight_layout(pad=10, w_pad=10, h_pad=10)
    plt.subplots_adjust(hspace=.3)

    if to_show:
        plt.show()

    fig.savefig('{}/status.png'.format(personal_dir))
    plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nb_weeks', type=int, nargs='?', default=4, help='number of weeks to track back')
    parser.add_argument('-s', '--show', type=str, default='True', help='option to show or just save figure. Defaults to True. ')
    args = parser.parse_args()
    to_show = args.show not in ['False', 'false', 'FALSE', 'f', 'F', '0', 'no', 'n', 'N', 'NO']
    main(args.nb_weeks, to_show)
