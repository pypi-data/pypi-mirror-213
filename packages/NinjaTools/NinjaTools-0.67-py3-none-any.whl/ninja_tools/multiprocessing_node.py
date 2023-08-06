import multiprocessing.managers as managers
from contextlib import contextmanager
from multiprocessing import Manager


class Node:
    def __init__(self, namespace):
        """
        Initialize a Node object with a shared namespace.

        :param namespace: A shared namespace object.
        """
        self.namespace = namespace

    def send(self, channel, data=None, auto_flush=False):
        """
        Send an object to a specific channel in the shared namespace.

        :param channel: The channel to send the object to.
        :param data: Additional data for the object.
        :param auto_flush: Whether to automatically flush the object after receiving it.
        """
        data = Object(data=data, channel=channel, namespace=self.namespace, auto_flush=auto_flush)

        setattr(self.namespace, channel, data)

    def receive(self, channel):
        """
        Receive an object from a specific channel in the shared namespace.

        :param channel: The channel to receive the object from.
        :return: The received object.
        """
        try:
            value = getattr(self.namespace, channel)
            if not value:
                value = Object(None, channel, self.namespace)

            if value.auto_flush:
                # Clear the channel
                setattr(self.namespace, channel, None)

            return value.data
        except AttributeError:
            return None


class Object:
    def __init__(self, data, channel, namespace, auto_flush=False):
        """
        Initialize an Object with a header, data, and channel.

        :param data: Additional data for the object.
        :param channel: The channel the object is associated with.
        :param namespace: The shared namespace the object is associated with.
        """
        self.data = data
        self.channel = channel
        self.namespace = namespace
        self.auto_flush = auto_flush

    def flush(self):
        """
        Remove the object from the shared namespace.
        """
        self.namespace[self.channel] = None

    def __call__(self):
        """
        Return the channel of the object.
        """
        return self.channel


class CustomChannels:
    def get_dict(self):
        """
        Return the dictionary representation of the namespace.
        """
        return self.__dict__


class Proxy(managers.NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'get_dict')

    def get_dict(self):
        """
        Return the dictionary representation of the namespace.
        """
        return self._callmethod('get_dict')


@contextmanager
def manager(namespace='MyNamespace'):
    """
    A context manager for the SyncManager.
    :param namespace: The name of the shared namespace.
    """

    managers.SyncManager.register(namespace, CustomChannels, Proxy)

    with Manager() as manager_:
        yield manager_


# Usage:
# main.py
# from multiprocessing import Process
# from test_node_send import Send
# from test_node_receive import Receive
# import ninja_tools.multiprocessing_node as node
#
# if __name__ == '__main__':
#     with node.manager() as manager:
#         channel = manager.MyNamespace()
#         channel.update = None
#
#         # Get Data
#         send = Process(target=Send, args=(channel,))
#         send.start()
#
#         # Test
#         receive = Process(target=Receive, args=(channel,))
#         receive.start()
#
#         send.join()
#         receive.join()

# Send.py
# from get_data import GetData
# from ninja_tools.multiprocessing_node import Node
#
#
# class Send:
#     def __init__(self, node):
#         self.node = Node(node)
#
#         self.start()
#
#     def start(self):
#         update = GetData(window_name='WINDOW_NAME')
#         while True:
#             updated_data = update.get_data()
#             if updated_data:
#                 self.node.send('update', updated_data)

# Receive.py
# from ninja_tools.multiprocessing_node import Node
#
#
# class Receive:
#     def __init__(self, node):
#         self.node = Node(node)
#
#         self.start()
#
#     def start(self):
#         while True:
#             data = self.node.receive('update')
#             if data:
#                 print(data.character.map_name)
