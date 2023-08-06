__all__ = [
        'FacilityKey',
        'ServiceKey',
        'ServiceTypeBase',
        'Payment'
]

from dtfield import dataclass, Validator, ContextBase, datetime, Decimal, ModelMap
from ..enums import *

@dataclass
class FacilityKey(ContextBase):
    facility_key: str = Validator(compare=False, label='Empresa', table='Facility', item_name='facility', default=None)
    
    
@dataclass
class ServiceKey(ContextBase):
    service_key: str = Validator(compare=False, label='Serviço', table='Service', item_name='service')
    
    
@dataclass
class ServiceTypeBase(ContextBase):
    type: ServiceType = Validator(hash=True)


@dataclass
class Payment(ContextBase):
    payment_method: PaymentMethod = Validator(default='DI')
    payment_value: Decimal = Validator(default=Decimal('0.0'))
    payment_date: datetime.date = Validator(default_factory=datetime.date.today)
    
    @classmethod
    async def total_payment(cls):
        return float(sum([Decimal(i.get('payment_value')) for i in await cls.fetch_all()])).__round__(2)
    
    
    @classmethod
    async def date_payment(cls, year: int, month: int, day: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in
                          await cls.fetch_all({
                                  'payment_date': str(datetime.date(year, month, day)),
                                  'facility_key': facility_key
                          })])).__round__(2)
    
    @classmethod
    async def month_payment(cls, year: int, month: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in await cls.fetch_all(
                {
                        'payment_date?contains': str(datetime.date(year, month, 1))[:8],
                        'facility_key': facility_key
                    
                })])).__round__(2)
    
    @classmethod
    async def year_payment(cls, year: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in
                          await cls.fetch_all({
                                  'payment_date?contains': str(year),
                                  'facility_key': facility_key
                          })])).__round__(2)
    
    @staticmethod
    async def liquid_income(year: int, month: int):
        invoices = await ModelMap['Invoice'].month_payment(year, month)
        expenses = await ModelMap['Expense'].month_payment(year, month)
        return float(invoices - expenses).__round__(2)


