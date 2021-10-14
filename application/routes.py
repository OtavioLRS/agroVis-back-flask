from application import app


# Index
@app.route('/', methods=['GET'])
def index():
    return "<h1>AgroVis-FCT => Backend - Flask</h1>"
