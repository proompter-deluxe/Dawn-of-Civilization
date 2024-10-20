from Core import *
from RFCUtils import *


def findSlot(iCiv):
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == iCiv)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if civ(iSlot) == -1)
	if iSlot is not None:
		return iSlot
	
	iSlot = next(iSlot for iSlot in range(iNumPlayers) if availableSlot(iSlot))
	if iSlot is not None:
		return iSlot

	return -1

def findMinorSlot(iCiv):
	return next(iSlot for iSlot in reversed(range(iNumPlayers)) if civ(iSlot) == -1)
	
def availableSlot(iSlot):
	if player(iSlot).isAlive():
		return False
	
	if player(iSlot).isHuman():
		return False
	
	if player(iSlot).isMinorCiv():
		return False
	
	return True

def slotCivsToString():
	civs = "Total slots: %s. List: " % iNumPlayers
	for iSlot in range(iNumPlayers):
		civilization = civ(iSlot)
		if civilization is None:
			civs += "None, "
		elif civilization == -1:
			civs += "-1, "
		else:
			civs += infos.civ(civilization).getText() + ", "
	
	return civs

def addPlayer(iPlayer, iCiv, iBirthTurn=-1, bAlive=False, bMinor=False):
	game.addPlayer(iPlayer, 0, iCiv, iBirthTurn, bAlive, bMinor)
	data.dSlots[iCiv] = iPlayer

def updateCivilization(iPlayer, iCiv, iBirthTurn=-1):
	data.dSlots[iCiv] = iPlayer
	data.players[iPlayer].resetStability()
	
	iCurrentCivilization = player(iPlayer).getCivilizationType()
	if iCiv == iCurrentCivilization:
		return
	
	resetRevealedOwner(iPlayer)
	
	addPlayer(iPlayer, iCiv, iBirthTurn=iBirthTurn, bAlive=True)
	
	initWars(iPlayer)
	
	if iCurrentCivilization in data.dSlots:
		del data.dSlots[iCurrentCivilization]

def initWars(iPlayer):
	iCiv = player(iPlayer).getCivilizationType()
	iTeam = player(iPlayer).getTeam()
	
	if iCiv == iNative:
		for iOtherPlayer in players.all().alive():
			if not player(iOtherPlayer).isBarbarian():
				team(gc.getBARBARIAN_TEAM()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
	
	else:
		team(gc.getBARBARIAN_TEAM()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
		
		if player(iNative).isExisting():
			team(player(iNative).getTeam()).declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def getImpact(iCiv):
	iActiveCiv = civ()

	if iActiveCiv == iCiv:
		return iImpactPlayer
	
	if iCiv in dNeighbours[iActiveCiv]:
		return iImpactPlayer
	
	if iCiv in dInfluences[iActiveCiv]:
		return iImpactPlayer
	
	iImpact = infos.civ(iCiv).getImpact()
	
	if not canEverRespawn(iCiv):
		iImpact -= 1
	
	if isOutdated(iCiv):
		iImpact -= 1
	
	return max(iImpactMarginal, iImpact)
			
def isOutdated(iCiv):
	if year() < year(dFall[iCiv]):
		return False
	
	# give an extra 100 year window after resurrection for relevance
	if any(year().between(iStart, iEnd + 100) for iStart, iEnd in dResurrections[iCiv]):
		return True

def getNextBirth():
	lUpcomingCivs = [iCiv for iCiv, iYear in dBirth.items() if turn() < year(iYear) - turns(5)]
	return find_min(lUpcomingCivs, dBirth.__getitem__).result

def getUnavailableSlots():
	return count(1 for iSlot in range(iNumPlayers) if not availableSlot(iSlot))

def allSlotsTaken():
	return getUnavailableSlots() >= iNumPlayers-1