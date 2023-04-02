import json
import os
import shutil
import subprocess
from pythumb import Thumbnail
from sys import platform
import xml.etree.ElementTree as ET

valid_locales = [
    "Cy-az-AZ",
    "Cy-sr-SP",
    "Cy-uz-UZ",
    "Lt-az-AZ",
    "Lt-sr-SP",
    "Lt-uz-UZ",
    "aa",
    "ab",
    "ae",
    "af",
    "af-ZA",
    "ak",
    "am",
    "an",
    "ar",
    "ar-AE",
    "ar-BH",
    "ar-DZ",
    "ar-EG",
    "ar-IQ",
    "ar-JO",
    "ar-KW",
    "ar-LB",
    "ar-LY",
    "ar-MA",
    "ar-OM",
    "ar-QA",
    "ar-SA",
    "ar-SY",
    "ar-TN",
    "ar-YE",
    "as",
    "av",
    "ay",
    "az",
    "ba",
    "be",
    "be-BY",
    "bg",
    "bg-BG",
    "bh",
    "bi",
    "bm",
    "bn",
    "bo",
    "br",
    "bs",
    "ca",
    "ca-ES",
    "ce",
    "ch",
    "co",
    "cr",
    "cs",
    "cs-CZ",
    "cu",
    "cv",
    "cy",
    "da",
    "da-DK",
    "de",
    "de-AT",
    "de-CH",
    "de-DE",
    "de-LI",
    "de-LU",
    "div-MV",
    "dv",
    "dz",
    "ee",
    "el",
    "el-GR",
    "en",
    "en-AU",
    "en-BZ",
    "en-CA",
    "en-CB",
    "en-GB",
    "en-IE",
    "en-JM",
    "en-NZ",
    "en-PH",
    "en-TT",
    "en-US",
    "en-ZA",
    "en-ZW",
    "eo",
    "es",
    "es-AR",
    "es-BO",
    "es-CL",
    "es-CO",
    "es-CR",
    "es-DO",
    "es-EC",
    "es-ES",
    "es-GT",
    "es-HN",
    "es-MX",
    "es-NI",
    "es-PA",
    "es-PE",
    "es-PR",
    "es-PY",
    "es-SV",
    "es-UY",
    "es-VE",
    "et",
    "et-EE",
    "eu",
    "eu-ES",
    "fa",
    "fa-IR",
    "ff",
    "fi",
    "fi-FI",
    "fj",
    "fo",
    "fo-FO",
    "fr",
    "fr-BE",
    "fr-CA",
    "fr-CH",
    "fr-FR",
    "fr-LU",
    "fr-MC",
    "fy",
    "ga",
    "gd",
    "gl",
    "gl-ES",
    "gn",
    "gu",
    "gu-IN",
    "gv",
    "ha",
    "he",
    "he-IL",
    "hi",
    "hi-IN",
    "ho",
    "hr",
    "hr-HR",
    "ht",
    "hu",
    "hu-HU",
    "hy",
    "hy-AM",
    "hz",
    "ia",
    "id",
    "id-ID",
    "ie",
    "ig",
    "ii",
    "ik",
    "io",
    "is",
    "is-IS",
    "it",
    "it-CH",
    "it-IT",
    "iu",
    "ja",
    "ja-JP",
    "jv",
    "ka",
    "ka-GE",
    "kg",
    "ki",
    "kj",
    "kk",
    "kk-KZ",
    "kl",
    "km",
    "kn",
    "kn-IN",
    "ko",
    "ko-KR",
    "kr",
    "ks",
    "ku",
    "kv",
    "kw",
    "ky",
    "ky-KZ",
    "la",
    "lb",
    "lg",
    "li",
    "ln",
    "lo",
    "lt",
    "lt-LT",
    "lu",
    "lv",
    "lv-LV",
    "mg",
    "mh",
    "mi",
    "mk",
    "mk-MK",
    "ml",
    "mn",
    "mn-MN",
    "mr",
    "mr-IN",
    "ms",
    "ms-BN",
    "ms-MY",
    "mt",
    "my",
    "na",
    "nb",
    "nb-NO",
    "nd",
    "ne",
    "ng",
    "nl",
    "nl-BE",
    "nl-NL",
    "nn",
    "nn-NO",
    "no",
    "nr",
    "nv",
    "ny",
    "oc",
    "oj",
    "om",
    "or",
    "os",
    "pa",
    "pa-IN",
    "pi",
    "pl",
    "pl-PL",
    "ps",
    "pt",
    "pt-BR",
    "pt-PT",
    "qu",
    "rm",
    "rn",
    "ro",
    "ro-RO",
    "ru",
    "ru-RU",
    "rw",
    "sa",
    "sa-IN",
    "sc",
    "sd",
    "se",
    "sg",
    "si",
    "sk",
    "sk-SK",
    "sl",
    "sl-SI",
    "sm",
    "sn",
    "so",
    "sq",
    "sq-AL",
    "sr",
    "ss",
    "st",
    "su",
    "sv",
    "sv-FI",
    "sv-SE",
    "sw",
    "sw-KE",
    "ta",
    "ta-IN",
    "te",
    "te-IN",
    "tg",
    "th",
    "th-TH",
    "ti",
    "tk",
    "tl",
    "tn",
    "to",
    "tr",
    "tr-TR",
    "ts",
    "tt",
    "tt-RU",
    "tw",
    "ty",
    "ug",
    "uk",
    "uk-UA",
    "ur",
    "ur-PK",
    "uz",
    "ve",
    "vi",
    "vi-VN",
    "vo",
    "wa",
    "wo",
    "xh",
    "yi",
    "yo",
    "za",
    "zh",
    "zh-CHS",
    "zh-CHT",
    "zh-CN",
    "zh-HK",
    "zh-MO",
    "zh-SG",
    "zh-TW",
    "zu"
]


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def download_thumbnails(pl_url, playlist_name):
    # Use yt-dlp to get the video URLs in the playlist
    if os.path.exists(f"{playlist_name}\\Thumbnails\\"):
        print("Already have thumbnails!")
        return
    video_urls = []
    video_ids = []
    command = f"yt-dlp --flat-playlist --get-id {pl_url}"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    print(output)
    real_output = output.splitlines()
    for id_part in real_output:
        real_url = "youtube.com/watch?v=" + id_part
        video_urls.append(real_url)
        video_ids.append(id_part)

    # Download the thumbnails for each video
    for i, video_url in enumerate(video_urls):
        # Use Pythumb to download the thumbnail
        t = Thumbnail(video_url)
        t.fetch()
        print(f"Downloaded thumbnail for video {i + 1}")
        filename = f"{i + 1}.jpg"
        t.save(f"{playlist_name}\\Thumbnails\\")
        print("filename: " + filename)
        os.rename(f"{playlist_name}\\Thumbnails\\" + video_ids[i] + ".jpg",
                  f"{playlist_name}\\Thumbnails\\" + f"{i + 1}.jpg")
        print(f"Renamed to: {playlist_name}\\Thumbnails\\" + f"{i + 1}.jpg")

    print("Thumbnails Downloaded! Finished!")


