from sanic import Sanic
from sanic import response
from sanic_jinja2 import SanicJinja2
from sanic_auth import Auth
from sanic_session import Session, InMemorySessionInterface
from sqlalchemy import create_engine

import settings
from load_data import load_data
from routes import setup_routes
from models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


app = Sanic(__name__)
app.static('static', './static')
app.config.update_config(settings)
session = Session(app, interface=InMemorySessionInterface())
engine = create_engine(app.config.DB_URL, echo=True, connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
Base.metadata.create_all(engine)
auth = Auth(app)
jinja = SanicJinja2(app, pkg_name="app")


def run():
    data_base_session = sessionmaker(bind=engine, autoflush=False)
    data_base_session = data_base_session()
    kwargs = {
        'data_base_session': data_base_session,
        'app': app,
        'jinja': jinja,
        'auth': auth,
        'response': response,
    }
    load_data(data_base_session, app)
    setup_routes(**kwargs)
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG,
    )
    data_base_session.close_all()


run()
