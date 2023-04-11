import os
import json
import uuid

# Flask
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from analysis import generate_dashboard


# Define the Flask app
app = Flask(__name__)


# Create the uploads folder at init
demo_dir = os.path.join(app.instance_path, 'demo')
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Home: Displays the input form and redirects to the dashboard when input file is received and validated.

    Returns:
        Any: Returns either a redirect or render_template
    """
    # Form data is received
    if request.method == 'POST':
        file_ref = request.files['csv_file']  # get input file

        # TODO: check if file is not too big

        # Save the file temporarily
        # This helps keep user privacy and file naming consistency
        id = str(uuid.uuid4())
        file_ref.save(os.path.join(uploads_dir, secure_filename(id + ".csv")))

        # No errors - go to dashboard
        return redirect(url_for('dashboard', id=id))
    else:
        # Render index.html if no form data is received
        return render_template('index.html')


@app.route('/dashboard/<id>')
def dashboard(id):
    """Dashboard: Displays the trip analysis

    Args:
        id (str): Unique trip ID generated during file input

    Returns:
        Any: render_template('dashboard.html)
    """
    filename = id + ".csv"

    # Demo trip
    if filename in os.listdir(demo_dir):
        return generate_dashboard(os.path.join(demo_dir, filename))

    # Check if the file exists, else 404
    if filename in os.listdir(uploads_dir):
        return generate_dashboard(os.path.join(uploads_dir, filename))
    else:
        return redirect(location='/404')


@app.route('/faq')
def faq():
    """FAQ: Static page displaying app FAQs

    Returns:
        Any: render_template('faq.html')
    """
    return render_template('faq.html', faqs=json.load(open('static/faq.json')))


@app.errorhandler(404)
def page_not_found(error):
    """404 Handler

    Args:
        error (str): Error encountered

    Returns:
        Any: render_template('page_not_found.html')
    """
    return render_template('page_not_found.html')


if __name__ == "__main__":
    app.run(debug=True)
