__all__ = [
        'SelfKey'
]

from dtfield import dataclass, Validator, ContextBase


@dataclass
class SelfKey(ContextBase):
    key: str = Validator(default=None, frozen=True, compare=False, label='Chave', hash=False)