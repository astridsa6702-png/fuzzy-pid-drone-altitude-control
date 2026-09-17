import numpy as np
import matplotlib.pyplot as plt
import turtle
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd


#GLOBAL PARAMS
TIMER = 0
TIME_STEP = 0.001
limit_counter = 3000
TK = TIME_STEP * limit_counter
SETPOINT = 100
SIM_TIME = 50
INITIAL_X = 0
INITIAL_Y = 0
MASS = 1 #kg
MAX_THRUST = 20 #Newtons
g = -9.81 #Gravitational constant
V_i = 0 #initial velocity
Y_i = 0 #initial height
historykp = []
historyki = []
historykd = []

MASS_TIME = 25

#---PID GAINS---

KP = 1
TI = 10
TD = 10
KI = KP * (TK/TI)
KD = KP * (TD/TK)
historykp.append(KP)
historyki.append(KI)
historykd.append(KD)


#fuzzy
rise_time = ctrl.Antecedent(np.arange(0, 200, 1), 'rise_time')
overshoot = ctrl.Antecedent(np.arange(0, 200, 1), 'overshoot')
settling_time = ctrl.Antecedent(np.arange(0, 200, 1), 'settling_time')

kp = ctrl.Consequent(np.arange(-0.5, 0.5, 0.05), 'kp')
ki = ctrl.Consequent(np.arange(-0.5, 0.5, 0.05), 'ki')
kd = ctrl.Consequent(np.arange(-0.5, 0.5, 0.05), 'kd')

# Define the fuzzy sets for each variable
rise_time['low'] = fuzz.trapmf(rise_time.universe, [0, 0, 50, 100])
rise_time['medium'] = fuzz.trimf(rise_time.universe, [50, 100, 150])
rise_time['high'] = fuzz.trimf(rise_time.universe, [100, 200, 200])

overshoot['low'] = fuzz.trapmf(overshoot.universe, [0, 0, 50, 100])
overshoot['medium'] = fuzz.trimf(overshoot.universe, [50, 100, 150])
overshoot['high'] = fuzz.trimf(overshoot.universe, [100, 200, 200])

settling_time['low'] = fuzz.trapmf(settling_time.universe, [0, 0, 50, 100])
settling_time['medium'] = fuzz.trimf(settling_time.universe, [50, 100, 150])
settling_time['high'] = fuzz.trimf(settling_time.universe, [100, 200, 200])

kp['NH'] = fuzz.trimf(kp.universe, [-0.5, -0.5, -0.3])
kp['NM'] = fuzz.trimf(kp.universe, [-0.4, -0.25, -0.1])
kp['NL'] = fuzz.trimf(kp.universe, [-0.2, -0.1, 0])
kp['Z'] = fuzz.trimf(kp.universe, [-0.05, 0, 0.05])
kp['PL'] = fuzz.trimf(kp.universe, [0, 0.1, 0.2])
kp['PM'] = fuzz.trimf(kp.universe, [0.1, 0.25, 0.4])
kp['PH'] = fuzz.trimf(kp.universe, [0.3, 0.5, 0.5])

kd['NH'] = fuzz.trimf(kd.universe, [-0.5, -0.5, -0.3])
kd['NM'] = fuzz.trimf(kd.universe, [-0.4, -0.25, -0.1])
kd['NL'] = fuzz.trimf(kd.universe, [-0.2, -0.1, 0])
kd['Z'] = fuzz.trimf(kd.universe, [-0.05, 0, 0.05])
kd['PL'] = fuzz.trimf(kd.universe, [0, 0.1, 0.2])
kd['PM'] = fuzz.trimf(kd.universe, [0.1, 0.25, 0.4])
kd['PH'] = fuzz.trimf(kd.universe, [0.3, 0.5, 0.5])

ki['NH'] = fuzz.trimf(ki.universe, [-0.5, -0.5, -0.3])
ki['NM'] = fuzz.trimf(ki.universe, [-0.4, -0.25, -0.1])
ki['NL'] = fuzz.trimf(ki.universe, [-0.2, -0.1, 0])
ki['Z'] = fuzz.trimf(ki.universe, [-0.05, 0, 0.05])
ki['PL'] = fuzz.trimf(ki.universe, [0, 0.1, 0.2])
ki['PM'] = fuzz.trimf(ki.universe, [0.1, 0.25, 0.4])
ki['PH'] = fuzz.trimf(ki.universe, [0.3, 0.5, 0.5])

