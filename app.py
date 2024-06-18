from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

def generate_response(prompt):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3:latest', prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )
        response = result.stdout.decode('utf-8').strip()
        error = result.stderr.decode('utf-8').strip()

        if error:
            print(f"Error: {error}")
        
        return response
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    bot_response = generate_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
