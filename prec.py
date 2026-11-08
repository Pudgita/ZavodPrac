import cv2


class CameraModule:
    """Открывает видеопотоки и показывает каждую камеру в отдельном окне."""

    def __init__(self, addresses):
        # addresses — список URL IP-камер или индексов локальных камер (0, 1).
        self.addresses = list(addresses)
        self.cameras = []

    def run(self):
        try:
            for i, address in enumerate(self.addresses):
                camera = cv2.VideoCapture(address)
                self.cameras.append(camera)

                if not camera.isOpened():
                    raise ConnectionError(f"Не удалось открыть камеру {i + 1}")

            while self.cameras:
                for i, camera in enumerate(self.cameras):
                    ok, frame = camera.read()

                    if not ok:
                        raise RuntimeError(f"Нет кадра от камеры {i + 1}")

                    cv2.imshow(f"Camera {i + 1}", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.close()

    def close(self):
        for camera in self.cameras:
            camera.release()
        self.cameras.clear()
        cv2.destroyAllWindows()


# if __name__ == "__main__":
#     camera_url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
#     module = CameraModule(addresses=[0, camera_url])
#     module.run()
module = CameraModule(
    addresses=["rtsp://127.0.0.1:1/unavailable"]
)
module.run()