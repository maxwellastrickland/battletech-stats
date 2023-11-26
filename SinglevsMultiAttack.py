# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:25:14 2023

@author: DungeonMaxter
"""

from random import randint
import pandas as pd

def roll():
    return randint(1,6)

def roll_twice():
    total = 0
    for turn in range(2):
        total += roll()
    return total


def single_attack(target, damage):
    score = 0
    if roll_twice() >= target:
        score += damage
    return score

def multi_attack(target, damage):
    score = 0
    for shots in range(damage):
        if roll_twice() >= target:
            score += 1
    return score

def pilot_attack(target, damage):
    score = 0
    pilot = roll()
    for shots in range(damage):
        if pilot + roll() >= target:
            score += 1
    return score

games_played = 1000
attacks = 40
damage = 4

single_df = pd.DataFrame(columns = ['target','rounds','red_player', 'blue_player'])
multi_df = pd.DataFrame(columns = ['target','rounds', 'red_player', 'blue_player'])
pilot_df = pd.DataFrame(columns = ['target','rounds', 'red_player', 'blue_player'])

for rounds in range(games_played):
    for target in range(2,13,1):
        single_red_score = 0
        single_blue_score = 0
        for blast in range(attacks):
            single_red_score += single_attack(target, damage)
            single_blue_score += single_attack(target, damage)
        single = {'target':target,'rounds':rounds+1,'red_player': single_red_score,'blue_player': single_blue_score}
        single_df = pd.concat([single_df, pd.DataFrame([single])], ignore_index=True, axis=0)
    
        multi_red_score = 0
        multi_blue_score = 0
        for blast in range(attacks):
            multi_red_score += multi_attack(target, damage)
            multi_blue_score += multi_attack(target, damage)
        multi = {'target':target,'rounds':rounds+1,'red_player': multi_red_score,'blue_player': multi_blue_score}
        multi_df = pd.concat([multi_df, pd.DataFrame([multi])], ignore_index=True, axis=0)
        
        pilot_red_score = 0
        pilot_blue_score = 0
        for blast in range(attacks):
            pilot_red_score += pilot_attack(target, damage)
            pilot_blue_score += pilot_attack(target, damage)
        pilot = {'target':target,'rounds':rounds+1,'red_player': pilot_red_score,'blue_player': pilot_blue_score}
        pilot_df = pd.concat([pilot_df, pd.DataFrame([pilot])], ignore_index=True, axis=0)

single_df['difference'] = abs(single_df.red_player - single_df.blue_player)
multi_df['difference'] = abs(multi_df.red_player - multi_df.blue_player)
pilot_df['difference'] = abs(pilot_df.red_player - pilot_df.blue_player)

single_df_summary = single_df.groupby('target').aggregate(['mean', 'std'])
multi_df_summary = multi_df.groupby('target').aggregate(['mean', 'std'])
pilot_df_summary = pilot_df.groupby('target').aggregate(['mean', 'std'])
print(single_df_summary[['red_player','blue_player','difference']])
print(multi_df_summary[['red_player','blue_player','difference']])
print(pilot_df_summary[['red_player','blue_player','difference']])

