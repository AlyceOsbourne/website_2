from app import create_app

if __name__ == '__main__':
    create_app().run(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
else:
    sgi = create_app()

# gunicorn -b 0.0.0.0:5000 -w 3 'run:sgi'