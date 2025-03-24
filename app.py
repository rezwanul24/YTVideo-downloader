from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os

app = Flask(__name__)

# Set download folder
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,  # Make yt-dlp quieter
    }

    try:
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_file = ydl.prepare_filename(info_dict)
        
        @after_this_request
        def cleanup(response):
            # Delete the video file after the download to save space
            try:
                os.remove(video_file)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(video_file, as_attachment=True, download_name=os.path.basename(video_file))

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Fix PORT issue
    app.run(host="0.0.0.0", port=port)  # Ensure no extra spaces here