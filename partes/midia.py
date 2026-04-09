import pygame
import cv2
import numpy as np

pygame.mixer.init()

class Midia:
    def __init__(self, pasta_sons="sons", pasta_imagens="imagens"):
        self.sons = {
            "L":           pygame.mixer.Sound(f"{pasta_sons}/Lula.WAV"),
            "Bolsonaru": pygame.mixer.Sound(f"{pasta_sons}/Bolsonaro.WAV"),
        }
        self.imagens = {
            "L":           cv2.imread(f"{pasta_imagens}/Lula.png"),
            "Bolsonaru": cv2.imread(f"{pasta_imagens}/Bolsonaro.png"),
        }
        self.gesto_atual = None

    def atualizar(self, gesto):
        if gesto == self.gesto_atual:
            return

        if self.gesto_atual is not None:
            self.sons[self.gesto_atual].stop()

        self.gesto_atual = gesto

        if gesto is not None:
            self.sons[gesto].play(-1)
            img = self.imagens.get(gesto)
            if img is not None:
                img_redim = cv2.resize(img, (400, 400))
                cv2.imshow("Teu Votu", img_redim)
                cv2.waitKey(1)
        else:
            preto = np.zeros((400, 400, 3), dtype=np.uint8)
            cv2.imshow("Tu", preto)
            cv2.waitKey(1)