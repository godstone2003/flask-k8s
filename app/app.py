from flask import Flask, request, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# HTML form
form_html = '''
    <h2>Enter your name</h2>
    <form method="POST" action="/greet">
        <input type="text" name="name" required>
        <input type="submit" value="Say Hola">
    </form>
'''

# Homepage route
@app.route('/')
def home():
    return form_html

# Greet route
@metrics.counter(
    'flask_greet_requests_total', 
    'Total number of greetings',
    labels={'method': lambda: request.method}
)

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name', 'Stranger')
    return f'<h3>Hola {name}!</h3><a href="/">Go Back</a>'

# Health check
@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
