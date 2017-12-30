# coding: utf-8

from nameko.standalone.rpc import ClusterRpcProxy


def rpc_proxy():
	return ClusterRpcProxy(config={'AMQP_URI': 'amqp://guest:guest@locahost:5672'})

