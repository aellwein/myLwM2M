# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

from abc import ABCMeta, abstractmethod

from lwm2m.hasher import Sha256Hasher, Hasher


class ClientPersistence(metaclass=ABCMeta):
    """
    This class is used by LWM2M server to load and store client information.
    This class is abstract and is to be implemented by subclasses.
    """

    @abstractmethod
    def get_client_for_location(self, location):
        """
        Get client for the given location.
        :param location: location URI
        :return: client information, or None.
        """
        pass

    @abstractmethod
    def get_client_for_endpoint_name(self, endpoint):
        """
        Get client for the given endpoint.
        :param endpoint: endpoint name of the client
        :return: client information, or None.
        """
        pass

    @abstractmethod
    def has_client_with_location(self, location):
        """
        Returns True, if the client with given location is known to this persistence.
        :param location: location URI
        :return: True, if the client is known, else False.
        """
        pass

    @abstractmethod
    def has_client_with_endpoint_name(self, endpoint):
        """
        Returns True, if the client with given endpoint name is known to this persistence.
        :param endpoint: endpoint name
        :return: True, if the client is known, else False.
        """
        pass

    @abstractmethod
    def put_client_for_endpoint_name(self, endpoint, client):
        """
        Stores the client information with the given endpoint name in this persistence.
        Hint: if the client already exists, it will be overwritten.
        :param endpoint: endpoint name
        :param client: client information
        """
        pass

    @abstractmethod
    def put_client_for_location(self, location, client):
        """
        Stores the client information with the given location URI in this persistence.
        Hint: if the client already exists, it will be overwritten.
        :param location: location URI
        :param client: client information
        """
        pass

    @abstractmethod
    def delete_client_for_location(self, location):
        """
        Deletes the client with the given location in this persistence.
        :param location: location URI
        """
        pass

    @abstractmethod
    def delete_client_for_endpoint_name(self, endpoint):
        """
        Deletes the client with the given endpoint name in this persistence.
        :param endpoint: endpoint name
        """
        pass


class InMemoryPersistence(ClientPersistence):
    """
    Implementation of default in-memory persistence.
    """

    def __init__(self, hasher=Sha256Hasher()):
        assert isinstance(hasher, Hasher), "hasher should be of type lwm2m.Hasher"
        self._hasher = hasher
        self._clients = dict()

    def get_client_for_location(self, location):
        assert location, "location must be present"
        return self._clients[str(location)] if str(location) in self._clients else None

    def get_client_for_endpoint_name(self, endpoint):
        assert endpoint, "endpoint must be present"
        location = self._hasher.hash_for(str(endpoint))
        return self._clients[location] if location in self._clients else None

    def has_client_with_location(self, location):
        assert location, "location must be present"
        return str(location) in self._clients

    def has_client_with_endpoint_name(self, endpoint):
        assert endpoint, "endpoint must be present"
        location = self._hasher.hash_for(str(endpoint))
        return location in self._clients

    def put_client_for_endpoint_name(self, endpoint, client):
        assert endpoint, "endpoint must be present"
        location = self._hasher.hash_for(str(endpoint))
        self._clients[location] = client

    def put_client_for_location(self, location, client):
        assert location, "location must be present"
        self._clients[str(location)] = client

    def delete_client_for_endpoint_name(self, endpoint):
        assert endpoint, "endpoint must be present"
        location = self._hasher.hash_for(str(endpoint))
        if location in self._clients:
            del self._clients[location]

    def delete_client_for_location(self, location):
        assert location, "location must be present"
        if str(location) in self._clients:
            del self._clients[str(location)]
