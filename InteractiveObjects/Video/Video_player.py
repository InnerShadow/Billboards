import os
import pygame
import tempfile
import threading

from moviepy.editor import VideoFileClip

from PyQt5.QtCore import pyqtSignal, QObject

from InteractiveObjects.Video.Video_downloader import VideoDownloader

from Entity.Schedules import Schedules
from InteractiveObjects.Video.MP4FileManager import MP4FileManager
from Entity.User import User

#Video player based on pygame
class VideoPlayer(QObject):
    not_finished = pyqtSignal(bool)

    def __init__(self, video_url : str, schedule : Schedules, user : User, x_pos : int, y_pos : int):
        super().__init__()
        self.video_url = video_url
        self.schedule = schedule

        self.user = user
        self.x_pos = x_pos
        self.y_pos = y_pos


    #Play video option
    def play(self, start_time : int):
        video = VideoFileClip(self.video_url)

        pygame.init()
        screen = pygame.display.set_mode((int(video.size[1] * 1.75), video.size[0] // 1.75))

        running = True

        clock = pygame.time.Clock()
        t = start_time

        audio = video.audio

        pygame.mixer.init(frequency = audio.fps, size = -16, channels = audio.nchannels)

        with tempfile.NamedTemporaryFile(delete = False, suffix = ".mp3") as temp_audio_file:
            audio.write_audiofile(temp_audio_file.name)

        pygame.mixer.music.load(temp_audio_file.name)

        #beat video by frames and play one by one with audio
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Close event
                    running = False

            frame = video.get_frame(t)

            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            pygame.mixer.music.play(0, t)
            t += 1 / video.fps
            clock.tick(video.fps)

            if t >= video.duration:
                break

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        os.remove(temp_audio_file.name)

        #Play next and if prev was not closed
        if running:
            self.not_finished.emit(running)

        pygame.quit()


    #Handler new playing ad
    def play_next(self):
        #Find ad_id base on schedule
        next_ad_id = 1

        for ad in self.schedule.ad_queue:
            next_ad_id += 1
            if self.video_url == ad.vidio_url:
                break
            
        if next_ad_id >= len(self.schedule.ad_queue):
            next_ad_id = 0

        self.next_ad = self.schedule.ad_queue[next_ad_id]

        #Tell server that i gonna eatch newxt ad
        watch_request = f"WATCH AD ad = {self.next_ad.ad_name}"
        _ = self.user.client.Get_response(watch_request)

        #Check if i have current .mp4 file
        if not os.path.exists(self.next_ad.vidio_url):
            #If not do download it 
            self.video_downloader = VideoDownloader(self.next_ad.vidio_url, self.user.client, self.x_pos, self.y_pos)

            #Then check if memory limit not passed
            self.mp4FileManager = MP4FileManager(self.next_ad.vidio_url)
            self.mp4FileManager.manage_mp4_files()

            #Than play video
            self.video_downloader.finished.connect(self.on_download_finished)
            self.video_downloader.start()

        else:
            #Simply play video
            self.on_download_finished()


    #Video player performans
    def on_download_finished(self):
        self.video_player = VideoPlayer(self.next_ad.vidio_url, self.schedule, self.user, self.x_pos, self.y_pos)
        playback_thread = threading.Thread(target = self.video_player.play, args = (0, ))
        playback_thread.start()

