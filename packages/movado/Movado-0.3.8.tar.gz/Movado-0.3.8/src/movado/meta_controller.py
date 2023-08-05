from collections import OrderedDict
from typing import Union, Callable, List, Dict, Any

from movado.controller import Controller
from movado.estimator import Estimator
from movado.mab_handler_cb import MabHandlerCB
from movado.async_list import AsyncList
from pygmo.core import hypervolume

# This inputs are used to populate the symbol table for class retrieval
# noinspection PyUnresolvedReferences
from movado.mab_controller import MabController  # pylint: disable=unused-import

# noinspection PyUnresolvedReferences
from movado.distance_controller import (
    DistanceController,
)  # pylint: disable=unused-import

# noinspection PyUnresolvedReferences


class MetaController(Controller):
    def __init__(
        self,
        controller: str,
        estimator: Estimator,
        exact_fitness: Callable[[List[float]], List[float]],
        params: "OrderedDict[str, List[Union[int, float, str]]]",
        problem_dimensionality: int = -1,
        solutions: AsyncList = None,
        debug=False,
    ):
        if problem_dimensionality == -1:
            raise Exception(
                "Please specify problem dimensionality for MetaController instantiation"
            )
        super(MetaController, self).__init__(
            estimator=estimator, exact_fitness=exact_fitness, debug=debug
        )
        self.__controllers: List[Controller] = self.__get_controllers(
            params, controller, estimator, exact_fitness
        )
        self.__mab: MabHandlerCB = MabHandlerCB(len(self.__controllers), debug)
        self.__reference_point: List[float] = [
            1 + (1 / (problem_dimensionality - 1))
        ] * problem_dimensionality
        self.__last_hv: Optional[float] = 0
        self.__solutions: AsyncList = solutions
        self.__last_action: int = -1
        self.__last_point: int = -1

    @staticmethod
    async def solution_update_waiter(event):
        await event.wait()
        hv_obj = hypervolume(self.__solutions[-1])
        hv = hv_obj.compute(self.__reference_point)
        self.__mab.learn(self.__last_action, -(hv - self.__last_hv), self.__last_point)
        self.__last_hv = hv
        self.__solutions.clear()

    @staticmethod
    def __get_controllers(
        params: "OrderedDict[str, List[Union[int, float, str]]]",
        controller: str,
        estimator: Estimator,
        exact_fitness: Callable[[List[float]], List[float]],
    ) -> List[Controller]:
        controllers: List[Controller] = []
        controller_class = globals().get(controller)
        if not controller_class:
            raise Exception("Controller '" + controller + "' was not found")
        indices = [0] * len(params.keys())
        ranges = [len(val) - 1 for val in params.values()]
        while True:
            updated = False
            current_params = {}
            for ind, key, val in enumerate(params.items()):
                current_params[key] = val[indices[ind]]
            for ind, param_ind in enumerate(indices):
                if param_ind < ranges[ind]:
                    indices[ind] += 1
                    updated = True
                    break
            controllers.append(
                controller_class(
                    estimator=estimator, exact_fitness=exact_fitness, **current_params
                )
            )
            if not updated:
                break
        return controllers

    def compute_objective(self, point: List[int]) -> List[float]:
        self.__last_action = self.__mab.predict(point)
        self.__last_point = point
        return self.__controllers[self.__last_action].compute_objective(
            self.__last_point
        )

    def _write_debug(self, debug_info: Dict[str, Any]):
        pass
