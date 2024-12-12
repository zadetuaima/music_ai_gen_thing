import warnings
warnings.filterwarnings("ignore", message="A matching Triton is not available, some optimizations will not be enabled. Error caught was: No module named 'triton'")
from flask import Flask, render_template, request, jsonify
import os
import download
import generate  # Import the new generation logic

app = Flask(__name__)
app.config["DEBUG"] = True

# Define a path for saving downloads (server-side)
DOWNLOADS_FOLDER = os.path.join(os.getcwd(), 'downloads')  # Ensure this folder exists
if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_and_generate', methods=['POST'])
def download_and_generate():
    """Downloads a song and generates new music based on the genre input."""
    playlist_url = request.form.get('playlist_url')
    genre = request.form.get('genre')
    seconds = request.form.get('seconds')

    try:
        if not playlist_url:
            return jsonify({"success": False, "message": "No playlist URL provided"}), 400

        if not genre:
            return jsonify({"success": False, "message": "No genre provided"}), 400

        if not seconds:
            return jsonify({"success": False, "message": "No duration provided"}), 400

        # Step 1: Download the playlist/track
        if "spotify.com" in playlist_url:
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            download.download_path = DOWNLOADS_FOLDER  # Update the download path
            download.download_spotify_playlist(playlist_id)
        elif "soundcloud.com" in playlist_url:
            download.download_path = DOWNLOADS_FOLDER  # Update the download path
            download.download_soundcloud_playlist(playlist_url)
        else:
            return jsonify({"success": False, "message": "URL not recognized"}), 400

        # Step 2: Generate new music with the melody and duration
        output_file_path = generate.generate_music(genre, DOWNLOADS_FOLDER, int(seconds))  # Pass seconds as an argument
        if output_file_path:
            return jsonify({"success": True, "message": "Music generated successfully!", "file_path": output_file_path})
        else:
            return jsonify({"success": False, "message": "Music generation failed"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