# Define the fuzzy rules
kp_rule1 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['low'], kp['Z'])
kp_rule2 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['medium'], kp['Z'])
kp_rule3 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['high'], kp['NL'])
kp_rule4 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['low'], kp['NL'])
kp_rule5 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['medium'], kp['NL'])
kp_rule6 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['high'], kp['NL'])
kp_rule7 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['low'], kp['NL'])
kp_rule8 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['medium'], kp['NL'])
kp_rule9 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['high'], kp['NL'])

kp_rule10 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['low'], kp['PM'])
kp_rule11 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['medium'], kp['PM'])
kp_rule12 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['high'], kp['PM'])
kp_rule13 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['low'], kp['PM'])
kp_rule14 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['medium'], kp['PM'])
kp_rule15 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['high'], kp['PM'])
kp_rule16 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['low'], kp['NM'])
kp_rule17 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['medium'], kp['NM'])
kp_rule18 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['high'], kp['NM'])

kp_rule19 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['low'], kp['PH'])
kp_rule20 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['medium'], kp['PH'])
kp_rule21 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['high'], kp['PH'])
kp_rule22 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['low'], kp['PH'])
kp_rule23 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['medium'], kp['PH'])
kp_rule24 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['high'], kp['PH'])
kp_rule25 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['low'], kp['NH'])
kp_rule26 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['medium'], kp['NH'])
kp_rule27 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['high'], kp['NH'])
# Add more rules as needed

# Create the control system
ki_rule1 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['low'], ki['Z'])
ki_rule2 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['medium'], ki['Z'])
ki_rule3 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['high'], ki['NM'])
ki_rule4 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['low'], ki['PM'])
ki_rule5 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['medium'], ki['PM'])
ki_rule6 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['high'], ki['PM'])
ki_rule7 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['low'], ki['PM'])
ki_rule8 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['medium'], ki['PM'])
ki_rule9 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['high'], ki['NM'])

ki_rule10 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['low'], ki['PL'])
ki_rule11 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['medium'], ki['PL'])
ki_rule12 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['high'], ki['PL'])
ki_rule13 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['low'], ki['PM'])
ki_rule14 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['medium'], ki['PM'])
ki_rule15 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['high'], ki['PM'])
ki_rule16 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['low'], ki['PH'])
ki_rule17 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['medium'], ki['PH'])
ki_rule18 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['high'], ki['PH'])

ki_rule19 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['low'], ki['NL'])
ki_rule20 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['medium'], ki['NL'])
ki_rule21 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['high'], ki['NL'])
ki_rule22 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['low'], ki['NM'])
ki_rule23 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['medium'], ki['NM'])
ki_rule24 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['high'], ki['NM'])
ki_rule25 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['low'], ki['NH'])
ki_rule26 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['medium'], ki['NH'])
ki_rule27 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['high'],ki['PH'])
# Kd

# Define the fuzzy rules
kd_rule1 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['low'], kd['Z'])
kd_rule2 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['medium'], kd['Z'])
kd_rule3 = ctrl.Rule(rise_time['low'] & overshoot['low'] & settling_time['high'], kd['Z'])
kd_rule4 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['low'], kd['PL'])
kd_rule5 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['medium'], kd['PL'])
kd_rule6 = ctrl.Rule(rise_time['low'] & overshoot['medium'] & settling_time['high'], kd['NL'])
kd_rule7 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['low'], kd['PL'])
kd_rule8 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['medium'], kd['PL'])
kd_rule9 = ctrl.Rule(rise_time['low'] & overshoot['high'] & settling_time['high'], kd['PL'])

kd_rule10 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['low'], kd['NL'])
kd_rule11 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['medium'], kd['NL'])
kd_rule12 = ctrl.Rule(rise_time['medium'] & overshoot['low'] & settling_time['high'], kd['NL'])
kd_rule13 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['low'], kd['Z'])
kd_rule14 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['medium'], kd['Z'])
kd_rule15 = ctrl.Rule(rise_time['medium'] & overshoot['medium'] & settling_time['high'], kd['Z'])
kd_rule16 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['low'], kd['PM'])
kd_rule17 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['medium'], kd['PM'])
kd_rule18 = ctrl.Rule(rise_time['medium'] & overshoot['high'] & settling_time['high'], kd['PM'])

