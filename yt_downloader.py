from pytube import YouTube
import ffmpeg
import os
import threading
import re

# Costants
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ORANGE = "\033[95m"
MAGENTA = "\033[96m"
GRAY = "\033[97m"
END = "\033[0m"

# Change the file extension of the file at the given path according to the given type
# If type = "video", then before the extension, (video) will be added
# If type = "audio", then before the extension, (audio) will be added
def rename_file(old_path, type):
    new_path = old_path
    if type == "video":
        # Add (video) before the extension
        extension = old_path[old_path.rfind("."):]
        new_path = old_path.replace(extension, " (video)" + extension)
    elif type == "audio":
        # Add (audio) before the extension
        extension = old_path[old_path.rfind("."):]
        new_path = old_path.replace(extension, " (audio)" + extension)
    try:
        os.rename(old_path, new_path)
    except:
        print(RED + "Error renaming file" + END)

# Merge the audio and video files into a new file with the title of the video using ffmpeg
def mergingFile(video_path, audio_path, output_path):
    try:
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)

        # merging the audio and video files and converting the output file to mp4 format (video or audio could be webm format)
        ffmpeg.output(video, audio, output_path, vcodec="copy", acodec="aac").run()

        print("\n" + GREEN + "Video and audio files merged successfully!!" + END)

        # Removing the audio and video files
        os.remove(video_path)
        os.remove(audio_path)
    except:
        print(RED + "Error merging audio and video files!! Splitted files are saved in the same folder as the program, but they are not merged!!" + END)
        print(ORANGE + "You can merge them manually using ffmpeg: ffmpeg -i "  + video_path + " -i " + audio_path + " -c:v copy -c:a aac " + output_path + END)

def printDetails(yt, i):
    print(MAGENTA + "\nDetails for Video", i, "\n" + END)
    print("Title of video:   ", yt.title)
    print("Number of views:  ", yt.views)
    print("Length of video:  ", yt.length, "seconds")

    # Getting the highest resolution possible
    stream = str(yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first())
    print("Video resolution: ", stream[stream.find("res=")+4:stream.find("fps")-1])
    print("Video fps:        ", stream[stream.find("fps=")+4:stream.find("vcodec")-1])

# Ask the user if he wants to download the video or not
# If yes, return True else return False
def askingPermissionToDownload():
    print(YELLOW + "\nDo you want to download this video? (Y/n):   " + END, end="")
    choice = input()
    if choice == 'y' or choice == 'Y':
        return True
    elif choice == 'n' or choice == 'N':
        return False
    else:
        return True 


def checkInstallation():
    # Check if pytube is installed or not
    try:
        import pytube
    except:
        # print error message in red color
        print(RED + "pytube is not installed!!" + END)
        print(GRAY + "Installing pytube..." + END)
        os.system("pip install pytube")
        print(GRAY + "pytube installed successfully!!" + END)

    # Check if ffmpeg is installed or not
    try:
        import ffmpeg
    except:
        print(RED + "ffmpeg is not installed!!" + END)
        print(GRAY + "Installing ffmpeg..." + END)
        os.system("pip install ffmpeg")
        print(GRAY + "ffmpeg installed successfully!!" + END)


# Main function
def main():
    checkInstallation()
    
    # Asking for the number of videos to download
    print(YELLOW + "Enter the number of videos you want to download: " + END, end="")
    n = int(input())

    # Asking for the links of the videos to download
    links = []
    print(YELLOW + "\nEnter all the links one per line:" + END)
    for i in range(0, n):
        temp = input()
        links.append(temp)

    # Showing all details for videos and downloading them one by one
    for i in range(0,n):
        link = links[i]
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        yt._age_restricted = True    # To download age restricted videos
        yt.bypass_age_gate()         # To download age restricted videos

        printDetails(yt, i+1)
        
        if askingPermissionToDownload():
            try:
                print("\nDownloading video...")

                yt_video = yt.streams.filter(type="video").order_by('resolution').desc().first()
                yt_video.download()

                rename_file(os.getcwd() + "\\" + str(yt_video.default_filename), "video")
            except:
                print(RED + "Error downloading video!!" + END)
                # Skip to the next video
                continue

            try:
                print("\nDownloading audio...")

                yt_audio = yt.streams.filter(type="audio").order_by('abr').desc().first()
                yt_audio.download()

                rename_file(os.getcwd() + "\\" + str(yt_audio.default_filename), "audio")
            except:
                print(RED + "Error downloading audio!!" + END)
                # Skip to the next video
                continue

            # Merging the audio and video files into a new file with the title of the video.
            # Both audio and video starts at the same time at 0 seconds
            try:
                # Get the path of the video and audio files
                default_filename_no_extension = yt_video.default_filename[:yt_video.default_filename.rfind(".")]
                video_path = os.getcwd() + "\\" + default_filename_no_extension + " (video)" + yt_video.default_filename[yt_video.default_filename.rfind("."):]
                audio_path = os.getcwd() + "\\" + default_filename_no_extension + " (audio)" + yt_audio.default_filename[yt_audio.default_filename.rfind("."):]

                # Start the thread and do not wait for it to finish
                t = threading.Thread(target=mergingFile, args=(video_path, audio_path, os.getcwd() + "\\" + default_filename_no_extension + ".mp4"))
                t.start()

            except:
                print(RED + "Error merging audio and video files!! Splitted files are saved in the same folder as the program, but they are not merged!!" + END)
                # Skip to the next video
                continue

            print(GREEN + "\nVideo downloaded successfully!!" + END)
        else:
            print(GRAY + "\nVideo skipped!!" + END)

if __name__ == "__main__":
    main()