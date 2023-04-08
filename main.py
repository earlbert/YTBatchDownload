# Import necessary modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pytube import YouTube
import os

# Define global variables
global links
links = []
global folder_path
folder_path = ''
global title

#function to browse for the folder where the files will be saved
def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    os.chdir(folder_path)

#function to store the text from the main text box in a list separated per line
def store_text():
    global links
    # Get the contents of the text box
    text = main_text_box.get('1.0', 'end')
    links = text.split()

    if len(links) == 0:
        messagebox.showinfo("Error", 'The list is empty.')

#function to download the links
def download_links():
    global title
    global links
    for link in links:
        try:
            yt = YouTube(link)
            title = yt.title
            # Create a Tkinter variable to hold the selected option
            combo_box_choice = combo_box.get()

            if combo_box_choice == "MP3":
                downloader = yt.streams.filter(only_audio = True).get_audio_only()
                print(f"Downloading: {title}")
                downloader.download()

                #converts downloaded file to mp3 (default is mp4)
                files_in_dir = os.listdir()
                for file in files_in_dir:
                    if file.endswith('.mp4'):
                        os.rename(file, os.path.splitext(file)[0] + '.mp3')
            else:
                downloader = yt.streams.get_highest_resolution()
                print(f"Downloading: {title}")
                downloader.download()
        except:
             messagebox.showinfo("Error", 'Not All Links Are Downloaded. Some Link(s) Does Not Exist.')

    #If there are no links or if the "Get Links" button was not clicked, show an error message
    if len(links) == 0:
        messagebox.showinfo("Error", 'The list is empty or you didnt click "Get Links".')

# Create the main window
window = tk.Tk()
window.geometry('600x300')
window.resizable(False, False)
window.title("YTD")
window.iconbitmap(r'youtube_icon.ico')
window.configure(bg = 'FireBrick')

# main text box for links input
main_text_box = tk.Text(window, width = 50, height = 10)
main_text_box.place(x = 100, y = 5)

main_text_box_label = tk.Label(window, text = 'Paste YouTube link(s) here')
main_text_box_label.place(x = 230, y = 173)

# button to store the links from the main text box into a list
store_button = tk.Button(window, text = "Save Links", command = store_text, width = 40)
store_button.place(x = 100, y = 200)

# select the file type to download
combobox_options = ["MP3", "MP4"]
combo_box = ttk.Combobox(window, values=combobox_options, state = "readonly", width = 14)
combo_box.current(0)
combo_box.place(x = 395, y = 200)

# button to download the links
download_button = tk.Button(window, text = "Download", command = download_links, width = 40)
download_button.place(x = 100, y = 230)

# button to browse for the folder where the files will be saved
browse_folder_button = tk.Button(window, text = "Save To", command = browse_folder, width = 14)
browse_folder_button.place(x = 395, y = 230)

window.mainloop()


