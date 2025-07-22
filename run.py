from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True enables auto-reload on code changes
    app.run(debug=True)
