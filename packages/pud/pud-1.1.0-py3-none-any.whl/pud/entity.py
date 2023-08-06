from datetime import datetime


class Entity:
    """Represents an entity to display on the screen.

    Attributes
    ----------
    name:
        The name of the entity.

    size:
        The human readable size of the entity.

    is_file:
        Indicates if this entity is a file or not.

    last_modified:
        The human readable representation of the date
        when this entity was last modified.
    """

    def __init__(
        self,
        name: str,
        size: str,
        is_file: bool,
        last_modified: datetime,
    ):
        self._name = name
        self._size = size
        self._is_file = is_file
        self._last_modified = last_modified

        if self._is_file:
            self.emoji = "📄"
        else:
            self.emoji = "📁"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def size(self) -> str:
        if self.is_file:
            return self._size
        return ""

    @property
    def is_file(self) -> bool:
        return self._is_file

    @property
    def last_modified(self) -> str:
        return self._last_modified

    def __repr__(self) -> str:
        return f"{self.emoji} {self.name if self.is_file else '/' + self.name}"
