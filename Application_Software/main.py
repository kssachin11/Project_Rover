from Layer_2.mqtt.mqtt_subscribe import MQTT_Subscribe
from Layer_1.camera.livefeed import CameraFeed
from queue import Queue
from threading import Thread
#from Layer_1.navigation.navigator import Navigator
from app import AppCommand, AppData


port = "/dev/ttyACM0"  # Replace with your actual port value
baudrate= 115200 # Replace with your actual baudrate value
address = 0x80
class Worker:
    def __init__(self,port,baudrate,address) -> None:
        
        self.appCommand = AppCommand()
        #self.appData = AppData()
        #self.navigator = Navigator()
        self.MqttSub = MQTT_Subscribe()
        #self.CamFeed = CameraFeed()

    def main(self):
        # Create the shared queue and launch all threads
        q1 = Queue() # for app command
        q2 = Queue() # for navigator target position

        t1 = Thread(
            target=self.appCommand.worker,
            args=(
                q1,
                q2,
            ),
        )

        t2 = Thread(target=self.MqttSub.subscribe_mqtt, args=(q1,))
        #t3 = Thread(target=self.CamFeed.camWorker)
        #t4 = Thread(target=self.appData.worker)
        #t5 = Thread(target=self.navigator.worker,args=(q2,))

        t1.start()
        t2.start()
        #t3.start()
        #t4.start()
        #t5.start()

        # Wait for all produced items to be consumed
        #t3.join()
        #q1.join()
        #q2.join()


if __name__ == "__main__":
    worker = Worker(port, baudrate, address)
    worker.main()
