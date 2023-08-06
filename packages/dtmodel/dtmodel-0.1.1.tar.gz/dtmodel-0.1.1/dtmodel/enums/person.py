__all__ = [
        'Gender',
        'EmployeeScope'
]

from dtfield.base_enum import *

class Gender(BaseEnum):
    M = 'Masculino'
    F = 'Feminino'
    

class EmployeeScope(BaseEnum):
    DIA = 'Diarista'
    CLT = 'CLT'
    SOC = 'Sócio Proprietário'
    TER = 'Terceirizado'
    EST = 'Estagiário'
    