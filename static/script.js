async function startTask() {
    let task = document.getElementById("taskName").value;
    let res = await fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    });
    let data = await res.json();
    alert(data.message);
    loadTasks();
}

async function stopTask() {
    let res = await fetch('/stop', { method: 'POST' });
    let data = await res.json();
    alert(data.message);
    loadTasks();
}

async function loadTasks() {
    let res = await fetch('/tasks');
    let data = await res.json();
    document.getElementById("tasks").innerText = JSON.stringify(data, null, 2);
}

async function getQuote() {
    let res = await fetch('/quote');
    let data = await res.json();
    document.getElementById("quote").innerText = data.quote;
}

async function startPomodoro() {
    let res = await fetch('/pomodoro/start', { method: 'POST' });
    let data = await res.json();
    alert(data.message);
    checkPomodoro();
}

async function stopPomodoro() {
    let res = await fetch('/pomodoro/stop', { method: 'POST' });
    let data = await res.json();
    alert(data.message);
    checkPomodoro();
}

async function checkPomodoro() {
    let res = await fetch('/pomodoro/status');
    let data = await res.json();
    document.getElementById("pomodoroStatus").innerText = data.active ? `Ends at: ${new Date(data.end_time * 1000)}` : "No active Pomodoro.";
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

loadTasks();
checkPomodoro();