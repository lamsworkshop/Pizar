import pizar

led = pizar.LED()
button = pizar.Button()
counter = pizar.Counter()
left = pizar.Motor(12, 18)
right = pizar.Motor(13, 19)
sonar = pizar.Sonar()
servo = pizar.Servo()
servo.start()

def mirror(a):
	for m in [0x081, 0x42, 0x24, 0x18]:
		if a & m != 0 and a & m != m:
			a ^= m
	return a

def led_handler(s):
	if s[1] == 'n':
		led.on()
	elif s[1] == 'f':
		led.off()
	elif s[1] == 'o':
		led.toggle()

def whl_handler(s):
	motor = left if s[0] == 'l' else right
	try:
		pwm = float(s[1:])
	except:
		pwm = 0
	motor.set_duty(pwm)

def stp_handler():
	left.set_duty(0)
	right.set_duty(0)

def srv_handler(s):
	try:
		angle = int(s[1:])
	except:
		angle = 0
	servo.set(int(s[0]), angle)

def trg_handler(s):
	if s[0] == 'b':
		return "pressed" if button.read() == 0 else "released"
	if s[0] == 'f':
		return "{:08b}".format(mirror(pizar.read_floor()))
	if s[0] == 's':
		return "%.1f" % sonar.read()
	if s[0] == 'l':
		return str(counter.read_left())
	if s[0] == 'r':
		return str(counter.read_right())

def handle(s):
	handler = s[:3]
	s = s[3:]
	if handler == 'LED':
		return led_handler(s)
	if handler == 'TRG':
		return trg_handler(s)
	if handler == 'SRV':
		return srv_handler(s)
	if handler == 'WHL':
		return whl_handler(s)
	if handler == 'STP':
		return stp_handler()
