from flask import Flask, render_template_string, jsonify, request
import secrets
import string

app = Flask(__name__)

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    chars = ""
    if use_uppercase: chars += string.ascii_uppercase
    if use_lowercase: chars += string.ascii_lowercase
    if use_digits:    chars += string.digits
    if use_symbols:   chars += string.punctuation

    if not chars: return None

    password = []
    if use_uppercase: password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase: password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:    password.append(secrets.choice(string.digits))
    if use_symbols:   password.append(secrets.choice(string.punctuation))

    remaining_length = length - len(password)
    for _ in range(max(0, remaining_length)):
        password.append(secrets.choice(chars))

    secrets.SystemRandom().shuffle(password)
    return "".join(password[:length])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Pass - Ultra Secure Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #8b5cf6;
            --secondary: #ec4899;
            --bg: #0f172a;
            --surface: rgba(30, 41, 59, 0.7);
            --text: #f8fafc;
            --accent: #00f2fe;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: radial-gradient(circle at top right, #1e1b4b, transparent),
                        radial-gradient(circle at bottom left, #312e81, transparent);
        }

        .container {
            position: relative;
            width: 100%;
            max-width: 500px;
            padding: 2rem;
            background: var(--surface);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 2rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, var(--accent), var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        p.subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }

        .display-box {
            background: rgba(15, 23, 42, 0.8);
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid rgba(139, 92, 246, 0.3);
            position: relative;
            overflow: hidden;
        }

        #password {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            color: var(--accent);
            letter-spacing: 1px;
            word-break: break-all;
        }

        .copy-btn {
            background: var(--primary);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }

        .copy-btn:hover {
            transform: scale(1.05);
            background: var(--secondary);
        }

        .controls {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.9rem;
            font-weight: 600;
            color: #cbd5e1;
            display: flex;
            justify-content: space-between;
        }

        input[type="range"] {
            width: 100%;
            accent-color: var(--primary);
        }

        .checkbox-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .checkbox-item:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        button.generate-btn {
            margin-top: 1rem;
            padding: 1rem;
            border: none;
            border-radius: 1rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 10px 20px -5px rgba(139, 92, 246, 0.5);
        }

        button.generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -10px rgba(139, 92, 246, 0.7);
        }

        .strength-meter {
            height: 4px;
            background: #334155;
            border-radius: 2px;
            margin-top: 0.5rem;
            overflow: hidden;
        }

        .strength-bar {
            height: 100%;
            width: 0%;
            transition: all 0.5s ease;
        }

        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 20%);
        }
    </style>
</head>
<body>
    <div class="particles"></div>
    <div class="container">
        <h1>Quantum Pass</h1>
        <p class="subtitle">Secure, Unbreakable, Python-Powered</p>

        <div class="display-box">
            <div id="password">Click Generate</div>
            <button class="copy-btn" onclick="copyPassword()">Copy</button>
        </div>

        <div class="controls">
            <div class="group">
                <label>Length: <span id="len-val">16</span></label>
                <input type="range" id="length" min="8" max="50" value="16" oninput="updateLen()">
                <div class="strength-meter">
                    <div id="strength-bar" class="strength-bar"></div>
                </div>
            </div>

            <div class="checkbox-grid">
                <label class="checkbox-item">
                    <input type="checkbox" id="upper" checked> Uppercase
                </label>
                <label class="checkbox-item">
                    <input type="checkbox" id="lower" checked> Lowercase
                </label>
                <label class="checkbox-item">
                    <input type="checkbox" id="digits" checked> Digits
                </label>
                <label class="checkbox-item">
                    <input type="checkbox" id="symbols" checked> Symbols
                </label>
            </div>

            <button class="generate-btn" onclick="generate()">Generate Password</button>
        </div>
    </div>

    <script>
        function updateLen() {
            document.getElementById('len-val').innerText = document.getElementById('length').value;
            updateStrength();
            generate(); // Generate instantly on slide
        }

        function generate() {
            const length = parseInt(document.getElementById('length').value);
            const useUpper = document.getElementById('upper').checked;
            const useLower = document.getElementById('lower').checked;
            const useDigits = document.getElementById('digits').checked;
            const useSymbols = document.getElementById('symbols').checked;

            let charset = "";
            if (useUpper) charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            if (useLower) charset += "abcdefghijklmnopqrstuvwxyz";
            if (useDigits) charset += "0123456789";
            if (useSymbols) charset += "!@#$%^&*()_+~`|}{[]:;?><,./-=";

            if (charset === "") {
                document.getElementById('password').innerText = "Select Options";
                return;
            }

            let password = "";
            const array = new Uint32Array(length);
            window.crypto.getRandomValues(array);

            for (let i = 0; i < length; i++) {
                password += charset[array[i] % charset.length];
            }

            document.getElementById('password').innerText = password;
            updateStrength();
        }

        // Initialize on load
        window.onload = generate;

        function updateStrength() {
            const bar = document.getElementById('strength-bar');
            const len = parseInt(document.getElementById('length').value);
            let score = 0;
            if (len > 12) score += 40;
            if (len > 24) score += 20;
            if (document.getElementById('upper').checked) score += 10;
            if (document.getElementById('digits').checked) score += 10;
            if (document.getElementById('symbols').checked) score += 20;

            bar.style.width = score + '%';
            if (score < 40) bar.style.background = '#ef4444';
            else if (score < 70) bar.style.background = '#f59e0b';
            else bar.style.background = '#10b981';
        }

        function copyPassword() {
            const pass = document.getElementById('password').innerText;
            if (pass === 'Click Generate') return;
            navigator.clipboard.writeText(pass);
            const btn = document.querySelector('.copy-btn');
            btn.innerText = 'Copied!';
            btn.style.background = '#10b981';
            setTimeout(() => {
                btn.innerText = 'Copy';
                btn.style.background = '#8b5cf6';
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.json
    password = generate_password(
        length=data.get('length', 16),
        use_uppercase=data.get('upper', True),
        use_lowercase=data.get('lower', True),
        use_digits=data.get('digits', True),
        use_symbols=data.get('symbols', True)
    )
    return jsonify({"password": password})

if __name__ == '__main__':
    app.run(port=5000)
