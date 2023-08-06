from __future__ import annotations

__all__ = [
        'Register',
        'PersonCode',
        'PersonKey',
        'PersonBase',
        'Salary',
        'WorkActivity',
        'Username',
        'Password',
        'PasswordRepeat',
        'ProfileKey',
        'PatientKey',
        'Creator',
        'RequiredCreator',
        'Age',
        'SocialName',
        'ProviderKey',
        'TherapistKey',
        'DoctorKey'
]

from dtfield import dataclass, Validator, ContextBase, datetime, Decimal, InitVar, re
from ..enums import *

def person_code(self):
    return '{}{}{}{}'.format(
            self.gender.name,
            re.sub(r'-', '', str(self.bdate)),
            self.fname[:2].upper(),
            self.lname.split()[-1][:2].upper()
    )


@dataclass
class Register(ContextBase):
    register: str = Validator()
    

@dataclass
class Age(ContextBase):
    age: float = Validator(default=None)


@dataclass
class PersonCode(ContextBase):
    code: str = Validator(default=None, update_auto=person_code)


@dataclass
class PersonKey(ContextBase):
    person_key: str = Validator(item_name='person', table='Person')
    
    @property
    def age(self):
        return self.person.age
    
    @property
    def fullname(self):
        return self.person.fullname
    
    @property
    def social_name(self):
        return self.person.social_name
    
    @property
    def bdate(self):
        return self.person.bdate


@dataclass
class PatientKey(ContextBase):
    patient_key: str = Validator(item_name='patient', table='Patient')

@dataclass
class DoctorKey(ContextBase):
    doctor_key: str = Validator(item_name='doctor', table='Doctor')
    
    
@dataclass
class TherapistKey(ContextBase):
    therapist_key: str = Validator(item_name='therapist', table='Therapist')


@dataclass
class Creator(ContextBase):
    creator: str = Validator(item_name='user', table='User', default=None)

@dataclass
class RequiredCreator(ContextBase):
    creator: str = Validator(item_name='user', table='User')


@dataclass
class PersonBase(ContextBase):
    fname: str = Validator()
    lname: str = Validator()
    bdate: datetime.date = Validator(compare=False)
    gender: Gender = Validator(compare=False)


@dataclass
class Salary(ContextBase):
    scope: EmployeeScope = Validator()
    base_value: Decimal = Validator(min=Decimal('0.0'), default=1)
    salary_indexed: bool = Validator(default=True)
    active: bool = Validator(default=True)
    
    
@dataclass
class WorkActivity(ContextBase):
    hours_day: float = Validator(min=0, max=24, default=8)
    days_month: float = Validator(min=0, max=31, default=22)
    telephonist: bool = Validator(default=True)
    housekeeping: bool = Validator(default=True)
    external: bool = Validator(default=True)
    manager: bool = Validator(default=True)
    financial: bool = Validator(default=True)
    assistant: bool = Validator(default=True)
    
    
@dataclass
class SocialName(ContextBase):
    name: str = Validator(default=None, label='Nome Social', compare=False)


@dataclass
class Username(ContextBase):
    username: str = Validator(min_lenght=5)
    
    
@dataclass
class Password(ContextBase):
    password: bytes = Validator(min_lenght=5, private=True)
    

@dataclass
class PasswordRepeat(ContextBase):
    password_repeat: InitVar[bytes] = None
    

@dataclass
class ProfileKey(ContextBase):
    profile_key: str = Validator(tables=['Patient', 'Doctor', 'Therapist', 'Employee'], item_name='profile')


@dataclass
class ProviderKey(ContextBase):
    provider_key: str = Validator(tables=['Doctor', 'Therapist'], item_name='provider')

