from flask import Flask, url_for, redirect, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'cotizaciones.db'

def get_db():
    # Conexion a la base de datos.
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Enable row factory for dict-like access
    return g.db

def close_db(e=None):
    # Cierre de la conexion a la base de datos.
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cotizaciones = db.execute('SELECT * FROM cotizaciones WHERE origen = "BOGOTA" AND destino = "CALI" AND peso IN(2.0, 5.0, 15.0) AND empresa = "Interrapidisimo"').fetchall()
    return render_template('index.html', cotizaciones=cotizaciones)

@app.route('/update_prices', methods=['POST'])
def update_price():
    db = get_db()
    # Actualizar precios de las cotizaciones.
    db.execute('UPDATE cotizaciones SET precio = precio +550 WHERE origen = "BOGOTA" AND destino = "CALI" AND empresa = "Interrapidisimo"')
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

