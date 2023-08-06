from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict, Union

from pandas import DataFrame, Series

from ayed.classes import Variable

PathLike = Union[Path, str]
PandasDF = Union[DataFrame, dict[str, DataFrame]]
Sheet = Union[DataFrame, Series]


class File(TypedDict):
    filenames: list[str]
    structs: list[str]
    variables: list[Variable]


Files = list[dict[str, File]]

@dataclass
class ReadSheetException(Exception):
    message: str
    
    def __str__(self) -> str:
        return self.message