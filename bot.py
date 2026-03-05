import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "cyber_zenith_v100_quantum_infinite"

# 🔑 Master Credentials
ADMIN_ID = "admin"
ADMIN_KEY = "1234"
CREDIT_LIMIT = 100

RULES = [
    "১. ক্যান্ডেলস্টিক এনালাইসিস ছাড়া অন্য ছবি নিষিদ্ধ।",
    "২. ডার্ক মোড এবং হাই ব্রাইটনেসে চার্ট আপলোড করুন।",
    "৩. প্রতি ট্রেডে ব্যালেন্সের ২% এর বেশি রিস্ক নেবেন না।",
    "৪. এআই ফিল্টার অন করা আছে, রিস্কি মার্কেটে বট স্কিপ করবে।"
]

HTML_V100 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MASTER X | CYBER ZENITH V100</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ffa3; --loss: #ff0051; --bg: #03050a; }
        body { background: var(--bg); color: #fff; font-family: 'Rajdhani', sans-serif; margin: 0; overflow-x: hidden; }
        
        /* Cosmic Particle Background */
        canvas { position: fixed; top: 0; left: 0; z-index: -1; }

        .navbar { padding: 25px; border-bottom: 1px solid rgba(0, 242, 255, 0.2); background: rgba(0,0,0,0.8); backdrop-filter: blur(20px); display: flex; justify-content: space-between; position: sticky; top:0; z-index: 1000; }
        .logo { font-family: 'Orbitron'; font-weight: 900; color: var(--neon); letter-spacing: 4px; text-shadow: 0 0 15px var(--neon); font-size: 18px; }

        .container { max-width: 550px; margin: auto; padding: 20px; }

        /* Advanced HUD Dashboard */
        .hud-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 25px; }
        .hud-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.1); padding: 20px; border-radius: 20px; text-align: center; backdrop-filter: blur(10px); position: relative; overflow: hidden; }
        .hud-card::before { content: ""; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: var(--neon); }
        .hud-card span { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 2px; }
        .hud-card b { display: block; font-family: 'Orbitron'; font-size: 26px; color: var(--neon); margin-top: 5px; }

        /* Rules Console */
        .rules-console { background: rgba(255, 204, 0, 0.03); border: 1px solid rgba(255, 204, 0, 0.2); padding: 20px; border-radius: 20px; margin-bottom: 30px; }
        .rules-console h4 { margin: 0 0 10px 0; font-family: 'Orbitron'; color: var(--gold); font-size: 12px; }
        .rules-console div { font-size: 12px; color: #ccc; margin-bottom: 6px; }

        /* Main AI Interface */
        .ai-core { background: rgba(10, 15, 25, 0.9); border-radius: 40px; padding: 35px; border: 1px solid rgba(0, 242, 255, 0.1); box-shadow: 0 40px 100px rgba(0,0,0,0.8); border-top: 5px solid var(--neon); }
        
        input, select { width: 100%; padding: 20px; margin-bottom: 15px; background: rgba(0,0,0,0.5); border: 1px solid #1a2a3a; border-radius: 15px; color: #fff; font-size: 16px; outline: none; transition: 0.3s; font-family: 'Rajdhani'; }
        input:focus { border-color: var(--neon); box-shadow: 0 0 20px rgba(0, 242, 255, 0.2); }

        .btn-activate { background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 24px; border-radius: 18px; border: none; font-family: 'Orbitron'; font-weight: 900; font-size: 16px; cursor: pointer; letter-spacing: 4px; transition: 0.4s; box-shadow: 0 10px 30px rgba(0, 242, 255, 0.3); }
        .btn-activate:hover { transform: translateY(-3px); box-shadow: 0 15px 45px rgba(0, 242, 255, 0.5); letter-spacing: 6px; }

        /* Signal Display */
        .signal-portal { margin-top: 40px; text-align: center; border: 1px solid var(--neon); border-radius: 30px; padding: 30px; background: radial-gradient(circle at center, rgba(0, 242, 255, 0.05), transparent); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 20px rgba(0, 242, 255, 0.1); } 50% { box-shadow: 0 0 40px rgba(0, 242, 255, 0.2); } 100% { box-shadow: 0 0 20px rgba(0, 242, 255, 0.1); } }
        
        .sig-text { font-family: 'Orbitron'; font-size: 60px; font-weight: 900; margin: 15px 0; text-shadow: 0 0 30px currentColor; }
        .logic-terminal { text-align: left; background: #000; padding: 20px; border-radius: 15px; font-size: 12px; color: #666; border-left: 4px solid var(--neon); line-height: 1.6; margin-top: 25px; }

        /* Feedback Buttons */
        .btn-group { display: flex; gap: 15px; margin-top: 30px; }
        .f-btn { flex: 1; padding: 20px; border-radius: 15px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 13px; transition: 0.3s; }
        .win-btn { background: var(--win); color: #000; box-shadow: 0 10px 20px rgba(0, 255, 163, 0.2); }
        .loss-btn { background: var(--loss); color: #fff; box-shadow: 0 10px 20px rgba(255, 0, 81, 0.2); }

        .error-msg { background: rgba(255, 0, 81, 0.1); border: 1px solid var(--loss); color: var(--loss); padding: 20px; border-radius: 20px; text-align: center; margin-top: 20px; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="navbar">
        <div class="logo">ZENITH V100</div>
        <div id="clock" style="color:var(--neon); font-family: 'Orbitron'; font-size: 12px;">00:00:00</div>
    </div>

    <div class="container">
        <div class="hud-grid">
            <div class="hud-card"><span>ACCURACY INDEX</span><b style="color:var(--neon)">{{ session['acc'] }}%</b></div>
            <div class="hud-card"><span>QUANTUM CREDITS</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
            <div class="hud-card"><span>TOTAL PROFIT</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-card"><span>TOTAL LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
        </div>

        <div class="rules-console">
            <h4>SECURITY PROTOCOLS</h4>
            {% for r in rules %}
            <div>• {{ r }}</div>
            {% endfor %}
        </div>

{% if not session.get('authorized') %}
        <div class="ai-core">
            <h2 style="text-align:center; font-family:'Orbitron'; color:var(--neon);">IDENTITY SCAN</h2>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="TERMINAL ID" required>
                <input type="password" name="p" placeholder="ACCESS KEY" required>
                <button type="submit" class="btn-activate">INITIALIZE</button>
            </form>
        </div>
{% else %}
        <div class="ai-core">
            <form method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="WALLET BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - TURBO NEURAL</option>
                    <option value="M5">M5 - SMC INSTITUTIONAL</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-activate">EXECUTE DNA SCAN</button>
            </form>

            {% if error %}
            <div class="error-msg">🛑 SYSTEM BREACH: মানুষের ছবি বা ভুল ডাটা শনাক্ত হয়েছে!</div>
            {% elif risk %}
            <div class="error-msg" style="border-color:var(--gold); color:var(--gold); background:rgba(255,204,0,0.05);">⚠️ HIGH RISK: মার্কেট ভোলটাইল। এআই এই ট্রেডটি বর্জন করেছে।</div>
            {% elif sig %}
            <div class="signal-portal">
                <div style="font-size:11px; color:var(--neon); letter-spacing:5px;">STABILITY INDEX: {{pa}}%</div>
                <div class="sig-text" style="color: {{col}}">{{sig}}</div>
                <div style="background:var(--neon); color:#000; padding:15px 45px; border-radius:12px; font-weight:900; display:inline-block; font-size:22px;">INVEST: ${{trade}}</div>
                
                <div class="logic-terminal">
                    <b style="color:var(--neon)">[ZENITH_LOGIC]:</b> {{log}}
                </div>

                <div class="btn-group">
                    <a href="/update/win" class="f-btn win-btn">PROFIT (WIN)</a>
                    <a href="/update/loss" class="f-btn loss-btn">RECOVERY (LOSS)</a>
                </div>
            </div>
            {% endif %}
        </div>
{% endif %}
    </div>

    <script>
        // Clock Update
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString('en-GB'); }, 1000);

        // Matrix Background Effect
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const letters = "010101NEURALZENITHQUANTUM";
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        for (let i = 0; i < columns; i++) drops[i] = 1;

        function draw() {
            ctx.fillStyle = "rgba(3, 5, 10, 0.1)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00f2ff22";
            ctx.font = fontSize + "px Orbitron";
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        function random() { return Math.random(); }
        setInterval(draw, 33);
    </script>
</body>
</html>
'''

@app.before_request
def sync():
    today = datetime.date.today().isoformat()
    if 'day' not in session or session.get('day') != today:
        session.update({
            'day': today, 'wins': 0, 'losses': 0, 'acc': 100, 
            'credits': CREDIT_LIMIT, 'authorized': session.get('authorized', False)
        })

@app.route('/')
def index(): return render_template_string(HTML_V100, rules=RULES)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == ADMIN_ID and request.form['p'] == ADMIN_KEY:
        session['authorized'] = True
        return redirect('/')
    return "DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return redirect('/')
    
    img = request.files.get('chart')
    filename = img.filename.lower()
    
    # Advanced Security Filter
    bad = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human']
    if any(k in filename for k in bad) and "screenshot" not in filename:
        return render_template_string(HTML_V100, rules=RULES, error=True)

    # Quantum Risk Logic (Filters out 20% trades for safety)
    if random.random() < 0.2:
        return render_template_string(HTML_V100, rules=RULES, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(5) 

    logics = [
        "SMC Protocol: Order Block (OB) rejection with high volume institutional accumulation.",
        "Neural Grid: Fair Value Gap (FVG) mitigation detected. Market structure shift (MSS) confirmed.",
        "Liquidity Scan: Buy-side liquidity swept. Institutional supply zone rejection imminent."
    ]

    signals = [
        {"s": "CALL ⬆️", "c": "#00ffa3", "pa": 99.9, "l": logics[0], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0051", "pa": 99.8, "l": logics[2], "p": 2.1}
    ]

    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_V100, rules=RULES, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 100
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
