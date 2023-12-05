from pytube import Search, YouTube
import ffmpy
from pprint import pp

# put output path where the initial song (double audio) is to be saved and put the path to save the actual path from the ffmpeg in save_track
output = "/Users/divnoor/PycharmProjects/spotify-song-downloader/track_downloads/bad_file/"
save_track = "/Users/divnoor/PycharmProjects/spotify-song-downloader/track_downloads/tracks/"


def youtube_search(query):
    """searches youtube for one song"""
    search_list = []
    search = Search(query)
    for result_no in range(2):
        search_title = search.results[result_no].title
        search_url = search.results[result_no].watch_url
        search_list.append(search_url)
    return search_list


def youtube_download(query, track_name):
    """downloads the required track"""
    track_to_download = YouTube(query, use_oauth=True, allow_oauth_cache=True)
    filtered = track_to_download.streams.filter(only_audio=True)
    track_itag = filtered[0].itag
    stream_to_download = track_to_download.streams.get_by_itag(track_itag)
    file_name_save = track_name
    stream_to_download.download(
        output_path=output,
        filename=f"{file_name_save}.mp3"
    )
    ff = ffmpy.FFmpeg(
        inputs={f"{output}{file_name_save}.mp3": None},
        outputs={f"{save_track}{file_name_save}.mp4": None}
    )
    ff.run()
