# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from th2_grpc_common import common_pb2 as th2__grpc__common_dot_common__pb2
from th2_grpc_data_provider import data_provider_template_pb2 as th2__grpc__data__provider_dot_data__provider__template__pb2


class DataProviderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getEvent = channel.unary_unary(
                '/DataProvider/getEvent',
                request_serializer=th2__grpc__common_dot_common__pb2.EventID.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.EventData.FromString,
                )
        self.getMessage = channel.unary_unary(
                '/DataProvider/getMessage',
                request_serializer=th2__grpc__common_dot_common__pb2.MessageID.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MessageData.FromString,
                )
        self.getMessageStreams = channel.unary_unary(
                '/DataProvider/getMessageStreams',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StringList.FromString,
                )
        self.searchMessages = channel.unary_stream(
                '/DataProvider/searchMessages',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MessageSearchRequest.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.FromString,
                )
        self.searchEvents = channel.unary_stream(
                '/DataProvider/searchEvents',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.EventSearchRequest.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.FromString,
                )
        self.getMessagesFilters = channel.unary_unary(
                '/DataProvider/getMessagesFilters',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.FromString,
                )
        self.getEventsFilters = channel.unary_unary(
                '/DataProvider/getEventsFilters',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.FromString,
                )
        self.getEventFilterInfo = channel.unary_unary(
                '/DataProvider/getEventFilterInfo',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.FromString,
                )
        self.getMessageFilterInfo = channel.unary_unary(
                '/DataProvider/getMessageFilterInfo',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.FromString,
                )
        self.matchEvent = channel.unary_unary(
                '/DataProvider/matchEvent',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.FromString,
                )
        self.matchMessage = channel.unary_unary(
                '/DataProvider/matchMessage',
                request_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.SerializeToString,
                response_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.FromString,
                )


class DataProviderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getEvent(self, request, context):
        """returns a single event with the specified id 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMessage(self, request, context):
        """returns a single message with the specified id 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMessageStreams(self, request, context):
        """returns a list of message stream names 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def searchMessages(self, request, context):
        """Creates a message stream that matches the filter. 

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def searchEvents(self, request, context):
        """Create a stream of event or event metadata that matches the filter. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMessagesFilters(self, request, context):
        """gets all the names of sse message filters 

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getEventsFilters(self, request, context):
        """get all names of sse event filters 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getEventFilterInfo(self, request, context):
        """gets filter info 

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getMessageFilterInfo(self, request, context):
        """get filter info 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def matchEvent(self, request, context):
        """Check that event with the specified id is matched by filter 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def matchMessage(self, request, context):
        """Check that message with the specified id is matched by filter 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataProviderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.getEvent,
                    request_deserializer=th2__grpc__common_dot_common__pb2.EventID.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.EventData.SerializeToString,
            ),
            'getMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.getMessage,
                    request_deserializer=th2__grpc__common_dot_common__pb2.MessageID.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MessageData.SerializeToString,
            ),
            'getMessageStreams': grpc.unary_unary_rpc_method_handler(
                    servicer.getMessageStreams,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StringList.SerializeToString,
            ),
            'searchMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.searchMessages,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MessageSearchRequest.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.SerializeToString,
            ),
            'searchEvents': grpc.unary_stream_rpc_method_handler(
                    servicer.searchEvents,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.EventSearchRequest.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.SerializeToString,
            ),
            'getMessagesFilters': grpc.unary_unary_rpc_method_handler(
                    servicer.getMessagesFilters,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.SerializeToString,
            ),
            'getEventsFilters': grpc.unary_unary_rpc_method_handler(
                    servicer.getEventsFilters,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.SerializeToString,
            ),
            'getEventFilterInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.getEventFilterInfo,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.SerializeToString,
            ),
            'getMessageFilterInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.getMessageFilterInfo,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.SerializeToString,
            ),
            'matchEvent': grpc.unary_unary_rpc_method_handler(
                    servicer.matchEvent,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.SerializeToString,
            ),
            'matchMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.matchMessage,
                    request_deserializer=th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.FromString,
                    response_serializer=th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DataProvider', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataProvider(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getEvent',
            th2__grpc__common_dot_common__pb2.EventID.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.EventData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getMessage',
            th2__grpc__common_dot_common__pb2.MessageID.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.MessageData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMessageStreams(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getMessageStreams',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.StringList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def searchMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/DataProvider/searchMessages',
            th2__grpc__data__provider_dot_data__provider__template__pb2.MessageSearchRequest.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def searchEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/DataProvider/searchEvents',
            th2__grpc__data__provider_dot_data__provider__template__pb2.EventSearchRequest.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.StreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMessagesFilters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getMessagesFilters',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getEventsFilters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getEventsFilters',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.ListFilterName.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getEventFilterInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getEventFilterInfo',
            th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getMessageFilterInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/getMessageFilterInfo',
            th2__grpc__data__provider_dot_data__provider__template__pb2.FilterName.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.FilterInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def matchEvent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/matchEvent',
            th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def matchMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DataProvider/matchMessage',
            th2__grpc__data__provider_dot_data__provider__template__pb2.MatchRequest.SerializeToString,
            th2__grpc__data__provider_dot_data__provider__template__pb2.IsMatched.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