kd_rule19 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['low'], kd['NL'])
kd_rule20 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['medium'], kd['NL'])
kd_rule21 = ctrl.Rule(rise_time['high'] & overshoot['low'] & settling_time['high'], kd['NL'])
kd_rule22 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['low'], kd['NM'])
kd_rule23 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['medium'], kd['NM'])
kd_rule24 = ctrl.Rule(rise_time['high'] & overshoot['medium'] & settling_time['high'], kd['NM'])
kd_rule25 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['low'], kd['NH'])
kd_rule26 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['medium'], kd['NH'])
kd_rule27 = ctrl.Rule(rise_time['high'] & overshoot['high'] & settling_time['high'], kd['NH'])
# Add more rules as needed

pid_ctrl = ctrl.ControlSystem(
	[kp_rule1, kp_rule2, kp_rule3, kp_rule4, kp_rule5, kp_rule6, kp_rule7, kp_rule8, kp_rule9, kp_rule10,
	 kp_rule11, kp_rule12, kp_rule13, kp_rule14, kp_rule15, kp_rule16, kp_rule17, kp_rule18, kp_rule19,
	 kp_rule20, kp_rule21, kp_rule22, kp_rule23, kp_rule24, kp_rule25, kp_rule26, kp_rule27,
	 kd_rule1, kd_rule2, kd_rule3, kd_rule4, kd_rule5, kd_rule6, kd_rule7, kd_rule8, kd_rule9, kd_rule10,
	 kd_rule11, kd_rule12, kd_rule13, kd_rule14, kd_rule15, kd_rule16, kd_rule17, kd_rule18, kd_rule19,
	 kd_rule20, kd_rule21, kd_rule22, kd_rule23, kd_rule24, kd_rule25, kd_rule26, kd_rule27,
	 ki_rule1, ki_rule2, ki_rule3, ki_rule4, ki_rule5, ki_rule6, ki_rule7, ki_rule8, ki_rule9, ki_rule10,
	 ki_rule11, ki_rule12, ki_rule13, ki_rule14, ki_rule15, ki_rule16, ki_rule17, ki_rule18, ki_rule19,
	 ki_rule20, ki_rule21, ki_rule22, ki_rule23, ki_rule24, ki_rule25, ki_rule26, ki_rule27
	 ])

# Create a simulation
pid_sim = ctrl.ControlSystemSimulation(pid_ctrl)

