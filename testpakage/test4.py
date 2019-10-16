import requests
import configparser
import time

streams_current = {}
usernames = 'muse_tw', 'latteda_', 'twnickcan'



def main():
    starttime = time.time()

    while True:
        mainloop()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

def mainloop():
    print("running main loop")
    global streams_current

    print("Current list of stream ids: {}".format(list(streams_current.keys())))

    # Get the current status of all users
    streams_new = get_streams()
    # Compare against the previous iteration of the loop
    # If this is the first time, streams_current will be empty so everything will be
    # new
    streamids_status = compare_streams(streams_current, streams_new)
    # Announce changes
    announce_streams(streamids_status, streams_current, streams_new)
    # copy new streams list to main list for next loop
    streams_current = streams_new


def get_streams():
    streams = {}
    headers = {'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'}
    width = 640
    height = 360


    for user in usernames:
        print("Checking {}".format(user))
        # note: the API url is something like: api.twitch.tv/kraken/streams/hannibal127
        r = requests.get('https://api.twitch.tv/helix/streams', params={'user_login': [f'{user}']}, headers=headers)
        res = r.json()

        print(res)

        if res['data'] != []:
            stream_id = res['data'][0]['id']
            streams[stream_id] = {}
            streams[stream_id]['username'] = user
            streams[stream_id]['url'] = 'https://www.twitch.tv/' + user
            streams[stream_id]['game'] = res['data'][0]['user_name']
            streams[stream_id]['status'] = res['data'][0]['title']
            streams[stream_id]['preview_l'] = res['data'][0]['thumbnail_url']
            streams[stream_id]['preview_l'] = streams[stream_id]['preview_l'].replace('{width}', '640')
            streams[stream_id]['preview_l'] = streams[stream_id]['preview_l'].replace('{height}', '360')
            print(streams[stream_id]['preview_l'.format(width, height)])

    return streams


def compare_streams(streams_current, streams_new):
    streamids_changed = {}
    streamids_changed['offline'] = []
    streamids_changed['online'] = []

    print("Current streams: {}".format(list(streams_current.keys())))
    print("New streams:     {}".format(list(streams_new.keys())))

    for key in streams_current:
        if key not in streams_new:
            streamids_changed['offline'].append(key)

    for key in streams_new:
        if key not in streams_current:
            streamids_changed['online'].append(key)

    print("Streams that just went offline: {}".format(streamids_changed['offline']))
    print("Streams that just went online:  {}".format(streamids_changed['online']))

    return streamids_changed


def announce_streams(streamids_changed, streams_current, streams_new):
    for streamid in streamids_changed['online']:
        ann_text = "{} has gone live on Twitch!".format(streams_new[streamid]['username'])
        att_text = "{}\nStatus: {}\nGame: {}".format(
            streams_new[streamid]['url'],
            streams_new[streamid]['status'],
            streams_new[streamid]['game'])

        payload = {
            'content': ann_text,
            'embeds': [
                {
                    'color': '#00FF00',
                    'text': att_text,
                    'image_url': streams_new[streamid][f'preview_l']
                }
            ]
        }

        p = requests.post('', json=payload)
        q = requests.post('', json=payload)



if __name__ == "__main__":
    main()