__all__ = [
        'PaymentMethod',
        'ServiceType'
]

from dtfield.base_enum import *


class PaymentMethod(BaseEnum):
    CA = 'Dinheiro'
    CR = 'Cartão de Crédito'
    DE = 'Cartão De Débito'
    TR = 'Transferência Bancária'
    PI = 'Pix'
    CH = 'Cheque'

    
    
class ServiceType(BaseEnum):
    CI = 'Consulta Inicial'
    CO = 'Consulta Regular'
    CE = 'Consulta Encaixe'
    CC = 'Consulta Cortesia'
    CP = 'Consulta Breve'
    RT = 'Retorno de Consulta'
    VH = 'Visita Hospitalar'
    SA = 'Terapia Assistida'
    VD = 'Visita Domiciliar'
    AD = 'Acerto de Débito'
    SU = 'Suporte de Logística'
    AL = 'Aluguel de Sala'
    AC = 'Aluguel Diário'
    SE = 'Sessão de Terapia'
    OS = 'Outro Serviço'
    VE = 'Venda de Produto'
