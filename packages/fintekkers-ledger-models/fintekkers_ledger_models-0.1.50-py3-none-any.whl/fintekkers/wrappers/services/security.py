from typing import Generator

from grpc import Channel

from fintekkers.models.security.security_pb2 import SecurityProto
from fintekkers.services.security_service.security_service_pb2 import Security_Stub
from fintekkers.services.security_service import  security_service_pb2_grpc

from fintekkers.requests.security.query_security_response_pb2 import QuerySecurityResponseProto
from fintekkers.wrappers.requests.security import QuerySecurityRequest, CreateSecurityRequest

from fintekkers.wrappers.models.util.environment import Environment, SECURITY_SERVICE

class SecurityService(Security_Stub):
    def __init__(self, stub:Security_Stub):
        self.stub = stub

    def Search(self, request:QuerySecurityRequest) -> Generator[SecurityProto, None, None]:
        # print(Environment().IS_RUNNING_LOCALLY)

        # stub:Channel = Environment().get_service_insecure_channel(SECURITY_SERVICE)
        
        # LOCAL_CHANNEL = Environment().get_service_insecure_channel(SECURITY_SERVICE)
        # service = security_service_pb2_grpc.SecurityStub(LOCAL_CHANNEL)
        # results = service.Search(request.proto)

        responses = self.stub.Search(request.proto)

        try:
            while not responses._is_complete():
                response:QuerySecurityResponseProto = responses.next()
                
                for security_proto in response.security_response:
                    yield security_proto
        except StopIteration:
            pass
        except Exception as e:
            print(e)
        
        #This will send the cancel message to the server to kill the connection
        responses.cancel()
