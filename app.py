from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/save', methods=['POST'])
def save_score():
    data = request.json
    name = data.get('name', 'Unknown')
    score = data.get('score', 0)
    with open("ranking.txt", "a") as f:
        f.write(f"{name},{score}\n")
    return jsonify({"status": "success"})

@app.route('/ranks', methods=['GET'])
def get_ranks():
    if not os.path.exists("ranking.txt"):
        return jsonify([])
    ranks = []
    with open("ranking.txt", "r") as f:
        for line in f:
            if ',' in line:
                name, score = line.strip().split(',')
                ranks.append({"name": name, "score": int(score)})
    ranks.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(ranks[:10])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
