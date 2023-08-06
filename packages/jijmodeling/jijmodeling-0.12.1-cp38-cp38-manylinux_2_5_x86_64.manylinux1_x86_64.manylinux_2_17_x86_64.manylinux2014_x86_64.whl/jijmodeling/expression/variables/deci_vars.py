from __future__ import annotations

import warnings

from typing import List, Optional, Tuple, Union

from jijmodeling.deprecation.deprecation import deprecated_kwargs, deprecated_name
import jijmodeling.exceptions.exceptions as _exceptions
import jijmodeling.expression.expression as _expression
import jijmodeling.expression.type_annotations as _type_annotations
import jijmodeling.expression.variables.variable as _variable


class DecisionVariable(_variable.Variable):
    def __init__(
        self,
        label: str,
        shape: Union[
            List[_type_annotations.ShapeElemInputType],
            Tuple[_type_annotations.ShapeElemInputType, ...],
            _type_annotations.ShapeElemInputType,
        ],
        uuid: Optional[str] = None,
    ):
        if "[" in label or "]" in label:
            raise _exceptions.ModelingError(
                "The label of decision variable cannot contain '[' or ']'."
            )
        super().__init__(label, shape, uuid)  # type: ignore


class Binary(DecisionVariable):
    """Binary decision variable 0 or 1.

    Example:
        ```python
        import jijmodeling as jm
        n = jm.Placeholder("n")
        x = jm.Binary("x", shape=(n,))
        # scalar variable
        y = jm.Binary("y")
        ```
    """

    @deprecated_name("Binary", "BinaryVar", kind="class")
    def __init__(
        self,
        label: str,
        shape=(),
        uuid: Optional[str] = None,
    ):
        super().__init__(label, shape, uuid)

    @property
    @deprecated_name("label", "name", kind="property")
    def label(self) -> str:
        return self._label

    @property
    def name(self) -> str:
        return self._label
    
    @property
    @deprecated_name("dim", "ndim", kind="property")
    def dim(self) -> int:
        return len(self.shape)
    
    @property
    def ndim(self) -> int:
        return len(self.shape)


@deprecated_kwargs(
    changes={"label":"name"},
    removes=["uuid"]
)
def BinaryVar(
    label: str,
    *,
    shape=(),
    uuid: Optional[str] = None,
) -> Binary:
    """Binary decision variable 0 or 1.

    Example:
        ```python
        import jijmodeling as jm
        n = jm.Placeholder("n")
        x = jm.BinaryVar("x", shape=(n,))
        # scalar variable
        y = jm.BinaryVar("y")
        ```
    """
    return Binary(label, shape, uuid)


class Integer(DecisionVariable):
    """Integer decision variable."""

    prefix = "_leint_"

    @deprecated_name("Integer", "IntegerVar", kind="class")
    def __init__(
        self,
        label: str,
        lower: Union[_expression.Expression, int, float],
        upper: Union[_expression.Expression, int, float],
        shape: Union[
            List[_type_annotations.ShapeElemInputType],
            Tuple[_type_annotations.ShapeElemInputType, ...],
            _type_annotations.ShapeElemInputType,
        ] = (),
        uuid: Optional[str] = None,
    ):
        super().__init__(label, shape, uuid)

        if isinstance(lower, (int, float)):
            self._lower: _expression.Expression = _expression.Number(lower)
        else:
            self._lower = lower
        if isinstance(upper, (int, float)):
            self._upper: _expression.Expression = _expression.Number(upper)
        else:
            self._upper = upper

        # check if self._lower is operatable or self._lower.shape equals to
        # self.shape
        from jijmodeling.match.expr_same import expr_same

        def has_equal_shape(shape1, shape2):
            if len(shape1) != len(shape2):
                return False
            else:
                return all(
                    map(
                        lambda x: expr_same(x[0], x[1], check_id=False),
                        zip(list(shape1), list(shape2)),
                    )
                )

        if not (
            self._lower.is_operatable()
            or has_equal_shape(self._lower.shape, self.shape)
        ):  # type: ignore
            raise _exceptions.ModelingError(
                "self._lower must be operatable or self._lower.shape must be equal to self.shape"
            )

        if not (
            self._upper.is_operatable()
            or has_equal_shape(self._upper.shape, self.shape)
        ):  # type: ignore
            raise _exceptions.ModelingError(
                "self._upper must be operatable or self._upper.shape must be equal to self.shape"
            )

        import jijmodeling.expression.utils as _utils

        _utils.check_non_decision_variable(
            [self.lower, self.upper],
            f"The lower and upper of '{self.label}' cannot contain decision variable.",
        )

    @property
    @deprecated_name("label", "name", kind="property")
    def label(self) -> str:
        return self._label
    
    @property
    def name(self) -> str:
        return self._label
    
    @property
    @deprecated_name("dim", "ndim", kind="property")
    def dim(self) -> int:
        return super().dim
    
    @property
    def ndim(self) -> int:
        return super().dim

    @property
    @deprecated_name("lower", "lower_bound", kind="property")
    def lower(self) -> _expression.Expression:
        return self._lower
    
    @property
    def lower_bound(self) -> _expression.Expression:
        return self._lower

    @property
    @deprecated_name("upper", "upper_bound", kind="property")
    def upper(self):
        return self._upper
    
    @property
    def upper_bound(self) -> _expression.Expression:
        return self._upper

    def children(self) -> List[_expression.Expression]:
        children = super().children() + [self.lower, self.upper]
        return children


@deprecated_kwargs(
    changes={"label":"name", "lower":"lower_bound", "upper":"upper_bound" },
    removes=["uuid"]
)
def IntegerVar(
    label: str,
    *,
    lower: Union[_expression.Expression, int, float],
    upper: Union[_expression.Expression, int, float],
    shape: Union[
        List[_type_annotations.ShapeElemInputType],
        Tuple[_type_annotations.ShapeElemInputType, ...],
        _type_annotations.ShapeElemInputType,
    ] = (),
    uuid: Optional[str] = None,
) -> Integer:
    return Integer(label, lower, upper, shape, uuid)


def LogEncInteger(*args, **kwargs) -> Integer:
    """
    This constructor method is deprecated.

    Returns:
        Integer: Integer object.
    """
    warnings.warn("LogEncInteger is deprecated. Please use jijmodeling.Integer.")
    return Integer(*args, **kwargs)
