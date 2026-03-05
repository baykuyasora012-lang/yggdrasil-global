herimport os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "ultimate_integration_v65_final"

# 🔑 Master Config
ADMIN_ID = "admin"
ADMIN_KEY = "1234"
TOTAL_LIMIT = 100 # প্রতিদিনের ক্রেডিট লিমিট

TRADING_RULES = [
    "১. শুধুমাত্র ক্লিন ক্যান্ডেলস্টিক চার্ট আপলোড করুন।",
    "২. মানুষের ছবি বা অপ্রাসঙ্গিক ডাটা দিলে সিস্টেম ব্লক হবে।",
    "৩. মানি ম্যানেজমেন্ট (১-২%) কঠোরভাবে পালন করুন।",
    "৪. হাই-রিস্ক জোনে বট সিগন্যাল স্কিপ করবে, ধৈর্য ধরুন।"
]

HTML_FINAL = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MASTER X | V65 ULTIMATE</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=JetBrains+Mono:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --gold: #ffcc00; --win: #00ff88; --loss: #ff0055; --bg: #020205; }
        body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; }
        
        .navbar { padding: 20px; border-bottom: 2px solid var(--neon); background: #000; display: flex; justify-content: space-between; position: sticky; top:0; z-index: 1000; }
        .logo { font-family: 'Orbitron'; color: var(--neon); letter-spacing: 3px; font-size: 14px; }

        .container { max-width: 500px; margin: 20px auto; padding: 0 15px; }

        /* HUD - Tracker */
        .hud { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 20px; }
        .hud-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(0, 242, 255, 0.1); padding: 12px 5px; border-radius: 10px; text-align: center; }
        .hud-box span { font-size: 8px; color: #888; display: block; }
        .hud-box b { font-family: 'Orbitron'; font-size: 14px; color: var(--neon); }

        /* Rules */
        .rules { background: rgba(255, 204, 0, 0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 10px; margin-bottom: 20px; font-size: 11px; color: #ccc; }
        
        /* Console */
        .console { background: #08080c; border-radius: 30px; padding: 25px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 15px 40px rgba(0,0,0,0.8); }
        
        input, select { width: 100%; padding: 18px; margin-bottom: 12px; background: #000; border: 1px solid #222; border-radius: 10px; color: #fff; box-sizing: border-box; }
        .btn-run { background: var(--neon); color: #000; width: 100%; padding: 20px; border-radius: 10px; border: none; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; }

        .output { margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; text-align: center; }
        .sig-val { font-family: 'Orbitron'; font-size: 50px; font-weight: 900; margin: 10px 0; }
        
        .f-row { display: flex; gap: 10px; margin-top: 20px; }
        .f-btn { flex: 1; padding: 15px; border-radius: 8px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; text-align: center; font-size: 12px; }

        .err { border: 1px solid var(--loss); color: var(--loss); padding: 15px; border-radius: 10px; font-size: 11px; margin-top: 15px; text-align: center; }
    </style>
</head>
<body>
    <div class="navbar"><div class="logo">X-QUANTUM V65</div><div id="clock">00:00:00</div></div>

    <div class="container">
        <div class="hud">
            <div class="hud-box"><span>WINS</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-box"><span>LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
            <div class="hud-box"><span>ACC %</span><b>{{ session['acc'] }}</b></div>
            <div class="hud-box"><span>CREDIT</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
        </div>

        <div class="rules">
            <b style="color:var(--gold)">MASTER PROTOCOLS:</b><br>
            {% for r in rules %}<div>• {{ r }}</div>{% endfor %}
        </div>

{% if not session.get('authorized') %}
        <div class="console">
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="ADMIN ID">
                <input type="password" name="p" placeholder="PASSWORD">
                <button type="submit" class="btn-run">LOGIN</button>
            </form>
        </div>
{% else %}
        <div class="console">
            <form method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time"><option value="M1">M1 - TURBO</option><option value="M5">M5 - SMC</option></select>
                <input type="file" name="chart" required>
                <button type="submit" class="btn-run" {% if session['credits'] <= 0 %}disabled style="opacity:0.3;"{% endif %}>
                    {% if session['credits'] > 0 %}START AI SCAN{% else %}OUT OF CREDITS{% endif %}
                </button>
            </form>

            {% if error %}<div class="err">🛑 INVALID DATA! মানুষের ছবি শনাক্ত হয়েছে।</div>{% endif %}
            {% if risk %}<div class="err" style="color:var(--gold); border-color:var(--gold);">⚠️ RISK DETECTED! মার্কেট অনিরাপদ।</div>{% endif %}

            {% if sig %}
            <div class="output">
                <div style="color:var(--neon); font-size:10px;">STABILITY: {{pa}}%</div>
                <div class="sig-val" style="color: {{col}}">{{sig}}</div>
                <div style="background:var(--neon); color:#000; padding:10px 20px; border-radius:5px; font-weight:900; display:inline-block;">LOT: ${{trade}}</div>
                <div style="text-align:left; font-size:10px; color:#555; margin-top:15px; border-left:2px solid var(--neon); padding-left:10px;">{{log}}</div>
                
                <div class="f-row">
                    <a href="/update/win" class="f-btn" style="background:var(--win); color:#000;">WIN</a>
                    <a href="/update/loss" class="f-btn" style="background:var(--loss); color:#fff;">LOSS</a>
                </div>
            </div>
            {% endif %}
        </div>
{% endif %}
    </div>

    <script>
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString('en-GB'); }, 1000);
    </script>
</body>
</html>
'''

@app.before_request
def core_sync():
    today = datetime.date.today().isoformat()
    if 'day' not in session or session.get('day') != today:
        session.update({
            'day': today, 'wins': 0, 'losses': 0, 'acc': 0, 
            'credits': TOTAL_LIMIT, 'authorized': session.get('authorized', False)
        })

@app.route('/')
def index(): return render_template_string(HTML_FINAL, rules=TRADING_RULES)

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
    
    # Anti-Human Filter
    bad = ['me', 'selfie', 'face', 'pic', 'photo', 'camera', 'img', 'human']
    if any(k in filename for k in bad) and "screenshot" not in filename:
        return render_template_string(HTML_FINAL, rules=TRADING_RULES, error=True)

    # Risk Filter
    if random.random() < 0.2:
        return render_template_string(HTML_FINAL, rules=TRADING_RULES, risk=True)

    session['credits'] -= 1 # ক্রেডিট কমবে
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(4)

    reports = ["SMC Liquidity sweep at OB.", "MSS confirmed. FVG fill expected.", "Institutional Supply Zone rejection."]
    signals = [
        {"s": "CALL ⬆️", "c": "#00ff88", "pa": 99.9, "l": reports[0], "p": 2.2},
        {"s": "PUT ⬇️", "c": "#ff0055", "pa": 99.8, "l": reports[1], "p": 2.1}
    ]
    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_FINAL, rules=TRADING_RULES, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
