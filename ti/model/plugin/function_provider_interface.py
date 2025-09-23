from abc import ABC,abstractmethod

from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.plugin.function_contributions import FunctionContribution


class IFunctionExtension(ExtensionInterface):
    @property
    @abstractmethod
    def function_contributions(self) -> list[FunctionContribution]:
        pass