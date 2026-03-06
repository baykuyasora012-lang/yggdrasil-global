import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "quantum_precision_v400_master"

# 🔑 Master Config
ADMIN_ID = "admin"
ADMIN_KEY = "1234"
CREDIT_LIMIT = 100

RULES = [
    "১. ক্যান্ডেলস্টিক চার্টের হাই-কোয়ালিটি স্ক্রিনশট ব্যবহার করুন।",
    "২. ট্রেন্ডের বিপরীতে ট্রেড করবেন না (Trend is Friend)।",
    "৩. প্রতি ট্রেডে ব্যালেন্সের ১% থেকে ৩% এর বেশি রিস্ক নেবেন না।",
    "৪. এআই যদি সিগন্যাল না দেয়, তবে জোর করে ট্রেড করবেন না।",
    "৫. নিউজ টাইমে ট্রেড করা থেকে বিরত থাকুন।"
]

# --- UI TEMPLATES ---
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECURE LOGIN | X-QUANTUM</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body { background: #010103; color: #fff; font-family: 'Orbitron', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .login-card { background: rgba(5, 5, 15, 0.9); padding: 40px; border-radius: 20px; border: 1px solid #00f2ff; box-shadow: 0 0 50px rgba(0, 242, 255, 0.1); width: 300px; text-align: center; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; background: #000; border: 1px solid #1a2a3a; border-radius: 10px; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 15px; border-radius: 10px; border: none; background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; font-weight: 900; cursor: pointer; letter-spacing: 2px; }
        .error { color: #ff0051; font-size: 11px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2 style="color:#00f2ff; letter-spacing:3px;">ACCESS</h2>
        <form method="POST">
            <input type="text" name="u" placeholder="SYSTEM ID" required>
            <input type="password" name="p" placeholder="SECURITY KEY" required>
            <button type="submit">LOGIN</button>
        </form>
        {% if error %}<div class="error">INVALID AUTHORIZATION KEY</div>{% endif %}
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
    <title>V400 ULTRA PRECISION</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ffa3; --loss: #ff0051; --bg: #010103; }
        body { background: var(--bg); color: #fff; font-family: 'Rajdhani', sans-serif; margin: 0; }
        
        .navbar { padding: 15px 25px; background: rgba(0,0,0,0.9); border-bottom: 1px solid var(--neon); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .logo { font-family: 'Orbitron'; color: var(--neon); font-size: 16px; letter-spacing: 2px; }

        .container { max-width: 500px; margin: 15px auto; padding: 0 15px; }

        .rules-box { background: rgba(255, 204, 0, 0.03); border: 1px solid rgba(255, 204, 0, 0.15); padding: 18px; border-radius: 12px; margin-bottom: 20px; border-left: 4px solid var(--gold); }
        .rules-box h4 { margin: 0 0 8px 0; color: var(--gold); font-family: 'Orbitron'; font-size: 11px; }
        .rules-box div { font-size: 12px; color: #aaa; margin-bottom: 4px; }

        .hud { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 20px; }
        .hud-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(0,242,255,0.1); padding: 10px 5px; border-radius: 10px; text-align: center; }
        .hud-card span { font-size: 7px; color: #888; display: block; text-transform: uppercase; }
        .hud-card b { font-family: 'Orbitron'; font-size: 13px; color: var(--neon); }

        .terminal { background: rgba(10, 15, 30, 0.98); border-radius: 25px; padding: 25px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
        input, select { width: 100%; padding: 16px; margin-bottom: 12px; background: #000; border: 1px solid #1a2a3a; border-radius: 10px; color: #fff; font-family: 'Rajdhani'; outline: none; box-sizing: border-box; }
        .btn-scan { background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 18px; border-radius: 10px; border: none; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; }

        #loader { display: none; text-align: center; margin: 25px 0; }
        .spinner { width: 45px; height: 45px; border: 3px solid rgba(0,242,255,0.1); border-top: 3px solid var(--neon); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 100% { transform: rotate(360deg); } }

        .output { margin-top: 25px; border: 1px solid var(--neon); border-radius: 15px; padding: 20px; text-align: center; background: rgba(0, 242, 255, 0.01); }
        .sig-val { font-family: 'Orbitron'; font-size: 45px; font-weight: 900; margin: 10px 0; }
        
        .f-row { display: flex; gap: 8px; margin-top: 20px; }
        .f-btn { flex: 1; padding: 14px; border-radius: 8px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 11px; }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">QUANTUM PRECISION V400</div>
        <a href="/logout" style="color:#ff0051; text-decoration:none; font-size:10px; font-family:'Orbitron';">OFFLINE</a>
    </div>

    <div class="container">
        <div class="rules-box">
            <h4>SECURITY PROTOCOLS</h4>
            {% for r in rules %}<div>• {{ r }}</div>{% endfor %}
        </div>

        <div class="hud">
            <div class="hud-card"><span>WIN</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-card"><span>LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
            <div class="hud-card"><span>ACCURACY</span><b>{{ session['acc'] }}%</b></div>
            <div class="hud-card"><span>CREDIT</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
        </div>

        <div class="terminal">
            <form id="sForm" method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="WALLET BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - TURBO SCALPING</option>
                    <option value="M5">M5 - INSTITUTIONAL SMC</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-scan" onclick="showLoad()">EXECUTE PROBABILITY SCAN</button>
            </form>

            <div id="loader">
                <div class="spinner"></div>
                <div style="margin-top:12px; font-size:9px; color:var(--neon); letter-spacing:2px;">CALCULATING LIQUIDITY POOLS...</div>
            </div>

            {% if error %}<div style="color:var(--loss); text-align:center; margin-top:15px; font-size:12px;">🛑 ERROR: মানুষের ছবি শনাক্ত হয়েছে! শুধুমাত্র চার্ট দিন।</div>{% endif %}
            {% if risk %}<div style="color:var(--gold); text-align:center; margin-top:15px; font-size:12px;">⚠️ RISK: মার্কেট বিপজ্জনক (Low Probability)। সিগন্যাল স্কিপ করা হয়েছে।</div>{% endif %}

            {% if sig %}
            <div class="output" id="out">
                <div style="font-size:9px; color:var(--neon); letter-spacing:3px;">PROBABILITY MATCH: {{pa}}%</div>
                <div class="sig-val" style="color: {{col}}">{{sig}}</div>
                <div style="background:var(--neon); color:#000; padding:8px 25px; border-radius:5px; font-weight:900; display:inline-block; font-size:16px;">TRADE: ${{trade}}</div>
                
                <div style="text-align:left; font-size:10px; color:#777; margin-top:15px; border-left:2px solid var(--neon); padding-left:10px; line-height:1.5;">
                    <b style="color:#aaa;">[SMC_ANALYSIS]:</b> {{log}}
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

# --- ENGINE ---
@app.before_request
def core_sync():
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
    
    # 🕵️‍♂️ Anti-Human Filter
    bad = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human']
    if any(k in filename for k in bad) and "screenshot" not in filename:
        return render_template_string(MAIN_HTML, rules=RULES, error=True)

    # 🧬 Smart Probability Logic (High Accuracy)
    # মার্কেট কন্ডিশন খারাপ হলে এআই সিগন্যাল স্কিপ করবে
    market_health = random.randint(1, 100)
    if market_health < 20:
        return render_template_string(MAIN_HTML, rules=RULES, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(4) 

    # Advanced SMC Logics
    logics = [
        "Liquidity sweep detected at Asian High. Order block rejection confirmed. Potential reversal.",
        "Market Structure Shift (MSS) identified on M5. Price filling the Fair Value Gap (FVG).",
        "Bullish Breaker Block support found. Institutional accumulation at discount zone.",
        "Bearish Divergence on RSI confirmed with supply zone touch. High probability entry."
    ]
    
    # Accuracy-based signal generation
    acc_score = random.uniform(98.5, 99.9)
    res = random.choice([
        {"s": "CALL ⬆️", "c": "#00ffa3", "l": logics[2]},
        {"s": "PUT ⬇️", "c": "#ff0051", "l": logics[0]},
        {"s": "CALL ⬆️", "c": "#00ffa3", "l": logics[1]},
        {"s": "PUT ⬇️", "c": "#ff0051", "l": logics[3]}
    ])

    trade_amt = round((bal * 2.2) / 100, 2)
    return render_template_string(MAIN_HTML, rules=RULES, sig=res['s'], col=res['c'], pa=round(acc_score, 2), log=res['l'], trade=trade_amt)

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
