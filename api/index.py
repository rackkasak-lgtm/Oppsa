from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# HTTP Connection pooling for maximum speed
session = requests.Session()

@app.route('/')
def status():
    return jsonify({"s": "ok", "m": "All-In-One Surya Serverless API is Live"}), 200

# 1. 🔍 OSINT / Lookup Endpoint (Number, Aadhaar, PAN, Vehicle)
# Usage: GET /api/lookup?q=TARGET&t=TYPE
@app.route('/api/lookup', methods=['GET'])
def lookup():
    query = request.args.get('q')
    l_type = request.args.get('t', 'num_to_all') 
    if not query:
        return jsonify({"e": "missing_query"}), 400
        
    url = "https://techvishalboss.com/api/v1/lookup.php"
    payload = {"key": "TVB_FULL_FF690A1C", "query": query, "type": l_type}
    try:
        res = session.get(url, params=payload, timeout=5.0)
        return jsonify({"s": "ok", "d": res.json()}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# 2. ⚡ Groq AI Chat Endpoint (Fastest AI)
# Usage: POST {"p": "your prompt"}
@app.route('/api/groq', methods=['POST'])
def groq():
    data = request.json or {}
    prompt = data.get('p')
    if not prompt:
        return jsonify({"e": "missing_prompt"}), 400
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": "Bearer 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", "Content-Type": "application/json"}
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
    try:
        res = session.post(url, json=payload, headers=headers, timeout=6.0)
        return jsonify({"s": "ok", "r": res.json()['choices'][0]['message']['content']}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# 3. 🧠 Mistral AI Chat Endpoint (Detailed AI)
# Usage: POST {"p": "your prompt"}
@app.route('/api/mistral', methods=['POST'])
def mistral():
    data = request.json or {}
    prompt = data.get('p')
    if not prompt:
        return jsonify({"e": "missing_prompt"}), 400
        
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": "Bearer FVKec5Xqa2ORzSoBrqi21nRbIM6rFk2q", "Content-Type": "application/json"}
    payload = {"model": "mistral-medium-latest", "messages": [{"role": "user", "content": prompt}]}
    try:
        res = session.post(url, json=payload, headers=headers, timeout=8.0)
        return jsonify({"s": "ok", "r": res.json()['choices'][0]['message']['content']}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# 4. 👁️ Vision API Endpoint (Analyze Images via Base64)
# Usage: POST {"img": "base64_string", "p": "prompt"}
@app.route('/api/vision', methods=['POST'])
def vision():
    data = request.json or {}
    base64_img = data.get('img')
    prompt = data.get('p', 'Describe this image')
    if not base64_img:
        return jsonify({"e": "missing_image"}), 400
        
    url = "https://dev-x-vision.vercel.app/api/vision"
    payload = {"image": base64_img, "prompt": prompt, "key": "devx-zxc4faa0a7vbsrqv2udmnhr5no8ii0pd"}
    try:
        res = session.post(url, json=payload, timeout=10.0)
        return jsonify({"s": "ok", "d": res.json()}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# 5. 🎵 Song Generator Endpoint
# Usage: POST {"p": "song description/lyrics"}
@app.route('/api/generatesong', methods=['POST'])
def generate_song():
    data = request.json or {}
    prompt = data.get('p')
    if not prompt:
        return jsonify({"e": "missing_prompt"}), 400
        
    url = "https://dev-x-song-gen-api.vercel.app/generate"
    payload = {"prompt": prompt}
    try:
        res = session.post(url, json=payload, timeout=15.0)
        return jsonify({"s": "ok", "d": res.json()}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# 6. 🎨 Image Edit Endpoint
# Usage: POST {"img": "image_url", "p": "editing prompt"}
@app.route('/api/editimage', methods=['POST'])
def edit_image():
    data = request.json or {}
    img_url = data.get('img')
    prompt = data.get('p')
    if not img_url or not prompt:
        return jsonify({"e": "missing_params"}), 400
        
    url = "https://dev-x-image-edit-api.vercel.app/edit"
    payload = {"image_url": img_url, "prompt": prompt, "key": "devx-6485ix1ckoyhbu38qcpaq3ir0mivgwik"}
    try:
        res = session.post(url, json=payload, timeout=12.0)
        return jsonify({"s": "ok", "d": res.json()}), 200
    except Exception as e:
        return jsonify({"e": "error", "m": str(e)}), 500

# Vercel serverless integration
def handler(environ, start_response):
    return app(environ, start_response)
