import asyncio
from http import HTTPStatus
import websockets
import time
import json
from collections import Counter
from OSC import *

c = OSCStreamingClient()
c.connect(('127.0.0.1', 3032))

def eos_out_handler(addr, tags, stuff, source):
	# print(addr, tags, stuff, source)
	pass

c.addMsgHandler('default', eos_out_handler)

fps = 0
lastTime = time.time()
counter = 0

connected = set()
rxGroup = set()

active = {'pan':False, 'tilt':False}

def requestFunction(path, request_headers):
	if path == "/transport":
		return None
	with open("tx.html", "r") as file:
		return HTTPStatus.OK, [('server', 'sensorstream-osc'), ('content-type', 'text/html')], file.read().encode('UTF-8')

async def server(websocket, path):
	print(path)
	connected.add(websocket)
	try:
		print(f'Connected users: {len(connected)}')
		for conn in connected:
			await conn.send(json.dumps({'type':'activeUpdate', **active}))
		async for message in websocket:
			data = json.loads(message)
			print(data)
			if data['type'] == 'orientationUpdate':
				global fps
				global counter
				global lastTime
				pan = round((-data['alpha']+180)*270/180)
				tilt = round(data['beta'])
				# print("fps: "+str(fps)+"	alpha: "+str(round(data['alpha']))+"	beta: "+str(round(data['beta']))+"	gamma: "+str(round(data['gamma'])))
				if active['pan']: c.sendOSC(OSCMessage("/eos/param/pan", str(pan)))
				if active['tilt']: c.sendOSC(OSCMessage("/eos/param/tilt", str(tilt)))
				if time.time() - lastTime >= 1:
					fps = counter
					counter = 0
					lastTime = time.time()
				counter += 1
				for conn in connected:
					await conn.send(json.dumps({'type':'orientationUpdate', 'pan':pan, 'tilt':tilt}))
			if data['type'] == 'togglePan':
				active['pan'] = not active['pan']
				for conn in connected:
					await conn.send(json.dumps({'type':'activeUpdate', **active}))
			if data['type'] == 'toggleTilt':
				active['tilt'] = not active['tilt']
				for conn in connected:
					await conn.send(json.dumps({'type':'activeUpdate', **active}))
			if data['type'] == 'toggleAll':
				active['tilt'] = not active['tilt']
				active['pan'] = not active['pan']
				for conn in connected:
					await conn.send(json.dumps({'type':'activeUpdate', **active}))
			if data['type'] == 'allOn':
				active['tilt'] = True
				active['pan'] = True
				for conn in connected:
					await conn.send(json.dumps({'type':'activeUpdate', **active}))
			if data['type'] == 'allOff':
				active['tilt'] = False
				active['pan'] = False
				for conn in connected:
					await conn.send(json.dumps({'type':'activeUpdate', **active}))
				# fps = 1/(time.time()-lastTime)
				# lastTime = time.time()
				# counter += 1
				# for conn in connected:
				# 	await conn.send(json.dumps(data))
	finally:
		connected.remove(websocket)
		print(f'Connected users: {len(connected)}')

start_server = websockets.serve(server, "0.0.0.0", 80, process_request=requestFunction)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()