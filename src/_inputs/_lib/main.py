#main Working program

import os
import pandas as pd
import json
import simpy
from jsonmerge import merge
from datetime import datetime,date,timedelta
import plotly.express as px
import plotly
import csv
from csv import DictWriter
import time
import random
import plotly.graph_objects as go
# import SecondWindow
import src._inputs._lib.main_inputs as mi
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import holidays

mcf_holidays = ["2022-03-01","2022-05-03","2022-05-16","2022-08-09","2022-08-11","2022-08-19","2022-10-04","2022-10-05","2022-10-24","2022-10-25","2022-10-26","2022-11-08"]
india_holidays = holidays.India(years = 2022)

input_folder = os.path.join(os.getcwd(),"src/_inputs/data")
output_folder = os.path.join(os.getcwd(),"src/_outputs")

Schedule = []
# machine_utilization = []
x=[] ##for machine utilization
y=[] ##for machine utilization
# inventory = []
completed_order = {
		"LWSCZAC (2nd Class AC Chair Car)" : 0,
		"LWFCZAC (Executive Class AC Chair Car)" : 0,
		"LWACCN (AC-3Tier)" : 0,
		"HUMSAFAR (AC-3Tier)" : 0,
		"LWACCW (AC-2 Tier)":0,
		"LWSCN (Non-AC Sleeper)":0,
		"LS (GS/EOG 100 SEATER)":0,
		"LWSDD (Deendayalu)": 0,
		"LWS (Antyodaya Coach)": 0,
		"LWLRRM (450KVA Power Car)":0,
		"LWLRRM (750KVA Power Car)":0,
		"LDSLR (Under Slung Luggage Cum brake Van)": 0,
		"LSLRD with DA set (Luggage Cum brake van)": 0,
		"LWCBAC (AC Buffet Car)":0,
		"LWSCZ (2nd Class Non-AC Chair Car)": 0,
		"TRC (AC Track recording Car)": 0,
		"TRSC (AC track recording staff Car)": 0,
		"LWFAC (AC 1st Class)": 0,
		"LFCWAC Composite (FAC+AC2T)":0,
		"LVPH (LHB Parcel Van)": 0,
		"LWACCNE (Gareeb Rath AC Sleeper Coach)":0,
		"LWS-AC (AC- General)":0
	}

def toClearCompletedOrders():
	for i in range(0,22):
		completed_order[i] = 0
		# print(completed_order[i])


##############################################################
#############Creating Virtual Machine Object Template#################
############################################################## 
def progressBarCalc(orders,completed_order):
	total_orders = 0
	compl_orders =0.01
	# global perc_orders
	for order in orders:
		for variant in order.keys():
			total_orders = total_orders + int(order[variant]["qty"])
			# print(total_orders)
			compl_orders = compl_orders + int(completed_order[variant])
			# print(compl_orders)
			progress_unit = int(compl_orders*100/total_orders)
			# print(progress_unit)
			# sw=SecondWindow.InventoryAndProgressBar()
			# sw.progressBarValue(progress_unit)
			# sw = SecondWindow.Ui_MainSecondWindow()
			
	return progress_unit

##############################################################
#############Creating Virtual Machine Object Template#################
############################################################## 

