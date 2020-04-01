from flask import Flask

app = Flask(__name__)

i = 0


@app.route("/")
def hello():
    global i
    print(i)
    i += 1
    return "Hello World!"


if __name__ == "__main__":
    app.run()
