from {{ project_name }}.factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
