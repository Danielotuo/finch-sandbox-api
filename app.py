from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os

# Create a Flask instance
app = Flask(__name__)

# Configure the secret key
app.secret_key = os.environ.get('SECRET_KEY')

headers = {'Content-Type': 'application/json'}


# Create a route for the index page
@app.route('/')
def provider_form():
    return render_template('provider_form.html')


# Create a route for the submit form page and choose the provider
@app.route('/submit_form', methods=['POST'])
def submit_form():
    provider = request.form.get('provider')

    # Validate the provider value
    if provider not in ["gusto", "bamboohr", "justworks", "paychex_flex", "workday"]:
        return jsonify(error="Invalid provider value"), 400

    data = json.dumps({
        "provider": provider,
        "products": ["company", "directory", "individual", "employment", "payment", "pay_statement"]
    })

    # Create sandbox, get access token, and store in session
    try:
        response = requests.post('https://finch-sandbox-se-interview.vercel.app/api/sandbox/create', headers=headers, data=data)
        response.raise_for_status()
        response_data = json.loads(response.text) 
        access_token = response_data['access_token']
        headers["Authorization"] = f"Bearer {access_token}"
        session['access_token'] = access_token

        # Get employer directory and display the data 
        employee_response = requests.get('https://finch-sandbox-se-interview.vercel.app/api/employer/directory', headers=headers)
        employee_response.raise_for_status()
        employee_data = json.loads(employee_response.text)
        individuals = employee_data['individuals']
        return render_template('employee_directory.html', employees=individuals)

    # Handle errors for each exception
    except requests.exceptions.HTTPError as errh:
        if employee_response.status_code == 404:
            return jsonify(error=f"This endpoint is not supported by the provider"), 404
        else:
            return jsonify(error=f"HTTP Error: {errh}"), employee_response.status_code
    except requests.exceptions.ConnectionError as errc:
        return jsonify(error=f"Error Connecting: {errc}"), 500
    except requests.exceptions.Timeout as errt:
        return jsonify(error=f"Timeout Error: {errt}"), 500
    except requests.exceptions.RequestException as err:
        return jsonify(error=f"Something went wrong: {err}"), 500



# Create a route for the employee individual or personal data page
@app.route('/submit_form/employee_data', methods=['GET', 'POST'])
def employee_data():
    if request.method == 'POST':

        # Check if access token is in session
        if 'access_token' in session:
            headers["Authorization"] = f"Bearer {session['access_token']}"
            employee_id = request.form['employee_id']
            payload = {"requests": [{"individual_id": employee_id}]}
            
            try:
                employee_response = requests.post("https://finch-sandbox-se-interview.vercel.app/api/employer/individual", json=payload, headers=headers)
                employee_response.raise_for_status()
                employee_data = json.loads(employee_response.text)
                employee_data = employee_data['responses']
                return render_template('employee_data.html', employee_data=employee_data)

            # Handle errors for each exception    
            except requests.exceptions.HTTPError as errh:
                return jsonify(error=f"HTTP Error: {errh}"), employee_response.status_code
            except requests.exceptions.ConnectionError as errc:
                return jsonify(error=f"Error Connecting: {errc}"), 500
            except requests.exceptions.Timeout as errt:
                return jsonify(error=f"Timeout Error: {errt}"), 500
            except requests.exceptions.RequestException as err:
                return jsonify(error=f"Something went wrong: {err}"), 500
        else:
            return jsonify(error="No access token found"), 403


# Create a route for the employee employment data page
@app.route('/submit_form/employment_data', methods=['GET', 'POST'])
def employment_data():
    if request.method == 'POST':
        if 'access_token' in session:
            headers["Authorization"] = f"Bearer {session['access_token']}"
            employee_id = request.form['employee_id']
            payload = {"requests": [{"individual_id": employee_id}]}
            try:
                employee_response = requests.post("https://finch-sandbox-se-interview.vercel.app/api/employer/employment", json=payload, headers=headers)
                employee_response.raise_for_status()
                employment_data = json.loads(employee_response.text)
                employment_data = employment_data['responses']
                return render_template('employment_data.html', employment_data=employment_data)

            # Handle errors for each exception
            except requests.exceptions.HTTPError as errh:
                return jsonify(error=f"HTTP Error: {errh}"), employee_response.status_code
            except requests.exceptions.ConnectionError as errc:
                return jsonify(error=f"Error Connecting: {errc}"), 500
            except requests.exceptions.Timeout as errt:
                return jsonify(error=f"Timeout Error: {errt}"), 500
            except requests.exceptions.RequestException as err:
                return jsonify(error=f"Something went wrong: {err}"), 500
        else:
            return jsonify(error="No access token found"), 403

        
# ses
@app.route('/other_route')
def other_route():
    if 'access_token' in session:
        headers["Authorization"] = f"Bearer {session['access_token']}"
        # Use the access token to make API calls
        return "session ready"
    else:
        return jsonify(error="No access token found"), 403
