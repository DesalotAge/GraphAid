from typing import NamedTuple, Optional


class Station(NamedTuple):
    id: int
    railway: str
    customhouse: str
    name: str
    x_coord: Optional[float]
    y_coord: Optional[float]
