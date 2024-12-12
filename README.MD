# README

Welcome to the Music AI Generator Thing bot V1. This has been built using Meta's Audiocraft, take a melody from a spotify song of your choosing, and combine it with a genre description to generate a song.
This particular script is to be used with Flask.

## Installation

Install audiocraft first by cloning in the repository.


```bash
git clone https://github.com/facebookresearch/audiocraft
cd audiocraft
```

Proceed with installing pytorch 2.0.1 and ffmpeg. The version of pytorch matching 2.0.1 is imperative. 


```bash
# Install pytorch
pip install 'torch>=2.0'

# Install ffmpeg
sudo apt-get install ffmpeg
# Or if you are using Anaconda or Miniconda
conda install 'ffmpeg<5' -c  conda-forge
```

The prerequisites of audiocraft should now be installed on your device. To use the script please then clone in all of the other files/folders from this repository into your audiocraft folder. 

```bash
git clone https://github.com/zadetuaima/music_ai_gen_thing
```

All the files should follow the path /usr/audiocraft/the_rest_of_your_cloned_in_files (do not place them in a folder within your audiocraft folder)

Now we can proceed to install the rest of the packages with:

```bash
pip install -r requirements.txt
```

Finally begin with flask

```bash
flask run
```

## Preperation

A Spotify API key is needed:

**Spotify API setup:**

Spotify API credentials, create a new application within the Spotify developer tab to get a client_id, client_secret, redirect and a username

### Example JSON for Spotify credentials

```json
{
    "username": "",
    "client_id": "",
    "client_secret": "",
    "redirect": ""
}
```

## Usage

- Paste a spotify song URL into the URL input.

- Give the bot a prompt to go off. This should be based around a genre and the 'vibe' you want the generated music to give off.

- Select the generated song length. 10s+ lengths will cause heavy CPU usage and may crash your computer if you have less than 8 cores.

## Advanced

- The model can also be changed. NOTE for musicgen-melody-large YOU MUST HAVE A GPU ON YOUR DEVICE, otherwise it will break your computer.

- The bitrate of the downloaded Spotify song can also be changed, with 320kbps being high quality and 128kpbs being low.

## Prompt Examples

- UK Drum and Bass with a wobbly bass
- Berlin techno
- Japanese flute, lofi hiphop, music for studying
- 90s rock song with electric guitar and heavy drums
- Beautiful piano masterpiece

