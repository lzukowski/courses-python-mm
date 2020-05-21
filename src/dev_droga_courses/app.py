from injector import Injector

from .db import PersistenceModule
from .subscription.plan import SubscriptionPlanModule

register: Injector = Injector([PersistenceModule, SubscriptionPlanModule])

__all__ = ['register']
