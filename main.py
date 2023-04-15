import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import os


class YTBatchDL:

    def __init__(self, main):
        self.main = main
        main.geometry('600x310')
        main.resizable(False, False)
        main.title("YouTube Batch Download")
        main.iconbitmap(r'youtube_icon.ico')
        main.configure(bg='white')

        self.links = []
        self.folder_path = ''
        self.title = ''
        self.is_all_processs_finished = False

        self.main_text_box = tk.Text(main, width=50, height=10, bg='white', fg='black')
        self.main_text_box.place(x=100, y=37)

        self.main_text_box_label = tk.Label(main, text='Paste YouTube link(s) here', bg='white', fg='black', font='Consolas')
        self.main_text_box_label.place(x=195, y=203)

        self.download_button = tk.Button(main, text="Download", command=self.store_and_download, width=44, height= 1, bg='#282828', font='Consolas', fg='white')
        self.download_button.place(x=100, y=230)

        self.combobox_options = ["MP3 - Audio Only", "MP4 - Video & Audio"]
        self.combo_box = ttk.Combobox(main, values=self.combobox_options, state="readonly", width=63)
        self.combo_box.current(0)
        self.combo_box.place(x=103, y=10)

        self.browse_folder_button = tk.Button(main, text="Save To", command=self.browse_folder, width=20, height=1,  bg='#282828', font='Consolas', fg='white')
        self.browse_folder_button.place(x=208, y=270)

    # function to browse for the folder where the files will be saved
    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        os.chdir(self.folder_path)

    # function to store the text from the main text box in a list separated per line and download the links
    def store_and_download(self):
        # Get the contents of the text box
        text = self.main_text_box.get('1.0', 'end')
        self.links = text.split()

        if len(self.links) == 0:
            messagebox.showinfo("Error", 'The list is empty.')
        else:
            for link in self.links:
                try:
                    yt = YouTube(link)
                    self.title = yt.title

                    # Create a Tkinter variable to hold the selected option
                    combo_box_choice = self.combo_box.get()

                    if combo_box_choice == "MP3 - Audio Only":
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

                    self.is_all_processs_finished = True 
                except:
                    messagebox.showinfo("Error", 'Something went wrong, Please try again.')

        if self.is_all_processs_finished == True:
            messagebox.showinfo("Download Complete!", "The download is complete.")
            self.is_all_processs_finished = False 

if __name__ == '__main__':
    root = tk.Tk()
    app = YTBatchDL(root)
    root.mainloop()
