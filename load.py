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


def print_fights(log_id, id):
    """Return list of bosses from the log"""
    fights = log_id['fights']
    for x in fights:
        if x['boss'] > 0:
            time = (x['end_time'] - x['start_time']) / 1000
            time = math.floor(time)
            text_one = str(x['id']) + " " + x['name'] + " : " + str(time) + " seconds"
            start_deathwish = x['end_time']-31000
            events = load_events(str(id), str(start_deathwish), str(x['end_time']), str(x['id']))
            deathwish = event_times(events)
            text_two = " Deathwish on: " + str(deathwish) + "%"
            print(text_one + text_two)


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

def event_times(events):
    """Prints event times"""
    event_lines = events['events']
    for x in event_lines:
        if  'hitPoints' in x:
            return(str(x['hitPoints']))

###############################################################################
# Code for when file is run from command line                                 #
###############################################################################

if __name__ == '__main__':

    combatlog = load_combatlog("6T9jDbqBH8cnzVxY")
    print_fights(combatlog, "6T9jDbqBH8cnzVxY")

#    end_time = 1655297
#    deathwish = end_time - 31000
#    events = load_events("6T9jDbqBH8cnzVxY", deathwish, end_time, 16)
#    event_times(events)



#{'events':
#[{'timestamp': 1590468, 'type': 'damage', 'sourceID': 15, 'sourceIsFriendly': True,
#  'targetID': 64, 'targetIsFriendly': False, 'ability': {'name': 'Heroic Strike', 'guid': 25286,
#  'type': 1, 'abilityIcon': 'ability_rogue_ambush.jpg'}, 'buffs': '22817.24425.22888.', 'hitType': 1,
#  'amount': 282, 'mitigated': 191, 'unmitigatedAmount': 473, 'resourceActor': 2,
#  'classResources': [{'amount': 0, 'max': 0, 'type': -1}],
#  'hitPoints': 100, 'maxHitPoints': 100, 'attackPower': 0, 'spellPower': 0, 'armor': 0,
#  'x': -121200, 'y': -805230, 'facing': -210, 'mapID': 0, 'itemLevel': 63, 'sourceMarker': 6
# },
# {'timestamp': 1590487, 'type': 'damage', 'sourceID': 15, 'sourceIsFriendly': True, 'targetID': 64,
#  'targetIsFriendly': False, 'ability': {'name': 'Bloodthirst', 'guid': 23894, 'type': 1,
#  'abilityIcon': 'spell_nature_bloodlust.jpg'}, 'buffs': '22817.24425.22888.', 'hitType': 8,
#  'amount': 0, 'sourceMarker': 6}, {'timestamp': 1590837, 'type': 'damage', 'sourceID': 12,
#  'sourceIsFriendly': True, 'targetID': 64, 'targetIsFriendly': False,
#  'ability': {'name': 'Melee', 'guid': 1, 'type': 1, 'abilityIcon': 'inv_axe_02.jpg'},
#  'buffs': '24425.24932.22888.', 'hitType': 6, 'amount': 192, 'mitigated': 155,
#  'unmitigatedAmount': 347, 'resourceActor': 2, 'classResources': [{'amount': 0, 'max': 0, 'type': -1}], 'hitPoints': 100, 'maxHitPoints': 100, 'attackPower': 0, 'spellPower': 0, 'armor': 0, 'x': -121200, 'y': -805230, 'facing': -210, 'mapID': 0, 'itemLevel': 63}, {'timestamp': 1591246, 'type': 'damage', 'sourceID': 15, 'sourceIsFriendly': True, 'targetID': 64, 'targetIsFriendly': False, 'ability': {'name': 'Melee', 'guid': 1, 'type': 1, 'abilityIcon': 'inv_axe_02.jpg'}, 'buffs':
#  '22817.24425.24932.22888.', 'hitType': 2, 'amount': 319, 'unmitigatedAmount': 267, 'resourceActor': 2, 'classResources': [{'amount': 0, 'max': 0, 'type': -1}], 'hitPoints': 100,
