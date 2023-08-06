__all__ = [
        'MedicalVisit',
        'Event'
]

import datetime
from dtfield import context_model, dataclass, InitVar, re, Validator, Parser, descdataclass
from ..bases import *
from ..functions import *
from ..enums import *


@context_model
@descdataclass
class MedicalVisit(SelfKey, End, VisitContext, TreatmentResponse, SOAP, Intro, MainComplaint, Start, Date, PatientKey):
    creator: str = Validator(default='zjhm79ltaw87', table='User', item_name='user')
    next: int = Validator(default=60, label='dias para próxima visita')


@context_model
@descdataclass
class Event(SelfKey, Creator, Age, RequiredName, PatientKey):
    when: str = Validator(auto=lambda self: self.patient.years, db=False)
    
    @property
    def bdate(self):
        return self.patient.person.bdate
    
    def __post_init__(self):
        if not self.age:
            if self.when:
                year = re.match(r'^[1-2][09]\d\d', self.when)
                if year:
                    self.age = years(self.bdate, datetime.date(int(year.group()), self.bdate.month, self.bdate.day))
                else:
                    month_year = re.match(r'^([0-3]?\d)[.\-/]([1-2][09]\d\d)', self.when)
                    if month_year:
                        self.age = years(self.bdate, datetime.date(int(month_year.group(2)), int(month_year.group(1)),
                                                                   self.bdate.day))
                    else:
                        day_month_year = re.match(r'^([0]?[1-9]|2[0-9]|3[0-1])[.\-/]([0]?[1-9]|10|11|12)[.\-/]([1-2][09]\d\d)', self.when)
                        if day_month_year:
                            self.age = years(self.bdate,
                                             datetime.date(int(day_month_year.group(3)), int(day_month_year.group(2)),
                                                           int(day_month_year.group(1))))
                        else:
                            self.age = Parser.get(self.when, float)
                        
                        
                    
    
