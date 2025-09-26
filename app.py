from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

JSON_FILE = 'timetable.json'

# Load JSON lúc start
def load_timetable():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Thêm timestamp nếu chưa có
            if 'last_updated' not in data:
                data['last_updated'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            return data
    # Mẫu rỗng nếu chưa có file
    return {"last_updated": datetime.now().strftime('%d/%m/%Y %H:%M')}

timetable_data = load_timetable()

@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    return jsonify(timetable_data)

@app.route('/api/timetable', methods=['POST'])
def update_timetable():
    global timetable_data
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON data!"}), 400
    
    # Cập nhật timestamp
    data['last_updated'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    timetable_data = data
    
    # Ghi lại file
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(timetable_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({"message": "Updated successfully!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)