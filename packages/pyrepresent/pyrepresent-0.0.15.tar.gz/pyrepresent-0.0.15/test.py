# test.py

import pandas as pd
import numpy as np

from represent import BaseModel

class Model(BaseModel):

    def __init__(self) -> None:

        self.self = self
        self.type = type(self)

        self.values = [1, 2, 3]

        self.objects = {
            'self': self.self,
            'type': self.type,
            self.self: self.self,
            self.type: self.type,
            (1, 2, 3): self.values
        }
        self.objects['data'] = self.objects

        self.zero = 0

        self.data = pd.DataFrame({1: [1, 2, 3]})
        self.array = np.array([[1, 2, 3], [4, 5, 6]])
    # end __init__
# Model

class Data(BaseModel):

    __slots__ = "x", "y"

    def __init__(self):

        self.x = 0
        self.y = 0
    # end __init__
# end Data

def main() -> None:
    """Tests the module."""

    print(Model())
    print(Data())
# end main

if __name__ == "__main__":
    main()
# end if