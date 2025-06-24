from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import webbrowser
from threading import Timer

app = Flask(__name__)
CORS(app)

DATABASE = 'users.db'

def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            stars REAL DEFAULT 0,
            last_farm INTEGER DEFAULT 0,
            last_daily INTEGER DEFAULT 0,
            last_steal INTEGER DEFAULT 0,
            ref_id INTEGER DEFAULT NULL,
            ref_num INTEGER DEFAULT 0,
            ref_week INTEGER DEFAULT 0,
            change_star INTEGER DEFAULT 0,
            boost_expire INTEGER DEFAULT 0,
            tap INTEGER DEFAULT 0,
            block INTEGER DEFAULT 0,
            total_earned REAL DEFAULT 0,
            gifts_redeemed INTEGER DEFAULT 0,
            total_withdrawn REAL DEFAULT 0,
            ref_profile TEXT DEFAULT 'default',
            profile_assigned_at INTEGER DEFAULT 0,
            last_pepe INTEGER DEFAULT 0,
            coins REAL DEFAULT 0,
            last_game_date INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute("SELECT id FROM users WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (id, coins) VALUES (1, 0)")
    
    conn.commit()
    conn.close()

create_db()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/get_user_data')
def get_user_data():
    user_id = request.args.get('user_id')
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT coins, last_game_date FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({
                'coins': user['coins'],
                'last_game_date': user['last_game_date']
            })
        else:
            cursor.execute('INSERT INTO users (id, coins) VALUES (?, 0)', (user_id,))
            conn.commit()
            return jsonify({
                'coins': 0,
                'last_game_date': 0
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/save_game_result', methods=['POST'])
def save_game_result():
    data = request.json
    user_id = data['user_id']
    coins = data['coins']
    game_date = data['game_date']
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE users 
            SET coins = coins + ?, 
                last_game_date = ?
            WHERE id = ?
        ''', (coins, game_date, user_id))
        
        conn.commit()
        return jsonify({
            'success': True,
            'message': f'Добавлено {coins} монет',
            'new_coins': coins
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

def open_browser():
    webbrowser.open_new('http://192.168.0.101:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True)