class Simulation(object):
	def __init__(self):
		self.Insight = Rocket()

		self.KP = KP
		self.TI = TI
		self.TD = TD
		self.KI = KI
		self.KD = KD
		self.pid = PID(KP,KI,KD,SETPOINT)
		self.screen = turtle.Screen()
		self.screen.setup(800,600)
		self.marker = turtle.Turtle()
		self.marker.penup()
		self.marker.left(180)
		self.marker.goto(15,SETPOINT)
		self.marker.color('red')
		self.sim = True
		self.timer = 0
		self.timer_fuzzy = 0
		self.poses = np.array([])
		self.times = np.array([])
		self.trs = np.array([])
		self.overs = np.array([])
		self.tss = np.array([])

		self.errors = np.array([])

		self.time_fuzzy = np.array([])
		self.response_fuzzy= np.array([])
		self.setpoint_fuzzy = np.array([])

		self.SETPOINT = SETPOINT
		self.pid_sim  = pid_sim
		self.counter = 0
		self.hasil_perstep = list()

	def calculate_overshoot(self,time, response, setpoint): #dah benar
		steady_state_value = setpoint[-1]  # Assuming the last value is the steady-state
		peak_value = max(response)  # Maximum value reached
		overshoot = ((peak_value - steady_state_value) / steady_state_value) * 100
		return overshoot, peak_value

	def calculate_settling_time(self,time, response, setpoint, tolerance=0.02):
		steady_state_value = setpoint[-1]
		upper_bound = steady_state_value * (1 + tolerance)
		lower_bound = steady_state_value * (1 - tolerance)

		# Find the last time the response goes outside the tolerance band
		for i in range(len(time) - 1, -1, -1):
			if response[i] > upper_bound or response[i] < lower_bound:
				return time[i + 1] if i + 1 < len(time) else time[i]
		return 0  # If response never goes out of bounds

	def calculate_rise_time(self, time, response, setpoint, low=0.10, high=0.90):
		setpoint_val = setpoint[-1]

		# Jika mendekati stabil, maka rise time = 0
		if abs(setpoint_val - SETPOINT) <= 2:
			return 0

		lower_bound = SETPOINT * low   # 10% dari setpoint global
		upper_bound = SETPOINT * high  # 90% dari setpoint global

		T_10 = None
		T_90 = None

		for i in range(len(time)):
			if T_10 is None and response[i] >= lower_bound:
				T_10 = time[i]
			if T_10 is not None and response[i] >= upper_bound:
				T_90 = time[i]
				break

		if T_10 is not None and T_90 is not None:
			return T_90 - T_10
		else:
			return time[-1] - time[0]  # Jika tidak ada waktu yang ditemukan

	def clamp(self,value,min_value,max_value):
		return max(min_value,min(value,max_value))

	def fuzzy_mamdani(self,tr,over,ts):

		# Example input values
		self.pid_sim.input['rise_time'] = tr
		self.pid_sim.input['overshoot'] = over
		self.pid_sim.input['settling_time'] = ts

		# Compute the output
		self.pid_sim.compute()

		mult_kp = self.pid_sim.output['kp']
		mult_ti = self.pid_sim.output['ki']
		mult_td = self.pid_sim.output['kd']
		

		return mult_kp,mult_ti,mult_td


	def cycle(self):
		global MASS
		while(self.sim):
			#Performance Evaluation
			posisi_saat_ini  = self.Insight.get_y()
			set_point = self.SETPOINT

			tr_rat = 0
			over_rat = 0
			ts_rat = 0

			thrust = self.pid.compute(self.Insight.get_y(),self.KP,self.KI,self.KD)
			# print(thrust)
			
			error = self.SETPOINT - self.Insight.get_y()
			self.errors = np.append(self.errors, error)
			
			self.Insight.set_ddy(thrust)
			self.Insight.set_dy()
			self.Insight.set_y()
			#time.sleep(TIME_STEP)
			self.timer += TIME_STEP
			self.timer_fuzzy += TIME_STEP
			self.counter += 1

			if (self.timer > MASS_TIME) :
			 	MASS = 0.5
				 
			if self.timer > SIM_TIME:
				print("SIM ENDED")
				self.sim = False
		
			# elif self.Insight.get_y() > 700:
			# 	print("OUT OF BOUNDS")
			# 	self.sim = False
			# elif self.Insight.get_y() < -700:
			# 	print("OUT OF BOUNDS")
			# 	self.sim = False
			self.poses = np.append(self.poses,self.Insight.get_y())
			self.times = np.append(self.times,self.timer)
			self.time_fuzzy = np.append(self.time_fuzzy,self.timer_fuzzy)
			self.setpoint_fuzzy = np.append(self.setpoint_fuzzy, set_point)
			self.response_fuzzy = np.append(self.response_fuzzy, self.Insight.get_y())

			if (self.counter == limit_counter):

				overshoot, peak = self.calculate_overshoot(self.time_fuzzy, self.response_fuzzy, self.setpoint_fuzzy)

				# Calculate settling time
				settling_time = self.calculate_settling_time(self.time_fuzzy, self.response_fuzzy, self.setpoint_fuzzy)

				# Calculate rise time
				rise_time = self.calculate_rise_time(self.time_fuzzy, self.response_fuzzy, self.setpoint_fuzzy)

				self.trs = np.append(self.trs,rise_time)
				self.overs = np.append(self.overs,overshoot)
				self.tss = np.append(self.tss,settling_time) 
			
				if (len(self.trs) > 1):
					tr_rat = self.trs[-1] * 100 / 1
				elif (len(self.trs) > 0):
					tr_rat = self.trs[-1] * 100 / self.trs[-1]

				if (len(self.overs) > 1):
					over_rat = self.overs[-1] * 100 / 50
				elif (len(self.overs) > 0):
					over_rat = self.overs[-1] * 100 / self.overs[-1]

				if (len(self.tss) > 1):
					ts_rat = self.tss[-1] * 100 / 1
				elif (len(self.tss) > 0):
					ts_rat = self.tss[-1] * 100 / self.tss[-1]

				tr_rat = self.clamp(tr_rat, 0, 200)
				over_rat = self.clamp(over_rat, 0, 200)
				ts_rat = self.clamp(ts_rat, 0, 200)

				KPMult, TIMult, TDMult = self.fuzzy_mamdani(tr_rat, over_rat, ts_rat)

				self.KP = self.KP + (self.KP * KPMult)
				self.TI = self.TI + (self.TI * TIMult)
				self.TD = self.TD + (self.TD * TDMult)

				self.KI = self.KP * (TK/self.TI)
				self.KD = self.KP * (self.TD/TK)

				historykp.append(self.KP)
				historyki.append(self.KI)
				historykd.append(self.KD)
				
				print(F"KpMult = {KPMult:.2f} - TiMult = {TIMult:.2f} - TdpMult = {TDMult:.2f} - KP = {self.KP:.2f} - KI = {self.KI:.2f} - KD = {self.KD:.2f} [tr = {tr_rat:.2f} - o = {over_rat:.2f} - ts = {ts_rat:.2f}] - m = {MASS}")
				self.hasil_perstep.append([rise_time,overshoot,settling_time,tr_rat,over_rat,ts_rat,KPMult,TIMult,TDMult,self.KP,self.KI,self.KD])
				self.counter = 0
				self.timer_fuzzy = 0
				self.setpoint_fuzzy = np.array([])
				self.timer_fuzzy =  np.array([])
				self.response_fuzzy= np.array([])

		df = pd.DataFrame(self.hasil_perstep, columns=['Risetime', 'OVershoot', 'Settlingg Time','Tr%','Os%','Ts%','KP Mult','KI Mult','KD Mult',"KP","KI","KD"])
		df.to_csv(str(time.time_ns())+'_data.csv', index=False)
		graph(self.times,self.poses)
		graph_pid(historykp, historyki, historykd)
		graph_error(self.times, self.errors) 
		

