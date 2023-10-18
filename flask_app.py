from app import app

if __name__ == "__main__":
    app.secret_key = "abcd"
    app.run(debug=True)
