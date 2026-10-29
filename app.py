from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            font-family: \'Segoe UI\', sans-serif;
        }

        .calculator {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255,255,255,0.05);
            width: 340px;
        }

        .display {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 16px;
            padding: 20px 20px 12px;
            margin-bottom: 20px;
            text-align: right;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .expression {
            color: rgba(255, 255, 255, 0.4);
            font-size: 14px;
            min-height: 20px;
            margin-bottom: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .result {
            color: #ffffff;
            font-size: 42px;
            font-weight: 300;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .error {
            color: #ff6b6b;
            font-size: 24px;
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        button {
            height: 64px;
            border: none;
            border-radius: 14px;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            outline: none;
        }

        button:active {
            transform: scale(0.93);
        }

        .btn-number {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .btn-number:hover {
            background: rgba(255, 255, 255, 0.18);
        }

        .btn-operator {
            background: rgba(100, 149, 237, 0.2);
            color: #6495ed;
            border: 1px solid rgba(100, 149, 237, 0.2);
        }

        .btn-operator:hover {
            background: rgba(100, 149, 237, 0.35);
        }

        .btn-equals {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #ffffff;
            border: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-equals:hover {
            background: linear-gradient(135deg, #7b93f0, #8a5cb8);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .btn-clear {
            background: rgba(255, 107, 107, 0.2);
            color: #ff6b6b;
            border: 1px solid rgba(255, 107, 107, 0.2);
        }

        .btn-clear:hover {
            background: rgba(255, 107, 107, 0.35);
        }

        .btn-special {
            background: rgba(255, 255, 255, 0.07);
            color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 16px;
        }

        .btn-special:hover {
            background: rgba(255, 255, 255, 0.13);
        }

        .btn-zero {
            grid-column: span 2;
        }

        .history-section {
            margin-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 16px;
        }

        .history-title {
            color: rgba(255, 255, 255, 0.35);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
        }

        .history-list {
            max-height: 100px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.2) transparent;
        }

        .history-item {
            color: rgba(255, 255, 255, 0.45);
            font-size: 13px;
            padding: 4px 0;
            text-align: right;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }

        .history-item:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="display">
            <div class="expression" id="expression"></div>
            <div class="result" id="result">0</div>
        </div>

        <div class="buttons">
            <button class="btn-clear" onclick="clearAll()">AC</button>
            <button class="btn-special" onclick="toggleSign()">+/-</button>
            <button class="btn-special" onclick="percentage()">%</button>
            <button class="btn-operator" onclick="setOperator(\'/')">÷</button>

            <button class="btn-number" onclick="appendNumber(\'7\')">7</button>
            <button class="btn-number" onclick="appendNumber(\'8\')">8</button>
            <button class="btn-number" onclick="appendNumber(\'9\')">9</button>
            <button class="btn-operator" onclick="setOperator(\'*\')">×</button>

            <button class="btn-number" onclick="appendNumber(\'4\')">4</button>
            <button class="btn-number" onclick="appendNumber(\'5\')">5</button>
            <button class="btn-number" onclick="appendNumber(\'6\')">6</button>
            <button class="btn-operator" onclick="setOperator(\'-\')">−</button>

            <button class="btn-number" onclick="appendNumber(\'1\')">1</button>
            <button class="btn-number" onclick="appendNumber(\'2\')">2</button>
            <button class="btn-number" onclick="appendNumber(\'3\')">3</button>
            <button class="btn-operator" onclick="setOperator(\'+\')">+</button>

            <button class="btn-number btn-zero" onclick="appendNumber(\'0\')">0</button>
            <button class="btn-number" onclick="appendDecimal()">.</button>
            <button class="btn-equals" onclick="calculate()">=</button>
        </div>

        <div class="history-section">
            <div class="history-title">History</div>
            <div class="history-list" id="history"></div>
        </div>
    </div>

    <script>
        let currentValue = \'0\';
        let previousValue = \'\';
        let operator = null;
        let shouldResetDisplay = false;
        let history = [];

        function updateDisplay(value, expr) {
            const resultEl = document.getElementById(\'result\');
            const exprEl = document.getElementById(\'expression\');
            resultEl.textContent = value;
            resultEl.className = \'result\' + (value === \'Error\' ? \' error\' : \'\');
            exprEl.textContent = expr || \'\';
        }

        function appendNumber(num) {
            if (shouldResetDisplay) {
                currentValue = num;
                shouldResetDisplay = false;
            } else {
                if (currentValue === \'0\' && num !== \'.\') {
                    currentValue = num;
                } else {
                    if (currentValue.length < 12) {
                        currentValue += num;
                    }
                }
            }
            updateDisplay(currentValue, buildExpression());
        }

        function appendDecimal() {
            if (shouldResetDisplay) {
                currentValue = \'0.\';
                shouldResetDisplay = false;
                updateDisplay(currentValue, buildExpression());
                return;
            }
            if (!currentValue.includes(\'.\')) {
                currentValue += \'.\';
                updateDisplay(currentValue, buildExpression());
            }
        }

        function setOperator(op) {
            if (operator && !shouldResetDisplay) {
                performCalculation();
            }
            previousValue = currentValue;
            operator = op;
            shouldResetDisplay = true;
            updateDisplay(currentValue, buildExpression(true));
        }

        function buildExpression(showOp) {
            if (!previousValue) return \'\';
            const opSymbol = { \'+\': \'+\', \'-\': \'−\', \'*\': \'×\', \'/\': \'÷\' };
            let expr = previousValue;
            if (operator) {
                expr += \' \' + (opSymbol[operator] || operator);
                if (!showOp && !shouldResetDisplay) {
                    expr += \' \' + currentValue;
                }
            }
            return expr;
        }

        function performCalculation() {
            if (!operator || !previousValue) return;
            const a = parseFloat(previousValue);
            const b = parseFloat(currentValue);
            let result;
            switch (operator) {
                case \'+\': result = a + b; break;
                case \'-\': result = a - b; break;
                case \'*\': result = a * b; break;
                case \'/\':
                    if (b === 0) { return \'Error\'; }
                    result = a / b;
                    break;
                default: return;
            }
            return result;
        }

        function calculate() {
            if (!operator || !previousValue) return;

            const a = parseFloat(previousValue);
            const b = parseFloat(currentValue);

            if (operator === \'/\' && b === 0) {
                updateDisplay(\'Error\', \'\'+ previousValue + \' ÷ \' + currentValue + \' =\');
                addToHistory(previousValue + \' ÷ \' + currentValue + \' = Error\');
                operator = null;
                previousValue = \'\';
                shouldResetDisplay = true;
                return;
            }

            fetch(\'/calculate\', {
                method: \'POST\',
                headers: { \'Content-Type\': \'application/json\' },
                body: JSON.stringify({ a: a, b: b, op: operator })
            })
            .then(r => r.json())
            .then(data => {
                const opSymbol = { \'+\': \'+\', \'-\': \'−\', \'*\': \'×\', \'/\': \'÷\' };
                const exprStr = previousValue + \' \' + (opSymbol[operator]||operator) + \' \' + currentValue + \' =\';
                const histStr = previousValue + \' \' + (opSymbol[operator]||operator) + \' \' + currentValue + \' = \' + data.result;

                let displayResult = data.result;
                if (typeof displayResult === \'number\') {
                    if (!Number.isFinite(displayResult)) {
                        displayResult = \'Error\';
                    } else {
                        displayResult = parseFloat(displayResult.toFixed(10)).toString();
                    }
                }

                updateDisplay(displayResult, exprStr);
                addToHistory(histStr);
                currentValue = displayResult;
                operator = null;
                previousValue = \'\';
                shouldResetDisplay = true;
            })
            .catch(() => {
                updateDisplay(\'Error\', \'\');
                operator = null;
                previousValue = \'\';
                shouldResetDisplay = true;
            });
        }

        function clearAll() {
            currentValue = \'0\';
            previousValue = \'\';
            operator = null;
            shouldResetDisplay = false;
            updateDisplay(\'0\', \'\');
        }

        function toggleSign() {
            if (currentValue !== \'0\') {
                if (currentValue.startsWith(\'-\')) {
                    currentValue = currentValue.slice(1);
                } else {
                    currentValue = \'-\' + currentValue;
                }
                updateDisplay(currentValue, buildExpression());
            }
        }

        function percentage() {
            const val = parseFloat(currentValue);
            currentValue = (val / 100).toString();
            updateDisplay(currentValue, buildExpression());
        }

        function addToHistory(entry) {
            history.unshift(entry);
            if (history.length > 10) history.pop();
            const histEl = document.getElementById(\'history\');
            histEl.innerHTML = history.map(h => `<div class="history-item">${h}</div>`).join(\'\');
        }

        document.addEventListener(\'keydown\', (e) => {
            if (e.key >= \'0\' && e.key <= \'9\') appendNumber(e.key);
            else if (e.key === \'.\') appendDecimal();
            else if (e.key === \'+\') setOperator(\'+\');
            else if (e.key === \'-\') setOperator(\'-\');
            else if (e.key === \'*\') setOperator(\'*\');
            else if (e.key === \'/\') { e.preventDefault(); setOperator(\'/\'); }
            else if (e.key === \'Enter\' || e.key === \'=\') calculate();
            else if (e.key === \'Escape\') clearAll();
            else if (e.key === \'Backspace\') {
                if (!shouldResetDisplay && currentValue.length > 1) {
                    currentValue = currentValue.slice(0, -1);
                } else {
                    currentValue = \'0\';
                }
                updateDisplay(currentValue, buildExpression());
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    try:
        a = float(data['a'])
        b = float(data['b'])
        op = data['op']
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400

    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b
    else:
        return jsonify({'error': 'Unknown operator'}), 400

    return jsonify({'result': result})

if __name__ == '__main__':
    import uvicorn
    from flask import Flask
    app.run(host='0.0.0.0', port=3000, debug=False)
