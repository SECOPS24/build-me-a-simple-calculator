# Simple Calculator

A sleek, modern web calculator with a dark glassmorphism UI, keyboard support, and calculation history.

## Features

- **Basic Operations**: Addition, Subtraction, Multiplication, Division
- **Extra Functions**: Toggle sign (+/-), Percentage (%)
- **Keyboard Support**: Use number keys, operators, Enter/= to calculate, Escape to clear, Backspace to delete
- **Calculation History**: Last 10 calculations displayed below the keypad
- **Error Handling**: Division by zero and invalid input are handled gracefully
- **Responsive Design**: Clean glassmorphism dark UI

## Running Locally

### With Python

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:3000

### With Docker

```bash
docker build -t simple-calculator .
docker run -p 3000:3000 simple-calculator
```

Open http://localhost:3000

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Calculator UI |
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| POST | `/calculate` | Perform a calculation |

### POST /calculate

**Request Body:**
```json
{
  "a": 10,
  "b": 5,
  "op": "+"
}
```

**Operators:** `+`, `-`, `*`, `/`

**Response:**
```json
{
  "result": 15.0
}
```
