from app.routes import app

# Este bloque solo es necesario para desarrollo local.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
