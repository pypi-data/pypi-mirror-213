import typing as t

from ellar.common import (
    IExceptionMiddlewareService,
    IExecutionContextFactory,
    IGuardsConsumer,
    IHostContextFactory,
    IHTTPConnectionContextFactory,
    IInterceptorsConsumer,
    IWebSocketContextFactory,
)
from ellar.core.services import Reflector
from ellar.di import EllarInjector

from .context import ExecutionContextFactory, HostContextFactory
from .context.factory import HTTPConnectionContextFactory, WebSocketContextFactory
from .exceptions.service import ExceptionMiddlewareService
from .guard import GuardConsumer
from .interceptors import EllarInterceptorConsumer

if t.TYPE_CHECKING:  # pragma: no cover
    from ellar.core.conf import Config


class CoreServiceRegistration:
    """Create Binding for all application service"""

    __slots__ = ("injector", "config")

    def __init__(self, injector: EllarInjector, config: "Config") -> None:
        self.injector = injector
        self.config = config

    def register_all(self) -> None:
        self.injector.container.register(
            IExceptionMiddlewareService, ExceptionMiddlewareService
        )

        self.injector.container.register(
            IExecutionContextFactory, ExecutionContextFactory
        )
        self.injector.container.register(IHostContextFactory, HostContextFactory)

        self.injector.container.register_scoped(
            IHTTPConnectionContextFactory, HTTPConnectionContextFactory
        )

        self.injector.container.register_scoped(
            IWebSocketContextFactory, WebSocketContextFactory
        )

        self.injector.container.register(Reflector)
        self.injector.container.register_singleton(
            IInterceptorsConsumer, EllarInterceptorConsumer
        )
        self.injector.container.register_singleton(IGuardsConsumer, GuardConsumer)
