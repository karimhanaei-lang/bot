from flask import Flask, render_template_string
import random

app = Flask(__name__)
quotes = [
    {"content": "بهترین راه برای انجام کارهای بزرگ، عشق ورزیدن به کاری است که انجام می‌دهید.", "author": "استیو جابز"},
    {"content": "همیشه به نظر می‌رسد که کار غیرممکن است تا وقتی که انجام شود.", "author": "نلسون ماندلا"},
    {"content": "یادگیری گنجینه‌ای است که صاحبش را همه جا دنبال می‌کند.", "author": "ضرب‌المثل"},
    {"content": "هیچ چیز جای سخت‌کوشی را نمی‌گیرد.", "author": "توماس ادیسون"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Quotes API Browser</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #f4f4f9; display: flex; 
               justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); 
                text-align: center; max-width: 500px; width: 80%; }
        p { font-size: 1.2rem; color: #555; line-height: 1.6; }
        .author { font-weight: bold; color: #888; margin-top: 20px; }
        button { background-color: #4CAF50; color: white; border: none; padding: 10px 20px; 
                border-radius: 5px; cursor: pointer; font-size: 1rem; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>✨ جمله تصادفی ✨</h1>
        <p>"{{ quote }}"</p>
        <div class="author">— {{ author }}</div>
        <button onclick="window.location.reload()">جمله بعدی 🎲</button>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    data = random.choice(quotes)
    return render_template_string(HTML_TEMPLATE, quote=data['content'], author=data['author'])

if __name__ == '__main__':
    app.run(debug=True)