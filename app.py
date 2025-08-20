# forensic_tool_web/app.py

import os
import datetime
import logging
import zipfile
import shutil
import uuid
from flask import Flask, render_template, request, session, send_from_directory, flash, jsonify
from werkzeug.utils import secure_filename
from termcolor import colored

# --- Local Imports ---
from hashing import hash_text, hash_file, hash_directory
from utils import get_file_metadata, format_size
from reporting import PDFReport

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = os.urandom(24)
# Get the absolute path for the app's directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['REPORTS_FOLDER'] = os.path.join(BASE_DIR, 'reports')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB max upload

# --- Logging Setup ---
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'logs/forensic_tool.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Routes ---

# Add a custom Jinja filter to use format_size in templates
@app.template_filter('format_size')
def _jinja2_filter_format_size(size):
    return format_size(size)

@app.route('/')
def index():
    """Renders the main page."""
    session.clear() # Clear session on new visit for a clean start
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_hash():
    """Handles hashing requests from the front-end JavaScript and returns JSON."""
    hash_type = request.form.get('hash_type')
    session['report_data'] = {} # Reset report data

    try:
        if hash_type == 'text':
            text_to_hash = request.form['text_input']
            if not text_to_hash:
                return jsonify({'status': 'error', 'message': 'Text input cannot be empty.'}), 400
            
            hashes = hash_text(text_to_hash)
            results_data = {'type': 'text', 'text': text_to_hash, 'hashes': hashes}
            session['report_data']['text_results'] = {'text': text_to_hash, 'hashes': hashes}
            logging.info(f"Hashed text input.")

        elif hash_type == 'file':
            file = request.files.get('file_input')
            if not file or file.filename == '':
                return jsonify({'status': 'error', 'message': 'No file was selected.'}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            metadata = get_file_metadata(filepath)
            hashes = hash_file(filepath)
            os.remove(filepath)
            
            results_data = {'type': 'file', 'metadata': metadata, 'hashes': hashes}
            session['report_data']['file_results'] = {'metadata': metadata, 'hashes': hashes}
            logging.info(f"Hashed file: {filename}")
        
        elif hash_type == 'directory':
            file = request.files.get('dir_input')
            if not file or not file.filename.endswith('.zip'):
                return jsonify({'status': 'error', 'message': 'A .zip archive must be uploaded.'}), 400
            
            temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
            os.makedirs(temp_dir)
            zip_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            results, summary = hash_directory(temp_dir)
            
            # Cleanup
            shutil.rmtree(temp_dir)
            os.remove(zip_path)
            
            results_data = {'type': 'directory', 'results': results, 'summary': summary}
            session['report_data']['dir_results'] = {'results': results, 'summary': summary}
            logging.info(f"Hashed directory from ZIP: {file.filename}")

        return jsonify({'status': 'success', 'data': results_data})
        
    except Exception as e:
        logging.error(f"An error occurred during hashing: {e}", exc_info=True)
        return jsonify({'status': 'error', 'message': f'An server error occurred: {e}'}), 500


@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generates and serves the PDF report."""
    if 'report_data' not in session or not session['report_data']:
        flash('Error: Session expired or no data to report. Please perform a new hash operation.', 'error')
        return render_template('index.html')

    try:
        case_id = request.form['case_id']
        case_metadata = {
            "investigator_name": request.form['investigator_name'],
            "case_id": case_id,
            "case_description": request.form['case_description'],
            "date_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        safe_case_id = "".join(c for c in case_id if c.isalnum() or c in ('_')).rstrip()
        report_filename = f"Forensic_Report_{safe_case_id}_{datetime.datetime.now():%Y%m%d_%H%M%S}.pdf"
        report_filepath = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        pdf = PDFReport(report_filepath)
        pdf.generate_cover_page(case_metadata)
        pdf.add_hashing_results(session.get('report_data', {}))
        pdf.save()
        logging.info(f"Generated report '{report_filename}'")
        
        return send_from_directory(app.config['REPORTS_FOLDER'], report_filename, as_attachment=True)
    
    except Exception as e:
        logging.error(f"Failed to generate report: {e}", exc_info=True)
        flash(f'Error creating PDF: {e}. Please check logs.', 'error')
        return render_template('index.html')


if __name__ == '__main__':
    # Ensure necessary directories exist
    for folder in [app.config['UPLOAD_FOLDER'], app.config['REPORTS_FOLDER']]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # --- Clear startup message ---
    print("="*80)
    print(colored("CYBER HUNTER WARRIOR - FORENSIC HASHING-X", 'cyan', attrs=['bold']))
    print(colored("The server is starting...", 'yellow'))
    print(colored("Access the tool by opening this URL in your web browser:", 'green'))
    print(colored("      => http://127.0.0.1:5000", 'white', 'on_blue'))
    print("="*80)
    
    app.run(debug=True, host='0.0.0.0')
