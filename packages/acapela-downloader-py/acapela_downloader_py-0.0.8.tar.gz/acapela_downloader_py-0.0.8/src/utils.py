import random
import string
import re
from requests import post

NONCE_ENDPOINT = "https://acapelavoices.acapela-group.com/index/getnonce/"
SYNTHESIZER_ENDPOINT = "https://www.acapela-group.com:8443/Services/Synthesizer"
cached_nonce = ""
cached_email = ""


def update_nonce_token():
    global NONCE_ENDPOINT
    global cached_nonce
    global cached_email
    global last_failed
    EMAIL_LENGTH = random.randint(10, 20)
    fake_email = ""
    for i in range(EMAIL_LENGTH):
        fake_email += random.choice(string.ascii_letters)
    fake_email += "@gmail.com"
    nonce_response = post(NONCE_ENDPOINT, json={
        "googleid": fake_email
    })
    if len(nonce_response.json()["nonce"]) > 1:
        cached_nonce = nonce_response.json()["nonce"]
        cached_email = fake_email


def get_sound_link(text, voice_id):
    update_nonce_token()
    finished = False
    while not finished:
        try:
            synthesizer_request_string = f"req_voice={voice_id}&cl_pwd=&cl_vers=1-30&req_echo=ON&cl_login=AcapelaGroup&req_comment=%7B%22nonce%22%3A%22{cached_nonce}%22%2C%22user%22%3A%22{cached_email}%22%7D&req_text={text}&cl_env=ACAPELA_VOICES&prot_vers=2&cl_app=AcapelaGroup_WebDemo_Android"
            synthesizer_request_bytes = bytes(synthesizer_request_string, 'utf-8')
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Content-Length': str(len(synthesizer_request_bytes))}
            synthesizer_request = post(SYNTHESIZER_ENDPOINT, headers=headers, data=synthesizer_request_string)
            split_res = re.split('&snd_url=|&snd_size', str(synthesizer_request.content))
            finished = True
            return split_res[1]
        except:
            print("generating new nonce")
            update_nonce_token()
    return ""



