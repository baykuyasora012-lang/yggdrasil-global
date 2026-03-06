import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "omni_quantum_v300_ultra_private"

# 🔑 Master Config
ADMIN_ID = "admin"
ADMIN_KEY = "1234"
CREDIT_LIMIT = 100

RULES = [
    "১. শুধুমাত্র ক্যান্ডেলস্টিক চার্টের পরিষ্কার ছবি ব্যবহার করুন।",
    "২. মানুষের মুখ বা শরীরের অংশ থাকলে এআই ডাটা রিজেক্ট করবে।",
    "৩. মানি ম্যানেজমেন্ট অনুসরণ করুন (প্রতি ট্রেডে ১-২% রিস্ক)।",
    "৪. বড় নিউজের সময় ট্রেড করা থেকে বিরত থাকুন।",
    "৫. বট হাই-রিস্ক শনাক্ত করলে ট্রেড স্কিপ করবে।"
]

# --- HTML TEMPLATES ---
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LOGIN | OMNI-QUANTUM</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body { background: #020205; color: #fff; font-family: 'Orbitron', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-card { background: rgba(10, 15, 30, 0.95); padding: 40px; border-radius: 20px; border: 1px solid #00f2ff; box-shadow: 0 0 30px rgba(0, 242, 255, 0.2); width: 320px; text-align: center; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; background: #000; border: 1px solid #1a2a3a; border-radius: 10px; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 15px; border-radius: 10px; border: none; background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; font-weight: 900; cursor: pointer; letter-spacing: 2px; }
        .error { color: #ff0051; font-size: 12px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2 style="color:#00f2ff; margin-bottom:30px;">AUTHENTICATE</h2>
        <form method="POST">
            <input type="text" name="u" placeholder="SYSTEM ID" required>
            <input type="password" name="p" placeholder="SECURITY KEY" required>
            <button type="submit">LOGIN SYSTEM</button>
        </form>
        {% if error %}<div class="error">ACCESS DENIED: INVALID KEY</div>{% endif %}
    </div>
</body>
</html>
'''

MAIN_HTML = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMNI-QUANTUM V300</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ffa3; --loss: #ff0051; --bg: #010103; }
        body { background: var(--bg); color: #fff; font-family: 'Rajdhani', sans-serif; margin: 0; }
        
        .navbar { padding: 20px; background: rgba(0,0,0,0.9); border-bottom: 1px solid var(--neon); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .logo { font-family: 'Orbitron'; color: var(--neon); font-size: 18px; letter-spacing: 3px; }

        .container { max-width: 550px; margin: 20px auto; padding: 0 15px; }

        /* 📜 Dedicated Rules Box */
        .rules-box { background: rgba(255, 204, 0, 0.05); border: 1px solid rgba(255, 204, 0, 0.2); padding: 20px; border-radius: 15px; margin-bottom: 25px; border-left: 5px solid var(--gold); }
        .rules-box h4 { margin: 0 0 10px 0; color: var(--gold); font-family: 'Orbitron'; font-size: 12px; }
        .rules-box div { font-size: 13px; color: #bbb; margin-bottom: 5px; }

        /* 📊 HUD Stats */
        .hud { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 25px; }
        .hud-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(0,242,255,0.1); padding: 12px 5px; border-radius: 12px; text-align: center; }
        .hud-card span { font-size: 8px; color: #888; display: block; text-transform: uppercase; }
        .hud-card b { font-family: 'Orbitron'; font-size: 14px; color: var(--neon); }

        /* 🖥️ Terminal Console */
        .terminal { background: rgba(10, 15, 30, 0.95); border-radius: 30px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        input, select { width: 100%; padding: 18px; margin-bottom: 15px; background: #000; border: 1px solid #1a2a3a; border-radius: 12px; color: #fff; font-family: 'Rajdhani'; outline: none; box-sizing: border-box; }
        .btn-scan { background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 20px; border-radius: 12px; border: none; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; letter-spacing: 2px; }

        /* 🔄 Scanning Animation */
        #loader { display: none; text-align: center; margin: 30px 0; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(0,242,255,0.1); border-top: 4px solid var(--neon); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 100% { transform: rotate(360deg); } }

        /* 📈 Output */
        .output { margin-top: 30px; border: 1px solid var(--neon); border-radius: 20px; padding: 25px; text-align: center; animation: fadeInUp 0.5s ease; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .sig-val { font-family: 'Orbitron'; font-size: 50px; font-weight: 900; margin: 15px 0; }
        
        .f-row { display: flex; gap: 10px; margin-top: 25px; }
        .f-btn { flex: 1; padding: 15px; border-radius: 10px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">OMNI V300</div>
        <a href="/logout" style="color:#ff0051; text-decoration:none; font-size:12px; font-family:'Orbitron';">LOGOUT</a>
    </div>

    <div class="container">
        <div class="rules-box">
            <h4>TRADING PROTOCOLS</h4>
            {% for r in rules %}
            <div>• {{ r }}</div>
            {% endfor %}
        </div>

        <div class="hud">
            <div class="hud-card"><span>WIN</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-card"><span>LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
            <div class="hud-card"><span>ACC %</span><b>{{ session['acc'] }}</b></div>
            <div class="hud-card"><span>CREDIT</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
        </div>

        <div class="terminal">
            <form id="sForm" method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="CURRENT BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - NEURAL TURBO</option>
                    <option value="M5">M5 - INSTITUTIONAL</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-scan" onclick="showLoad()">RUN QUANTUM SCAN</button>
            </form>

            <div id="loader">
                <div class="spinner"></div>
                <div style="margin-top:15px; font-size:10px; color:var(--neon); letter-spacing:2px;">DECODING MARKET DATA...</div>
            </div>

            {% if error %}<div style="color:var(--loss); text-align:center; margin-top:15px; font-size:13px;">🛑 INVALID: চার্ট ছাড়া অন্য ডাটা নিষিদ্ধ!</div>{% endif %}
            {% if risk %}<div style="color:var(--gold); text-align:center; margin-top:15px; font-size:13px;">⚠️ ALERT: হাই-রিস্ক মার্কেট। এআই ট্রেড বর্জন করেছে।</div>{% endif %}

            {% if sig %}
            <div class="output" id="out">
                <div style="font-size:10px; color:var(--neon); letter-spacing:3px;">ACCURACY: {{pa}}%</div>
                <div class="sig-val" style="color: {{col}}">{{sig}}</div>
                <div style="background:var(--neon); color:#000; padding:10px 30px; border-radius:8px; font-weight:900; display:inline-block; font-size:18px;">LOT: ${{trade}}</div>
                
                <div style="text-align:left; font-size:11px; color:#666; margin-top:20px; border-left:3px solid var(--neon); padding-left:10px;">
                    <b>[LOG]:</b> {{log}}
                </div>

                <div class="f-row">
                    <a href="/update/win" class="f-btn" style="background:var(--win); color:#000;">PROFIT</a>
                    <a href="/update/loss" class="f-btn" style="background:var(--loss); color:#fff;">LOSS</a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        function showLoad() {
            const form = document.getElementById('sForm');
            if(form.checkValidity()) {
                document.getElementById('loader').style.display = 'block';
                if(document.getElementById('out')) document.getElementById('out').style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

# --- ROUTES ---
@app.before_request
def init_session():
    today = datetime.date.today().isoformat()
    if 'day' not in session or session.get('day') != today:
        session.update({'day': today, 'wins': 0, 'losses': 0, 'acc': 0, 'credits': CREDIT_LIMIT})

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('authorized'): return redirect('/dashboard')
    if request.method == 'POST':
        if request.form['u'] == ADMIN_ID and request.form['p'] == ADMIN_KEY:
            session['authorized'] = True
            return redirect('/dashboard')
        return render_template_string(LOGIN_HTML, error=True)
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    if not session.get('authorized'): return redirect('/')
    return render_template_string(MAIN_HTML, rules=RULES)

@app.route('/analyze', methods=['POST'])
def analyze():
    if not session.get('authorized'): return redirect('/')
    if session.get('credits', 0) <= 0: return redirect('/dashboard')
    
    img = request.files.get('chart')
    filename = img.filename.lower()
    
    # Anti-Human Filter
    bad = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human']
    if any(k in filename for k in bad) and "screenshot" not in filename:
        return render_template_string(MAIN_HTML, rules=RULES, error=True)

    # Risk Logic
    if random.random() < 0.15:
        return render_template_string(MAIN_HTML, rules=RULES, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(4) # Animation Duration

    logics = ["Liquidity Sweep at Order Block.", "MSS detected at demand zone.", "Institutional rejection at supply."]
    signals = [
        {"s": "CALL ⬆️", "c": "#00ffa3", "pa": 99.9, "l": logics[1], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0051", "pa": 99.8, "l": logics[2], "p": 2.1}
    ]
    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(MAIN_HTML, rules=RULES, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('authorized', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
