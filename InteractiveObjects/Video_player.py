import os
import pygame
import tempfile
import threading

from moviepy.editor import VideoFileClip

from InteractiveObjects.Video_downloader import VideoDownloader

from Entity.Schedules import Schedules
from Entity.MP4FileManager import MP4FileManager
from Entity.User import User

class VideoPlayer:
    def __init__(self, video_url : str, schedule : Schedules, user : User, x_pos : int, y_pos : int):
        self.video_url = video_url
        self.schedule = schedule

        self.user = user
        self.x_pos = x_pos
        self.y_pos = y_pos


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

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

        os.remove(temp_audio_file.name)

        if running:
            self.play_next()

        else:
            pygame.quit()


    def play_next(self):
        next_ad_id = 1

        for ad in self.schedule.ad_queue:
            next_ad_id += 1
            if self.video_url == ad.vidio_url:
                break
            
        if next_ad_id >= len(self.schedule.ad_queue):
            next_ad_id = 0

        self.next_ad = self.schedule.ad_queue[next_ad_id]

        watch_request = f"WATCH AD ad = {self.next_ad.ad_name}"
        _ = self.user.client.Get_response(watch_request)

        if not os.path.exists(self.next_ad.vidio_url):
            self.video_downloader = VideoDownloader(self.next_ad.vidio_url, self.user.client, self.x_pos, self.y_pos)

            self.mp4FileManager = MP4FileManager(self.next_ad.vidio_url)
            self.mp4FileManager.manage_mp4_files()

            self.video_downloader.finished.connect(self.on_download_finished)
            self.video_downloader.start()

        else:
            self.on_download_finished()


    def on_download_finished(self):
        self.video_player = VideoPlayer(self.next_ad.vidio_url, self.schedule, self.user, self.x_pos, self.y_pos)
        playback_thread = threading.Thread(target = self.video_player.play, args = (0, ))
        playback_thread.start()

