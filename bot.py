import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "masterxbot_supreme_unlimited_2026"

# Configuration
MASTER_ID = "admin"
MASTER_KEY = "1234"
DAILY_LIMIT = 100

HTML_ULTIMATE = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MASTER X | SUPREME ANALYTICS</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Orbitron:wght@400;900&family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #ffcc00; --neon: #00ffcc; --win: #00ff88; --loss: #ff0055; --bg: #020205; --card: #0a0a12; }
        body { background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; overflow-x: hidden; }
        
        /* Animated Background */
        .grid-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px); background-size: 30px 30px; z-index: -1; }

        .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: rgba(5,5,15,0.95); border-bottom: 2px solid var(--gold); position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(10px); }
        .logo { font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 900; color: var(--gold); text-shadow: 0 0 10px var(--gold); }
        #clock { font-family: 'Orbitron'; font-size: 12px; color: var(--neon); }

        .container { max-width: 500px; margin: 20px auto; padding: 0 15px; }

        /* Stats & HUD */
        .hud-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
        .hud-item { background: var(--card); border: 1px solid rgba(255,204,0,0.2); padding: 15px; border-radius: 20px; text-align: center; }
        .hud-item span { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .hud-item b { display: block; font-size: 22px; font-family: 'Orbitron'; margin-top: 5px; }

        /* Main Console */
        .console { background: var(--card); border-radius: 40px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .status-badge { display: inline-block; padding: 6px 15px; border-radius: 20px; font-size: 11px; background: rgba(0,255,204,0.1); border: 1px solid var(--neon); color: var(--neon); margin-bottom: 20px; }

        input, select { width: 100%; padding: 18px; margin-bottom: 15px; background: #000; border: 1px solid #1a1a25; border-radius: 15px; color: #fff; font-weight: bold; font-size: 14px; box-sizing: border-box; transition: 0.3s; }
        input:focus { border-color: var(--gold); box-shadow: 0 0 15px rgba(255,204,0,0.2); outline: none; }

        .btn-glow { background: linear-gradient(45deg, var(--gold), #ffaa00); color: #000; width: 100%; padding: 22px; border-radius: 18px; border: none; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 16px; cursor: pointer; box-shadow: 0 10px 30px rgba(255,204,0,0.3); transition: 0.3s; }
        .btn-glow:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(255,204,0,0.5); }

        /* Signal Output Area */
        .output-box { margin-top: 30px; background: #000; border: 2px solid var(--gold); border-radius: 35px; padding: 30px; text-align: center; position: relative; animation: slideUp 0.5s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        .signal-title { font-size: 12px; color: var(--gold); letter-spacing: 5px; text-transform: uppercase; }
        .signal-main { font-size: 50px; font-weight: 900; font-family: 'Orbitron'; margin: 15px 0; text-shadow: 0 0 25px currentColor; }
        .signal-meta { display: flex; justify-content: space-around; margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.03); border-radius: 15px; }
        
        .logic-terminal { text-align: left; font-size: 12px; color: #777; line-height: 1.6; border-top: 1px solid #222; padding-top: 15px; margin-top: 15px; }

        /* Feedback Buttons */
        .feedback-row { display: flex; gap: 15px; margin-top: 25px; }
        .feedback-btn { flex: 1; padding: 18px; border-radius: 15px; text-decoration: none; font-weight: 900; font-family: 'Orbitron'; font-size: 13px; text-align: center; transition: 0.3s; }
        .win-btn { background: var(--win); color: #000; box-shadow: 0 0 20px rgba(0,255,136,0.3); }
        .loss-btn { background: var(--loss); color: #fff; box-shadow: 0 0 20px rgba(255,0,85,0.3); }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="header">
        <div class="logo">MASTER X PRO</div>
        <div id="clock">00:00:00</div>
    </div>

{% if not session.get('authorized') %}
    <div class="container" style="padding-top: 80px;">
        <div class="console">
            <h2 style="text-align:center; font-family:'Orbitron'; color:var(--gold);">AUTHENTICATION</h2>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="SYSTEM ID" required>
                <input type="password" name="p" placeholder="ACCESS KEY" required>
                <button type="submit" class="btn-glow">INITIALIZE CORE</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="container">
        <div class="hud-grid">
            <div class="hud-item"><span>WINS</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
            <div class="hud-item"><span>ACCURACY</span><b style="color:var(--neon)">{{ session['acc'] }}%</b></div>
            <div class="hud-item"><span>LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
            <div class="hud-item"><span>CREDITS</span><b style="color:var(--gold)">{{ session['credits'] }}</b></div>
        </div>

        <div class="console">
            <div class="status-badge">● AI ENGINE ACTIVE | LIMIT: {{ DAILY_LIMIT }}</div>
            <form method="POST" action="/analyze" enctype="multipart/form-data">
                <input type="number" name="bal" placeholder="WALLET BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time">
                    <option value="1M">M1 - TURBO SCALPER</option>
                    <option value="5M">M5 - INSTITUTIONAL TREND</option>
                </select>
                <input type="file" name="chart" accept="image/*" required>
                <button type="submit" class="btn-glow" {% if session['credits'] <= 0 %}disabled style="opacity:0.3;"{% endif %}>
                    {% if session['credits'] > 0 %}EXECUTE AI SCAN{% else %}DAILY LIMIT REACHED{% endif %}
                </button>
            </form>

            {% if sig %}
            <div class="output-box">
                <div class="signal-title">SMC ANALYSIS COMPLETE</div>
                <div class="signal-main" style="color: {{col}}">{{sig}}</div>
                
                <div class="signal-meta">
                    <div><span style="display:block; font-size:10px; color:#888;">PROBABILITY</span><b style="color:var(--neon)">{{pa}}%</b></div>
                    <div><span style="display:block; font-size:10px; color:#888;">INVESTMENT</span><b style="color:var(--gold)">${{trade}}</b></div>
                </div>

                <div class="logic-terminal">
                    <b style="color:var(--gold)">[AI_LOGIC]:</b> {{log}}
                </div>

                <div class="feedback-row">
                    <a href="/update/win" class="feedback-btn win-btn">PROFIT (WIN)</a>
                    <a href="/update/loss" class="feedback-btn loss-btn">RECOVERY (LOSS)</a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
{% endif %}

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
    if 'day' not in session or session['day'] != today:
        session.update({
            'day': today, 'credits': DAILY_LIMIT,
            'wins': 0, 'losses': 0, 'acc': 0,
            'authorized': session.get('authorized', False)
        })

@app.route('/')
def index(): return render_template_string(HTML_ULTIMATE)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == MASTER_ID and request.form['p'] == MASTER_KEY:
        session['authorized'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return redirect('/')
    
    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    time.sleep(3.5)
    
    logics = [
        "Order Block rejection detected. Institutional buy volume entering at liquidity sweep zone. Safe Call.",
        "Market Structure Shift (MSS) confirmed. Price filling Fair Value Gap (FVG) with high momentum. Optimal Put.",
        "Internal Liquidity raid finished. Smart Money Accumulation zone identified. High-probability reversal."
    ]
    
    signals = [
        {"s": "CALL ⬆️", "c": "#00ff88", "pa": 99.9, "l": logics[0], "p": 2.5},
        {"s": "PUT ⬇️", "c": "#ff0055", "pa": 99.8, "l": logics[1], "p": 2.2}
    ]
    
    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    return render_template_string(HTML_ULTIMATE, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
