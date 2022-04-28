import time

from opengl_interfacing.utils import lightsplusminus

start_time = time.time()
av_start_time = start_time
counter = 0
lightCounter = 0

def fps_update(height=1200, renderer=None):
    global fps_counter, av_start_time, start_time, time_per_frame, counter, lightCounter

    temp_time = (time.time() - start_time)

    if temp_time != 0:
        counter += 1
        if (time.time() - av_start_time) > 1:
            if lightCounter <=0.2:
               file2 = open(r"test_{}.txt".format(height), "a")
               txt = "{} \n".format(counter / (time.time() - av_start_time))
               txt = txt.replace(".", ",")
               file2.writelines(txt)
               file2.close()

            #print("FPS: ",   counter/(time.time() - av_start_time))
            counter = 0
            lightCounter = lightsplusminus(lightCounter,renderer)
            av_start_time = time.time()

        time_per_frame = temp_time
        #print("FPS: ", 1 / tim)

    start_time = time.time()





