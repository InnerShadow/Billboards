import os

class MP4FileManager:
    def __init__(self, last_downloaded_mp4):
        self.last_downloaded_mp4 = last_downloaded_mp4

        with open("Data/memory.txt", 'r') as f:
            self.max_folder_size = int(f.read()) * 1024 * 1024


    def get_mp4_files_in_data_folder(self):
        mp4_files = [f for f in os.listdir("Data") if f.endswith(".mp4")]
        return mp4_files


    def get_file_size(self, filename):
        return os.path.getsize(os.path.join("Data", filename))


    def delete_mp4_file(self, filename):
        os.remove(os.path.join("Data", filename))


    def manage_mp4_files(self):
        mp4_files = self.get_mp4_files_in_data_folder()
        while sum(self.get_file_size(filename) for filename in mp4_files) > self.max_folder_size:
            for filename in mp4_files:
                if filename != self.last_downloaded_mp4:
                    self.delete_mp4_file(filename)
                    mp4_files.remove(filename)

