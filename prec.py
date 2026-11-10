import cv2
from ultralytics import YOLO

model = YOLO('yolov12n-face.pt')

class CameraModule:
    """Открывает видеопотоки и показывает каждую камеру в отдельном окне."""

    def __init__(self, addresses):
        # addresses — список URL IP-камер или индексов локальных камер (0, 1).
        self.addresses = list(addresses)
        self.cameras = []
        self.infer = 0 

    def run(self):
        try:
            for i, address in enumerate(self.addresses):
                camera = cv2.VideoCapture(address)
                self.cameras.append(camera)

                if not camera.isOpened():
                    raise ConnectionError(f"Не удалось открыть камеру {i + 1}")


            while self.cameras:
                self.infer += 1
                for i, camera in enumerate(self.cameras):

                    ok, frame = camera.read()

                    
                    if not ok:
                        raise RuntimeError(f"Нет кадра от камеры {i + 1}")

                    frame = cv2.flip(frame, 1)

                    if self.infer % 3 != 0:
                        continue

                    self.frame_ai = model.predict(frame)
                    self.image_ai = self.frame_ai[0].plot()

                    cv2.imshow(f"Camera {i + 1}", self.image_ai)


                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.close()

    def get_info(self):
        print(self.frame_ai[0].boxes)

    def close(self):
        for camera in self.cameras:
            camera.release()
        self.cameras.clear()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera_url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
    # module = CameraModule(addresses=[0, camera_url])
    module = CameraModule(addresses=[0])
    module.run()
    module.get_info()
