# server.py
from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = [
            {
                'format_id': f['format_id'],
                'ext': f['ext'],
                'resolution': f.get('height', 'audio-only'),
                'url': f.get('url')
            }
            for f in info.get('formats', [])
            if f.get('url')
        ]

        return jsonify({
            'success': True,
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'formats': formats
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
