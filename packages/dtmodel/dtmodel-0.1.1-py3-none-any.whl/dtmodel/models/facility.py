__all__ = [
        'Facility',
        'Invoice',
        'Service',
        'Expense'
]

import datetime

from dtfield import context_model, descdataclass, Validator, Decimal
from ..bases import *


@context_model
@descdataclass
class Facility(SelfKey, Email, Phone, Address, RequiredName):
    pass


@context_model
@descdataclass
class Invoice(SelfKey, Created, Creator, Payment, FacilityKey, PatientKey):
    pass


@context_model
@descdataclass
class Expense(Search, SelfKey, Created, Creator, Payment, FacilityKey):
    pass


@context_model
@descdataclass
class Service(Search, SelfKey, Created, Creator, Description, Active, OptionalName, FacilityKey, Percentage, Price, ServiceTypeBase):
    DETA_QUERY = {'active': True}
    therapist_key: str = Validator(default=None, table='Therapist', item_name='provider')
    doctor_key: str = Validator(default=None, table='Doctor', item_name='provider')
    
    def __post_init__(self):
        assert self.therapist_key or self.doctor_key
    
    def __str__(self):
        return f'{self.provider} {self.type.value} R$ {self.price}'
    
    def __lt__(self, other):
        return (self.provider.person.short_name, self.price) < (other.provider.person.short_name, other.price)