# 📔Checkin

Okay chat here's the idea *hear me out*. A CLI app that you can use to track your mood each day throughout the year. Using a terminal plotting library (hopefully) it can display statistics through the year so far, all data gets saved as a csv and can be exported to a spreadsheet. It can track the following data:

| Tracking data   | range        | Extra notes |
|-----------------|--------------|-------------|
| Mood            | 0 - 5        |             |
| Energy          | 1 - 10       |             |
| Productive Hours| 0.0 - 24.0   |             |
| Hours of Sleep  | 0.0 - 24.0   |             |
| Cry             | y/n          |             |


## Hopeful Features
- Spreadsheet exporting from the csv files
- editing previous checkins
    - 1-12 month then 1-3[01] day
- graph specific metrics in the terminal
- (VERY MAYBE) customize using a config what metrics checkin tracks
    - E.g. Only track mood and energy
    - Change the display of the mood values from default (purely visual/ux)

## Commands
- `checkin start` - starts the checkin session and its prompts
- `checkin export` - dumps the dsv into a 
- `checkin edit` - change a previous checkin
    - `-v` flag to view missed days


