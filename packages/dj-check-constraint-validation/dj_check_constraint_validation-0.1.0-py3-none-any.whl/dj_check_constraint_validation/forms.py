from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint

from dj_check_constraint_validation.core import eval_q


class CheckConstraintsMixin:
    def validate_check_constraints(self):
        check_constraints = [
            constraint
            for constraint in self.Meta.model._meta.constraints
            if isinstance(constraint, CheckConstraint)
        ]
        errors = []
        for constraint in check_constraints:
            if not eval_q(constraint.check, self.cleaned_data):
                errors.append(
                    ValidationError(f"Check constraint {constraint.name} failed")
                )
        if errors:
            raise ValidationError(errors)

    def clean(self):
        self.validate_check_constraints()
        return super().clean()