def download_video(pl_url, playlist_name):
    vids = False
    # Check if playlist directory already exists with videos
    if os.path.exists(playlist_name):
        if os.listdir(playlist_name):
            print("Already have videos")
            vids = True

    # Check if playlist file exists
    playlist_file = f"{playlist_name}\\{playlist_name}.xspf"
    if os.path.exists(playlist_file):
        print("Already have playlist!")
        return

    video_urls = []
    video_ids = []
    command = f"yt-dlp --flat-playlist --get-id {pl_url}"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    print(output)
    real_output = output.splitlines()
    for id_part in real_output:
        real_url = "https://youtube.com/watch?v=" + id_part
        video_urls.append(real_url)
        video_ids.append(id_part)

    if not vids:
        try:
            for i, url in enumerate(video_urls):
                subprocess.run(f"yt-dlp {url}", shell=True, check=True)
                for file in os.listdir():
                    if file.endswith(".webm"):
                        filename = f"{i + 1}. " + file
                        os.rename(file, filename)
                        shutil.move(filename, playlist_name)

            print("Videos Downloaded!")

        except Exception as e:
            print(f"Failed to download playlist {pl_url}: {e}")

    print("Generating playlist...")
    generate_xspf_playlist(playlist_name, video_ids)


def generate_xspf_playlist(playlist_name, video_ids):
    try:
        # generate XSPF playlist
        tracks = []
        for i, video_id in enumerate(video_ids):
            video_title = get_video_title(video_id)
            video_path = os.path.join(playlist_name, f"{i + 1}. {video_title}.webm")
            location = os.path.normpath(video_path)
            location = location.replace(fr"{playlist_name}\{playlist_name}", playlist_name)
            ext = os.path.splitext(video_path)[1]
            tracks.append({
                "location": location,
                "title": f"{i + 1}. {video_title.replace(ext, '')}{ext}",
                "creator": "",
                "duration": "",
                "album": "",
                "trackNum": str(i + 1),
                "annotation": "",
                "info": "",
                "image": ""
            })
        playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
        title_elem = ET.SubElement(playlist, "title")
        title_elem.text = playlist_name
        creator_elem = ET.SubElement(playlist, "creator")
        creator_elem.text = ""
        tracklist_elem = ET.SubElement(playlist, "trackList")
        for track in tracks:
            track_elem = ET.SubElement(tracklist_elem, "track")
            for key, value in track.items():
                if value:
                    elem = ET.SubElement(track_elem, key)
                    elem.text = value
        xspf_str = ET.tostring(playlist, encoding="unicode")

        # save XSPF playlist in the same folder as the videos
        playlist_path = os.path.join(".", playlist_name, f"{playlist_name}.xspf")
        if os.path.exists(playlist_path):
            return
        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write(xspf_str)

        print("XSPF playlist generated and saved!")

    except Exception as e:
        print(f"Failed to generate XSPF playlist {playlist_name}: {e}")


