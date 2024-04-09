from re import M
from Layers.L1_App.mqtt.mqtt_subscribe import MQTT_Subscribe
from Layers.L1_App.camera.livefeed import CameraFeed
from queue import Queue
from app import AppCommand, Navigator, AppData, manoeuvre
from threading import Thread
class Worker:
    def __init__(self) -> None:
        self.appCommand = AppCommand()
        print("init appCommand")
        self.navigator = Navigator()
        print("init navigator")
        self.MqttSub = MQTT_Subscribe()
        print("init MqttSub")
        self.AppData = AppData()
        print("init AppData")
        self.CamFeed = CameraFeed()
        print("init CamFeed")

        #self.manouver = manoeuvre()

    def main(self):
        # Create the shared queue
        print("main")
        q1 = Queue()  # for app command
        q2 = Queue()  # for navigator target position
        """ appCommand will keep checking the queue for the command from the mobile app."""
        t1 = Thread(target=self.appCommand.worker,args=(q1,q2,),)
        print("init thread 1")
        """ MqttSub will keep checking the mqtt broker for the data and queue it."""
        t2 = Thread(target=self.MqttSub.subscribe_mqtt, args=(q1,))
        print("init thread 2")
        """ AppData publishes the data to the mqtt broker. 
            when q2 is obtained the worker logs the coordinates for navigation"""
        t3 = Thread(target=self.AppData.worker, args=(q2,))
        print("init thread 3")
        """ navigator thread will only work if there is a target position in the queue.
        It will keep checking the queue and if there is a target position it will generate the 
        shortest path. Once the path is generated it will clear the queue."""
        t4 = Thread(target=self.navigator.worker, args=(q2,)) 
        print("init thread 4")
        """ CamFeed will open webcam and shre the frames to mobile app."""
        #t5 = Thread(target=self.CamFeed.camWorker)
        #print("init thread 5")
        
        # Start the threads
        t1.start()  
        print("thread 1 started")
        t2.start()
        print("thread 2 started")
        t3.start()
        print("thread 3 started")
        t4.start()
        print("thread 4 started")
        #t5.start()
        #print("thread 5 started")
        
        # Wait for the threads to finish
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
if __name__ == "__main__":
    worker = Worker()
    worker.main()