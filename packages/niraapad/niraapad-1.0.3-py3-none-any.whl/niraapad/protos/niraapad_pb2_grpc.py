# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from niraapad.protos import niraapad_pb2 as niraapad_dot_protos_dot_niraapad__pb2


class NiraapadStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.StaticMethod = channel.unary_unary(
        '/Niraapad/StaticMethod',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodReq.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodResp.FromString,
        )
    self.StaticMethodTrace = channel.unary_unary(
        '/Niraapad/StaticMethodTrace',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodTraceMsg.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.FromString,
        )
    self.Initialize = channel.unary_unary(
        '/Niraapad/Initialize',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeReq.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeResp.FromString,
        )
    self.InitializeTrace = channel.unary_unary(
        '/Niraapad/InitializeTrace',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeTraceMsg.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.FromString,
        )
    self.GenericGetter = channel.unary_unary(
        '/Niraapad/GenericGetter',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterReq.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterResp.FromString,
        )
    self.GenericGetterTrace = channel.unary_unary(
        '/Niraapad/GenericGetterTrace',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterTraceMsg.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.FromString,
        )
    self.GenericSetter = channel.unary_unary(
        '/Niraapad/GenericSetter',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterReq.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterResp.FromString,
        )
    self.GenericSetterTrace = channel.unary_unary(
        '/Niraapad/GenericSetterTrace',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterTraceMsg.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.FromString,
        )
    self.GenericMethod = channel.unary_unary(
        '/Niraapad/GenericMethod',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodReq.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodResp.FromString,
        )
    self.GenericMethodTrace = channel.unary_unary(
        '/Niraapad/GenericMethodTrace',
        request_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodTraceMsg.SerializeToString,
        response_deserializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.FromString,
        )


class NiraapadServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def StaticMethod(self, request, context):
    """Used for all static and class methods
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StaticMethodTrace(self, request, context):
    """Used for all static and class methods
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Initialize(self, request, context):
    """Used for the __init__ method of class Serial
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def InitializeTrace(self, request, context):
    """Used for the __init__ method of class Serial
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericGetter(self, request, context):
    """Used for property getters
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericGetterTrace(self, request, context):
    """Used for property getters
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericSetter(self, request, context):
    """Used for property setters
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericSetterTrace(self, request, context):
    """Used for property setters
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericMethod(self, request, context):
    """Used for the remaining methods
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenericMethodTrace(self, request, context):
    """Used for the remaining methods
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NiraapadServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'StaticMethod': grpc.unary_unary_rpc_method_handler(
          servicer.StaticMethod,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodReq.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodResp.SerializeToString,
      ),
      'StaticMethodTrace': grpc.unary_unary_rpc_method_handler(
          servicer.StaticMethodTrace,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.StaticMethodTraceMsg.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.SerializeToString,
      ),
      'Initialize': grpc.unary_unary_rpc_method_handler(
          servicer.Initialize,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeReq.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeResp.SerializeToString,
      ),
      'InitializeTrace': grpc.unary_unary_rpc_method_handler(
          servicer.InitializeTrace,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.InitializeTraceMsg.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.SerializeToString,
      ),
      'GenericGetter': grpc.unary_unary_rpc_method_handler(
          servicer.GenericGetter,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterReq.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterResp.SerializeToString,
      ),
      'GenericGetterTrace': grpc.unary_unary_rpc_method_handler(
          servicer.GenericGetterTrace,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericGetterTraceMsg.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.SerializeToString,
      ),
      'GenericSetter': grpc.unary_unary_rpc_method_handler(
          servicer.GenericSetter,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterReq.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterResp.SerializeToString,
      ),
      'GenericSetterTrace': grpc.unary_unary_rpc_method_handler(
          servicer.GenericSetterTrace,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericSetterTraceMsg.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.SerializeToString,
      ),
      'GenericMethod': grpc.unary_unary_rpc_method_handler(
          servicer.GenericMethod,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodReq.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodResp.SerializeToString,
      ),
      'GenericMethodTrace': grpc.unary_unary_rpc_method_handler(
          servicer.GenericMethodTrace,
          request_deserializer=niraapad_dot_protos_dot_niraapad__pb2.GenericMethodTraceMsg.FromString,
          response_serializer=niraapad_dot_protos_dot_niraapad__pb2.EmptyMsg.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Niraapad', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
