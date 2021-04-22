from abc import ABC, abstractmethod


class BaseTask(ABC):
    @abstractmethod
    def get_url(self):
        """ Should return url for task """