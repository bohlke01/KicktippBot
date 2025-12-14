from abc import ABC, abstractmethod


class BasePredictor(ABC):
    """Abstract base class for all predictors."""

    @abstractmethod
    def predict(self, data) -> list[list[int]]:
        pass

    @abstractmethod
    def fit(self, data, labels):
        pass
