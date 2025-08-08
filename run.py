from app import create_app
import webbrowser

app = create_app()

if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000")
    app.run(debug=True)

