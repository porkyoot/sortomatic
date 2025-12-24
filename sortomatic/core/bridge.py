import asyncio
from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass
from sortomatic.utils.logger import logger

@dataclass
class Event:
    name: str
    payload: Any = None

class Bridge:
    """
    An EventBus-styled bridge to decouple UI from Backend.
    Supports basic pub/sub and request/response patterns.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Bridge, cls).__new__(cls)
            cls._instance._subscribers: Dict[str, List[Callable]] = {}
            cls._instance._request_handlers: Dict[str, Callable] = {}
        return cls._instance

    def on(self, event_name: str, handler: Callable):
        """Subscribe to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.debug(f"Bridge: Subscribed to {event_name}")

    def off(self, event_name: str, handler: Callable):
        """Unsubscribe from an event."""
        if event_name in self._subscribers:
            try:
                self._subscribers[event_name].remove(handler)
                logger.debug(f"Bridge: Unsubscribed from {event_name}")
            except ValueError:
                pass

    def handle_event(self, event_name: str, handler: Callable):
        """Alias for on()."""
        self.on(event_name, handler)

    def emit(self, event_name: str, payload: Any = None):
        """Emit an event (non-blocking)."""
        if event_name in self._subscribers:
            for handler in self._subscribers[event_name]:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(payload))
                else:
                    handler(payload)

    def handle_request(self, request_name: str):
        """Decorator to register a handler for a specific request type."""
        def decorator(handler: Callable):
            self._request_handlers[request_name] = handler
            logger.debug(f"Bridge: Registered handler for request '{request_name}'")
            return handler
        return decorator

    async def request(self, request_name: str, payload: Any = None) -> Any:
        """
        Request data from the backend.
        This is an async call that waits for the handler's response.
        """
        if request_name not in self._request_handlers:
            logger.error(f"Bridge: No handler registered for request '{request_name}'")
            return None
        
        handler = self._request_handlers[request_name]
        try:
            if asyncio.iscoroutinefunction(handler):
                return await handler(payload)
            else:
                return handler(payload)
        except Exception as e:
            logger.exception(f"Bridge: Error handling request '{request_name}': {e}")
            return None

# Global singleton bridge
bridge = Bridge()
