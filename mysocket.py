import asyncio
import websockets
import time

print("Ctrl-C to cancel, try to connect in order to trigger the try switch.")
connected = set()

async def handler(websocket, path):
    # add to set() to avoid duplicate references to socket
    try:
        connected.add(websocket)
        async for message in websocket:
            print(message)
    # if the websocket throws an error, it probably disconnected
    # remove it from the set so you don't try to write to it
    finally:
        connected.remove(websocket)

async def broadcast_time():
    while True:
        await asyncio.sleep(1)
        if(len(connected)):
            print("broadcasting to ", len(connected), " clients")
            # I wonder if asyncio.wait is sequential or concurrent
            await asyncio.wait([ws.send(str(time.time())) for ws in connected])

start_server = websockets.serve(handler, 'localhost', 4000)
event_loop = asyncio.get_event_loop()

# this might be the totally wrong way to intercept interrupts
try:
    event_loop.run_until_complete(start_server)
    event_loop.run_until_complete(broadcast_time())
    event_loop.run_forever()
except KeyboardInterrupt:
    print("Received exit, exiting")
