# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from app.log.command import config_pb2 as app_dot_log_dot_command_dot_config__pb2


class LoggerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RestartLogger = channel.unary_unary(
                '/v2ray.core.app.log.command.LoggerService/RestartLogger',
                request_serializer=app_dot_log_dot_command_dot_config__pb2.RestartLoggerRequest.SerializeToString,
                response_deserializer=app_dot_log_dot_command_dot_config__pb2.RestartLoggerResponse.FromString,
                )
        self.FollowLog = channel.unary_stream(
                '/v2ray.core.app.log.command.LoggerService/FollowLog',
                request_serializer=app_dot_log_dot_command_dot_config__pb2.FollowLogRequest.SerializeToString,
                response_deserializer=app_dot_log_dot_command_dot_config__pb2.FollowLogResponse.FromString,
                )


class LoggerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RestartLogger(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FollowLog(self, request, context):
        """Unstable interface
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LoggerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RestartLogger': grpc.unary_unary_rpc_method_handler(
                    servicer.RestartLogger,
                    request_deserializer=app_dot_log_dot_command_dot_config__pb2.RestartLoggerRequest.FromString,
                    response_serializer=app_dot_log_dot_command_dot_config__pb2.RestartLoggerResponse.SerializeToString,
            ),
            'FollowLog': grpc.unary_stream_rpc_method_handler(
                    servicer.FollowLog,
                    request_deserializer=app_dot_log_dot_command_dot_config__pb2.FollowLogRequest.FromString,
                    response_serializer=app_dot_log_dot_command_dot_config__pb2.FollowLogResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'v2ray.core.app.log.command.LoggerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LoggerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RestartLogger(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/v2ray.core.app.log.command.LoggerService/RestartLogger',
            app_dot_log_dot_command_dot_config__pb2.RestartLoggerRequest.SerializeToString,
            app_dot_log_dot_command_dot_config__pb2.RestartLoggerResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FollowLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/v2ray.core.app.log.command.LoggerService/FollowLog',
            app_dot_log_dot_command_dot_config__pb2.FollowLogRequest.SerializeToString,
            app_dot_log_dot_command_dot_config__pb2.FollowLogResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
