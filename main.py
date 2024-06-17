from waitress import serve
import app.routes

if __name__ == "__main__":
    serve(app.routes.app, host="0.0.0.0", port=8080)
