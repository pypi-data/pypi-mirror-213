from simpleaudio import *
import time


class myPlayObject(PlayObject):
    def __init__(self, play_id):
        super().__init__(play_id)

    def stop(self):
        pass

    def wait_done(self, frame_time=0.05):
        if self.is_playing:
            time.sleep(frame_time)
