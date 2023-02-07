from time import sleep
import motorLib

motorA = motorLib.Motor(20, 21, 1, (14, 15, 18), 400)
motorA.initial_set_up()

step_count = 1200
for x in range (step_count):
	motorA.motor_steps(1)


sleep(0.5)
motorA.set_resolution('Half')
motorA.set_counter_clockwise()
step_count = step_count*motorA.scale

for x in range (step_count):
	motorA.motor_steps(1)

motorB = motorLib.Motor(19, 26, 1, (14, 15, 18), 400)
motorB.initial_set_up()

step_count = 1200
for x in range (step_count):
	motorB.motor_steps(1)


sleep(0.5)
motorB.set_resolution('Half')
motorB.set_counter_clockwise()
step_count = step_count*motorB.scale

for x in range (step_count):
	motorB.motor_steps(1)







