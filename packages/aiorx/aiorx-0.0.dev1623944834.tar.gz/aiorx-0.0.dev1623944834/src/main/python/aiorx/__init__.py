import asyncio
from typing import Generic, TypeVar
import inspect
import functools

E = TypeVar('E')


class Observer(Generic[E]):
    async def on_next(self, event: E):
        pass

    async def on_error(self, error):
        pass

    async def on_complete(self):
        pass


class Subscription:

    def unsubscribe(self):
        raise NotImplementedError()


class SubscriptionAdapter(Subscription):

    def __init__(self, unsubscribe):
        self._unsubscribe = unsubscribe

    def unsubscribe(self):
        self._unsubscribe()


class Observable(Generic[E]):

    def subscribe(self, *args, **kwargs) -> Subscription:
        raise NotImplementedError()


def as_async(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def ensure_async(fn):
    if inspect.iscoroutinefunction(fn):
        return fn
    return as_async(fn)


async def throw(ex: Exception):
    raise ex


async def noop(event):
    pass


class ObserverAdapter(Observer):

    @classmethod
    def create_from(cls, *args, **kwargs):
        if len(args) > 0 and getattr(args[0], 'on_next', False):
            return args[0]
        return cls(*args, **kwargs)

    def __init__(self, on_next=noop, on_error=throw, on_complete=noop):
        self.on_next = ensure_async(on_next)
        self.on_error = ensure_async(on_error)
        self.on_complete = ensure_async(on_complete)


class ObservableAdapter(Observable[E]):

    def __init__(self, subscribe, unsubscribe=None):
        self._subscribe = subscribe
        self._unsubscribe = unsubscribe

    def subscribe(self, *args, **kwargs) -> Subscription:
        observer = ObserverAdapter.create_from(*args, **kwargs)
        unsubscribe = self._subscribe(observer)
        return SubscriptionAdapter(self._unsubscribe or unsubscribe)


class ObservableDecorator(Observable):

    def __init__(self, parent: Observable, observer_factory):
        self.parent = parent
        self.observer_factory = observer_factory

    def subscribe(self, *args, **kwargs) -> Subscription:
        observer = self.observer_factory(*args, **kwargs)
        return self.parent.subscribe(observer)


class Tap(Generic[E]):

    def __init__(self, *args, **kwargs):
        self.observer = ObserverAdapter.create_from(*args, **kwargs)

    def __call__(self, observable: Observable[E]) -> Observable[E]:
        def factory(*args, **kwargs) -> Observer[E]:
            listener = ObserverAdapter.create_from(*args, **kwargs)

            async def on_next(event: E):
                await self.observer.on_next(event)
                await listener.on_next(event)

            async def on_error(error):
                await self.observer.on_error(error)
                await listener.on_error(error)

            async def on_complete():
                await self.observer.on_complete()
                await listener.on_complete()

            return ObserverAdapter(on_next, on_error, on_complete)

        return ObservableDecorator(observable, factory)


class Filter(Generic[E]):

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, observable: Observable[E]) -> Observable[E]:
        def factory(*args, **kwargs) -> Observer[E]:
            listener = ObserverAdapter.create_from(*args, **kwargs)

            async def on_next(event: E):
                if self.condition(event):
                    await listener.on_next(event)

            async def on_error(error):
                await listener.on_error(error)

            async def on_complete():
                await listener.on_complete()

            return ObserverAdapter(on_next, on_error, on_complete)

        return ObservableDecorator(observable, factory)


class Map(Generic[E]):

    def __init__(self, map_fn):
        self.map_fn = map_fn

    def __call__(self, observable: Observable[E]) -> Observable[E]:
        def factory(*args, **kwargs) -> Observer[E]:
            listener = ObserverAdapter.create_from(*args, **kwargs)

            async def on_next(event: E):
                await listener.on_next(self.map_fn(event))

            async def on_error(error):
                await listener.on_error(error)

            async def on_complete():
                await listener.on_complete()

            return ObserverAdapter(on_next, on_error, on_complete)

        return ObservableDecorator(observable, factory)


class Subject(Observable[E], Observer[E]):

    def __init__(self):
        self.listeners = []

    async def on_next(self, event: E):
        await asyncio.gather(*[listener.on_next(event) for listener in self.listeners])

    async def on_error(self, error):
        await asyncio.gather(*[listener.on_error(error) for listener in self.listeners])

    async def on_complete(self):
        await asyncio.gather(*[listener.on_complete() for listener in self.listeners])
        # @todo should fail for new subscribers?
        self.listeners = None

    def subscribe(self, *args, **kwargs) -> Subscription:
        listener = ObserverAdapter.create_from(*args, **kwargs)
        self.listeners.append(listener)
        return SubscriptionAdapter(lambda: self.listeners.remove(listener))
