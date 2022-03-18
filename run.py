from flaskblog import create_app

app = create_app()

if __name__ == "__main__":   # run module directly, no need for python -m flask run, and env vars
    app.run(debug=True)
