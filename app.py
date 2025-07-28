import os

from flask import Flask, render_template, jsonify, send_from_directory

from caching import init_caching
from config import OPENAI_API_KEY, DOCUQUERY_PDF
from question import get_answer
from summarize import generate_summary

app = Flask(__name__)
init_caching(app)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/documents/<filename>')
def serve_pdf(filename):
    pdf_directory = os.path.join(app.root_path, 'documents')
    return send_from_directory(pdf_directory, filename)


# Upload route removed – documents are now pre-populated


@app.route('/ask_question/<question>')
def ask_question(question):
    answer, page = get_answer(question)
    return jsonify({'answer': answer, 'page_number': page})


@app.route('/summarize')
def summarize():
    summary = generate_summary(DOCUQUERY_PDF)
    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run()
