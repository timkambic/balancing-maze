import time

class PID_controller():
    def __init__(self):
		self.Kp = 0
		self.Kd = 0
		self.Ki = 0
		self.max_output = 15
		self.min_output = -15

		#self.Initialize()

    def Initialize(self,invar1,invar2,invar3):
        # initialize delta t variables
		self.prevtm = time.time()
		
		self.Kp = invar1
		self.Ki = invar2
		self.Kd = invar3
				
		self.prev_err = 0

        # term result variables
		self.proportional = 0
		self.integral = 0
		self.derivative = 0
    def SetOutputLimits(self,min_v,max_v):
		self.min_output = min_v
		self.max_output = max_v

    def Compute(self, error):
		self.currtm = time.time()               # get t
		dt = self.currtm - self.prevtm          # get delta t
		de = error - self.prev_err              # get delta error
		# proportional term
		self.proportional = self.Kp * error 
		
		# integral term
		self.integral += error * dt                   
		if self.integral > self.max_output:
			self.integral = self.max_output
		if self.integral < self.min_output:
			self.integral = self.min_output
		# derivative term	
		if dt != 0:                              # no div by zero
			self.derivative = de/dt                     
		else:
			self.derivative = 0
			
		self.prevtm = self.currtm               # save t for next pass
		self.prev_err = error                   # save t-1 error

		# sum the terms and return the result
		output = self.proportional + (self.Ki * self.integral) + (self.Kd * self.derivative)
		if output > self.max_output:
			output = self.max_output
		elif output < self.min_output:
			output = self.min_output

		return output

# mypid = PID_controller()
# mypid.Initialize(1,1,0.1)
# for i in range(10, -1,-1):
	# print mypid.Compute(0.1*i)
	# time.sleep(0.0333)
# a = input()
		