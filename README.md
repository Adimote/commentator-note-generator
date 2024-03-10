# commentator-note-generator

Generates commentator notes for a virtual competition livestream, based on the .json response file from the sr.comp.http /matches srcomp API endpoint.


This produces two sections, interleaved;

One has the details of the teams for the upcoming match, and the other has the scores for the previous match.

Normally I send both of these at the same time at the end of the previous match.

I normally also add a lot of manually-inserted details about the teams to the 'upcoming' message. especially their performance in the last match, or some random facts about the school.

# Installation

This package has no dependencies, just clone this repo and run the script.

# Running

## Fetch matches from the API

Use `curl` to fetch the `/matches` json response from sr.comp.http into a file.

Example:
```curl https://srcomp.studentrobotics.org/comp-api/matches > matches.json```

Though you won't want to query the production API, because if you're running this script you're likely preparing for a *future* event.

To do this for future events, you'll need to run your own instance of sr.comp.http, see https://github.com/peterJCLaw/srcomp-http about setting this up.

## Run the script

If you're on Windows, I recommend you pipe the results into a file, then use something like Notepad to paste it into Slack/ a Google doc for further editing. This is because we insert tab characters to neaten up the tabular data, and windows CMD replaces tabs with 4 spaces when copying for some reason.

Just run:

```python generate-scores-from-matches.py matches.json > messages.txt```

Then the messages will be in messages.txt



