from dataclass_bakery_patched.generators.random_generator import RandomGenerator
from typing import Any, Type

import random


class RandomEnumGenerator(RandomGenerator):
    def generate(self, enum_t: Type, *args, **kwargs) -> Any:
        return random.choice([opt for opt in enum_t])
