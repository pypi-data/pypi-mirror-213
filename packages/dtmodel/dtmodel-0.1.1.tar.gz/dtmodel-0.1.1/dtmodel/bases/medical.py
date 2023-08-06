__all__ = [
        'MainComplaint',
        'SOAP',
        'Intro',
        'TreatmentResponse',
        'VisitContext'
]

from dtfield import dataclass, Validator, ContextBase

@dataclass
class MainComplaint(ContextBase):
    main_complaint: str = Validator(default=None)
    

@dataclass
class Intro(ContextBase):
    intro: str = Validator(default=None, repr=False)

@dataclass
class SOAP(ContextBase):
    subjective: str = Validator(default=None, repr=False)
    objective: str = Validator(default=None, repr=False)
    assessment: str = Validator(default=None, repr=False)
    plan: str = Validator(default=None, repr=False)
    
    
@dataclass
class TreatmentResponse(ContextBase):
    treatment: str = Validator(default=None, repr=False)
    response: str = Validator(default=None, repr=False)
    
    
@dataclass
class VisitContext(ContextBase):
    context: str = Validator(default=None, repr=False)
    complement: str = Validator(default=None, repr=False)
    
