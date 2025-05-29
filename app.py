from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# In-memory journal (clears on restart)
journal_entries = []

cozy_vibes = [
    "Wrap yourself in a blanket and read your favorite book 📖",
    "Take a deep breath and dance like nobody's watching 💃",
    "Bake something sweet — maybe cookies or cupcakes? 🧁",
    "Light a candle, close your eyes, and dream for 2 minutes 🕯️",
    "Write a short story based on a random word you love ✍️"
]

baking_ideas = [
    "Try making banana chocolate chip muffins 🍌🍫",
    "How about some red velvet cupcakes? ❤️🧁",
    "Invent your own cookie flavor today! 🍪",
    "Mini cinnamon rolls would smell amazing 🌀",
    "Make chai-spiced cupcakes for cozy vibes ☕🧁"
]

dance_breaks = [
    "Put on your favorite high-energy song and spin! 🎶",
    "Mirror freestyle: just feel the music 💃",
    "Stretch, sway, and breathe with lo-fi music 🎧",
    "Make a dance move inspired by the word 'sunlight' ☀️"
]

sweet_messages = [
    "You're a soft storm of magic and light 💖",
    "You make cozy look cool ✨",
    "If kindness was a color, you'd be a sunset 🌇",
    "You're poetry in motion and sugar in tea 🍯",
    "The world is luckier with you in it 🌸"
]

compliments = [
    "Devya, you're absolutely glowing today 🌟",
    "Your smile could light up the whole sky 🌈",
    "You're made of stardust and kindness ✨",
    "You have the heart of a poet and the spark of a star 💫",
    "The universe must've smiled when you were born 🌼"
]

mood_responses = {
    "happy": "Yay! Keep spreading those good vibes 🌞",
    "sad": "It’s okay to feel down. Here’s a hug 🤗",
    "tired": "Rest, recharge, and know you're doing great 😴",
    "bored": "Try dancing, drawing, or making a dream list! 🎨",
    "excited": "Use that energy to make magic happen! 💥"
}

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
  <title>Devya's Cozy Space 💖</title>
  <style>
    body {
      background-color: #fff0f5;
      font-family: 'Comic Sans MS', cursive;
      text-align: center;
      padding: 20px;
      min-height: 100vh;
      overflow-x: hidden;
    }
    h1 { color: #d63384; font-size: 3rem; }
    p { color: #6a1b9a; font-size: 1.2rem; }
    button {
      background: #f06292;
      color: white;
      border: none;
      padding: 10px 20px;
      margin: 10px;
      border-radius: 20px;
      font-weight: bold;
      cursor: pointer;
    }
    button:hover { background: #ec407a; }
    #result, #compliment, #mood-result { margin-top: 20px; font-size: 1.2rem; color: #880e4f; }
    textarea {
      width: 80%%;
      height: 100px;
      border-radius: 10px;
      padding: 10px;
      margin-top: 20px;
      border: 2px solid #f48fb1;
    }
    .heart {
      position: absolute;
      animation: float 6s infinite;
      font-size: 2rem;
      color: #f43f5e;
      opacity: 0.6;
    }
    @keyframes float {
      0%% { transform: translateY(0); opacity: 1; }
      100%% { transform: translateY(-800px); opacity: 0; }
    }
  </style>
</head>
<body>
  <h1>Hi Devya 💕</h1>
  <p>This is your cozy, magical corner of the internet ✨</p>

  <div>
    <button onclick="fetchVibe('/vibe')">✨ Cozy Vibe</button>
    <button onclick="fetchVibe('/bake')">🧁 Baking Idea</button>
    <button onclick="fetchVibe('/dance')">💃 Dance Break</button>
    <button onclick="fetchVibe('/message')">💌 Sweet Message</button>
  </div>

  <div id="result"></div>

  <hr>

  <h2>🌸 Compliment for You</h2>
  <div id="compliment">You're magical ✨</div>

  <hr>

  <h2>🧠 Mood Check</h2>
  <select id="mood">
    <option value="">-- Select your mood --</option>
    <option value="happy">😊 Happy</option>
    <option value="sad">😢 Sad</option>
    <option value="tired">😴 Tired</option>
    <option value="bored">😐 Bored</option>
    <option value="excited">🤩 Excited</option>
  </select>
  <button onclick="checkMood()">Get Advice</button>
  <div id="mood-result"></div>

  <hr>

  <h2>📓 Your Journal</h2>
  <form onsubmit="saveNote(); return false;">
    <textarea id="note" placeholder="Write a sweet note..."></textarea><br>
    <button type="submit">Save Note</button>
  </form>
  <div id="notes"></div>

  <script>
    function fetchVibe(endpoint) {
      fetch(endpoint)
        .then(res => res.json())
        .then(data => {
          document.getElementById('result').innerText = data;
        });
    }

    function checkMood() {
      const mood = document.getElementById("mood").value;
      if (!mood) return;
      fetch("/mood?feeling=" + mood)
        .then(res => res.json())
        .then(data => {
          document.getElementById('mood-result').innerText = data;
        });
    }

    function saveNote() {
      const note = document.getElementById("note").value;
      if (!note) return;
      fetch("/journal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note })
      })
      .then(() => {
        document.getElementById("note").value = "";
        loadNotes();
      });
    }

    function loadNotes() {
      fetch("/journal")
        .then(res => res.json())
        .then(data => {
          document.getElementById("notes").innerHTML = data.map(n => `<p>💖 ${n}</p>`).join('');
        });
    }

    // Compliment Carousel
    const compliments = %s;
    let index = 0;
    setInterval(() => {
      document.getElementById("compliment").innerText = compliments[index];
      index = (index + 1) %% compliments.length;
    }, 5000);

    // Floating hearts
    setInterval(() => {
      let heart = document.createElement('div');
      heart.className = 'heart';
      heart.style.left = Math.random() * 100 + 'vw';
      heart.style.top = '100vh';
      heart.innerText = '❤️';
      document.body.appendChild(heart);
      setTimeout(() => heart.remove(), 6000);
    }, 700);

    loadNotes();
  </script>
</body>
</html>
    ''' % compliments  # Inserts Python list directly into JavaScript

@app.route('/vibe')
def vibe(): return jsonify(random.choice(cozy_vibes))

@app.route('/bake')
def bake(): return jsonify(random.choice(baking_ideas))

@app.route('/dance')
def dance(): return jsonify(random.choice(dance_breaks))

@app.route('/message')
def message(): return jsonify(random.choice(sweet_messages))

@app.route('/mood')
def mood():
    feeling = request.args.get("feeling", "")
    return jsonify(mood_responses.get(feeling, "Tell me how you feel 💬"))

@app.route('/journal', methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        note = request.json.get("note")
        if note: journal_entries.append(note)
        return '', 204
    return jsonify(journal_entries)
    import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not set
    app.run(host='0.0.0.0', port=port)
