from collections.abc import Sequence

from bmi_map._mapper import LanguageMapper
from bmi_map._parameter import Parameter


class SidlMapper(LanguageMapper):
    def map(self) -> str:
        return f"int {self._name}({SidlMapper.map_params(self._params)});"

    @staticmethod
    def map_type(dtype: str) -> str:
        if dtype.startswith("array"):
            dtype, dims = Parameter.split_array_type(dtype)
            if dtype == "any":
                dtype = ""
            if dims:
                return f"array<{dtype.strip()}, {len(dims)}>"
            else:
                return f"array<{dtype.strip()},>"
        else:
            return dtype

    @staticmethod
    def map_params(params: Sequence[tuple[str, str, str]]) -> str:
        return ", ".join(
            [
                f"{name} {intent} {SidlMapper.map_type(dtype)}"
                for name, intent, dtype in params
            ]
        )