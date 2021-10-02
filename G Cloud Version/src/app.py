from flask import Flask, render_template, url_for, request, redirect
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime
import os
from werkzeug.utils import redirect

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://postgres:1234@34.94.29.46/postgres?host=/cloudsql/lista-de-tarefas-327315:us-west2:dblistadetarefas' # 3 slashes pois é um path relativo
# 'postgresql+psycopg2://postgres:1234@34.94.29.46/postgres?host=/cloudsql/lista-de-tarefas-327315:us-west2:dblistadetarefas' 
# 'postgresql+pg8000://<db_user>:<db_pass>@/<db_name>?unix_sock=<socket_path>/<cloud_sql_instance_name>
# 'postgresql+psycopg2://postgres:1234@34.94.29.46:5432/dblistadetarefas
# db = SQLAlchemy(app)

def init_connection_engine():
    db_config = {
        # [START cloud_sql_postgres_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_postgres_sqlalchemy_limit]

        # [START cloud_sql_postgres_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_postgres_sqlalchemy_backoff]

        # [START cloud_sql_postgres_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]

        # [START cloud_sql_postgres_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]
        "pool_pre_ping": True
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    # [START cloud_sql_postgres_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = 'postgres'
    db_pass = '1234'
    db_name = 'postgres'
    db_socket_dir = '/cloudsql'
    cloud_sql_connection_name = 'lista-de-tarefas-327315:us-west2:dblistadetarefas'

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_socket]
    pool.dialect.description_encoding = None
    return pool

db = None

@app.before_first_request
def create_tables():
    global db
    db = init_connection_engine()
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tarefas "
            "( id SERIAL NOT NULL, content VARCHAR(200) NOT NULL, "
            "date_created timestamp NOT NULL, PRIMARY KEY (id) );"
        )

"""class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
"""

@app.route("/", methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST':
        conteudo = request.form['content'] # conteudo do input
        # [START cloud_sql_postgres_sqlalchemy_connection]
        # Preparing a statement before hand can help protect against injections.
        try:
            # Using a with statement ensures that the connection is always released
            # back into the pool at the end of statement (even if an error occurs)
            with db.connect() as conn:
                conn.execute(
                    "INSERT INTO tarefas (content, date_created)"
                    f" VALUES ('{conteudo}', current_timestamp)"                    
                )
            return redirect('/')

        except:
            # If something goes wrong, handle the error in this section. This might
            # involve retrying or adjusting parameters depending on the situation.
            # [START_EXCLUDE]
            return "Houve um problema ao adicionar sua tarefa."
            # [END_EXCLUDE]
        # [END cloud_sql_postgres_sqlalchemy_connection]
    else:
        with db.connect() as conn:
            tarefas = conn.execute(
                "SELECT * FROM tarefas "
                "ORDER BY date_created"
            ).fetchall()
            
        #Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tarefas)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        with db.connect() as conn:
            conn.execute(
                f"DELETE FROM tarefas WHERE id = {id};"               
            )
        return redirect('/')
    except:
        return 'Houve um problema ao deletar a tarefa'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    with db.connect() as conn:
        tarefas = conn.execute(
            f"SELECT * FROM tarefas WHERE id = {id};"
        ).fetchone()


    if request.method == 'POST':
        new_content = request.form['content']

        try:
            with db.connect() as conn:
                conn.execute(
                    f"UPDATE tarefas SET content = '{new_content}', date_created = current_timestamp WHERE id = {id};"           
                )
            return redirect('/')
        except:
            return 'Houve um problema ao atualizar a tarefa'
    else:          
        return render_template('update.html', task=tarefas)
        


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))