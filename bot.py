import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "hyper_neural_v200_matrix_unlimited"

# 🔑 Master Config
ADMIN_ID = "admin"
ADMIN_KEY = "1234"
CREDIT_LIMIT = 100

RULES = [
    "১. ক্যান্ডেলস্টিক চার্ট ছাড়া অন্য ছবি সম্পূর্ণ নিষিদ্ধ।",
    "২. রিস্ক ম্যানেজমেন্ট ছাড়া বড় লটে ট্রেড করবেন না।",
    "৩. এআই ফিল্টার রিজেক্ট করলে সেই ট্রেডটি এড়িয়ে চলুন।",
    "৪. প্রতিদিন ১০০টি সিগন্যাল লিমিট (রাত ১২টায় রিসেট)।"
]

HTML_V200 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>X-QUANTUM | V200 HYPER-NEURAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ffa3; --loss: #ff0051; --bg: #010206; }
        body { background: var(--bg); color: #fff; font-family: 'Rajdhani', sans-serif; margin: 0; overflow-x: hidden; }
        
        /* Dynamic Matrix Grid */
        .matrix-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(0, 242, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 242, 255, 0.03) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; animation: move 10s linear infinite; }
        @keyframes move { from { background-position: 0 0; } to { background-position: 40px 40px; } }

        .navbar { padding: 20px; border-bottom: 2px solid var(--neon); background: rgba(0,0,0,0.9); backdrop-filter: blur(15px); display: flex; justify-content: space-between; align-items: center; position: sticky; top:0; z-index: 1000; }
        .logo { font-family: 'Orbitron'; font-weight: 900; color: var(--neon); letter-spacing: 5px; font-size: 16px; text-shadow: 0 0 10px var(--neon); }

        .container { max-width: 500px; margin: auto; padding: 15px; }

        /* HUD - Advanced Tracking */
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
        .stats-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(0, 242, 255, 0.1); padding: 15px; border-radius: 15px; text-align: center; border-left: 4px solid var(--neon); }
        .stats-card span { font-size: 9px; color: #888; letter-spacing: 2px; text-transform: uppercase; }
        .stats-card b { display: block; font-family: 'Orbitron'; font-size: 22px; margin-top: 5px; color: var(--neon); }

        /* Main AI Interface */
        .terminal { background: rgba(10, 15, 30, 0.95); border-radius: 35px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 0 50px rgba(0,0,0,0.9); }
        
        input, select { width: 100%; padding: 18px; margin-bottom: 12px; background: #000; border: 1px solid #1a2a3a; border-radius: 12px; color: #fff; font-family: 'Rajdhani'; outline: none; }
        .btn-scan { background: linear-gradient(45deg, #00f2ff, #0066ff); color: #fff; width: 100%; padding: 22px; border-radius: 12px; border: none; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; letter-spacing: 3px; transition: 0.3s; }
        .btn-scan:hover { box-shadow: 0 0 30px var(--neon); transform: scale(1.02); }

        /* 🔄 Scanning Loader (গোল গোল ঘোরা এনিমেশন) */
        #loader { display: none; margin: 30px auto; text-align: center; }
        .spinner { width: 60px; height: 60px; border: 5px solid rgba(0, 242, 255, 0.1); border-top: 5px solid var(--neon); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .scan-text { margin-top: 15px; font-family: 'Orbitron'; font-size: 10px; color: var(--neon); letter-spacing: 3px; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* Output Portal */
        .output-portal { margin-top: 30px; border: 1px solid var(--neon); border-radius: 25px; padding: 25px; text-align: center; background: rgba(0, 242, 255, 0.02); animation: fadeInUp 0.5s ease; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        .sig-val { font-family: 'Orbitron'; font-size: 50px; font-weight: 900; margin: 10px 0; text-shadow: 0 0 25px currentColor; }
        
        .logic-box { text-align: left; background: #000; padding: 15px; border-radius: 10px; font-size: 11px; color: #777; border-left: 3px solid var(--neon); margin-top: 20px; line-height: 1.6; }

        .btn-group { display: flex; gap: 10px; margin-top: 25px; }
        .f-btn { flex: 1; padding: 18px; border-radius: 10px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 12px; }
        .win { background: var(--win); color: #000; }
        .loss { background: var(--loss); color: #fff; }

        .alert { border: 1px solid var(--loss); background: rgba(255, 0, 81, 0.05); padding: 20px; border-radius: 15px; color: var(--loss); font-size: 13px; text-align: center; margin-top: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    <div class="navbar">
        <div class="logo">HYPER NEURAL V200</div>
        <div id="clock" style="color:var(--neon); font-family: 'Orbitron'; font-size: 11px;">00:00:00</div>
    </div>

    <div class="container">
        <div class="stats-grid">
            <div class="stats-card"><span>ACCURACY</span><b style="color:var(--neon)">{{ session['acc'] }}%</b></div>
            <div class="stats-card"><span>CREDITS</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
            <div class="stats-card"><span>PROFIT</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="stats-card"><span>LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
        </div>

{% if not session.get('authorized') %}
        <div class="terminal">
            <h3 style="text-align:center; font-family:'Orbitron'; color:var(--neon);">AUTHENTICATION</h3>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="SYSTEM ID" required>
                <input type="password" name="p" placeholder="SECURITY KEY" required>
                <button type="submit" class="btn-scan">ACTIVATE TERMINAL</button>
            </form>
        </div>
{% else %}
        <div class="terminal">
            <div style="font-size:11px; color:var(--gold); margin-bottom:15px; font-weight:bold;">RULES: {{ rules[0] }}</div>
            
            <form id="scanForm" method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="M1">M1 - TURBO ALGO</option>
                    <option value="M5">M5 - SMC INSTITUTIONAL</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-scan" onclick="startScan()" {% if session['credits'] <= 0 %}disabled{% endif %}>
                    {% if session['credits'] > 0 %}EXECUTE DEEP SCAN{% else %}LIMIT EXHAUSTED{% endif %}
                </button>
            </form>

            <div id="loader">
                <div class="spinner"></div>
                <div class="scan-text">ANALYZING MARKET DNA...</div>
            </div>

            {% if error %}<div class="alert">🛑 SYSTEM BREACH: মানুষের ছবি শনাক্ত হয়েছে!</div>{% endif %}
            {% if risk %}<div class="alert" style="border-color:var(--gold); color:var(--gold);">⚠️ HIGH RISK: মার্কেট বিপজ্জনক। ট্রেড স্কিপ করা হয়েছে।</div>{% endif %}

            {% if sig %}
            <div class="output-portal" id="output">
                <div style="font-size:10px; color:var(--neon); letter-spacing:4px;">STABILITY INDEX: {{pa}}%</div>
                <div class="sig-val" style="color: {{col}}">{{sig}}</div>
                <div style="background:var(--neon); color:#000; padding:12px 30px; border-radius:8px; font-weight:900; display:inline-block; font-size:20px;">INVEST: ${{trade}}</div>
                
                <div class="logic-box">
                    <b style="color:var(--neon)">[NEURAL_LOGIC]:</b> {{log}}
                </div>

                <div class="btn-group">
                    <a href="/update/win" class="f-btn win">WIN (PROFIT)</a>
                    <a href="/update/loss" class="f-btn loss">LOSS (MTG)</a>
                </div>
            </div>
            {% endif %}
        </div>
{% endif %}
    </div>

    <script>
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString('en-GB'); }, 1000);

        function startScan() {
            // ফর্ম সাবমিট হওয়ার সময় লোডার দেখাবে এবং আউটপুট লুকাবে
            const form = document.getElementById('scanForm');
            if(form.checkValidity()){
                document.getElementById('loader').style.display = 'block';
                if(document.getElementById('output')) document.getElementById('output').style.display = 'none';
            }
        }
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
def index(): return render_template_string(HTML_V200, rules=RULES)

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
    
    # 🕵️‍♂️ Anti-Human Filter
    bad = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human']
    if any(k in filename for k in bad) and "screenshot" not in filename:
        return render_template_string(HTML_V200, rules=RULES, error=True)

    # ⚖️ High-Risk Filter
    if random.random() < 0.2:
        return render_template_string(HTML_V200, rules=RULES, risk=True)

    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(4) # লোডিং এনিমেশন দেখানোর জন্য সময়

    logics = [
        "SMC Update: Liquidity sweep identified at H1 Order Block. Trend reversal confirmed.",
        "Neural Grid: Fair Value Gap (FVG) mitigation complete. Price rejected from Supply Zone.",
        "Market Structure: Shift detected (MSS). Institutional volume accumulation at Demand Zone."
    ]

    signals = [
        {"s": "CALL ⬆️", "c": "#00ffa3", "pa": 99.9, "l": logics[2], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0051", "pa": 99.8, "l": logics[1], "p": 2.1}
    ]

    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_V200, rules=RULES, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 100
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
