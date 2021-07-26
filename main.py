from multiprocessing import Process
from bluetooth_detector import bluetooth_loop
from movement_detection import movement_detection_loop

if __name__ == '__main__':
    p = Process(target=bluetooth_loop)
    p.start()
    p = Process(target=movement_detection_loop)
    p.start()
    p.join()
