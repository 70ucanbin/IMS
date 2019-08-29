from ims import app

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    pass