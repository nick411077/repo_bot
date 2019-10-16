import time
import sys
import configparser
import discord
from discord.ext import commands

import requests
import zc.lockfile


twitch_client_id = 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'
twitch_user = 'muse_tw'
stream_api_url = 'https://api.twitch.tv/helix/streams'
stream_url = None
discord_url = ''
discord_message = ':mega: {{Name}} is live now, playing {{Game}}! Sassy Squad Assemble! @here'
lock = None
image_priority = None
discord_description = 'Come watch me!'

def main():
    twitch_json = {'data': []}
    while len(twitch_json['data']) == 0:
        twitch_headers = {'Client-ID': twitch_client_id}
        twitch_params = {'user_login': twitch_user.lower()}
        twitch_request = requests.get(stream_api_url, headers=twitch_headers, params=twitch_params)
        twitch_json = twitch_request.json()

        if len(twitch_json['data']) == 1:
            print("Stream is live.")

            stream_json = twitch_json['data'][0]
            stream_title = stream_json['title']
            stream_game_id = stream_json['game_id']
            stream_preview_temp = stream_json['thumbnail_url']
            stream_preview_temp = stream_preview_temp.replace('{width}', '1280')
            stream_preview_temp = stream_preview_temp.replace('{height}', '720')
            preview_request = requests.get(stream_preview_temp)
            if '404' not in preview_request.url:
                stream_preview = stream_preview_temp
            else:
                stream_preview = None

            game_search_url = "https://api.twitch.tv/helix/games"
            game_headers = {'Client-ID': twitch_client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            game_params = {'id': stream_game_id}
            game_request = requests.get(game_search_url, headers=game_headers, params=game_params)
            search_response = game_request.json()

            stream_game = "something"
            game_logo = None
            if len(search_response['data']) > 0:
                game_data = search_response['data'][0]
                stream_game = game_data['name']
                game_logo_temp = game_data['box_art_url']
                game_logo_temp = game_logo_temp.replace('{width}', '340')
                game_logo_temp = game_logo_temp.replace('{height}', '452')
                logo_request = requests.get(game_logo_temp)
                if '404' not in logo_request.url:
                    # Scrub ./ from the boxart URL if present so it works with the Discord API properly
                    game_logo = game_logo_temp.replace('./', '')

            user_search_url = "https://api.twitch.tv/helix/users"
            user_headers = {'Client-ID': twitch_client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            user_params = {'login': twitch_user.lower()}
            user_request = requests.get(user_search_url, headers=user_headers, params=user_params)
            user_response = user_request.json()

            user_logo = None
            print(str(user_response))
            if len(user_response['data']) == 1:
                user_data = user_response['data'][0]
                user_logo_temp = user_data['profile_image_url']
                logo_request = requests.get(user_logo_temp)
                if '404' not in logo_request.url:
                    # Scrub ./ from the boxart URL if present so it works with the Discord API properly
                    user_logo = user_logo_temp.replace('./', '')

            global discord_description
            discord_description = discord_description.replace('{{Name}}', twitch_user)
            discord_description = discord_description.replace('{{Game}}', stream_game)
            global discord_message
            discord_message = discord_message.replace('{{Name}}', twitch_user)
            discord_message = discord_message.replace('{{Game}}', stream_game)

            if image_priority == "Game":
                if game_logo:
                    stream_logo = game_logo
                else:
                    if stream_preview:
                        stream_logo = stream_preview
                    else:
                        stream_logo = user_logo
            else:
                if stream_preview:
                    stream_logo = stream_preview
                else:
                    if game_logo:
                        stream_logo = game_logo
                    else:
                        stream_logo = user_logo

            discord_payload = {
                "content": discord_message,
                "embeds": [
                    {
                        "title": stream_title,
                        "url": stream_url,
                        "description": discord_description,
                        "image": {
                            "url": stream_logo
                        }
                     }
                ]
            }

            status_code = 0
            while status_code != 204:
                discord_request = requests.post(discord_url, json=discord_payload)
                status_code = discord_request.status_code

                if discord_request.status_code == 204:
                    print("Successfully called Discord API. Waiting 5 seconds to terminate...")
                    time.sleep(5)
                else:
                    print("Failed to call Discord API. Waiting 5 seconds to retry...")
                    time.sleep(5)
        else:
            print("Stream is not live. Waiting 5 seconds to retry...")
            time.sleep(5)

main()