def get_video_title(video_id):
    # get video info using yt-dlp with the -j flag to output as json
    command = ["yt-dlp", "-j", f"https://www.youtube.com/watch?v={video_id}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # parse json output to get video title
    video_info = json.loads(output.decode("utf-8"))
    title = video_info["title"]

    return title


def DownloadPlaylist(download_thumbs=True, download_subtitles=False):
    lang_code = "en"
    p_url = input("Enter the YouTube playlist URL: ")
    if not p_url.startswith("https://") or p_url.startswith("youtube.com"):
        exit("Invalid link!")

    p_name = input("Playlist name: ")
    # Check if dir is not made and make it
    isExist = os.path.exists(p_name)

    if download_subtitles:
        lang_code = input("Input valid lang code (2 chars): ")
        if lang_code == "":
            lang_code = "en"
        if not valid_locales.__contains__(lang_code):
            exit("Invalid locale!")

    if not isExist:
        os.mkdir(p_name)

    download_video(p_url, p_name)  # Download videos in playlist (long process)
    if download_thumbs:
        download_thumbnails(p_url, p_name)  # Download thumbnails of those videos and names them numerically
    if download_subtitles:
        DownloadSubtitles(p_url, p_name, lang_code)

    print(f"{Color.GREEN}Downloaded playlist and finished process!{Color.END}\n{Color.CYAN}Enjoy the videos! :){Color.END}")


def ConvertVideosInFolder():
    path_to_vids = input("Input path to videos: ")
    video_files = []
    for dirpath, _, filenames in os.walk(path_to_vids):
        for f in filenames:
            video_files.append(os.path.abspath(os.path.join(dirpath, f)))

    print(f"{Color.CYAN}=----------------------------------------------={Color.END}")
    print(
        f"Select what format you want:\n{Color.BOLD}1.{Color.END} .mp4 {Color.BOLD}{Color.UNDERLINE}(default){Color.END}\n{Color.BOLD}2.{Color.END} .mov\n{Color.BOLD}3.{Color.END} .avi\n{Color.BOLD}4.{Color.END} .wmv\n{Color.BOLD}5.{Color.END} .mkv\n{Color.BOLD}6.{Color.END} .mpg")
    print(f"{Color.CYAN}=----------------------------------------------={Color.END}")
    vid_format = input("Input Option: ")

    if vid_format == "1":
        ext = ".mp4"
    elif vid_format == "2":
        ext = ".mov"
    elif vid_format == "3":
        ext = ".avi"
    elif vid_format == "4":
        ext = ".wmv"
    elif vid_format == "5":
        ext = ".mkv"
    elif vid_format == "6":
        ext = ".mpg"
    else:
        ext = ".mp4"

    for video_file in video_files:
        base_name = os.path.splitext(video_file)
        cmd = f'cmd /C ffmpeg -i "{video_file}" -c:v libx264 -qp 0 "{base_name[0] + ext}"'
        subprocess.run(cmd, shell=True, check=True)


def DownloadPlaylistThumbnails():
    url = input("Input playlist url: ")
    if not url.startswith("https://") or url.startswith("youtube.com"):
        exit("Invalid link!")

    # Use yt-dlp to get the video URLs in the playlist
    video_urls = []
    video_ids = []
    command = f"yt-dlp --flat-playlist --get-id {url}"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    print(output)
    real_output = output.splitlines()
    for id_part in real_output:
        real_url = "https://youtube.com/watch?v=" + id_part
        video_urls.append(real_url)
        video_ids.append(id_part)

    # Download the thumbnails for each video
    for i, video_url in enumerate(video_urls):
        # Use Pythumb to download the thumbnail
        t = Thumbnail(video_url)
        t.fetch()
        print(f"Downloaded thumbnail for video {i + 1}")
        filename = f"{i + 1}.jpg"
        t.save(f"Thumbnails\\")
        print("filename: " + filename)
        os.rename(f"Thumbnails\\" + video_ids[i] + ".jpg",
                  f"Thumbnails\\" + f"{i + 1}.jpg")
        print(f"Renamed to: Thumbnails\\" + f"{i + 1}.jpg")


def DownloadSubtitles(override_url="none", p_name="none", override_lang="none"):
    lang = "en"
    if os.path.exists(f"{p_name}\\Subtitles"):
        print("Already have subtitles!")
        return
    if override_url == "none":
        url = input("Input video / playlist url: ")
        if not url.startswith("https://") or url.startswith("youtube.com"):
            exit("Invalid link!")
    else:
        url = override_url

    if override_lang == "none":
        lang = input("Input valid lang code (2 chars): ")
        if not valid_locales.__contains__(lang):
            exit("Invalid locale!")

    if url.__contains__("list"):
        pl = True
    else:
        pl = False

    if pl:
        # Use yt-dlp to get the video URLs in the playlist
        video_urls = []
        command = f"yt-dlp --flat-playlist --get-id {url}"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        print(output)
        real_output = output.splitlines()
        for id_part in real_output:
            real_url = "https://youtube.com/watch?v=" + id_part
            video_urls.append(real_url)

        for video_url in video_urls:
            print("Checking if subs exist or not...")
            output = subprocess.check_output(f'yt-dlp -j {video_url}', shell=True)
            video_info = json.loads(output)

            # Check if the video has available subtitles
            if video_info['subtitles']:
                # Download subtitles in the default format
                subprocess.run(f'yt-dlp --no-download --write-sub --sub-lang {lang} {video_url}', shell=True,
                               check=True)
            else:
                # Download automatically generated subtitles in SRT format
                subprocess.run(f'yt-dlp --no-download --write-auto-sub --sub-lang {lang} {video_url}', shell=True,
                               check=True)

        if not os.path.exists("Subtitles"):
            os.mkdir("Subtitles")

        for filename in os.listdir():
            # Check if the file is a subtitle file
            if filename.endswith(".vtt") or filename.endswith(".srt"):
                # Move the file to the "Subtitles" folder
                shutil.move(filename, os.path.join("Subtitles", filename))
    else:
        print("Checking if subs exist or not...")
        output = subprocess.check_output(f'yt-dlp -j {url}', shell=True)
        video_info = json.loads(output)

        # Check if the video has available subtitles
        if video_info['subtitles']:
            # Download subtitles in the default format
            subprocess.run(f'yt-dlp --no-download --write-sub --sub-lang {lang} {url}', shell=True, check=True)
        else:
            # Download automatically generated subtitles in SRT format
            subprocess.run(f'yt-dlp --no-download --write-auto-sub --sub-lang {lang} {url}', shell=True, check=True)

        for filename in os.listdir():
            # Check if the file is a subtitle file
            if filename.endswith(".vtt") or filename.endswith(".srt"):
                # Move the file to the "Subtitles" folder
                shutil.move(filename, os.path.join("Subtitles", filename))

    if p_name != "none":
        shutil.move("Subtitles", f"{p_name}\\Subtitles")


if __name__ == "__main__":
    os.chdir("C:\\Users\\cflis\\OneDrive\\Desktop")
    if not platform == "win32":
        exit("This code only works on windows! Sorry")
    print(f"{Color.RED}YOUTUBE{Color.END} {Color.BLUE}PLAYLIST{Color.END} {Color.GREEN}DOWNLOADER{Color.END}")
    print(f"{Color.CYAN}================================================{Color.END}")
    print(
        f"Select what you want to do:\n{Color.BOLD}1.{Color.END} Download a full playlist with thumbnails {Color.BOLD}{Color.UNDERLINE}(default){Color.END}\n{Color.BOLD}2.{Color.END} Download a full playlist without thumbnails\n{Color.BOLD}3.{Color.END} Convert a folder with .webm's to a format using ffmpeg\n{Color.BOLD}4.{Color.END} Download thumbnails for an existing playlist\n{Color.BOLD}5.{Color.END} Download subtitles from a youtube video / playlist\n{Color.BOLD}6.{Color.END} Download a youtube playlist and subtitles\n{Color.BOLD}7.{Color.END} Download a youtube playlist with thumbnails and subtitles")
    print(f"{Color.CYAN}================================================{Color.END}")
    choice = input("Input Option: ")

    if choice == "1":
        DownloadPlaylist(True)
    elif choice == "2":
        DownloadPlaylist(False)
    elif choice == "3":
        ConvertVideosInFolder()
    elif choice == "4":
        DownloadPlaylistThumbnails()
    elif choice == "5":
        DownloadSubtitles()
    elif choice == "6":
        DownloadPlaylist(False, True)
    elif choice == "7":
        DownloadPlaylist(True, True)
    else:
        DownloadPlaylist(True)
