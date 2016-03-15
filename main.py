#!/usr/bin/python
import sys
import os
import getopt

class Armor():
	def __init__(self):
		self.master_helms = {}
		self.master_chests = {}
		self.master_gauntlets = {}
		self.master_greaves = {}
	
	def add(self, t, name, d, w):
		if t == "helms":
			self.master_helms[name] = (d,w)
		elif t == "chests":
			self.master_chests[name] = (d,w)
		elif t == "gauntlets":
			self.master_gauntlets[name] = (d,w)
		elif t == "greaves":
			self.master_greaves[name] = (d,w)

class Main():
	def __init__(self, args):
		self.args = args
		self.user = None
		self.parse_args()
		self.owned_file = "%s_owned.txt" % self.user
		if not os.path.isfile(self.owned_file): # make sure owned file exists
			self.create_owned_file()
			sys.exit()

		self.owned_helms = []
		self.owned_chests = []
		self.owned_gauntlets = []
		self.owned_greaves = []
		try:
			self.read_owned_file()
		except IOError:
			print "Error: something went wrong reading", self.owned_file
			sys.exit()
		self.master = Armor()
		self.build_master()
		print self.master.master_helms

	def build_master(self):
		lists = [self.owned_helms, self.owned_chests, self.owned_gauntlets, self.owned_greaves]
		types = ["helms","chests","gauntlets","greaves"]
		for i in range(4):
			with open("DS3_%s.csv" % types[i], "r+") as f:
				master_list = f.read()
			for item in lists[i]:
				if item in master_list:
					d = master_list[master_list.find(item)+len(item)+1] # this is super hacky
					w = master_list[master_list.find(item)+len(item)+3]
					self.master.add(types[i],item,d,w)
				else:
					print item, "does not exist in master list.",
					add = raw_input("Would you like to interactively add it? ")
					if add.strip() in ["yes",'y']:
						d,w = self.add_item(item, types[i])
						self.master.add(types[i], item, d, w)
					else:
						print item, "must be intered in master list to continue."
						sys.exit()

	def add_item(self, item, t):
		print "Entering stats for %s." % item
		defense = raw_input("Defense: ")
		weight = raw_input("Weight: ")
		if defense.isdigit() and weight.isdigit():
			with open("DS3_%s.csv" % t, "a") as f:
				f.write("%s,%s,%s%s" % (item, defense, weight, os.linesep))
			print item, "has been added to DS3_%s.csv" % t
			return defense, weight
		else:
			print "Values entered were not interpretable as numbers."
			print item, "not added to master list."
			sys.exit()
	
	def read_owned_file(self):
		with open(self.owned_file, 'r') as f:
			for line in f:
				l = line.strip()
				if l[0] == '#':
					category = l[1:]
				elif category == "HELMS":
					self.owned_helms.append(l)
				elif category == "CHESTS":
					self.owned_chests.append(l)
				elif category == "GAUNTLETS":
					self.owned_gauntlets.append(l)
				elif category == "GREAVES":
					self.owned_greaves.append(l)
				else:
					raise IOError
	
	def create_owned_file(self):
		create = raw_input("%s was not found. Would you like it to be created for you? " % self.owned_file)
		if create in ["yes","y"]:
			with open(self.owned_file, "w") as f:
				f.write("#HELMS{0}No Helm{0}#CHESTS{0}No Chest{0}#GAUNTLETS{0}No Gauntlets{0}#GREAVES{0}No Greaves".format(os.linesep))
			print self.owned_file, "has been created."
		else:
			print "Cannot continue without", self.owned_file

	
	def usage(self):
		print "USAGE NOT YET IMPLIMENTED"
	
	def parse_args(self):
		try:
			opts,args = getopt.getopt(self.args, "hu:", ["help","user="])
		except getopt.GetOptError:
			self.usage()
			sys.exit()
		for opt,arg in opts:
			if opt in ["-h","--help"]:
				usage()
				sys.exit(1)
			elif opt in ["-u","--user"]:
				self.user = arg

		if self.user==None:	# make sure user has been updated
			self.usage()
			sys.exit()

if __name__=="__main__":
	Main(sys.argv[1:])
