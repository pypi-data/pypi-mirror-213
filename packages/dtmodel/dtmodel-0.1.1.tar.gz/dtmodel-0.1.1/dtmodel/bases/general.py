__all__ = [
        'Address',
        'Phone',
        'Email',
        'RequiredName',
        'OptionalName',
        'Date',
        'Created',
        'Description',
        'Active',
        'Search',
        'Price',
        'Percentage',
        'Start',
        'End'
	]

from dtfield import dataclass, Validator, ContextBase, datetime, Decimal, normalize_lower, ModelMap
from ..functions import *


@dataclass
class Active(ContextBase):
    active: bool = Validator(default=True)
    
    
@dataclass
class Start(ContextBase):
    start: datetime.datetime = Validator(default_factory=local_now, label='início')
    
    
@dataclass
class End(ContextBase):
    end: datetime.datetime = Validator(post_init_factory=local_now, label='final')
    
    
@dataclass
class Price(ContextBase):
    price: Decimal = Validator()
    
    
@dataclass
class Address(ContextBase):
    address: str = Validator(default_factory=str, repr=False, compare=False)
    city: str = Validator(default_factory=str, compare=False)
    
    
@dataclass
class Phone(ContextBase):
    phone: str = Validator(default_factory=str, compare=False)
    
    
@dataclass
class Description(ContextBase):
    description: str = Validator(default=None, compare=False, repr=False)


@dataclass
class Email(ContextBase):
    email: str = Validator(default_factory=str, compare=False)
    
    
@dataclass
class RequiredName(ContextBase):
    name: str = Validator()
    
    
@dataclass
class OptionalName(ContextBase):
    name: str = Validator(default=None)
    
    
@dataclass
class Percentage(ContextBase):
    percentage: float = Validator(default=None, min=0.0, max=100.0, step=0.01)
    
    
@dataclass
class Date(ContextBase):
    date: datetime.date = Validator(default_factory=datetime.date.today, compare=True)
    
    @property
    def past_days(self):
        return days(self.date)
    
    @property
    def past_months(self):
        return months(self.date)
    
    @property
    def past_years(self):
        return months(self.date)
    
    
@dataclass
class Created(ContextBase):
    created: datetime.datetime = Validator(post_init_factory=datetime.date.today, repr=False)
    
    def __lt__(self, other):
        return self.created.date() < other.created.date()
    
    @property
    def past_days(self):
        return days(self.created.date())
    
    @property
    def past_months(self):
        return months(self.created.date())
    
    @property
    def past_years(self):
        return years(self.created.date())
    
    
@dataclass
class Search(ContextBase):
    search: str = Validator(default=None, auto=lambda self: normalize_lower(str(self)), repr=False)
