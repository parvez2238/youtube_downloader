import yt_dlp as youtube_dl
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def download_audio(song_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        #'ffmpeg_location': '/path/to/ffmpeg',  # Specify the path to ffmpeg
        #'ffprobe_location': '/path/to/ffprobe',  # Specify the path to ffprobe
        'quiet': True,  # Suppress output
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([song_url])
            return {'success': True, 'message': 'Download successful!'}
        except youtube_dl.utils.DownloadError as e:
            return {'success': False, 'message': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def handle_download():
    song_url = request.form.get('song_url')
    output_dir = request.form.get('output_dir')

    if not song_url or not output_dir:
        return jsonify({'success': False, 'message': 'Missing song URL or output directory.'})

    result = download_audio(song_url, output_dir)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
