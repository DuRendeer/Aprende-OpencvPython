import cv2
import mediapipe as mp
import math

class Detector:
    def __init__(self):
        self._mp_hands = mp.solutions.hands
        self._mp_draw  = mp.solutions.drawing_utils
        self.hands = self._mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def processar(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = self.hands.process(rgb)
        gesto = None

        if resultado.multi_hand_landmarks:
            for hand_lm in resultado.multi_hand_landmarks:
                self._mp_draw.draw_landmarks(
                    frame, hand_lm, self._mp_hands.HAND_CONNECTIONS
                )
                gesto = self._detectar_gesto(hand_lm.landmark)

        return frame, gesto

    def _outros_fechados(self, lm):
        for ponta, mcp in [(12, 9), (16, 13), (20, 17)]:
            if lm[ponta].y < lm[mcp].y:
                return False
        return True

    def _detectar_gesto(self, lm):
        if not self._outros_fechados(lm):
            return None

        ind_tip = lm[8]
        wrist   = lm[0]

        dx = ind_tip.x - wrist.x
        dy = ind_tip.y - wrist.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 0.1:
            return None

        angulo = math.degrees(math.atan2(-dy, dx))

        if 45 < angulo <= 135:
            return "L"

        if -45 <= angulo <= 45 or angulo > 135 or angulo < -45:
            return "Bolsonaru"

        return None