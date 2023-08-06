__all__ = [
        'VisitType',
]

from dtfield.base_enum import *



class VisitType(BaseEnum):
    CI = 'Inicial'
    CO = 'Seguimento'
    CE = 'Encaixe'
    CC = 'Cortesia'
    CP = 'Breve'
    RT = 'Retorno'
    VH = 'Hospitalar'
    VD = 'Domiciliar'
    
