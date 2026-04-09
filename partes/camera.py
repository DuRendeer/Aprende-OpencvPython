import cv2

class Camera:
    def __init__(self, indice=0):
        self.cap = cv2.VideoCapture(indice)
        if not self.cap.isOpened():
            raise RuntimeError("Num deu pra abri camera.")

    def ler_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        return True, cv2.flip(frame, 1)

    def liberar(self):
        self.cap.release()