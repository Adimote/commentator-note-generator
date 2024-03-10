# Query /matches from the API and dump it in input
import argparse
import json

parser = argparse.ArgumentParser(prog='Generate scores from matches.json file')

parser.add_argument('filename')
args = parser.parse_args()

def common_entries(*dcts):
    if not dcts:
        return
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield (i,) + tuple(d[i] for d in dcts)

emoji_0 = ":large_green_square:"
emoji_1 = ":large_orange_square:"
emoji_2 = ":large_purple_square:"
emoji_3 = ":large_yellow_square:"
emojis = [emoji_0, emoji_1, emoji_2, emoji_3]

def pre_match(match, last_appearances):
    teams = match["teams"]
    match_num = match["num"]
    return f"""*{match["display_name"]}:*
{emoji_0} Zone 0 \t{teams[0]} \t{last_appearance_txt(teams[0], match_num, last_appearances)}
{emoji_1} Zone 1 \t{teams[1]} \t{last_appearance_txt(teams[1], match_num, last_appearances)}
{emoji_2} Zone 2 \t{teams[2]} \t{last_appearance_txt(teams[2], match_num, last_appearances)}
{emoji_3} Zone 3 \t{teams[3]} \t{last_appearance_txt(teams[3], match_num, last_appearances)}"""

def last_appearance_txt(tla, match_num, last_appearances):
    return "*Last appearance*" if last_appearances[tla] == match_num else ""

def calculate_last_appearances(matches):
    teams = {}
    for match in matches:
        for tla in match["teams"]:
            teams[tla] = match["num"]
    return teams

def human_rankings(rankings):
    for ranking in rankings:
        # (If there's a tied position)
        result = ""
        if ranking == 1:
            result = "1st"
        elif ranking == 2:
            result = "2nd"
        elif ranking == 3:
            result = "3rd"
        elif ranking == 4:
            result = "4th"

        yield f"={result}" if len([r for r in rankings if r == ranking]) > 1  else f"{result}"
        
def convert_to_human_rankings(rankings_dict):
    keys, values = zip(*rankings_dict.items())
    values = human_rankings(values)
    return dict(zip(keys,values))

def post_match(match):
    results = [f"*{match['display_name']} Results:*"]
    scores = match["scores"]
    human_rankings = convert_to_human_rankings(scores["ranking"])
    for tla, ranking in sorted(scores["ranking"].items(), key=lambda item: item[1]):
        corner = match["teams"].index(tla)
        score = scores["game"][tla]
        human_ranking = human_rankings[tla]
        results.append(f"{human_ranking}   \t{emojis[corner]} {tla} - Zone {corner} \t{score} point{'s' if score != 1 else ''}")
    return "\n".join(results)


with open(args.filename) as jsonfile:
    matches = json.load(jsonfile)
    last_appearances = calculate_last_appearances(filter(lambda m: "scores" in m, matches["matches"]))
    for match in matches["matches"]:
        if "scores" not in match:
            continue
        print(pre_match(match, last_appearances))
        print()
        print(post_match(match))
        print()
        
