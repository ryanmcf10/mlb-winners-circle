import mlbgame as mlb
import datetime
import sys

from teams import *
from opening_days import *

current_year = datetime.datetime.now().year

def trim_spring_training_games(season, year):
    result = []
    opening_day = opening_days[str(year)]

    for game in season:
        if game.date.date() >= opening_day:
            result.append(game)

    return result

def calculate_wins(team, year):
    nickname = team['team']
    print("Calculating wins for {}".format(nickname))

    all_games = mlb.games(year, home=nickname, away=nickname)
    season = mlb.combine_games(all_games)
    season = trim_spring_training_games(season, year)

    wins = 0
    for game in season:
        try:
            if game.w_team == nickname:
                team['wins-versus'][game.l_team] += 1
                wins += 1
        except:
            pass

    print("Done.\n")

def main(year):
    filename = "./data/results{}.csv".format(str(year))
    print("Calculating wins for {}...".format(str(year)))
    print("Results will be stored in {}".format(filename))
    print('======================================\n')

    f = open(filename, 'w')
    f.write("team,opponent,wins,color\n")

    count = 0
    for team in teams:
        calculate_wins(teams[team], year)

        wins = teams[team]['wins-versus']
        nickname = teams[team]['team']

        for opponent, win_total in wins.items():
            line = nickname + "," + opponent + "," + str(win_total) + "," + str(count) + "\n"
            f.write(line)
        
        count += 1

    f.close()
    print("Done.")

if __name__ == '__main__':
    if len(sys.argv) == 1:
            main(current_year)
    if len(sys.argv) > 1:
        for year in sys.argv[1:]:
            try:
                year = int(year)
            except:
                print("Invalid argument: must input a year (1980-{})".format(str(current_year)))
                break

            if year >= 1980 and year <= current_year:
                main(year)
            else:
                print("Invalid argument: must input a year (1980-{})".format(str(current_year)))
                break
