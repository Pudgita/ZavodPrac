import cv2


class CameraManager:
    """Подключается к камерам и получает по одному кадру с каждой."""

    def __init__(self, camera_addresses):
        # Словарь вида: имя камеры -> адрес видеопотока.
        self._cameras = {
            name: cv2.VideoCapture(address)
            for name, address in camera_addresses.items()
        }

    def get_frames(self):
        """Возвращает словарь имя камеры -> кадр или None, если кадр не получен."""
        frames = {}

        for name, camera in self._cameras.items():
            if not camera.isOpened():
                frames[name] = None
                continue

            success, frame = camera.read()
            frames[name] = frame if success else None

        return frames

    def close(self):
        """Освобождает подключения к камерам."""
        for camera in self._cameras.values():
            camera.release()


if __name__ == "__main__":
    cameras = {
        # Замени пример на адрес видеопотока, который дадут на заводе.
        # Одного IP может быть недостаточно: часто нужна полная RTSP-ссылка.
        "camera_1": "rtsp://IP-АДРЕС/ПУТЬ_ПОТОКА",
        # Для второй камеры добавь ещё одну строку:
        # "camera_2": "rtsp://IP-АДРЕС/ПУТЬ_ПОТОКА",
    }

    manager = CameraManager(cameras)

    try:
        frames = manager.get_frames()

        for camera_name, frame in frames.items():
            if frame is None:
                print(f"{camera_name}: кадр не получен")
            else:
                # frame — изображение в памяти; shape показывает высоту, ширину и каналы.
                print(f"{camera_name}: кадр получен, размер {frame.shape}")
                # Позже сюда можно будет передать кадр нейросети.
    finally:
        manager.close()
