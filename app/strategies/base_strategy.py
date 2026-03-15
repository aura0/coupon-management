from abc import ABC, abstractmethod

class CouponStrategy(ABC):

    @abstractmethod
    def calculate(self, cart, details):
        pass