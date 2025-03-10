from flask import Flask, request, jsonify
# Importer evt. andre moduler du har brug for
# f.eks. fra onboarding_process import din_funktion

app = Flask(__name__)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    user_message = data.get("message")
    
    # Her kan du kalde din eksisterende onboarding- eller chatbot-logik.
    # For nu giver vi bare et simpelt svar, der ekkoer brugermeddelelsen:
    reply = f"Du skrev: {user_message}"
    
    # Hvis du senere vil udvide til fx at generere en PDF eller gemme data,
    # kan du kalde funktioner fra din onboarding_process.py eller andre moduler.
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)