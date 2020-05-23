from injector import Injector, Binder

from dev_droga_courses import app
from dev_droga_courses.subscription import plan
from .in_memory import InMemoryIndividualPlanRepository


def configure_for_testing(binder: Binder) -> None:
    binder.bind(
        plan.IndividualPlanRepository,
        to=InMemoryIndividualPlanRepository,
    )


register: Injector = app.register.create_child_injector(configure_for_testing)
