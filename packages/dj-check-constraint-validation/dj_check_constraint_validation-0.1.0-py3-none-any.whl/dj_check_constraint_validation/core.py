import operator
import typing

from django.db.models import Q
from django.db.models.expressions import Combinable
from django.db.models.expressions import CombinedExpression
from django.db.models.expressions import F

expression_funcs = {
    Combinable.ADD: operator.add,
    Combinable.SUB: operator.sub,
    Combinable.MUL: operator.mul,
    Combinable.DIV: operator.truediv,
    Combinable.POW: operator.pow,
    Combinable.MOD: operator.mod,
}


def eval_q(q: Q, data: typing.Dict):
    """ """

    def eval_expression(expression):
        if isinstance(expression.lhs, CombinedExpression):
            lhs_value = eval_expression(expression.lhs)
        else:
            lhs_value = data[expression.lhs.name]
        rhs_value = data[expression.rhs.name]
        return expression_funcs[expression.connector](lhs_value, rhs_value)

    def eval_children(children, connector=Q.AND, result=True):
        if not children:
            return result

        child = children[0]
        if isinstance(child, Q):
            result = result and eval_children(child.children, child.connector, result)
            if child.negated:
                result = not result

        key = child[0]
        if isinstance(child[1], F):
            value = data[child[1].name]
        elif isinstance(child[1], CombinedExpression):
            value = eval_expression(child[1])
        else:
            value = child[1]

        if connector == Q.AND:
            result = result and (data[key] == value)
        else:
            result = result or (data[key] == value)
        return eval_children(children[1:], q.connector, result)

    result = eval_children(q.children)
    if q.negated:
        result = not result
    return result
