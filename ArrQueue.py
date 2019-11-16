import requests
import json

#Radarr
radarrAPI = 'https://radarr.com/api/queue?apikey=yourKeyHere'
radarrUsername = 'yourUsernameHere'
radarrPassword = 'yourPasswordHere'
radarrDiscordWebhook = 'yourWebhookURLHere'
radarrDiscordUserID = 'yourUserIDHere'

queue = json.loads(requests.get(radarrAPI, auth=(radarrUsername, radarrPassword)).content.decode('utf-8'))

for movie in queue:
    bad = False
    #print(movie['title']+": "+movie['trackedDownloadStatus'])
    try:
        if movie['trackedDownloadStatus'] == 'Warning':
            for status in movie['statusMessages'][0]:
                if 'XEM' not in status['messages'][0]:
                    bad = True
                    break

        if bad:
            result = requests.post(r''+radarrDiscordWebhook, data="{\"username\": \"Radarr\", \"content\": \"<@"+radarrDiscordUserID+"> stuck movies found in radarr\"}", headers={"Content-Type": "application/json"})
            break

    except KeyError:
        pass

#Sonarr
sonarrAPI = 'https://sonarr.com/api/queue?apikey=yourKeyHere'
sonarrUsername = 'yourUsernameHere'
sonarrPassword = 'yourPasswordHere'
sonarrDiscordWebhook = 'yourWebhookURLHere'
sonarrDiscordUserID = 'yourUserIDHere'

queue = json.loads(requests.get(sonarrAPI, auth=(sonarrUsername, sonarrPassword)).content.decode('utf-8'))

errors = []

for episode in queue:
    bad = False
    #print(episode['title']+": "+episode['trackedDownloadStatus'])
    try:
        if episode['trackedDownloadStatus'] == 'Warning':
            for status in episode['statusMessages']:
                if 'XEM' not in status['messages'][0] and 'TBA' not in status['messages'][0]:
                    bad = True
                    break
        if bad:
            if episode['title'] not in errors:
                result = requests.post(r''+sonarrDiscordWebhook, data="{\"username\": \"Sonarr\", \"content\": \"<@"+radarrDiscordUserID+"> stuck TV found in sonarr\"}", headers={"Content-Type": "application/json"})
                errors.append(episode['title'])
            break
    except KeyError:
        pass
