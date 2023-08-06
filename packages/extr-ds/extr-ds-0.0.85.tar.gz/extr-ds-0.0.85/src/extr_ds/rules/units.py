from typing import List, Callable
from extr.entities import AbstractEntityExtractor
from .majority import InferenceResult
from ..labelers.iob import IOB

class StaticUnit():
    def __init__(self, tokenize: Callable[[str], List[str]], extractor: AbstractEntityExtractor):
        self._iob = IOB(tokenize, extractor)

    def __call__(self, text):
        labels = self._iob.label(text).labels
        return InferenceResult(
            labels=labels,
            confidences=[.90 if label == 'O' else .99 for label in labels],
            weight=1
        )
