import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import os


class YTBatchDL:
    def __init__(self, main):
        self.main = main
        main.geometry('600x300')
        main.resizable(False, False)
        main.title("YouTube Batch Download")
        main.iconbitmap(r'youtube_icon.ico')
        main.configure(bg='FireBrick')

        self.links = []
        self.folder_path = ''
        self.title = ''

        self.main_text_box = tk.Text(main, width=50, height=10)
        self.main_text_box.place(x=100, y=5)

        self.main_text_box_label = tk.Label(main, text='Paste YouTube link(s) here')
        self.main_text_box_label.place(x=230, y=173)

        self.store_button = tk.Button(main, text="Save Links", command=self.store_text, width=40)
        self.store_button.place(x=100, y=200)

        self.combobox_options = ["MP3", "MP4"]
        self.combo_box = ttk.Combobox(main, values=self.combobox_options, state="readonly", width=14)
        self.combo_box.current(0)
        self.combo_box.place(x=395, y=200)

        self.download_button = tk.Button(main, text="Download", command=self.download_links, width=40)
        self.download_button.place(x=100, y=230)

        self.browse_folder_button = tk.Button(main, text="Save To", command=self.browse_folder, width=14)
        self.browse_folder_button.place(x=395, y=230)

    #function to browse for the folder where the files will be saved
    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        os.chdir(self.folder_path)

    #function to store the text from the main text box in a list separated per line
    def store_text(self):
        # Get the contents of the text box
        text = self.main_text_box.get('1.0', 'end')
        self.links = text.split()

        if len(self.links) == 0:
            messagebox.showinfo("Error", 'The list is empty.')

    #function to download the links
    def download_links(self):
        for link in self.links:
            try:
                yt = YouTube(link)
                self.title = yt.title

                # Create a Tkinter variable to hold the selected option
                combo_box_choice = self.combo_box.get()

                if combo_box_choice == "MP3":
                    downloader = yt.streams.filter(only_audio=True).get_audio_only()
                    print(f"Downloading: {self.title}")
                    downloader.download()

                    #converts downloaded file to mp3 (default is mp4)
                    files_in_dir = os.listdir()
                    for file in files_in_dir:
                        if file.endswith('.mp4'):
                            os.rename(file, os.path.splitext(file)[0] + '.mp3')
                else:
                    downloader = yt.streams.get_highest_resolution()
                    print(f"Downloading: {self.title}")
                    downloader.download()
            except:
                messagebox.showinfo("Error", 'Not All Links Are Downloaded. Some Link(s) Does Not Exist.')

        #If there are no links or if the "Get Links" button was not clicked, show an error message
        if len(self.links) == 0:
            messagebox.showinfo("Error", 'The list is empty or you didnt click "Get Links".')


if __name__ == '__main__':
    root = tk.Tk()
    app = YTBatchDL(root)
    root.mainloop()
