from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# --- 데이터베이스 대신 임시로 메모리에 저장하지만 ---
# --- 실전에서는 여기에 DB 연결 코드가 들어갑니다. ---
# --- 파일(ranking.txt)을 쓰지 않는 것이 포인트입니다. ---

rank_data = [] # 서버 메모리에 저장 (서버가 켜져있는 동안 유지)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/save', methods=['POST'])
def save_score():
    data = request.json
    name = data.get('name', 'Unknown').upper()
    score = data.get('score', 0)
    
    global rank_data
    rank_data.append({"name": name, "score": score})
    rank_data.sort(key=lambda x: x['score'], reverse=True)
    rank_data = rank_data[:10] # Top 10만 유지
    
    return jsonify({"status": "success"})

@app.route('/ranks', methods=['GET'])
def get_ranks():
    return jsonify(rank_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
