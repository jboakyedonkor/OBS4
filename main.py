from web_client import app

if __name__ == '__main__':
    app.run()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
