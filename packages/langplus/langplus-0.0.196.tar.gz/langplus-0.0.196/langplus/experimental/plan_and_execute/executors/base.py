from abc import abstractmethod
from typing import Any

from pydantic import BaseModel

from langplus.callbacks.manager import Callbacks
from langplus.chains.base import Chain
from langplus.experimental.plan_and_execute.schema import StepResponse


class BaseExecutor(BaseModel):
    @abstractmethod
    def step(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> StepResponse:
        """Take step."""

    @abstractmethod
    async def astep(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> StepResponse:
        """Take step."""


class ChainExecutor(BaseExecutor):
    chain: Chain

    def step(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> StepResponse:
        """Take step."""
        response = self.chain.run(**inputs, callbacks=callbacks)
        return StepResponse(response=response)

    async def astep(
        self, inputs: dict, callbacks: Callbacks = None, **kwargs: Any
    ) -> StepResponse:
        """Take step."""
        response = await self.chain.arun(**inputs, callbacks=callbacks)
        return StepResponse(response=response)
