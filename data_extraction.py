# Gets time usage data from a pgn downloaded from chess.com
import re
import datetime


def time_dif(start, end, inc=0):
    start = datetime.datetime.strptime(start, '%H:%M:%S.%f')
    end = datetime.datetime.strptime(end, '%H:%M:%S.%f')
    delta = end - start
    seconds = delta.total_seconds()
    return float(seconds) + inc


def make_data(name, fn):
    f = open(fn, 'r')
    str = f.read()
    games = str.split('\n[Event')
    game_data = []

    for game in games:
        # find color of player
        p = game.find(name)
        color = game[p - 7: p - 2]

        # extract timestamps from game
        timestamps = re.findall('%clk\s*(.+?)]', game)

        # fix for formatting omitting decimals if .0
        fixed_timestamps = []
        for timestamp in timestamps:
            if timestamp.find('.') == -1:
                timestamp += '.0'
            fixed_timestamps.append(timestamp)
        timestamps = fixed_timestamps

        # just get our timestamps
        if color == 'White':
            start = 0
        else:
            start = 1
        timestamps = timestamps[start::2]

        # find time used on each move
        time_control = re.findall('TimeControl\s\"(.+)\"', game)[0]
        plus = time_control.find('+')
        if plus == -1:
            inc = 0
        else:
            inc = int(time_control[plus:])
        
        timedifs = []
        for moveidx in (range(len(timestamps) - 1)):
            timedifs.append(time_dif(timestamps[moveidx+1], timestamps[moveidx], inc=inc))

        # save the data
        game_data.append(timedifs)

    return game_data


def combine_games(game_data):
    combined_list = []
    for game in game_data:
        combined_list += game
    return combined_list
