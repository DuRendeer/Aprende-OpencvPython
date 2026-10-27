import os
import subprocess
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(PASTA, ".venv")
PYTHON_VENV = os.path.join(VENV, "Scripts", "python.exe")

if os.path.exists(PYTHON_VENV) and os.path.normcase(sys.prefix) != os.path.normcase(VENV):
    sys.exit(subprocess.call([PYTHON_VENV, os.path.abspath(__file__)]))

import cv2
import numpy as np
sys.path.insert(0, "partes")

from camera   import Camera
from detector import Detector
from midia    import Midia

LABELS = {
    "L":           "Lula la",
    "Bolsonaru": "Bolsonaroo!",
}

def main():
    cam      = Camera(indice=0)
    detector = Detector()
    midia    = Midia(pasta_sons="sons", pasta_imagens="imagens")

    preto = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.imshow("Teu Votu", preto)
    cv2.waitKey(1)

    while True:
        ok, frame = cam.ler_frame()
        if not ok:
            break

        frame, gesto = detector.processar(frame)
        midia.atualizar(gesto)

        label = LABELS.get(gesto, "Voto Nulo")
        cv2.putText(frame, label, (10, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        cv2.imshow("Tu", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.liberar()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()