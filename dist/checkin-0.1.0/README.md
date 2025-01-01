# 📔Checkin

This project is not working or anything yet (not really at least), if you are reading this and you aren't me, go away >:( come back later <3.

Okay chat here's the idea *hear me out*. A CLI app that you can use to track your mood each day throughout the year. Using a terminal plotting library (hopefully) it can display statistics through the year so far, all data gets saved as a csv and can be exported to a spreadsheet. It can track the following data:

| Tracking data   | range        | Extra notes |
|-----------------|--------------|-------------|
| Mood            | 0 - 5        |             |
| Energy          | 1 - 10       |             |
| Daily Activities| Multi-select |             |
| Cry             | y/n          |             |
| Productive Hours| 0.0 - 24.0   |             |
| Hours of Sleep  | 0.0 - 24.0   |             |

## Hopeful Features
- Spreadsheet exporting from the csv files
- editing previous checkins
    - 1-12 month then 1-3[01] day
- graph specific metrics in the terminal
- (VERY MAYBE) customize using a config what metrics checkin tracks
    - E.g. Only track mood and energy
    - Change the display of the mood values from default (purely visual/ux)

## Commands
### `checkin start`
Starts the checkin session and its prompts.

### `checkin edit`
Change a previous checkin.
- `-v, --view` flag to view and edit missed checkins.
- `%Y-%m-%d` argument to specify the date of the checkin to edit.

### `checkin graph`
Prompts the user to select a metric to graph right in the terminal.

### `checkin spotify`
Fetches and displays Spotify data.
- `-m` flag to show past month's top played.
- `-y` flag to show past year's top played.
- `-h` flag to show past 6 months' top played.
- `-a` flag to display artists instead of songs (defaults to getting songs).
- `--top n` option to get the top `n` items.
- `--store` flag to store top played data.



## To-do list
- [ ] finish adding metrics to track
- [ ] list old entries and missed entries
    - For this I need to figure out a way to have a scrollable selector lol
- [x] prompt user to add missing entries
- [x] edit previous entries
    - [ ] Okay preferably I could have a cool like date selector thing but i havent found one yet
- [x] change date format of stored data and graph
- [x] automatically start storing spotify data near end of month