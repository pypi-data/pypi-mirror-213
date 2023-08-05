from typing import Dict, Any, List

from pyhon.parameter.base import HonParameter


def str_to_float(string: str | float) -> float:
    try:
        return int(string)
    except ValueError:
        return float(str(string).replace(",", "."))


class HonParameterRange(HonParameter):
    def __init__(self, key: str, attributes: Dict[str, Any], group: str) -> None:
        super().__init__(key, attributes, group)
        self._min: float = str_to_float(attributes["minimumValue"])
        self._max: float = str_to_float(attributes["maximumValue"])
        self._step: float = str_to_float(attributes["incrementValue"])
        self._default: float = str_to_float(attributes.get("defaultValue", self.min))
        self._value: float = self._default

    def __repr__(self):
        return f"{self.__class__} (<{self.key}> [{self.min} - {self.max}])"

    @property
    def min(self) -> float:
        return self._min

    @min.setter
    def min(self, mini: float) -> None:
        self._min = mini

    @property
    def max(self) -> float:
        return self._max

    @max.setter
    def max(self, maxi: float) -> None:
        self._max = maxi

    @property
    def step(self) -> float:
        if not self._step:
            return 1
        return self._step

    @step.setter
    def step(self, step: float) -> None:
        self._step = step

    @property
    def value(self) -> str | float:
        return self._value if self._value is not None else self.min

    @value.setter
    def value(self, value: str | float) -> None:
        value = str_to_float(value)
        if self.min <= value <= self.max and not (value - self.min) % self.step:
            self._value = value
            self.check_trigger(value)
        else:
            raise ValueError(f"Allowed: min {self.min} max {self.max} step {self.step}")

    @property
    def values(self) -> List[str]:
        return [str(i) for i in range(int(self.min), int(self.max) + 1, int(self.step))]
