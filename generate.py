import warnings
warnings.filterwarnings("ignore", message="torch.nn.utils.weight_norm is deprecated in favor of torch.nn.utils.parametrizations.weight_norm")
warnings.filterwarnings("ignore", message="Error caught was: No module named 'triton'")

import os
from audiocraft.models import MusicGen
import torchaudio
import torch
from tqdm import tqdm

def get_audio_file_path(download_path):
    """Gets the first audio file found in the directory."""
    files = os.listdir(download_path)
    audio_files = [file for file in files if file.endswith(('.mp3', '.wav'))]
    if not audio_files:
        raise FileNotFoundError(f"No audio files found in directory: {download_path}")
    return os.path.join(download_path, audio_files[0])


def generate_music(text_prompt, download_path, seconds):
    """Generates music using the given text prompt and a melody from the download path."""
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        model.set_generation_params(duration=seconds)  # Set duration based on slider input

        audio_file_path = get_audio_file_path(download_path)
        melody, sr = torchaudio.load(audio_file_path)

        wav = model.generate_with_chroma([text_prompt], melody, sr, progress=lambda x: tqdm(x, desc="Generating Music", unit="step"))
        waveform = wav[0]
        if waveform.ndim == 3:
            waveform = waveform[0]

        waveform = waveform.cpu()
        output_file_name = f"generated_{text_prompt.replace(' ', '_')}_{seconds}s.wav"
        output_file_path = os.path.join(r'C:\Users\Zade\Documents\creative_code\music_ai\audiocraft\generated', output_file_name)
        torchaudio.save(output_file_path, waveform, sample_rate=model.sample_rate)
        return output_file_path
    except Exception as e:
        print(f"Error generating music: {e}")
        return None
