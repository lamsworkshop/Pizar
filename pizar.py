#!/usr/bin/python3

from threading import Thread
import pigpio
from time import sleep

pi = pigpio.pi()
if not pi.connected:
	exit()

pi.set_mode(10, pigpio.OUTPUT)
pi.write(10, 1)

class LED:
	def __init__(self, pin=16):
		self.pin = pin
		pi.set_mode(pin, pigpio.OUTPUT)
		pi.write(pin, 0)
		self.state = 0
	def on(self):
		pi.write(self.pin, 1)
		self.state = 1
	def off(self):
		pi.write(self.pin, 0)
		self.state = 0
	def toggle(self):
		self.state = 0 if self.state == 1 else 1
		pi.write(self.pin, self.state)

class Button:
	def __init__(self, pin=7):
		self.pin = pin
		pi.set_mode(pin, pigpio.INPUT)
	def read(self):
		return pi.read(self.pin)

class Counter:
	def __init__(self, left=5, right=6):
		pi.set_mode(left, pigpio.INPUT)
		pi.set_mode(right, pigpio.INPUT)
		self.left = pi.callback(left)
		self.right = pi.callback(right)
	def read_left(self):
		return self.left.tally()
	def read_right(self):
		return self.right.tally()

class Motor:
	def __init__(self, m1, m2):
		pi.set_mode(m1, pigpio.OUTPUT)
		pi.set_mode(m2, pigpio.OUTPUT)
		pi.set_PWM_frequency(m1, 400)
		pi.set_PWM_frequency(m2, 400)
		self.m1 = m1
		self.m2 = m2
	def set_duty(self, duty):
		if duty > 0:
			duty = duty * 2.55
			motor1 = self.m1
			motor0 = self.m2
		else:
			duty = -duty * 2.55
			motor1 = self.m2
			motor0 = self.m1
		duty = int(duty)
		if duty > 255:
			duty = 255
		pi.set_PWM_dutycycle(motor1, duty)
		pi.set_PWM_dutycycle(motor0, 0)

class Servo(Thread):
	def __init__(self, servo=24, a0=17, a1=22, a2=23):
		super(Servo, self).__init__()
		self.servo = 1<<servo
		self.a0 = a0
		self.a1 = a1
		self.a2 = a2
		pi.set_mode(servo, pigpio.OUTPUT)
		pi.set_mode(a0, pigpio.OUTPUT)
		pi.set_mode(a1, pigpio.OUTPUT)
		pi.set_mode(a2, pigpio.OUTPUT)
		self.duty = [0]*8
	def run(self):
		while True:
			for i in range(8):
				pi.write(self.a0, i & 1)
				pi.write(self.a1, (i>>1) & 1)
				pi.write(self.a2, i>>2)
				d = self.duty[i]
				if d == 0:
					pi.wave_add_generic([
						pigpio.pulse(0, self.servo, 2500)])
				else:
					pi.wave_add_generic([
						pigpio.pulse(self.servo, 0, d),
						pigpio.pulse(0, self.servo, 2500-d)])
				wid = pi.wave_create()
				pi.wave_send_once(wid)
				while pi.wave_tx_busy():
					pass
				pi.wave_delete(wid)
	def set(self, num, angle):
		if angle < 400:
			angle = 0
		if angle > 2100:
			angle = 2100
		self.duty[num] = angle

sonarDict = {}

def sonar(gpio, level, tick):
	global sonarDict
	if level == 1:
		sonarDict[gpio] = [tick, tick]
	else:
		sonarDict[gpio][1] = tick

class Sonar:
	def __init__(self, trigger=8, echo=25):
		self.trigger = trigger
		self.echo = echo
		pi.set_mode(trigger, pigpio.OUTPUT)
		pi.set_mode(echo, pigpio.INPUT)
	def read(self):
		global sonarDict
		tick = pi.get_current_tick()
		sonarDict[self.echo] = [tick, tick]
		cb = pi.callback(self.echo, pigpio.EITHER_EDGE, sonar)
		pi.gpio_trigger(self.trigger, 10)
		while sonarDict[self.echo][0] == sonarDict[self.echo][1]:
			if pigpio.tickDiff(tick, pi.get_current_tick()) > 20000:
				break;
		cb.cancel()
		ticks = sonarDict[self.echo]
		sonarDict.pop(self.echo)
		return pigpio.tickDiff(ticks[0], ticks[1]) * 0.01715

def read_floor():
	h = pi.spi_open(0, 40000, 0x61)
	c, r = pi.spi_xfer(h, [0, 0, 127])
	pi.spi_close(h)
#	pi.write(10, 1)
	return r[2]

def mirror(a):
	for m in [0x081, 0x42, 0x24, 0x18]:
		if a & m != 0 and a & m != m:
			a ^= m
	return a

if __name__ == "__main__":
#	servo = Servo()
#	servo.set(0, 1000)
#	servo.start()
	s = Sonar()
	print(s.read())
	print(s.read())
	print(s.read())
	print("{:08b}".format(mirror(read_floor())))
'''
	try:
		while True:
			print("\r{:08b}".format(read_floor()), end="")
	except:
		pi.write(10, 1)
'''
