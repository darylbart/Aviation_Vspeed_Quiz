from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Dictionary of V-speeds for different aircraft
v_speeds = {
    "Sling2": {
        "Vx": 65,  # Best angle of climb speed
        "Vr": 55,  # Rotation speed
        "Vy": 75,  # Best rate of climb speed
        "Vne": 160,  # Never exceed speed
        "Vno": 129,  # Maximum structural cruising speed
        "Vs": 48,  # Stall speed clean configuration
        "Vso": 40  # Stall speed landing configuration
    },
    "RV12": {
        "Vx": 60,  # Best angle of climb speed
        "Vr": 50,  # Rotation speed
        "Vy": 70,  # Best rate of climb speed
        "Vne": 140,  # Never exceed speed
        "Vno": 120,  # Maximum structural cruising speed
        "Vs": 45,  # Stall speed clean configuration
        "Vso": 37  # Stall speed landing configuration
    }
}

# Get a random question for a selected aircraft
def get_random_question(aircraft):
    return random.choice(list(v_speeds[aircraft].keys()))

@app.route('/', methods=['GET', 'POST'])
def quiz():
    aircraft = request.args.get('aircraft', 'Sling2')  # Default to Sling2 if none selected
    
    if request.method == 'POST':
        user_answer = request.form['answer'].strip()
        correct_answer = int(request.form['correct_answer'])
        question = request.form['question']
        aircraft = request.form['aircraft']
        
        if user_answer.isdigit() and int(user_answer) == correct_answer:
            message = {"text": "✅ Correct!", "color": "green"}
        else:
            message = {"text": f"❌ Incorrect! The correct answer for {question} on {aircraft} is {correct_answer}.", "color": "red"}
        
        return render_template('quiz.html', message=message, question=get_random_question(aircraft), v_speeds=v_speeds, aircraft=aircraft)
    
    return render_template('quiz.html', question=get_random_question(aircraft), v_speeds=v_speeds, aircraft=aircraft, message=None)

@app.route('/vspeeds', methods=['GET'])
def get_vspeeds():
    aircraft = request.args.get('aircraft', 'Sling2')
    return jsonify(v_speeds.get(aircraft, {}))

if __name__ == '__main__':
    app.run(debug=True)