def graph(x,y):
    plt.plot(x,y)
    plt.show()

def graph_pid(historykp, historyki, historykd) :
	#x = list(range(len(historykp)))
	x = [i * limit_counter * TIME_STEP for i in range(len(historykp))]

	plt.figure(figsize=(10, 5))
	plt.plot(x, historykp, label='Kp', marker='o')
	plt.plot(x, historykd, label='Kd', marker='x')
	plt.plot(x, historyki, label='Ki', marker='s')

	plt.xlabel('Waktu (detik)')
	plt.ylabel('Nilai')
	plt.title('Grafik Nilai Kp, Ki, dan Kd')
	plt.xlim(0, SIM_TIME)
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()

def graph_error(x, errors):
    plt.figure(figsize=(10, 5))
    plt.plot(x, errors, label='Error', color='red')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)  # garis nol
    plt.xlabel('Waktu (detik)')
    plt.ylabel('Error')
    plt.title('Grafik Error')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


class Rocket(object):
	def __init__(self):
		global Rocket
		self.Rocket = turtle.Turtle()
		self.Rocket.shape('square')
		self.Rocket.color('black')
		self.Rocket.penup()
		self.Rocket.goto(INITIAL_X,INITIAL_Y)
		self.Rocket.speed(0)
		#physics
		self.ddy = 0
		self.dy = V_i
		self.y = INITIAL_Y
	def set_ddy(self,thrust):
		self.ddy = g + thrust / MASS
	def get_ddy(self):
		return self.ddy
	def set_dy(self):
		self.dy += self.ddy
	def get_dy(self):
		return self.dy
	def set_y(self):
		self.Rocket.sety(self.y + self.dy)
	def get_y(self):
		self.y = self.Rocket.ycor()
		return self.y

class PID(object):
	def __init__(self,KP,KI,KD,target):
		self.kp = KP
		self.ki = KI
		self.kd = KD
		self.setpoint = target
		self.error = 0
		self.integral_error = 0
		self.error_last = 0
		self.derivative_error = 0
		self.output = 0
	def compute(self, pos,KP,KI,KD):
		self.kp = KP
		self.ki = KI
		self.kd = KD
		self.error = self.setpoint - pos
		self.integral_error += self.error * TIME_STEP
		self.derivative_error = (self.error - self.error_last)
		self.error_last = self.error
		self.output = self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error
		

		if self.output >= MAX_THRUST:
			self.output = MAX_THRUST
		elif self.output <= 0:
			self.output = 0
		return self.output


def main():
	sim = Simulation()
	sim.cycle()

main()