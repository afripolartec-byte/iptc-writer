import tempfile, os, subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route('/write-iptc', methods=['POST'])
def write_iptc():
    if 'image' not in request.files or 'title' not in request.form:
        return jsonify({'error': 'Missing image or title'}), 400
    
    image_file = request.files['image']
    title = request.form.get('title')
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        image_file.save(tmp.name)
        tmp_path = tmp.name
    
    subprocess.run([
        'exiftool',
        f'-IPTC:ObjectName={title}',
        f'-XMP-dc:title={title}',
        '-overwrite_original', tmp_path
    ], check=True)
    
    return send_file(tmp_path, mimetype='image/jpeg',
                     as_attachment=True, download_name=image_file.filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
