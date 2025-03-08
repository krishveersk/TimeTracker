from flask import Flask, render_template, request, jsonify
import time
import json
import random
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data/tasks.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": [], "pomodoro": None}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def  save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def t1mestamp(timestamp):
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


QUOTES = [
    "Faith is love taking the form of aspiration. — William Ellery Channing",
    "You can't cross the sea merely by standing and staring at the water. — Rabindranath Tagore",
    "No bird soars too high if he soars with his own wings. — William Blake",
    "Don't judge each day by the harvest you reap but by the seeds that you plant. — Robert Louis Stevenson",
    "I believe there's an inner power that makes winners or losers. And the winners are the ones who really listen to the truth of their hearts. — Sylvester Stallone",
    "It is our attitude at the beginning of a difficult task which, more than anything else, will affect its successful outcome. — William James",
    "Think like a queen. A queen is not afraid to fail. Failure is another stepping stone to greatness. — Oprah Winfrey",
    "Keep your feet on the ground, but let your heart soar as high as it will. Refuse to be average or to surrender to the chill of your spiritual environment. — Arthur Helps",
    "I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.' — Muhammad Ali",
    "Don't stop when you're tired, stop when you're done. — David Goggins",
    "You define your own life. Don't let other people write your script. — Oprah Winfrey",
    "You are never too old to set another goal or to dream a new dream. — Malala Yousafzai",
    "People tell you the world looks a certain way. Parents tell you how to think. Schools tell you how to think. TV. Religion. And then at a certain point, if you're lucky, you realize you can make up your own mind. Nobody sets the rules but you. You can design your own life. — Carrie Ann Moss",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
    "For me, becoming isn't about arriving somewhere or achieving a certain aim. I see it instead as forward motion, a means of evolving, a way to reach continuously toward a better self. The journey doesn't end. — Michelle Obama",
    "Spread love everywhere you go. — Mother Teresa",
    "Do not allow people to dim your shine because they are blinded. Tell them to put some sunglasses on. — Lady Gaga",
    "If you make your internal life a priority, then everything else you need on the outside will be given to you, and it will be extremely clear what the next step is. — Gabrielle Bernstein",
    "You don't always need a plan. Sometimes you just need to breathe, trust, let go and see what happens. — Mandy Hale",
    "No matter what people tell you, words and ideas can change the world. — Robin Williams",
    "What lies behind you and what lies in front of you, pales in comparison to what lies inside of you. — Ralph Waldo Emerson",
    "It always seems impossible until it's done. — Nelson Mandela",
    "I'm going to be gone one day, and I have to accept that tomorrow isn't promised. Am I OK with how I'm living today? It's the only thing I can help. If I didn't have another one, what have I done with all my todays? Am I doing a good job? — Hayley Williams",
    "I am experienced enough to do this. I am knowledgeable enough to do this. I am prepared enough to do this. I am mature enough to do this. I am brave enough to do this. — Alexandria Ocasio-Cortez",
    "Belief creates the actual fact. — William James",
    "I'm not going to continue knocking that old door that doesn't open for me. I'm going to create my own door and walk through that. — Ava DuVernay",
    "You can be everything. You can be the infinite amount of things that people are. — Kesha",
    "It is during our darkest moments that we must focus to see the light. — Aristotle",
    "Not having the best situation, but seeing the best in your situation is the key to happiness. — Marie Forleo",
    "Believe you can, and you're halfway there. — Theodore Roosevelt",
    "Weaknesses are just strengths in the wrong environment. — Marianne Cantwell",
    "Just don't give up trying to do what you really want to do. Where there is love and inspiration, I don't think you can go wrong. — Ella Fitzgerald",
    "I've missed more than 9,000 shots in my career. I've lost almost 300 games. Twenty-six times, I've been trusted to take the game-winning shot and missed. I've failed over and over and over again in my life. And that is why I succeed. — Michael Jordan",
    "In a gentle way, you can shake the world. — Mahatma Gandhi",
    "Learning how to be still, to really be still and let life happen—that stillness becomes a radiance. — Morgan Freeman",
    "Everyone has inside of him a piece of good news. The good news is that you don't know how great you can be! How much you can love! What you can accomplish! And what your potential is! — Anne Frank",
    "All you need is the plan, the road map and the courage to press on to your destination. — Earl Nightingale",
    "I care about decency and humanity and kindness. Kindness today is an act of rebellion. — Pink",
    "If you have good thoughts they will shine out of your face like sunbeams and you will always look lovely. — Roald Dahl",
    "Try to be a rainbow in someone else's cloud. — Maya Angelou",
    "We must let go of the life we have planned, so as to accept the one that is waiting for us. — Joseph Campbell",
    "Find out who you are and be that person. That's what your soul was put on this earth to be. Find that truth, live that truth and everything else will come. — Ellen DeGeneres",
    "Real change, enduring change, happens one step at a time. — Ruth Bader Ginsburg",
    "Wake up determined, go to bed satisfied. — Dwayne 'The Rock' Johnson",
    "Nobody is built like you; you design yourself. — Jay-Z",
    "You gain strength, courage and confidence by every experience in which you really stop to look fear in the face. You are able to say to yourself, 'I lived through this horror. I can take the next thing that comes along.' You must do the thing you think you cannot do. — Eleanor Roosevelt",
    "Live your beliefs, and you can turn the world around. — Henry David Thoreau",
    "Life is like riding a bicycle. To keep your balance, you must keep moving. — Albert Einstein",
    "Don't try to lessen yourself for the world; let the world catch up to you. — Beyoncé",
    "There's nothing more powerful than not giving a f—k. — Amy Schumer",
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_task():
    data = load_data()
    content = request.json
    task_name = content.get("task", "Unnamed Task")
    start_time = time.time()

    for task in data["tasks"]:
        if task.get("end_time") is None:
            task["end_time"] = start_time

    data["tasks"].append({
        "task": task_name,
        "start_time": start_time,
        "end_time": None
    })
    save_data(data)

    return jsonify({"message": f"Started task: {task_name}"})

@app.route('/stop', methods=['POST'])
def stop_task():
    data = load_data()
    stop_time = time.time()

    for task in data["tasks"]:
        if task.get("end_time") is None:
            task["end_time"] = stop_time
            save_data(data)
            return jsonify({"message": f"Stopped task: {task['task']}"})
    
    return jsonify({"message": "No active task found."})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    data = load_data()
    ftasks = [{
        "task": task["task"], 
        "start_time": t1mestamp(task["start_time"]),  
        "end_time": t1mestamp(task["end_time"])  
    } for task in data["tasks"]]

    return jsonify(ftasks)


@app.route('/quote', methods=['GET'])
def get_quote():
    return jsonify({"quote": random.choice(QUOTES)})

@app.route('/pomodoro/start', methods=['POST'])
def start_pomodoro():
    data = load_data()
    if data.get("pomodoro") is not None:
        return jsonify({"message": "A Pomodoro session is already running!"})
    
    end_time = time.time() + (25 * 60)
    data["pomodoro"] = {"active": True, "end_time": end_time}
    save_data(data)

    return jsonify({"message": "A Pomodoro session has started!"})

@app.route('/pomodoro/stop', methods=['POST'])
def stop_pomodoro():
    data = load_data()
    data["pomodoro"] = None
    save_data(data)
    return jsonify({"message": "Pomodoro session has stopped!"})

@app.route('/pomodoro/status', methods=['GET'])
def pomodoro_status():
    data = load_data()
    return jsonify(data.get("pomodoro", {"active": False}))

@app.route('/stats', methods=['GET'])
def get_stats():
    data = load_data()
    total_tasks = len(data["tasks"])
    total_time = sum(
        (task["end_time"] - task["start_time"])
        for task in data["tasks"] if task["end_time"]
    )

    return jsonify({
        "total_tasks": total_tasks,
        "total_time": round(total_time / 60, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)