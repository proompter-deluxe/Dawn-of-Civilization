from MapParser import *


PATH_TEMPLATE = "Mods/DoC-Cross-Overhaul/PrivateMaps/%s.txt"


def parseBaseMap():
	mapName = "RFC_Earth"
	parser = MapParser()
	parser.read(PATH_TEMPLATE % mapName)
	return parser

def parseScenarioMap(scenario):
	parser = parseBaseMap()
	parser.read(PATH_TEMPLATE % scenario.fileName)
	return parser