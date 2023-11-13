import os 
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

def authenticate_youtube():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "api.json"  # Replace with the path to your client_secret.json file

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, ["https://www.googleapis.com/auth/youtube"]
    )
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    return youtube

def create_playlist(youtube, playlist_name, playlist_description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": playlist_description
            },
            "status": {
                "privacyStatus": "private"
            }
            }
        )
    response = request.execute()
    return response['id']

def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

def main():
    youtube = authenticate_youtube()
    playlist_tittle = "Musicas Tunais dos Caloiros"
    video_titles = []
    
    with open("list.json", "r") as f:
        video_titles = json.load(f)
    
    playlist_id = create_playlist(youtube, playlist_tittle, "Musicas Tunais dos Caloiros")
    for video_title in video_titles:
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=video_title
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        add_video_to_playlist(youtube, playlist_id, video_id)

    print("Playlist criada com sucesso!")

if __name__ == "__main__":
    main()