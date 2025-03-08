# Track Time & Pomodoro (API-Based)

- The API is made using python and is fully compatible to run on a Raspberry Pi Zero.

## Features

1. Track time spent on tasks with added start/stop functionality.
2. View task history along with timestamps.
3. A Pomodoro timer.
4. Get motivational quotes.
5. View task statistics like total tasks and total time spent.
6. Toggle between light and dark mode.

## Installing the API on a Raspberry Pi Zero

1. Clone the repository

```
git clone https://github.com/krishveersk/TimeTracker
cd TimeTracker
```

2. Install Modules
   `pip install -r requirements.txt`

3. Run the application
   `python app.py`

- The server will start at http://127.0.0.1:5000/

## Accessing the website

- Simply open your browser and go to the following IP address to access the UI.

## API Endpoints

### /start (POST)

- Starts a new task.

### /stop (POST)

- Stops the active task.

### /tasks (GET)

- Gets a list of all the tasks and outputs it.

### /pomodoro/start (POST)

- Starts a standard pomodoro timer of 25 minutes.

### /pomodoro/stop (POST)

- Stops the pomodoro session.

### /pomodoro/status (GET)

- Checks the pomodoro status.

### /quotes (GET)

- Fetches a random motivational quote.

### /stats (GET)

- Fetches total tasks and total time spent.

## Using the Website to access the API

- Start or stop tasks using the buttons.
- The website will also list current and past tasks.
- With a click of a button the website will fetch and display
- Start or stop Pomodoro sessions
- Toggle between light and dark mode

## Modifying the code

### Adding your own set of quotes

- Go to the app.py file and there locate something that looks like something like below, and go add your own quotes separated by commas.

```
QUOTES = [
   "Quote 1",
   "Quote 2",
   "Quote 3"
]
```

### Change Pomodoro Duration

- To modify the duration go to the app.py file and find the line below and edit 25 to any value of minutes you want to have in one Pomodoro situation.

`end_time = time.time() + (25 * 60)`

- The project is hosted on render so that it can be viewed by anyone in the world and they can also access it.
https://timetracker-svvb.onrender.com
