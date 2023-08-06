import requests

def create(question, options, api_key, background='#228C22', foreground='#613B16', text='#FFFFFF', max_ip='1'):
    url = "https://polls.vishok.tech/api/create"
    params = {
        "question": question,
        "options": options,
        "background": background,
        "foreground": foreground,
        "text": text,
        "max": max_ip,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    response = response.json()
    if response['message'] == 'success':
        return response['poll_id']
    else:
        return response['message'], response['error']
    
def find(pid):
    url = "https://polls.vishok.tech/api/poll"
    params = {
        "poll_id": pid
    }
    response = requests.get(url, params=params)
    response = response.json()
    if response['message'] == 'success':
        return response
    else:
        return response['message'], response['error']

def vote(pid, vote):
    url = "https://polls.vishok.tech/api/vote"
    params = {
        "poll_id": pid,
        "vote": vote
    }
    response = requests.get(url, params=params)
    response = response.json()
    if response['message'] == 'success':
        return response
    else:
        return response['message'], response['error']

def delete(pid, api_key):
    url = "https://polls.vishok.tech/api/delete"
    params = {
        "poll_id": pid,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    response = response.json()
    if response['message'] == 'success':
        return True
    else:
        return response['message'], response['error']


