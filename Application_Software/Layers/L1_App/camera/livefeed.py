import websockets
import time
import asyncio
import cv2, base64
import numpy as np


# The above class is a Python implementation of the Singleton design pattern using metaclasses.
class Singleton_meta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CameraFeed(metaclass=Singleton_meta):
    def __init__(self) -> None:
        self.port = 8000
        print("Starting server on port : ", self.port)

        self.frame_rate = 10
        self.cameraPort = 0

    def reduceQuality(self, cap):
        _, frame = cap.read()
        #print("original image size: {}".format(frame.shape))

        p = 0.9
        new_width = int(frame.shape[1] * p)
        new_height = int(frame.shape[0] * p)

        resized = cv2.resize(
            frame, (new_width, new_height), interpolation=cv2.INTER_AREA
        )
        #print("resized image size: {}".format(resized.shape))
        return resized

    async def transmit(self, websocket, path):
        """
        This is an asynchronous function that captures frames from a webcam, reduces their quality,
        encodes them in base64, and sends them over a WebSocket connection to a client.
        
        :param websocket: A WebSocket object representing the connection between the server and the
        client
        :param path: The path parameter in the transmit function is the URL path requested by the client
        to establish a WebSocket connection. It is used by the server to identify the WebSocket
        connection and handle incoming messages from the client
        """
        print("Client Connected !")
        try:
            prev = 0

            cap = cv2.VideoCapture(self.cameraPort)

            while cap.isOpened():
                time_elapsed = time.time() - prev
                frame = self.reduceQuality(cap)

                if time_elapsed > 1.0 / self.frame_rate:
                    prev = time.time()
                    encoded = cv2.imencode(".jpg", frame)[1]

                    data = str(base64.b64encode(encoded))
                    data = data[2 : len(data) - 1]

                    await websocket.send(data)

            cap.release()

        except websockets.connection.ConnectionClosed as e:
            print("Client Disconnected !")
            cap.release()

        except:
            print("Someting went Wrong with webcam !")

    def camWorker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        start_server = websockets.serve(self.transmit, port=self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()





