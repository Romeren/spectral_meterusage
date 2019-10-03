import grpc
from concurrent import futures
import time

# import the generated classes
import meterValue_pb2
import meterValue_pb2_grpc

# import the original functions.py
import functions

# create a class to define the server functions, derived from
# meterValue_pb2_grpc.meterUsageValuesServicer
class meterUsageValuesServicer(meterValue_pb2_grpc.meterUsageValuesServicer):

    # functions.get_data is exposed here
    # the request and response are of the data type
    # meterValue_pb2.Dates
    def get_data(self, request, context):
        response = meterValue_pb2.Date()
        response.value = functions.get_data(request.value)
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_meterUsageValuesServicer_to_server`
# to add the defined class to the server
meterValue_pb2_grpc.add_meterUsageValuesServicer_to_server(
        meterUsageValuesServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)