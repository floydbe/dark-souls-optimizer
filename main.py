#!/usr/bin/python
import sys
import os
import getopt


class Armor():
	def __init__(self):
		self.master = {}

	def add(self, name, t, d, w):
		self.master[name] = (t, d, w)
	
	def get_type(self, t):
		return {k:v for k,v in self.master.items() if v[0]==t}

		
def add_item(item, t):
	print "Entering stats for %s." % item
	defense = raw_input("Defense: ")
	weight = raw_input("Weight: ")
	with open("DS3_%s.csv" % t, "a") as f:
		f.write("%s,%s,%s%s" % (item, defense, weight, os.linesep))
	print item, "has been added to DS3_%s.csv" % t
	return defense, weight

def build_armor_dict(a, l, t):
# a is an Armor object
# l is list of item name strings
# t is string of item type
	with open("DS3_%s.csv" % t, "r+") as f:
		master_list = f.read()
	for item in l:
		if item in master_list:
			d = master_list[master_list.find(item)+len(item)+1] # this is super hacky...
			w = master_list[master_list.find(item)+len(item)+3]
			a.add(item, t, d, w)
		else:
			print item, "does not exist in master list.",
			add = raw_input("Would you like to interactively add it? ")
			if add.strip() in ["yes","y"]:
				d, w = add_item(item, t)
				a.add(item, t, d, w)
			else:
				print item, "must be entered in master list to continue."
				sys.exit()

def read_owned_file(owned_file):
	helms = []
	chests = []
	gauntlets = []
	greaves = []
	with open(owned_file, 'r') as f:
		for line in f:
			l = line.strip()
			if l[0] == '#':
				category = l[1:]
			elif category == "HELMS":
				helms.append(l)
			elif category == "CHESTS":
				chests.append(l)
			elif category == "GAUNTLETS":
				gauntlets.append(l)
			elif category == "GREAVES":
				greaves.append(l)
			else:
				raise IOError
	return helms,chests,gauntlets,greaves

def create_owned_file(owned_file):
	create = raw_input("%s was not found. Would you like it to be created for you? " % owned_file)
	if create in ["yes","y"]:
		with open(owned_file, "w") as f:
			f.write("#HELMS{0}No Helm{0}#CHESTS{0}No Chest{0}#GAUNTLETS{0}No Gauntlets{0}#GREAVES{0}No Greaves".format(os.linesep))
		print owned_file, "has been created."
	else:
		print "Cannot continue without", owned_file


def usage():
	print "USAGE NOT YET IMPLETMENTED"

def main(argv):
	try:
		opts,args = getopt.getopt(argv, "hu:", ["help","user="])
	except getopt.GetOptError:
		usage()
		sys.exit()

	user = None	# initialize so we can tell if it has been updated

	for opt,arg in opts:
		if opt in ["-h","--help"]:
			usage()
			sys.exit(1)
		elif opt in ["-u","--user"]:
			user = arg

	if user==None:	# make sure user has been updated
		usage()
		sys.exit()
	
	owned_file = "%s_owned.txt" % user
	if not os.path.isfile(owned_file): # make sure owned file exists
		create_owned_file(owned_file)
		sys.exit()
	
	try:
		helms,chests,gauntlets,greaves = read_owned_file(owned_file)
	except IOError:
		print "Error: something went wrong reading", owned_file
	
	a = Armor()
	build_armor_dict(a,helms,"helms")	
	build_armor_dict(a,chests,"chests")
	build_armor_dict(a,gauntlets,"gauntlets")
	build_armor_dict(a,greaves,"greaves")

	print a.get_type("helms")	

if __name__=="__main__":
	main(sys.argv[1:])
