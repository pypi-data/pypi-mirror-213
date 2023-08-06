__all__ = ['BaseEnum']


from dtfield import Enum

class BaseEnum(Enum):
    """Enum base model class"""
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return NotImplemented
    
    @classmethod
    def table(cls):
        return cls.__name__
    
    def json(self):
        return self.name
    
    @property
    def key(self):
        return self.name
    
    def __str__(self):
        return self.value
    
    @property
    def display(self):
        return self.value
    
    @classmethod
    def members(cls):
        return cls.__members__.values()
    
    @classmethod
    def option(cls, item: 'BaseEnum' = None, selected: bool = False):
        if not item:
            return '<option></option>'
        return f'<option id="{type(item).__name__}.{item.key}" value="{item.key}" ' \
               f'{"selected" if selected is True else ""}>{item.display}</option>'
    
    @classmethod
    def options(cls, default: str = None):
        if default:
            if isinstance(default, cls):
                default = default.name
        return ''.join([cls.option(), *[cls.option(member, member.key == default) for member in cls.members()]])

