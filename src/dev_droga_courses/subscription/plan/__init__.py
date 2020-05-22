from injector import Binder, Module

from . import cmd
from . import exce
from .db import ORMIndividualPlanRepository
from .repository import IndividualPlanRepository
from .service import CommandHandlerService


class SubscriptionPlanModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IndividualPlanRepository, to=ORMIndividualPlanRepository)


__all__ = [
    'SubscriptionPlanModule',
    'CommandHandlerService',
    'IndividualPlanRepository',
    'cmd',
    'exce',
]
