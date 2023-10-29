import pygame
import tempfile
import os

from moviepy.editor import VideoFileClip

class VideoPlayer:
    def __init__(self, video_url : str):
        self.video_url = video_url

    def play(self, start_time = 0):
        video = VideoFileClip(self.video_url)

        pygame.init()
        screen = pygame.display.set_mode((int(video.size[1] * 1.75), video.size[0] // 1.75))

        running = True

        clock = pygame.time.Clock()
        t = start_time

        audio = video.audio

        pygame.mixer.init(frequency = audio.fps, size = -16, channels=audio.nchannels)

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

        pygame.quit()
