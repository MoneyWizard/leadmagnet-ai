from flask import Flask, request, send_file, render_template_string
import openai, os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import io
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)
HTML_FORM = """<!DOCTYPE html><html><head><title>AI Lead Magnet Generator</title><style>body{font-family:sans-serif;max-width:600px;margin:50px auto;padding:20px;}input,button{width:100%;padding:15px;font-size:18px;margin:10px 0;}button{background:#007cba;color:white;border:none;cursor:pointer;}</style></head><body><h1>AI Lead Magnet Generator</h1><p>Enter niche -> Get instant PDF checklist</p><form method="POST"><input type="text" name="niche" placeholder="e.g. Realtors, Ecommerce, SaaS founders" required><button type="submit">Generate PDF</button></form></body></html>"""
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        niche = request.form['niche']
        prompt = "Create a professional 50-point checklist titled '{} Lead Magnet Ideas'. Make each point actionable and specific. Format as numbered list.".format(niche)
        response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=2000)
        content = response.choices[0].message.content
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.drawString(100, height-100, niche + " Lead Magnet Checklist")
        y = height - 200
        lines = content.splitlines()
        for line in lines[:55]:
            if y < 100: 
                p.showPage()
                y = height - 100
            p.drawString(100, y, line[:80])
            y -= 20
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=niche.replace(" ","_")+"_lead_magnets.pdf", mimetype='application/pdf')
    return render_template_string(HTML_FORM)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
