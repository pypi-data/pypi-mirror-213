import requests

from utils import get_sound_link


def generate_audio(txt, voice="", file_output="out.mp3"):
    if voice == "":
        voice = "enu_willhappy_22k_ns.bvcu"
    link = get_sound_link(txt, voice)
    if link != "":
        res = requests.get(link, allow_redirects=True)
        open(file_output, 'wb').write(res.content)
    else:
        raise Exception("AcapelaDownloader: Failed to get audio file link.")