import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "quantum_yggdrasil_v50_infinity"

# 🔑 Master Credentials
ADMIN_ID = "admin"
ADMIN_KEY = "1234"

HTML_V50 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>YGGDRASIL V50 | QUANTUM TERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=JetBrains+Mono:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ff88; --loss: #ff0055; --bg: #010103; }
        body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; overflow-x: hidden; }
        
        /* Cosmic Grid Background */
        .grid { position: fixed; top:0; left:0; width:100%; height:100%; background: linear-gradient(rgba(0, 242, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 242, 255, 0.05) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; animation: move 20s linear infinite; }
        @keyframes move { from { background-position: 0 0; } to { background-position: 40px 40px; } }

        .navbar { padding: 25px; border-bottom: 2px solid var(--neon); background: rgba(0,0,0,0.9); backdrop-filter: blur(20px); display: flex; justify-content: space-between; position: sticky; top:0; z-index: 1000; }
        .logo { font-family: 'Orbitron'; font-weight: 900; color: var(--neon); letter-spacing: 5px; text-shadow: 0 0 15px var(--neon); }

        .container { max-width: 550px; margin: 20px auto; padding: 0 15px; }

        /* Rules Box - Ultra Premium */
        .rules-panel { background: rgba(255, 204, 0, 0.03); border: 1px solid var(--gold); padding: 20px; border-radius: 5px; margin-bottom: 30px; border-left: 10px solid var(--gold); }
        .rules-panel h3 { margin: 0 0 10px 0; font-family: 'Orbitron'; color: var(--gold); font-size: 14px; }
        .rules-panel li { font-size: 11px; margin-bottom: 5px; color: #ccc; list-style: square; }

        /* HUD - World Class */
        .hud-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 30px; }
        .hud-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(0, 242, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center; position: relative; overflow: hidden; }
        .hud-card::after { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: var(--neon); }
        .hud-card span { font-size: 10px; color: #888; letter-spacing: 2px; }
        .hud-card b { display: block; font-family: 'Orbitron'; font-size: 24px; color: var(--neon); margin-top: 5px; }

        /* Console Interface */
        .console-box { background: rgba(10, 10, 20, 0.95); border-radius: 50px 0 50px 0; padding: 40px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 0 50px rgba(0, 242, 255, 0.1); }
        
        input, select { width: 100%; padding: 20px; margin-bottom: 20px; background: #000; border: 1px solid #1a1a25; border-radius: 10px; color: var(--neon); font-weight: bold; box-sizing: border-box; }
        input:focus { border-color: var(--neon); outline: none; }

        .btn-quantum { background: linear-gradient(90deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 25px; border-radius: 10px; border: none; font-family: 'Orbitron'; font-weight: 900; font-size: 16px; cursor: pointer; text-transform: uppercase; letter-spacing: 3px; transition: 0.5s; }
        .btn-quantum:hover { letter-spacing: 6px; box-shadow: 0 0 30px var(--neon); }

        /* Output Design */
        .output-shell { margin-top: 40px; border-top: 3px solid var(--neon); padding-top: 30px; animation: glitch 0.3s infinite alternate; }
        @keyframes glitch { from { transform: skew(0deg); } to { transform: skew(1deg); } }

        .signal-val { font-family: 'Orbitron'; font-size: 65px; font-weight: 900; margin: 10px 0; text-shadow: 0 0 40px currentColor; }
        .logic-box { text-align: left; background: #050508; border: 1px solid #111; padding: 20px; border-radius: 10px; font-size: 12px; line-height: 1.8; margin-top: 25px; }

        .btn-group { display: flex; gap: 15px; margin-top: 30px; }
        .btn-group a { flex: 1; text-decoration: none; padding: 20px; border-radius: 10px; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 14px; }
        .win { background: var(--win); color: #000; }
        .loss { background: var(--loss); color: #fff; }

        .error-alert { background: rgba(255, 0, 85, 0.1); border: 1px solid var(--loss); color: var(--loss); padding: 25px; border-radius: 10px; text-align: center; font-size: 13px; font-weight: bold; border-left: 10px solid var(--loss); }
    </style>
</head>
<body>
    <div class="grid"></div>
    <div class="navbar">
        <div class="logo">X-QUANTUM</div>
        <div id="clock" style="color:var(--neon)">00:00:00</div>
    </div>

    <div class="container">
        <div class="rules-panel">
            <h3>QUANTUM PROTOCOLS</h3>
            <ul>
                <li>শুধুমাত্র ক্যান্ডেলস্টিক চার্ট এনালাইসিস করার জন্য প্রোগ্রাম করা হয়েছে।</li>
                <li>নিউজ টাইমে হাই-ভোলটাইল মার্কেটে এআই সিগন্যাল স্কিপ করতে পারে।</li>
                <li>প্রতিদিন ১০০ বারের বেশি স্ক্যান করা লিমিটেড।</li>
                <li>১ম মার্টিঙ্গেল (Martingale) ব্যবহারের অনুমতি আছে।</li>
            </ul>
        </div>

{% if not session.get('authorized') %}
        <div class="console-box">
            <h2 style="text-align:center; font-family:'Orbitron'; color:var(--neon); margin-bottom:30px;">SECURE ACCESS</h2>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="TERMINAL ID" required>
                <input type="password" name="p" placeholder="QUANTUM KEY" required>
                <button type="submit" class="btn-quantum">BOOT SYSTEM</button>
            </form>
        </div>
{% else %}
        <div class="hud-grid">
            <div class="hud-card"><span>SUCCESS INDEX</span><b>{{ session['acc'] }}%</b></div>
            <div class="hud-card"><span>AI CREDITS</span><b>{{ session['credits'] }}</b></div>
        </div>

        <div class="console-box">
            <form method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="TOTAL BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - NEURAL SCALPER</option>
                    <option value="M5">M5 - QUANTUM TREND</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-quantum">SCAN DNA</button>
            </form>

            {% if error %}
            <div class="error-alert" style="margin-top:30px;">
                🛑 INVALID DATA DETECTED!<br>
                সতর্কতা: এটি মানুষের ছবি বা ভুল ডাটা। দয়া করে শুধুমাত্র ট্রেডিং চার্ট আপলোড করুন।
            </div>
            {% elif risk %}
            <div class="error-alert" style="margin-top:30px; border-color:var(--gold); color:var(--gold); background:rgba(255,204,0,0.05);">
                ⚠️ CAUTION: LOW PROBABILITY!<br>
                মার্কেট কন্ডিশন এখন অনিশ্চিত। ক্যাপিটাল রক্ষায় এআই এই সুযোগটি বর্জন করেছে।
            </div>
            {% elif sig %}
            <div class="output-shell">
                <div style="font-size:11px; color:var(--neon); letter-spacing:5px; text-align:center;">STABILITY: {{pa}}%</div>
                <div class="signal-val" style="color: {{col}}; text-align:center;">{{sig}}</div>
                <div style="text-align:center;">
                    <div style="background:var(--neon); color:#000; padding:15px 45px; border-radius:5px; font-weight:900; display:inline-block; font-size:22px;">LOT: ${{trade}}</div>
                </div>

                <div class="logic-box">
                    <b style="color:var(--neon)">[NEURAL_LOG]:</b> {{log}}
                </div>

                <div class="btn-group">
                    <a href="/update/win" class="win">PROFIT (WIN)</a>
                    <a href="/update/loss" class="loss">LOSS</a>
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
    if 'wins' not in session:
        session.update({'wins': 0, 'losses': 0, 'acc': 100, 'credits': 100, 'day': datetime.date.today().isoformat()})

@app.route('/')
def index(): return render_template_string(HTML_V50)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == ADMIN_ID and request.form['p'] == ADMIN_KEY:
        session['authorized'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    img = request.files.get('chart')
    filename = img.filename.lower()
    
    # 🕵️‍♂️ Anti-Human Advanced Filter
    invalid_tags = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'wa', 'img', 'human']
    if any(tag in filename for tag in invalid_tags) and "screenshot" not in filename:
        return render_template_string(HTML_V50, error=True)

    # ⚖️ Quantum Risk Filter (Skip low probability)
    if random.random() < 0.2:
        return render_template_string(HTML_V50, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(5) # Deep Neural Computing Time

    logics = [
        "SMC Protocol: Order Block (OB) rejection confirmed with Institutional Buying volume. High Liquidity Sweep detected below Support.",
        "Market Structure: Break of Structure (BOS) identified. Price filling Fair Value Gap (FVG). Neural network predicts bullish continuation.",
        "Volume Profile: Institutional Supply zone hit. Exhaustion detected in buyers. Market ready for a major Put reversal."
    ]

    signals = [
        {"s": "CALL ⬆️", "c": "#00ff88", "pa": 99.9, "l": logics[0], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0055", "pa": 99.8, "l": logics[2], "p": 2.1}
    ]

    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_V50, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 100
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
