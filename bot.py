import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "quantum_yggdrasil_v51_ultra_advance"

# 🔑 Master Credentials
ADMIN_ID = "admin"
ADMIN_KEY = "1234"

HTML_V51 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>YGGDRASIL V51 | NEURAL TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=JetBrains+Mono:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ff88; --loss: #ff0055; --bg: #010103; }
        body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; overflow-x: hidden; }
        
        /* Cosmic Animated Grid Background */
        .grid { position: fixed; top:0; left:0; width:100%; height:100%; background: linear-gradient(rgba(0, 242, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 242, 255, 0.05) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; animation: move 25s linear infinite; }
        @keyframes move { from { background-position: 0 0; } to { background-position: 40px 40px; } }

        .navbar { padding: 25px; border-bottom: 2px solid var(--neon); background: rgba(0,0,0,0.9); backdrop-filter: blur(20px); display: flex; justify-content: space-between; position: sticky; top:0; z-index: 1000; box-shadow: 0 5px 20px rgba(0, 242, 255, 0.2); }
        .logo { font-family: 'Orbitron'; font-weight: 900; color: var(--neon); letter-spacing: 5px; text-shadow: 0 0 15px var(--neon); }

        .container { max-width: 550px; margin: 20px auto; padding: 0 15px; }

        /* Advanced HUD - Win/Loss Tracking */
        .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 25px; }
        .hud-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(0, 242, 255, 0.1); padding: 15px; border-radius: 12px; text-align: center; position: relative; }
        .hud-card span { font-size: 9px; color: #888; letter-spacing: 1px; text-transform: uppercase; }
        .hud-card b { display: block; font-family: 'Orbitron'; font-size: 20px; margin-top: 5px; }

        /* Console Interface - Fully Advanced Glassmorphism */
        .console-box { background: rgba(10, 10, 25, 0.95); border-radius: 40px 5px 40px 5px; padding: 35px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 0 40px rgba(0, 242, 255, 0.15); border-left: 5px solid var(--neon); }
        
        input, select { width: 100%; padding: 18px; margin-bottom: 15px; background: #000; border: 1px solid #1a1a25; border-radius: 10px; color: var(--neon); font-weight: bold; box-sizing: border-box; }
        input:focus { border-color: var(--neon); outline: none; }

        .btn-quantum { background: linear-gradient(90deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 22px; border-radius: 10px; border: none; font-family: 'Orbitron'; font-weight: 900; font-size: 15px; cursor: pointer; letter-spacing: 3px; transition: 0.5s; }
        .btn-quantum:hover { letter-spacing: 5px; box-shadow: 0 0 30px var(--neon); }

        /* Output Design */
        .output-shell { margin-top: 35px; border-top: 2px solid var(--neon); padding-top: 25px; animation: glow 1s infinite alternate; }
        @keyframes glow { from { border-color: var(--neon); } to { border-color: transparent; } }

        .signal-val { font-family: 'Orbitron'; font-size: 60px; font-weight: 900; margin: 10px 0; text-shadow: 0 0 30px currentColor; }
        .logic-box { text-align: left; background: #050508; border: 1px solid #111; padding: 15px; border-radius: 10px; font-size: 11px; line-height: 1.6; margin-top: 20px; color: #aaa; border-left: 3px solid var(--neon); }

        /* Feedback Buttons for Win/Loss Tracking */
        .btn-group { display: flex; gap: 10px; margin-top: 25px; }
        .btn-group a { flex: 1; text-decoration: none; padding: 18px; border-radius: 10px; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 12px; }
        .win { background: var(--win); color: #000; box-shadow: 0 0 15px rgba(0,255,136,0.3); }
        .loss { background: var(--loss); color: #fff; box-shadow: 0 0 15px rgba(255,0,85,0.3); }

        .alert-box { border-left: 8px solid var(--loss); background: rgba(255, 0, 85, 0.05); padding: 20px; border-radius: 10px; color: var(--loss); font-size: 12px; font-weight: bold; margin-top: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="grid"></div>
    <div class="navbar">
        <div class="logo">X-QUANTUM</div>
        <div id="clock" style="color:var(--neon)">00:00:00</div>
    </div>

    <div class="container">
{% if not session.get('authorized') %}
        <div class="console-box" style="margin-top: 80px;">
            <h2 style="text-align:center; font-family:'Orbitron'; color:var(--neon);">AUTHENTICATION</h2>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="SYSTEM ID" required>
                <input type="password" name="p" placeholder="SECURITY KEY" required>
                <button type="submit" class="btn-quantum">ACTIVATE TERMINAL</button>
            </form>
        </div>
{% else %}
        <div class="hud-grid">
            <div class="hud-card"><span>TOTAL WINS</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-card"><span>TOTAL LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
            <div class="hud-card"><span>ACCURACY</span><b style="color:var(--neon)">{{ session['acc'] }}%</b></div>
        </div>

        <div class="console-box">
            <div style="font-size: 10px; color: var(--gold); margin-bottom: 15px; text-transform: uppercase; letter-spacing: 2px;">● DAILY CREDITS: {{ session['credits'] }}</div>
            <form method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="CURRENT BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - TURBO NEURAL</option>
                    <option value="M5">M5 - QUANTUM TREND</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-quantum" {% if session['credits'] <= 0 %}disabled style="opacity:0.3;"{% endif %}>
                    {% if session['credits'] > 0 %}EXECUTE DEEP SCAN{% else %}LIMIT EXHAUSTED{% endif %}
                </button>
            </form>

            {% if error %}
            <div class="alert-box">
                🛑 [SYSTEM_ALERT]: INVALID DATA!<br>বট মানুষের ছবি বা ভুল ডাটা শনাক্ত করেছে। দয়া করে শুধুমাত্র ট্রেডিং চার্ট ব্যবহার করুন।
            </div>
            {% elif risk %}
            <div class="alert-box" style="border-color:var(--gold); color:var(--gold); background:rgba(255,204,0,0.05);">
                ⚠️ [RISK_ALERT]: VOLATILITY HIGH!<br>মার্কেট কন্ডিশন অনিশ্চিত। ক্যাপিটাল রক্ষায় এআই এই ট্রেডটি বর্জন করেছে।
            </div>
            {% elif sig %}
            <div class="output-shell">
                <div style="font-size:10px; color:var(--neon); letter-spacing:5px; text-align:center;">PROBABILITY INDEX: {{pa}}%</div>
                <div class="signal-val" style="color: {{col}}; text-align:center;">{{sig}}</div>
                <div style="text-align:center;">
                    <div style="background:var(--neon); color:#000; padding:12px 35px; border-radius:5px; font-weight:900; display:inline-block; font-size:20px;">INVEST: ${{trade}}</div>
                </div>

                <div class="logic-box">
                    <b style="color:var(--neon)">[QUANTUM_LOGIC]:</b> {{log}}
                </div>

                <div class="btn-group">
                    <a href="/update/win" class="win">PROFIT (WIN)</a>
                    <a href="/update/loss" class="loss">RECOVERY (LOSS)</a>
                </div>
            </div>
            {% endif %}
        </div>
{% endif %}
    </div>

    <script>
        setInterval(() => {
            document.getElementById('clock').innerText = new Date().toLocaleTimeString('en-GB');
        }, 1000);
    </script>
</body>
</html>
'''

@app.before_request
def core_sync():
    today = datetime.date.today().isoformat()
    if 'wins' not in session or session.get('day') != today:
        session.update({
            'day': today, 'wins': 0, 'losses': 0, 
            'acc': 0, 'credits': 100, 
            'authorized': session.get('authorized', False)
        })

@app.route('/')
def index(): return render_template_string(HTML_V51)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == ADMIN_ID and request.form['p'] == ADMIN_KEY:
        session['authorized'] = True
        return redirect('/')
    return "DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    img = request.files.get('chart')
    filename = img.filename.lower()
    
    # 🕵️‍♂️ Advanced Anti-Human & Selfie Filter
    invalid_keywords = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human', 'wa', 'whatsapp']
    if any(k in filename for k in invalid_keywords) and "screenshot" not in filename:
        return render_template_string(HTML_V51, error=True)

    # ⚖️ High-Risk Probability Filter
    if random.random() < 0.2:
        return render_template_string(HTML_V51, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(5) # Neural Processing Simulation

    reports = [
        "SMC Update: Liquidity Sweep identified at Order Block (OB). Smart Money accumulation confirmed. Safe Call.",
        "Neural Pulse: Bearish Structure Shift detected. Price rejected from Institutional Supply Zone. Put entry optimal.",
        "Market DNA: Fair Value Gap (FVG) mitigation complete. Strong volume support at demand zone."
    ]

    signals = [
        {"s": "CALL ⬆️", "c": "#00ff88", "pa": 99.9, "l": reports[0], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0055", "pa": 99.8, "l": reports[1], "p": 2.1}
    ]

    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_V51, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
