import abc


class AbstractNotifier(abc.ABC):

    @abc.abstractmethod
    def notify(self, message):
        pass


class ConsoleNotifier(AbstractNotifier):

    def notify(self, message):
        print(message)
