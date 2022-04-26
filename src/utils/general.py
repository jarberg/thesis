import time

from opengl_interfacing.utils import lightsplusminus

start_time = time.time()
av_start_time = start_time
counter = 0
lightcount = 0
def fps_update(lightcount=0, height=400, renderer=None):
    global fps_counter, av_start_time, start_time, time_per_frame, counter

    tim = (time.time() - start_time)

    if tim != 0:
        counter += 1
        if (time.time() - av_start_time) > 1:
            if lightcount <=100:
               file2 = open(r"test_{}.txt".format(height), "a")
               txt = "{} \n".format(counter / (time.time() - av_start_time))
               txt = txt.replace(".", ",")
               file2.writelines(txt)
               file2.close()

            #print("FPS: ",   counter/(time.time() - av_start_time))
            counter = 0
            lightsplusminus(lightcount, renderer)
            av_start_time = time.time()

        time_per_frame = tim
        #print("FPS: ", 1 / tim)

    start_time = time.time()





