from injector import Module

from . import cmd
from . import exce
from .repository import IndividualPlanRepository
from .service import CommandHandlerService


class SubscriptionPlanModule(Module):
    pass


__all__ = [
    'SubscriptionPlanModule',
    'CommandHandlerService',
    'IndividualPlanRepository',
    'cmd',
    'exce',
]
