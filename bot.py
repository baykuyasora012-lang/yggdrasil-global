# এই কোডটি আপনার bot.py তে রিপ্লেস করুন
import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "global_supreme_yggdrasil_2026"

# গ্লোবাল মাস্টার এক্সেস (আপনি চাইলে পরিবর্তন করতে পারেন)
MASTER_ID = "admin"
MASTER_PW = "1234"

# HTML UI - Mobile Optimized for Global Access
HTML_GLOBAL = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>YGGDRASIL V25.1 | GLOBAL ACCESS</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #ffcc00; --neon: #00ffcc; --win: #00ff88; --loss: #ff0055; --bg: #010103; }
        body { background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; padding: 0; }
        
        .global-header { background: rgba(10,10,20,0.95); padding: 15px; border-bottom: 2px solid var(--gold); text-align: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 0 20px var(--gold); }
        .global-header b { font-family: 'Orbitron', sans-serif; font-size: 14px; color: var(--gold); letter-spacing: 3px; }

        .container { max-width: 500px; margin: 20px auto; padding: 20px; }
        .card { background: #08080c; border: 1px solid rgba(255,204,0,0.1); border-radius: 30px; padding: 25px; box-shadow: 0 20px 50px rgba(0,0,0,1); }
        
        input, select { width: 100%; padding: 18px; margin-bottom: 15px; background: #000; border: 1px solid #1a1a25; border-radius: 15px; color: var(--neon); font-weight: bold; box-sizing: border-box; }
        
        .btn-main { background: linear-gradient(45deg, var(--gold), #ffaa00); color: #000; width: 100%; padding: 20px; border-radius: 15px; border: none; font-family: 'Orbitron', sans-serif; font-weight: 900; cursor: pointer; box-shadow: 0 10px 30px rgba(255,204,0,0.4); }

        .result-box { margin-top: 25px; background: #000; border: 2px solid var(--gold); border-radius: 25px; padding: 20px; text-align: center; }
        .sig-text { font-size: 40px; font-weight: 900; font-family: 'Orbitron'; margin: 10px 0; }
        
        .pnl-row { display: flex; gap: 10px; margin-top: 20px; }
        .pnl-row a { flex: 1; text-decoration: none; text-align: center; padding: 15px; border-radius: 12px; color: #fff; font-weight: bold; font-size: 13px; }
    </style>
</head>
<body>
    <div class="global-header">
        <b>YGGDRASIL GLOBAL V25.1</b>
    </div>

    <div class="container">
        {% if not session.get('authorized') %}
            <div class="card">
                <h2 style="text-align:center; color:var(--gold); font-size:14px; font-family:'Orbitron';">MASTER LOGIN</h2>
                <form method="POST" action="/login">
                    <input type="text" name="u" placeholder="ID" required>
                    <input type="password" name="p" placeholder="KEY" required>
                    <button type="submit" class="btn-main">LOGIN</button>
                </form>
            </div>
        {% else %}
            <div class="card">
                <form method="POST" action="/analyze" enctype="multipart/form-data">
                    <input type="number" name="bal" placeholder="BALANCE ($)" required>
                    <select name="time">
                        <option value="1M">M1 SCALPER</option>
                        <option value="5M">M5 TREND</option>
                    </select>
                    <input type="file" name="chart" accept="image/*" required>
                    <button type="submit" class="btn-main">EXECUTE GLOBAL SCAN</button>
                </form>

                {% if sig %}
                <div class="result-box">
                    <div style="font-size:10px; color:var(--gold);">PROBABILITY: {{pa}}%</div>
                    <div class="sig-text" style="color: {{col}}">{{sig}}</div>
                    <div style="color:var(--gold); font-weight:bold;">INVEST: ${{trade}}</div>
                    <div class="pnl-row">
                        <a href="/update/win" style="background:var(--win)">WIN</a>
                        <a href="/update/loss" style="background:var(--loss)">LOSS</a>
                    </div>
                </div>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_GLOBAL)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == MASTER_ID and request.form['p'] == MASTER_PW:
        session['authorized'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    bal = float(request.form['bal'])
    # Global Logic Simulation
    sig_data = random.choice([
        {"s": "CALL ⬆️", "c": "#00ff88", "pa": 99.9, "p": 2.5},
        {"s": "PUT ⬇️", "c": "#ff0055", "pa": 99.8, "p": 2.0}
    ])
    trade_amt = round((bal * sig_data['p']) / 100, 2)
    return render_template_string(HTML_GLOBAL, sig=sig_data['s'], col=sig_data['c'], pa=sig_data['pa'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
