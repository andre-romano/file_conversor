# src/file_conversor/utils/ema_eta.py

import time

from file_conversor.utils.validators import is_close


class EmaEta:
    """ 
    Estimates ETA (Estimated Time of Arrival) using an Exponential Moving Average (EMA) approach.
    This class tracks the progress of a task and estimates the remaining time based on the speed of progress.
    """

    def __init__(self, alpha: float = 0.5) -> None:
        """ 
        Initializes the EmaEta estimator. The alpha parameter controls the smoothing factor for the EMA calculation. 

        :param alpha: Smoothing factor for EMA (0 < alpha <= 1). Higher values give more weight to recent progress.
        """
        super().__init__()
        self._last_time: float = time.time()
        self._last_progress: int = 0

        self._avg_speed: float = 0.0  # seconds per 1% progress
        self._alpha: float = alpha    # EMA smoothing factor

    def estimate_eta(self, progress: int) -> str:
        if is_close(progress, 0):
            return "..."
        if is_close(progress, 100):
            return "00:00:00"  # Task completed, no time remaining

        current_time = time.time()

        delta_progress = progress - self._last_progress
        delta_time = current_time - self._last_time

        if delta_progress > 0:
            current_speed = float(delta_time / delta_progress)
            if is_close(self._avg_speed, 0.0):
                self._avg_speed = current_speed
            else:
                self._avg_speed = (self._alpha * current_speed) + ((1 - self._alpha) * self._avg_speed)

        # Atualiza os marcadores para a próxima vez que a função for chamada
        self._last_time = current_time
        self._last_progress = progress

        # O tempo restante é a velocidade média suavizada multiplicada pelo que falta
        remaining = self._avg_speed * (100 - progress)

        minutes, seconds = divmod(int(remaining), 60)
        hours, minutes = divmod(int(minutes), 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


__all__ = [
    "EmaEta",
]
