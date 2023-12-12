import time

from src.service import ERCService


class Application:
    def __init__(self, service: ERCService) -> None:
        self._service = service

    def run(self) -> None:
        while True:
            try:
                self._service.process_batch()
                time.sleep(1)
            except KeyboardInterrupt:
                break
