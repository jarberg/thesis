import time

from opengl_interfacing.utils import lightsplusminus

start_time = time.time()
av_start_time = start_time
counter = 0
lightCounter = 0

def fps_update():
    global fps_counter, av_start_time, start_time, time_per_frame, counter, lightCounter

    temp_time = (time.time() - start_time)

    if temp_time != 0:
        counter += 1
        if (time.time() - av_start_time) > 1:

            counter = 0

            av_start_time = time.time()

        time_per_frame = temp_time

    start_time = time.time()
    return time_per_frame





