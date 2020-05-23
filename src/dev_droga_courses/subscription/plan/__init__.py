from injector import Binder, Module

from . import cmd, exce, settings
from .db import ORMIndividualPlanRepository
from .repository import IndividualPlanRepository
from .service import CommandHandlerService


class SubscriptionPlanModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IndividualPlanRepository, to=ORMIndividualPlanRepository)
        binder.bind(settings.MaxActivePlans, to=3)


__all__ = [
    'SubscriptionPlanModule',
    'CommandHandlerService',
    'IndividualPlanRepository',
    'cmd',
    'exce',
    'settings',
]
