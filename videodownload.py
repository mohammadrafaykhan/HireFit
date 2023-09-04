# Import the necessary libraries/modules
from pytube import YouTube
from sys import argv

# Get the YouTube video URL from command line arguments
link = argv[1]

# Create a YouTube object using the provided video URL
yt = YouTube(link)

# Print the title of the YouTube video
print("Title: ", yt.title)

# Print the number of views of the YouTube video
print("Views: ", yt.views)

# Get the highest resolution video stream
yd = yt.streams.get_highest_resolution()

# Specify the folder where you want to save the downloaded video
# Change './YTfolder' to your desired folder path
download_folder = "./YTfolder"

# Download the video to the specified folder
yd.download(download_folder)

# Print a message indicating that the download is complete
print("Download completed!")
