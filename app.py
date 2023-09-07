import os

from flask import Flask, render_template, jsonify, request, send_from_directory

from caching import init_caching, get_cached_data
from config import OPENAI_API_KEY
from question import get_answer
from summarize import generate_summary
from upload import handle_upload

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


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['document']
    resp, err = handle_upload(uploaded_file)
    if err:
        return jsonify({'error': resp}), err
    else:
        return jsonify({'pdf_url': resp})


@app.route('/ask_question/<question>')
def ask_question(question):
    file_path = get_cached_data('uploaded_file')
    answer, page = get_answer(question, file_path)
    return jsonify({'answer': answer, 'page_number': page})


@app.route('/summarize')
def summarize():
    file_path = get_cached_data('uploaded_file')
    summary = generate_summary(file_path)
    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run()
