from operator import le

from simpleruleengine.operator.numeric_operator import NumericOperator


class Lte(NumericOperator):
    def __init__(self, base_value):
        super().__init__(base_value)

    def evaluate(self, value_to_evaluate):
        return le(value_to_evaluate, self._base_value)
