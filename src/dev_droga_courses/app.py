from injector import Injector

from .subscription.plan import SubscriptionPlanModule

register: Injector = Injector([SubscriptionPlanModule])

__all__ = ['register']