def call_this(request,orders):
	orders_given = []
	
	
	def create_order(order_variant, order_qty,
                     order_priority, order_start_date):
		orders_given.append(
			{order_variant:
				{'qty': order_qty,
					'priority': order_priority,
					'start_date': order_start_date}
				}
		)
		
	if len(orders) > 0:
		for order in orders:
			create_order(order.orderVariant,int(order.orderQuantity),int(order.orderPriority),str(order.orderStartDate))

	class Machine(object):
		def __init__(self,name,line,machine_no,status,operation):
			self.name = name
			self.line = line
			self.machine_no = machine_no
			self.status = status
			self.available = True
			self.operation = operation

	#######################################################################################
	#######Start delivery of required components to a machine and start the operation#######
	#######################################################################################
		def distribution_and_operation(self,env,components_list):
		# while done_in:
			# print("delivery started")
			yield env.timeout(0)
			env.process(self.start_operation(env,operations[self.operation],components_list))

	#######################################################################
	################Start the operation on a Machine#######################
	#######################################################################
		def start_operation(self,sim_inst,operation,components):
			if self.status == "READY":
				print("*******************************************************")
				print("*****************Something went wrong.*****************")
				print("*******************************************************")
				print(self.name,self.status)
				return
			# self.status = "NOT READY"
			proc_t = operation["time"][components[0].coach_variant]
			done_in = proc_t
			if self.name not in x:
				x.append(self.name)
				y.append(0)
			y[x.index(self.name)]+=proc_t
			# machine_utilization[self.name]+=proc_t
			data = dict()
			while done_in:
				start = env.now
				data["Operation"] = operation["name"]
				data["Machine"] = self.name
				data["Coach Variant"] = components[0].coach_variant
				data["Start Time"] = convert_to_date(start*60)
				data["Input"] = []
				for item in components:
					data["Input"].append(item.name)
				# print("started processing %s on machine %s at %s"%(operation["name"],self.name,start))
				yield env.timeout(done_in)
				# self.part_being_proc = None
				self.available = True
				self.status = "READY"
				# print("Completed the process step of %s on machine %s at %s"
								#   "next machine."%(operation["name"], self.name, env.now))
				done_in = 0
			variant = components[0].coach_variant
			priority = components[0].priority
			comp_no = components[0].component_no
			line = components[0].line
			data["Output"] = []
			data["End Time"] = convert_to_date(env.now*60)
			for item in operation["outputs"]:
				if item["name"] == "Coach":
					data["Output"].append("Coach")
					completed_order[variant]+=1 
					break
				if item in operation["inputs"]:
					for comp in components:
						if comp.name == item["name"] and comp.component_no == item["part_no"] and comp.assembly_code == item["assembly_code"]:
							comp_tup = (item["name"],item["part_no"],item["assembly_code"])
							# print(comp_tup)
							new_comp = Component(comp.name,comp.coach_variant,comp.priority,comp.line,comp.component_no,process_flow[comp.line][comp_tup][0]["route"][comp.seq+1],"READY",comp.seq+1,comp.assembly_code,"")
							data["Output"].append(new_comp.name)
							components.remove(comp)
							del comp
							mi.inventory.append(new_comp)
				else:
					comp_tup = (item["name"],item["part_no"],item["assembly_code"])
					if comp_tup not in process_flow[line]:
						# completed_order[variant]+=1 
						# break
						# print(comp_tup)
						if comp_tup in process_flow["SH"]:
							line = "SH"
						else:
							print("some problem with changing line")
							exit()
					new_comp = Component(comp_tup[0],variant,priority,line,comp_tup[1],process_flow[line][comp_tup][0]["route"][0],"READY",0,comp_tup[2],"")
					data["Output"].append(new_comp.name)
					mi.inventory.append(new_comp)
			for comp in components:
				del comp
			data["Coach Variant Manufactured"] = completed_order[variant]		
			Schedule.append(data)
			
					
	##############################################################
	#############Creating Virtual Components Object Template##############
	##############################################################
	class Component(object):
		def __init__(self,name,coach_variant,priority,line,component_no,machine,status,seq,assembly_code,start_date):
			self.name = name
			self.coach_variant = coach_variant
			self.priority = priority
			self.line = line
			self.component_no = component_no
			self.machine = machine
			self.status = status
			self.seq = seq
			self.assembly_code = assembly_code
			self.start_date = start_date


	######################################################################################################
	#############Importing Machine Data and Creating Machine Objects using the above class################
	#####################################################################################################
	machines_data_from_csv = pd.read_csv(os.path.join(input_folder,"machine.csv"))
	machine_data_list = []
	for index, row in machines_data_from_csv.iterrows():
		d = {"name":row[0],"line":row[1],"machine_no":row[2],"status":row[3],"operation":row[4]}
		machine_data_list.append(d)

	machines_list = [Machine(mach["name"],mach["line"],mach["machine_no"],mach["status"],mach["operation"]) for mach in machine_data_list]

	def print_machines(machines_list):
		print("*******************************************************")
		print("*************Machines in the Virtual Factory***********")
		print("*******************************************************")
		for mach in machines_list:
			print("Name:",mach.name,"Line:",mach.line,"Machine No:",mach.machine_no,"Status:",mach.status)

	# print_machines(machines_list)

	##################################################################################################
	#############Importing Process flow and Process it to make a usable data structure#################
	##################################################################################################
	lines = ['SWL','EWL','RF','UF','SH']
	process_flow = {}
	swl_process_flow = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'swl_process_flow',header = None,skiprows = [0],engine="openpyxl")
	ewl_process_flow = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'ewl_process_flow',header = None,skiprows = [0],engine="openpyxl")
	rf_process_flow = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'rf_process_flow',header = None,skiprows = [0],engine="openpyxl")
	uf_process_flow = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'uf_process_flow',header = None,skiprows = [0],engine="openpyxl")
	sh_process_flow = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'sh_process_flow',header = None,skiprows = [0],engine="openpyxl")
	all_process_flows = [swl_process_flow,ewl_process_flow,rf_process_flow,uf_process_flow,sh_process_flow]
	for j in range(len(all_process_flows)):
		# print(i)
		pf = all_process_flows[j]
		process_d = {}
		columns = list(pf)
		for index, row in pf.iterrows():
				# print(row)
				# exit()
				comp_no = row[2]
				if pd.isnull(row[2]):
						comp_no = 0
				ac = str(row[0])
				if pd.isnull(row[0]):
						ac = "Z"
				if ac!=0 and '=' in str(ac):
						index = ac.index("=")
						ac = ac[index+1:]
				p = (row[1],comp_no,ac)
				if p in process_d:
						print(p)

				if pd.isnull(row[1]) == False and p not in process_d:
						process_d[p] = []
				temp = {}
				temp["route"] = []
				temp["qpc"] = row[3]
				for i in range(4,len(columns)): 
					if pd.isnull(row[i]) == False:
						temp["route"].append(row[i])
				process_d[p].append(temp)

		d = {lines[j]: process_d}
		process_flow.update(d)

	# print(process_flow)

	##############################################################
	#############Importing Operation details#################
	##############################################################
	swl_op = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'swl_operation_components',header = None,skiprows = [0],engine="openpyxl")
	ewl_op = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'ewl_operation_components',header = None,skiprows = [0],engine="openpyxl")
	rf_op = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'rf_operation_components',header = None,skiprows = [0],engine="openpyxl")
	uf_op = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'uf_operation_components',header = None,skiprows = [0],engine="openpyxl")
	sh_op = pd.read_excel(os.path.join(input_folder,'operation_data.xlsx'),sheet_name = 'sh_operation_components',header = None,skiprows = [0],engine="openpyxl")
	operations = {}
	operation_list = [swl_op,ewl_op,rf_op,uf_op,sh_op]
	for op in operation_list:
		for index, row in op.iterrows():
			# print(row[0],row[1],row[2],row[3],row[4])
			if pd.isnull(row[0]):
				continue
			if row[0] not in operations:
				operations[row[0]] = {}
				operations[row[0]]["name"] = row[0]
			if "inputs" not in operations[row[0]]:
				operations[row[0]]["inputs"] = []
			if "outputs" not in operations[row[0]]:
				operations[row[0]]["outputs"] = []
			if row[4] == "I":
				ac = str(row[5])
				if pd.isnull(row[5]):
					ac = "Z"
				if ac != 0 and '=' in str(ac):
					index = ac.index("=")
					# ac = ac[index+1:]
					ac = ac[0:index]
				
				operations[row[0]]["inputs"].append({
					"name": row[1],
					"part_no": 0 if pd.isnull(row[2]) else row[2],
					"qpc": row[3],
					"assembly_code": ac
					})
			elif row[4] == "O":
				ac = str(row[5])
				if pd.isnull(row[5]):
					ac = "Z"
				if ac != 0 and '=' in str(ac):
					index = ac.index("=")
					# ac = ac[index+1:]
					ac = ac[0:index]

				operations[row[0]]["outputs"].append({
					"name": row[1],
					"part_no": 0 if pd.isnull(row[2]) else row[2],
					"qpc": row[3],
					"assembly_code": ac
					})

	uf_operation_details = pd.read_excel(os.path.join(input_folder,'manufacturing_data_all_variants.xlsx'),sheet_name ='UF' ,engine="openpyxl")
	ew_operation_details = pd.read_excel(os.path.join(input_folder,'manufacturing_data_all_variants.xlsx'),sheet_name ='EW' ,engine="openpyxl")
	sw_operation_details = pd.read_excel(os.path.join(input_folder,'manufacturing_data_all_variants.xlsx'),sheet_name ='SW' ,engine="openpyxl")
	rf_operation_details = pd.read_excel(os.path.join(input_folder,'manufacturing_data_all_variants.xlsx'),sheet_name ='RF' ,engine="openpyxl")
	sh_operation_details = pd.read_excel(os.path.join(input_folder,'manufacturing_data_all_variants.xlsx'),sheet_name ='Shell_assembly' ,engine="openpyxl")

	manufacturing_operation_list = [sw_operation_details,ew_operation_details,rf_operation_details,uf_operation_details,sh_operation_details]
	#print(manufacturing_operation_list)

	machine_list = []

	#print(uf_operation_details)

	#print(manufacturing_operation_list)
	for op in manufacturing_operation_list:
		for index, row in op.iterrows():
			#print(row[0],row[1],row[2])
			if pd.isnull(row[0]):
				continue
			if row[0] not in operations:
				operations[row[0]]= {}
			else:
				#operations[row[0]]["name"] = row[0]
				operations[row[0]]["machine"] = []
				if "&" in row[1]:
					operations[row[0]]["machine"] = row[1].split(" & ")
				else:
					operations[row[0]]["machine"].append(row[1])
				operations[row[0]]["time"] = dict()
				operations[row[0]]["time"]["LWSCZAC (2nd Class AC Chair Car)"] = row[2]
				operations[row[0]]["time"]["LWFCZAC (Executive Class AC Chair Car)"] = row[3]
				operations[row[0]]["time"]["LWACCN (AC-3Tier)"] = row[4]
				operations[row[0]]["time"]["HUMSAFAR (AC-3Tier)"] = row[5]
				operations[row[0]]["time"]["LWACCW (AC-2 Tier)"] = row[6]
				operations[row[0]]["time"]["LWSCN (Non-AC Sleeper)"] = row[7]
				operations[row[0]]["time"]["LS (GS/EOG 100 SEATER)"] = row[8]
				operations[row[0]]["time"]["LWSDD (Deendayalu)"] = row[9]
				operations[row[0]]["time"]["LWS (Antyodaya Coach)"] = row[10]
				operations[row[0]]["time"]["LWLRRM (450KVA Power Car)"] = row[11]
				operations[row[0]]["time"]["LWLRRM (750KVA Power Car)"] = row[12]
				operations[row[0]]["time"]["LDSLR (Under Slung Luggage Cum brake Van)"] = row[13]
				operations[row[0]]["time"]["LSLRD with DA set (Luggage Cum brake van)"] = row[14]
				operations[row[0]]["time"]["LWCBAC (AC Buffet Car)"] = row[15]
				operations[row[0]]["time"]["LWSCZ (2nd Class Non-AC Chair Car)"] = row[16]
				operations[row[0]]["time"]["TRC (AC Track recording Car)"] = row[17]
				operations[row[0]]["time"]["TRSC (AC track recording staff Car)"] = row[18]
				operations[row[0]]["time"]["LWFAC (AC 1st Class)"] = row[19]
				operations[row[0]]["time"]["LFCWAC Composite (FAC+AC2T)"] = row[20]
				operations[row[0]]["time"]["LVPH (LHB Parcel Van)"] = row[21]
				operations[row[0]]["time"]["LWACCNE (Gareeb Rath AC Sleeper Coach)"] = row[22]
				operations[row[0]]["time"]["LWS-AC (AC- General)"] = row[23]


	##############################################################
	###############Creating a Virtual Factory##################
	##############################################################
	env = simpy.Environment()


	###################################################################################
	#############Getting the earliest start date to start macufacturing#################
	###################################################################################
	earliest_start_date = ""
	min_time_step = 10e10
	for order in orders_given:
		for variant in order.keys():
			if order[variant]["start_date"] == "":
				continue
			if time.mktime(datetime.strptime(order[variant]["start_date"],"%Y-%m-%d").timetuple())<min_time_step:
				min_time_step = time.mktime(datetime.strptime(order[variant]["start_date"],"%Y-%m-%d").timetuple())
				earliest_start_date = order[variant]["start_date"]

	print("earliest_start_date:",earliest_start_date )


	###################################################################################################
	#############Initialize all the input components to start manufacturing operations#################
	###################################################################################################

	for order in orders_given:
		for variant in order.keys():
			for i in range(order[variant]["qty"]):
				for line in process_flow.keys():
					for comp_tup in process_flow[line]:
						# if str(comp_tup[2]).islower():
							for temp in process_flow[line][comp_tup]:
								for j in range(temp["qpc"]): 
									for items in mi.forPreInventory:
										if items.name == comp_tup[0] and items.component_no == comp_tup[1] :
											items.coach_variant = variant
											items.priority = order[variant]["priority"]
											# items.line = line
											items.seq = 0
											items.assembly_code = comp_tup[2]
											items.start_date = order[variant]["start_date"]
											new_comp1 = Component(items.name,items.coach_variant,items.priority,items.line,items.component_no,items.machine,items.status,items.seq,items.assembly_code,items.start_date)
											mi.inventory.append(new_comp1)
											mi.forPreInventory.remove(items)
											del items 			#to remove item from preinventory

	for item in mi.inventory:
		print(item.name)
		print(item.assembly_code)
	# exit()

	for order in orders_given:
		for variant in order.keys():
			for i in range(order[variant]["qty"]):
				for line in process_flow.keys():
					for comp_tup in process_flow[line]:
						if str(comp_tup[2]).islower():
							for temp in process_flow[line][comp_tup]:
								for j in range(temp["qpc"]): 
									# coach_variant,priority,line,component_no,machine_no,status
									new_comp = Component(comp_tup[0],variant,order[variant]["priority"],line,comp_tup[1],process_flow[line][comp_tup][0]["route"][0],"READY",0,comp_tup[2],order[variant]["start_date"])
									mi.inventory.append(new_comp)

	###################################################
	#############Some helper functions#################
	###################################################								   	
	def print_inv(inventory):
		print("******************Storage mi.inventory******************")
		for item in mi.inventory:
			print(item.assembly_code,end = ", ")
			print(item.name)
		print("")
	timestamp = time.mktime(datetime.strptime(earliest_start_date,"%Y-%m-%d").timetuple())
	def convert_to_date(timesteps):
		timestamps = timestamp + timesteps
		return datetime.fromtimestamp(timestamps).strftime("%Y-%m-%d %H:%M:%S")
	def convert_to_timesteps(date):
		end = time.mktime(datetime.strptime(date,"%Y-%m-%d").timetuple())
		start = time.mktime(datetime.strptime(earliest_start_date,"%Y-%m-%d").timetuple())
		return (end - start)/60
	# print_inv(mi.inventory)
	def checkDate(Schedule):
		for i in Schedule:
			start_date_and_time = i["Start Time"]
			end_date_and_time = i["End Time"]
			start_date_only = start_date_and_time.split(' ')
			end_date_only = end_date_and_time.split(' ')
			start_date_split = start_date_only[0].split('-')
			end_date_split = end_date_only[0].split('-')
			date_for_datetime = date(int(start_date_split[0]),int(start_date_split[1]),int(start_date_split[2]))
			end_date_for_datetime = date(int(end_date_split[0]),int(end_date_split[1]),int(end_date_split[2]))
			if date_for_datetime.weekday() == 6:
				d1 = date_for_datetime + timedelta(days=1)
				d2 = end_date_for_datetime + timedelta(days=1)
				new_start_date = d1.strftime("%Y-%m-%d")
				new_end_date = d2.strftime("%Y-%m-%d")
				new_appended_start_date = new_start_date +" "+start_date_only[1]
				new_appended_end_date = new_end_date +" "+end_date_only[1]
				i["Start Time"] = new_appended_start_date
				i["End Time"] = new_appended_end_date

			elif date_for_datetime in india_holidays:
				d1 = date_for_datetime + timedelta(days=1)
				d2 = end_date_for_datetime + timedelta(days=1)
				new_start_date = d1.strftime("%Y-%m-%d")
				new_end_date = d2.strftime("%Y-%m-%d")
				new_appended_start_date = new_start_date +" "+start_date_only[1]
				new_appended_end_date = new_end_date +" "+end_date_only[1]
				i["Start Time"] = new_appended_start_date
				i["End Time"] = new_appended_end_date
					
			elif str(date_for_datetime) in mcf_holidays:
				d1 = date_for_datetime + timedelta(days=1)
				d2 = end_date_for_datetime + timedelta(days=1)
				new_start_date = d1.strftime("%Y-%m-%d")
				new_end_date = d2.strftime("%Y-%m-%d")
				new_appended_start_date = new_start_date +" "+start_date_only[1]
				new_appended_end_date = new_end_date +" "+end_date_only[1]
				i["Start Time"] = new_appended_start_date
				i["End Time"] = new_appended_end_date

	###############################################################################################
	##########Check if the required input components of a machine are there in mi.inventory###########
	###############################################################################################
	###2 mi.inventory files for shop floor and 
	def check_if_components_ready_and_start_operation(inventory,priority,machine,input_components,output_components,line,variant):
		components_list = []
		# for outputItem in output_components:
		# 	if outputItem in mi.inventory:
		# 		break
			# else:
		for component in input_components:
			for item in mi.inventory:
				if item.line == line and (item.machine == machine.name or machine.name in item.machine) and item.name == component["name"] and item.component_no == component["part_no"] and item.priority == priority and item.coach_variant == variant and (item.start_date=="" or convert_to_timesteps(item.start_date) <= env.now):
					components_list.append(item)
					break
		start_operation(input_components,components_list)
	
	def start_operation(input_components,components_list):
		if len(input_components) == len(components_list):
			for item in components_list:
				mi.inventory.remove(item)
			machine.status = "NOT READY"
			env.process(machine.distribution_and_operation(env,components_list))		


	##############################################################################################
	############Function to check if order is completed and stop the factory simulation###########
	##############################################################################################
	def order_is_completed(orders_given,completed_order):
		# progressBarCalc(orders,completed_order)
		for order in orders_given:
			for variant in order.keys():
				if order[variant]["qty"] != completed_order[variant]:
					return False
		return True

	#######################################################
	#############Main Scheduling Algorithm#################
	#######################################################
	while True:
		if order_is_completed(orders_given,completed_order):
			break
		for line in lines:
			for machine in machines_list:
				if machine.line == line and machine.status == "READY":
					for priority in range(1,11):
						if machine.status == "READY":
							input_components = operations[machine.operation]["inputs"]
							output_components = operations[machine.operation]["outputs"]
							for variant in completed_order.keys():
								if machine.status == "READY":
									check_if_components_ready_and_start_operation(mi.inventory,priority,machine,input_components,output_components,line,variant)				
							
		env.step()


	# print(completed_order)
	# import pprint
	# print(Schedule)
	
	print("Time: ",env.now)
	#######################################################
	################Plotting gantt chart###################
	#######################################################
	# checkDate(Schedule)
	title = ""
	# for order in orders:
	# 	for variant in order.keys():
	# 		if order[variant]["qty"] > 0:
	# 			title += variant + ": " + " Quantity: " + str(order[variant]["qty"]) + " Priority: " + str(
	# 				order[variant]["priority"]) + " Start Date: " + order[variant]["start_date"] + "<br>"

	df = pd.DataFrame(Schedule)
	fig_machine = px.timeline(df, x_start="Start Time", x_end="End Time", y="Machine",
							hover_data=["Input", "Output", "Coach Variant Manufactured"], color="Coach Variant",
							title=title)
	fig_operation = px.timeline(df, x_start="Start Time", x_end="End Time", y="Operation",
								hover_data=["Input", "Output", "Coach Variant Manufactured"], color="Coach Variant")
	# fig_machine.update_yaxes(autorange="reversed")
	fig_machine.update_layout(
		#     title=title,
		#     # xaxis_title="Time",
		yaxis_title="Machines",
		#     # legend_title="Legend Title",
		title_font=dict(
			family="Times New Roman",
			size=14,
			color="RebeccaPurple"
		),
		font_family="Courier New, monospace",
		font_color='#222A2A'
		# font_color="RebeccaPurple"
	)
	fig_machine.update_yaxes(categoryorder='category ascending')
	fig_machine.update_yaxes(autorange="reversed")
	fig_operation.update_yaxes(autorange="reversed")
	# fig.update_layout(shapes=[
	#     dict(
	#         type='line',
	#         yref='paper', y0=0, y1=1,
	#         xref='x',
	#     )
	# ])
	fig_machine.write_html(os.path.join("templates","machine_loading_fig.html"),full_html = False)
	fig_operation.write_html(os.path.join("templates","operations_chart_fig.html"),full_html = False)
	##########################################################################
	################Writing manufacturing operations in excel#################
	##########################################################################
	with open(os.path.join(input_folder,'manufacturing_operations.csv'), 'w') as outfile:
		writer = DictWriter(outfile, (
		'Operation', 'Machine', 'Coach Variant', 'Start Time', 'End Time', 'Input', 'Output',
		'Coach Variant Manufactured'))
		writer.writeheader()
		writer.writerows(Schedule)

	global x
	global y
	y=[round((i/env.now)*100,2) for i in y]


	def sort_list(list1, list2):
	
		zipped_pairs = zip(list2, list1)
	
		z = [x for _, x in sorted(zipped_pairs)]
		
		return z
	y=sort_list(y,x)
	x=sorted(x)
	fig_machine_util = go.Figure(data=[go.Bar(
				x=x, y=y,
				text=y,
				textposition='auto',
			)])
	fig_machine_util.update_layout(
	#     title=title,
		xaxis_title="Machine",
		yaxis_title="Percentage of utilization",
	#     # legend_title="Legend Title",
		title_font=dict(
			family="Times New Roman",
			size=14,
			color="RebeccaPurple"
		),
		font_family = "Courier New, monospace",
		font_color = '#222A2A'
		# font_color="RebeccaPurple"
	)
	color = ['lightsalmon','lightsalmon','lightsalmon','tab:purple','tab:purple','tab:purple','tab:purple','tab:purple','tab:blue','tab:blue','gold','gold','gold','gold','gold','gold','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange',]
	fig_machine_util.write_html(os.path.join("templates",'machine_utilization_fig.html'))
	cew = mpatches.Patch(color='lightsalmon', label='End Wall Machines')
	crf = mpatches.Patch(color='tab:purple', label='Roof Machines')
	csh = mpatches.Patch(color='tab:blue', label='Shell Assembly Machines')
	csw = mpatches.Patch(color='gold', label='Side Wall Machines')
	cuf = mpatches.Patch(color='darkorange', label='Underframe Machines')
	# plt.legend(handles=[red_patch])
	fig = plt.figure()
	ax = fig.add_subplot()
	ax.bar(x, y,color=color)
	ax.set_title('Machine Utilization')
	ax.set_ylabel('% of utilization')
	ax.set_xlabel('Machine')
	ax.legend(handles=[cew,crf,csh,csw,cuf])
	plt.xticks(rotation=60)
	for index, value in enumerate(y):
		ax.text(index-0.15, value-8,
				str(value),color='white',rotation='270',ha='center',fontdict=dict(fontsize=10,fontfamily='Times New Roman',fontweight='bold'))
	# plt.show()
	#things to Remember
	# 1 no time data should be zero
	# 2 no data should be empty 
