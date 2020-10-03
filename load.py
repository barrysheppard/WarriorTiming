###############################################################################
# Title: Warrior Timings                                                      #
# Developer: Barry Sheppard                                                   #
# Task: Get a warcraft combat log and return best times to use abilities      #
###############################################################################


###############################################################################
# Import                                                                      #
###############################################################################
import requests
import json
import pandas as pd
import math

###############################################################################
# Functions                                                                   #
###############################################################################


def boss_percentage(time_mark, raid_id, boss_id):
        start = time_mark
        end = time_mark + 1000 # one second after
        events = load_events(str(raid_id), str(start), str(end), str(boss_id))
        event_lines = events['events']
        for x in event_lines:
            if  'hitPoints' in x :
                return(str(x['hitPoints']))
                break
        else:
            return(100)


def check_log(log_id):
    """The primary piece of code that is called"""
    combatlog = load_combatlog(log_id)
    print_fights(combatlog, log_id)


def load_combatlog(log_id):
    """Return combat log"""
    api_id = "2ffbd9cca71b2ba1ffa76671d71a4c29"
    website = "https://classic.warcraftlogs.com/v1/report/fights/"
    url = website + log_id + "?api_key=" + api_id
    try:
        r = requests.get(url)
        # If the response was successful, no Exception will be raised
        r.raise_for_status()
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = json.loads(r.content.decode())
    return(data)


def load_events(id, start_time, end_time, targetID):
        """Return events log"""
        api_id = "2ffbd9cca71b2ba1ffa76671d71a4c29"
        website = "https://classic.warcraftlogs.com/v1/report/events/damage-done/"
        url = website + id + "?api_key=" + api_id + "&start=" + str(start_time) + "&end=" + str(end_time) + "&targetID=" + str(targetID)
        try:
            r = requests.get(url)
            # If the response was successful, no Exception will be raised
            r.raise_for_status()
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            data = json.loads(r.content.decode())
        return(data)


def print_fights(log, log_id):
    """Return list of bosses from the log"""
    fights = log['fights']
    for x in fights:
        if x['boss'] > 0 and x['kill'] == True :
            time = (x['end_time'] - x['start_time']) / 1000
            time = math.floor(time)
            text_one = x['name'] + " : " + str(time) + " seconds"
            # Diamond flask is 60 seconds
            start_diamondflask = x['end_time']-60000
            boss_percent = boss_percentage(start_diamondflask, log_id, x['id'])
            text_two = ", Diamond Flask on: " + str(boss_percent) + "%"
            # Deathwish is 30 seconds
            start_deathwish = x['end_time']-30000
            boss_percent = boss_percentage(start_deathwish, log_id, x['id'])
            text_three = ", Deathwish on: " + str(boss_percent) + "%"
            # Mighty Rage Pot / Rek is 20 seconds
            start_mragepot = x['end_time']-20000
            boss_percent = boss_percentage(start_mragepot, log_id, x['id'])
            text_four = ", Mighty Rage Pot / Rek on: " + str(boss_percent) + "%"

            print(text_one + text_two + text_three + text_four)


###############################################################################
# Code for when file is run from command line                                 #
###############################################################################

if __name__ == '__main__':

    check_log("8AkzDGqNW4RFLgma")
