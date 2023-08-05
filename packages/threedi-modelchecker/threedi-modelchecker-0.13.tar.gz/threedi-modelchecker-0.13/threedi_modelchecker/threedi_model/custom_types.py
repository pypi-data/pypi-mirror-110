from sqlalchemy.types import Integer
from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import VARCHAR


class CustomEnum(TypeDecorator):
    """Column type for storing integer python enums.

    The CustomEnum will make use of the backend 'impl' datatype to store
    the data. Data is converted back it's enum_class python object if possible.
    If not, the raw 'impl' is returned.

    CustomEnum should not be used directly but inherited by a class which
    provides the `impl` datatype.
    """

    def __init__(self, enum_class):
        """

        :param enum_class: instance of enum.Enum
        """
        super().__init__()
        self.enum_class = enum_class
        self.enums = [e.value for e in enum_class]

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_class):
            return value.value
        else:
            return value

    def process_result_value(self, value, dialect):
        if value in self.enums:
            return self.enum_class(value)
        else:
            return value


class IntegerEnum(CustomEnum):
    """Column type for storing integer python enums.

    The CustomEnum will make use of the backend 'impl' datatype to store
    the data. Data is converted back it's enum_class python object if possible.
    If not, the raw 'impl' is returned.

    CustomEnum should not be used directly but inherited by a class which
    provides the `impl` datatype.
    """

    impl = Integer


class VarcharEnum(CustomEnum):

    impl = VARCHAR
