from django.db.models import Sum, Case, Value, When, IntegerField


def BooleanSum(field):
    return Sum(
        Case(
            When(then=Value(1), **{field: True}),
            default=0,
            output_field=IntegerField()
            )
        )
