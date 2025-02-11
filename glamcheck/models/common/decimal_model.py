from decimal import Decimal

from pydantic import BaseModel, Field


class DecimalModel(BaseModel):
    value_before_division: int = Field(description="value before division")
    divisor_power: int = Field(description="divisor's power of 10", ge=0)

    def __init__(self, value: str):
        canonical_repr = str(Decimal(value))
        index_of_point = canonical_repr.find(".")

        # Value is integer
        if index_of_point == -1:
            value_before_division = int(canonical_repr)
            divisor_power = 0
        else:
            # Remove "." from representation of value
            value_before_division = int(str(canonical_repr).replace(".", ""))

            # Minus one because of character '.'
            divisor_power = len(canonical_repr) - index_of_point - 1

        super().__init__(value_before_division=value_before_division, divisor_power=divisor_power)

    def get_decimal(self) -> Decimal:
        s = str(self.value_before_division)

        # Result is integer
        if self.divisor_power == 0:
            return Decimal(s)

        # Add zeros after point. For example (value=23, divisor_power=4): "23" -> "0023"
        with_zeros = "0" * (self.divisor_power - len(s)) + s

        # Insert point
        with_point = with_zeros[:-self.divisor_power] + "." + with_zeros[-self.divisor_power:]

        return Decimal(with_point)
