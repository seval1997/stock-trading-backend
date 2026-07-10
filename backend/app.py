from flask import Flask

app = Flask(__name__)

@app.route("/api/health")
def health():
    return {"status": "ok", "message": "Backend is alive"}

if __name__ == "__main__":
    app.run(debug=True)
