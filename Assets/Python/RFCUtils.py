from Civilizations import *
from Civilizations import dNeverTrain
from Core import *

from Events import events
from Popups import popup

import BugCore
import CvScreenEnums

MainOpt = BugCore.game.MainInterface

bStabilityOverlay = False

# used: AIWars
# finds a free adjacent plot to spawn units in, uses capital location as fallback
def findNearestLandPlot(tPlot, iPlayer):
	plot = plots.surrounding(tPlot).where(lambda p: not p.isWater() and not p.isPeak() and not p.isUnit()).random()
	if plot: return plot
	
	# if no plot is found, return that player's capital
	return plots.capital(iPlayer)

# only used in Plague
def isMortalUnit(unit):
	# great leaders
	if unit.getUpgradeDiscount() >= 100: return False
	
	# mechanical units
	if infos.unit(unit).isMechUnit(): return False
	
	# civilian units
	if not unit.canFight(): return False
	
	return True

# used: Plague
def isDefenderUnit(unit):
	pUnitInfo = infos.unit(unit)
	
	if not pUnitInfo: return False
	
	# Archery units with city defense
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_ARCHER') and pUnitInfo.getCityDefenseModifier() > 0:
		return True
		
	# Melee units with mounted modifiers
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_MELEE') and pUnitInfo.getUnitCombatModifier(infos.type('UNITCOMBAT_HEAVY_CAVALRY')) > 0:
		return True
		
	# Conscriptable gunpowder units
	if pUnitInfo.getUnitCombatType() == infos.type('UNITCOMBAT_GUN') and pUnitInfo.getConscriptionValue() > 1:
		return True
		
	return False

# other utils functions
def checkUnitsInEnemyTerritory(iPlayer1, iPlayer2):
	return units.owner(iPlayer1).any(lambda u: plot(u).getOwner() == iPlayer2)

# used: AIWars
def restorePeaceAI(iMinorCiv, bOpenBorders):
	teamMinor = team(iMinorCiv)
	for iPlayer in players.major().existing().ai():
		if team(iMinorCiv).isAtWar(player(iPlayer).getTeam()):
			bInvadingIndependents = checkUnitsInEnemyTerritory(iPlayer, iMinorCiv)
			bInvadedByIndependents = checkUnitsInEnemyTerritory(iMinorCiv, iPlayer)
			if not bInvadingIndependents and not bInvadedByIndependents:
				teamMinor.makePeace(iPlayer)
				if bOpenBorders:
					teamMinor.signOpenBorders(iPlayer)

# used: AIWars
def restorePeaceHuman(iMinorCiv, bOpenBorders): 
	teamMinor = team(iMinorCiv)
	iHuman = active()
	if player().isExisting():
		if teamMinor.isAtWar(iHuman):
			bInvadingIndependents = checkUnitsInEnemyTerritory(iHuman, iMinorCiv)
			bInvadedByIndependents = checkUnitsInEnemyTerritory(iMinorCiv, iHuman)
			if not bInvadingIndependents and not bInvadedByIndependents:
				teamMinor.makePeace(iHuman)

# used: AIWars
def minorWars(iMinorCiv):
	teamMinor = team(iMinorCiv)
	for city in cities.owner(iMinorCiv):
		for iPlayer in players.major().existing().ai():
			if plot(city).getPlayerSettlerValue(iPlayer) > 0 or plot(city).getPlayerSettlerValue(iPlayer) >= 3:
				if not teamMinor.isAtWar(iPlayer):
					team(iPlayer).declareWar(player(iMinorCiv).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

# used: Rise
def updateMinorTechs(iMinorCiv, iMajorCiv):
	techs = infos.techs().where(team(iMajorCiv).isHasTech)
	
	if civ(iMinorCiv) == iNative:
		techs = techs.where(lambda iTech: all(iEnabledTech in techs for iEnabledTech in getEnabledTechs(iTech)))
		
		nativePlayers = players.of(*lBioNewWorld)
		if nativePlayers:
			techs = techs.where(lambda iTech: nativePlayers.all(lambda p: team(p).isHasTech(iTech)))

	for iTech in techs:
		team(iMinorCiv).setHasTech(iTech, True, iMinorCiv, False, False)
		

# used: RFCUtils
def getEnabledTechs(iTech):
	return infos.techs().where(lambda iOtherTech: isRequirement(iTech, iOtherTech))


# RFCUtils
def isRequirement(iPrereq, iTech):
	return any(infos.tech(iTech).getPrereqAndTechs(i) == iPrereq for i in range(4)) or (infos.tech(iTech).getPrereqOrTechs(0) == iPrereq and infos.tech(iTech).getPrereqOrTechs(1) == -1)


# used: RFCUtils, History
def flipCity(tCityPlot, bConquest, bKillUnits, iNewOwner, lOldOwners = []):
	"""Changes owner of city specified by tCityPlot.
	bConquest specifies if it's conquered or traded.
	If bKillUnits != 0 all the units in the city will be killed.
	lOldOwners is a list. Flip happens only if the old owner is in the list.
	An empty list will cause the flip to always happen."""
	pNewOwner = player(iNewOwner)
	x, y = location(tCityPlot)
	flipCity = city(x, y)
	
	if flipCity:
		iOldOwner = flipCity.getOwner()
		if not lOldOwners or iOldOwner in lOldOwners:
			
			if bKillUnits:
				for unit in units.at(x, y).where(lambda unit: not unit.isCargo()):
					unit.kill(False, iNewOwner)
					
			pNewOwner.acquireCity(flipCity, bConquest, not bConquest)
			
			flippedCity = city(x, y)
			flippedCity.setInfoDirty(True)
			flippedCity.setLayoutDirty(True)
			
			return flippedCity
			
	return None


# used: RFCUtils, History
def cultureManager(tCityPlot, iCulturePercent, iNewOwner, iOldOwner, bBarbarian2x2Decay, bBarbarian2x2Conversion, bAlwaysOwnPlots):
	"""Converts the culture of the city and of the surrounding plots to the new owner of a city.
	iCulturePercent determine the percentage that goes to the new owner.
	If old owner is barbarian, all the culture is converted"""
	city = city_(tCityPlot)
	
	if city:
		iCulture = city.getActualCulture(iOldOwner)
		iConvertedCulture = iCulture * iCulturePercent / 100
		
		city.changeCulture(iOldOwner, -iConvertedCulture, False)
		city.changeCulture(iNewOwner, iConvertedCulture, False)
		
		if not player(iNewOwner).isBarbarian():
			city.setCulture(barbarian(), 0, True)
			
	if bBarbarian2x2Decay or bBarbarian2x2Conversion:
		if not player(iNewOwner).isBarbarian() and not player(iNewOwner).isMinorCiv():
			for plot in plots.surrounding(tCityPlot, radius=2):
				if location(plot) == tCityPlot or not plot.isCity():
					for iMinor in players.minor().barbarian():
						iMinorCulture = plot.getCulture(iMinor)
						
						if bBarbarian2x2Decay:
							plot.setCulture(iMinor, iMinorCulture/4, True)
							
						if bBarbarian2x2Conversion:
							plot.setCulture(iMinor, 0, True)
							plot.changeCulture(iNewOwner, iMinorCulture, True)
							
	for plot in plots.surrounding(tCityPlot):
		iCulture = plot.getActualCulture(iOldOwner)
		iConvertedCulture = iCulture * iCulturePercent / 100
		
		if plot.isCity():
			plot.changeCulture(iNewOwner, iConvertedCulture, True)
			plot.changeCulture(iOldOwner, -iConvertedCulture, True)
		else:
			plot.changeCulture(iNewOwner, iConvertedCulture / 3, True)
			plot.changeCulture(iOldOwner, -iConvertedCulture / 3, True)
			
			if bAlwaysOwnPlots:
				plot.setOwner(iNewOwner)

# used: Rules
def spreadMajorCulture(iMajorCiv, tPlot):
	for city in plots.surrounding(tPlot, radius=3).cities():
		if city.getOwner() in players.minor():
			iOwner = city.getOwner()
			
			iDenominator = 25
			if plot(city).getPlayerSettlerValue(iMajorCiv) >= 5:
				iDenominator = 10
			elif plot(city).getPlayerSettlerValue(iMajorCiv) >= 2:
				iDenominator = 15
				
			city.changeCulture(iMajorCiv, city.getCulture(city.getOwner()) / iDenominator, True)
			plot(city).changeCulture(iMajorCiv, plot(city).getCulture(city.getOwner()) / iDenominator, True)

# used: Congresses, History, RFCUtils, Rise, Rules, Scenarios
def convertPlotCulture(tPlot, iPlayer, iPercent, bOwner):
	plot = plot_(tPlot)
	city = city_(tPlot)
	
	if city:
		iTotalConvertedCulture = 0
		for iLoopPlayer in players.all().without(iPlayer):
			iConvertedCulture = city.getActualCulture(iLoopPlayer) * iPercent / 100
			city.changeCulture(iLoopPlayer, -iConvertedCulture, True)
			iTotalConvertedCulture += iConvertedCulture
		
		city.changeCulture(iPlayer, iTotalConvertedCulture, True)
		
	iTotalConvertedCulture = 0
	for iLoopPlayer in players.all().without(iPlayer):
		iCulture = plot.getActualCulture(iLoopPlayer)
		iConvertedCulture = iCulture * iPercent / 100
		plot.changeCulture(iLoopPlayer, -iConvertedCulture, True)
		iTotalConvertedCulture += iConvertedCulture
	
	plot.resetCultureConversion()
	plot.changeCulture(iPlayer, iTotalConvertedCulture, True)
	
	if bOwner and plot.isOwned():
		plot.setOwner(iPlayer)
		
# used: Rules
def convertTemporaryCulture(tPlot, iPlayer, iPercent, bOwner):
	plot = plot_(tPlot)
	if not plot.isOwned() or not plot.isCore(plot.getOwner()):
		plot.setCultureConversion(iPlayer, iPercent)
	
		if bOwner:
			plot.setOwner(iPlayer)

# used: RFCUtils
# relocates units in a city plot to a free surrounding tile
def pushOutGarrisons(tCityPlot, iOldOwner):
	destination = plots.surrounding(tCityPlot, radius=2).owner(iOldOwner).without(tCityPlot).land().passable().no_enemies(iOldOwner).first()
	
	if destination:
		for unit in units.at(tCityPlot).owner(iOldOwner):
			if unit.getDomainType() == DomainTypes.DOMAIN_LAND:
				move(unit, destination)

# used: RFCUtils
def relocateSeaGarrisons(tCityPlot, iOldOwner):
	destination = cities.owner(iOldOwner).without(tCityPlot).coastal().first()
			
	if destination:
		for unit in units.at(tCityPlot).owner(iOldOwner):
			if unit.getDomainType() == DomainTypes.DOMAIN_SEA:
				move(unit, destination)

# used: Congresses, RFCUtils, Rules
def createGarrisons(tCityPlot, iNewOwner, iNumUnits):
	createRoleUnit(iNewOwner, tCityPlot, iDefend, iNumUnits)

# used: Rise, Stability
def clearPlague(iPlayer):
	for city in cities.owner(iPlayer).building(iPlague):
		city.setHasRealBuilding(iPlague, False)

# used: History
def removeReligionByArea(area, iReligion):
	for city in cities.of(area):
		removeReligion(city, iReligion)
			
# used: History, RFCUtils
def removeReligion(city, iReligion):
	if city.isHasReligion(iReligion) and not city.isHolyCity():
		city.setHasReligion(iReligion, False, False, False)
		
	if city.hasBuilding(temple(iReligion)):
		city.setHasRealBuilding(temple(iReligion), False)
		
	if city.hasBuilding(monastery(iReligion)):
		city.setHasRealBuilding(monastery(iReligion), False)
		
	if city.hasBuilding(cathedral(iReligion)):
		city.setHasRealBuilding(cathedral(iReligion), False)

# used: CvRandomEventInterface, History, Rules
# TODO: this shouldn't be here
def colonialConquest(iPlayer, tPlot):
	iCiv = civ(iPlayer)
	city = city_(tPlot)
	target = player(city.getOwner())
	plot = plot_(tPlot)

	message(active(), 'TXT_KEY_EVENT_COLONIAL_CONQUEST', adjective(iPlayer), plot.getX(), plot.getY(), name(target), color=iYellow, force=True)
	
	if player and not team(target).isAtWar(iPlayer):
		team(iPlayer).declareWar(target.getID(), True, WarPlanTypes.WARPLAN_TOTAL)
			
	targetPlot = plots.surrounding(tPlot).where(lambda p: not p.isCity() and not p.isPeak() and not p.isWater()).random()
	
	if iCiv in [iSpain, iPortugal, iNetherlands]:
		iNumUnits = 2
	elif iCiv in [iFrance, iEngland]:
		iNumUnits = 3
		
	iExp = 0
	if not player(iPlayer).isHuman(): iExp = 2
	
	# TODO: this lacks additional experience
	dConquerorUnits = {
		iAttack: 2*iNumUnits,
		iSiege: iNumUnits,
	}
	createRoleUnits(iPlayer, targetPlot, dConquerorUnits.items())

# used: CvRandomEventInterface, History
# this shouldn't be here
def colonialAcquisition(iPlayer, tPlot):
	iCiv = civ(iPlayer)
	plot = plot_(tPlot)

	message(active(), 'TXT_KEY_EVENT_COLONIAL_ACQUISITION', adjective(iPlayer), plot.getX(), plot.getY(), color=iYellow, force=True)

	if iCiv in [iSpain, iPortugal]:
		iNumUnits = 1
	elif iCiv in [iFrance, iEngland, iNetherlands]:
		iNumUnits = 2
		
	if plot.isCity():
		flipCity(plot, False, True, iPlayer)
	else:
		plot.setCulture(iPlayer, 10, True)
		plot.setOwner(iPlayer)
		
		for current in plots.surrounding(plot):
			if location(plot) == location(current):
				convertPlotCulture(current, iPlayer, 80, True)
			else:
				convertPlotCulture(current, iPlayer, 60, True)
				
		player(iPlayer).found(*location(plot))
	
	if plot.getOwner() >= 0 and not is_minor(plot.getOwner()) and team(player(iPlayer).getTeam()).canChangeWarPeace(plot.getTeam()):
		player(iPlayer).forcePeace(plot.getOwner())
		
	makeUnits(iPlayer, iWorker, tPlot, iNumUnits)
	createRoleUnit(iPlayer, plot, iAttack, iNumUnits)
		
	iMissionary = missionary(player(iPlayer).getStateReligion())
	if iMissionary:
		makeUnit(iPlayer, iMissionary, plot)

# used: CvRandomEventInterface, History
# this shouldn't be here
def getColonialTargets(iPlayer, bEmpty=False):
	iCiv = civ(iPlayer)
	
	# per "event"
	dNumCities = {
		iFrance: 2,
		iSpain: 2,
		iEngland: 2,
		iPortugal: 2,
		iNetherlands: 2,
	}
	
	iNumCities = dNumCities[iCiv]

	# human player only gets this event once as opposed to several times
	if player(iPlayer).isHuman():
		iNumCities = 3
		
	lColonialRegions = [iRegion for iRegion in lAsia if iRegion != rLevant]
	if iCiv == iFrance:
		lColonialRegions += [rMadagascar]
	elif iCiv == iSpain:
		lColonialRegions += lCentralAmerica
	else:
		lColonialRegions += lSubSaharanAfrica
		
	targetPlots = plots.all().coastal().regions(*lColonialRegions)
	
	cityPlots, emptyPlots = targetPlots.split(CyPlot.isCity)
	targetCities = cityPlots.notowners(players.group(iCivGroupEurope)).where(lambda p: p.getWarValue(iCiv) > 1).highest(iNumCities, metric=lambda p: p.getWarValue(iCiv))
	
	if bEmpty:
		nearbyCityPlots, settlePlots = emptyPlots.split(lambda p: plots.surrounding(p).any(CyPlot.isCity))
		
		targetPlots = settlePlots.where(lambda p: p.getSettlerValue(iCiv) > 0).sample_priority(iNumCities - len(targetCities), lambda p: p.getSettlerValue(iCiv))
		targetPlots += nearbyCityPlots.expand(1).where(lambda p: p.isCity() and p.getOwner() != iPlayer).sample_priority(iNumCities - len(targetCities) - len(targetPlots), lambda p: p.getSettlerValue(iCiv))
		
		return targetCities + targetPlots
	
	return targetCities
	
# used: History --> not used anymore
def getBorderPlots(iPlayer, tTL, tBR, iDirection = DirectionTypes.NO_DIRECTION, iNumPlots = 1):
	dMetrics = {
		DirectionTypes.NO_DIRECTION : lambda plot: 0,
		DirectionTypes.DIRECTION_EAST : lambda plot: plot.getX(),
		DirectionTypes.DIRECTION_WEST : lambda plot: -plot.getX(),
		DirectionTypes.DIRECTION_NORTH : lambda plot: plot.getY(),
		DirectionTypes.DIRECTION_SOUTH : lambda plot: -plot.getY()
	}
	
	metric = dMetrics[iDirection]
	lTargetCities = cities.start(tTL).end(tBR).owner(iPlayer).highest(iNumPlots, metric)
	
	return filter(None, [getPlotNearCityInDirection(city, iDirection) for city in lTargetCities])
	
# used: RFCUtils
def getPlotNearCityInDirection(city, iDirection):
	secondRing = plots.ring(city, radius=2).where(lambda p: not p.isCity() and not p.isWater() and not p.isUnit() and not p.isPeak())
	return secondRing.where(lambda p: estimate_direction(city, p) == iDirection).random()
	
# used: RFCUtils
def hasEnemyUnit(iPlayer, tPlot):
	return units.at(tPlot).notowner(iPlayer).atwar(iPlayer).any()
	
# used: Barbs, History, RFCUtils
def isFree(iPlayer, tPlot, bNoCity=False, bNoEnemyUnit=False, bCanEnter=False, bNoCulture=False, iCityDistance=1):
	plot = plot_(tPlot)
	
	if bNoCity:
		if cities.surrounding(plot, radius=iCityDistance):
			return False
			
	if bNoEnemyUnit:
		if plots.surrounding(plot).any(lambda p: hasEnemyUnit(iPlayer, p)):
			return False
		
	if bCanEnter:
		if plot.isPeak(): return False
		if plot.isWater(): return False
		if plot.getFeatureType() in [iMud, iJungle, iRainforest]: return False
	
	if bNoCulture:
		if plot.isOwned() and plot.getOwner() != iPlayer and plot.getOwner() in players.major():
			return False
		
	return True
			
# used: Scenarios
def foundCapital(iPlayer, tPlot, sName, iSize, iCulture, lBuildings=[], lReligions=[], iScenario=None):
	if iScenario is not None:
		if scenario() != iScenario: return
		
	x, y = tPlot
	player(iPlayer).found(x, y)
	
	city = city_(tPlot)
	if city:
		city.setCulture(iPlayer, iCulture, True)
		city.setName(sName, False)
		
		if city.getPopulation() < iSize:
			city.setPopulation(iSize)
			
		for iReligion in lReligions:
			city.setHasReligion(iReligion, True, False, False)
			
		for iBuilding in lBuildings:
			city.setHasRealBuilding(iBuilding, True)
			
	return city

# used: Rules
def freeSlaves(city, iPlayer):
	iNumSlaves = city.getFreeSpecialistCount(iSpecialistSlave)
	if iNumSlaves:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		makeUnits(iPlayer, base_unit(iSlave), city, iNumSlaves)
	
# used: GreatPeople
def replace(unit, iUnitType):
	replaced = makeUnit(unit.getOwner(), iUnitType, unit)
	replaced.convert(unit)
	return replaced

# used: RFCUtils
def getRoleDomain(iRole):
	if iRole in [iWorkerSea, iSettleSea, iAttackSea, iAssaultSea, iFerry, iEscort, iExploreSea, iLightEscort]:
		return DomainTypes.DOMAIN_SEA
	return DomainTypes.DOMAIN_LAND

# used: RFCUtils
def getRoleLocation(iRole, location):
	if getRoleDomain(iRole) == DomainTypes.DOMAIN_SEA:
		seaPlots = plots.surrounding(location, radius=3).sea().closest_within(location, radius=3)
		if seaPlots:
			return seaPlots[data.iSeed % seaPlots.count()]
	
	return location

# used: RFCUtils
def getRoleAI(iRole, iPlayer):
	if iRole == iDefend:
		return UnitAITypes.UNITAI_CITY_DEFENSE
	elif iRole in [iAttack, iShock]:
		return UnitAITypes.UNITAI_ATTACK
	elif iRole in [iCityAttack, iShockCity, iCitySiege]:
		return UnitAITypes.UNITAI_ATTACK_CITY
	elif iRole == iCounter:
		iCiv = civ(iPlayer)
		# specific civs are offensive with their spear units
		if iCiv in [iAssyria, iGreece, iMacedon, iPersia, iPhoenicia, iGhorids]:
			return UnitAITypes.UNITAI_ATTACK_CITY
		else:
			return UnitAITypes.UNITAI_COUNTER
	elif iRole == iWorkerSea:
		return UnitAITypes.UNITAI_WORKER_SEA
	elif iRole == iSettle:
		return UnitAITypes.UNITAI_SETTLE
	elif iRole == iSettleSea:
		return UnitAITypes.UNITAI_SETTLER_SEA
	elif iRole == iAttackSea:
		return UnitAITypes.UNITAI_ATTACK_SEA
	elif iRole in [iAssaultSea, iFerry]:
		return UnitAITypes.UNITAI_ASSAULT_SEA
	elif iRole == iEscort:
		return UnitAITypes.UNITAI_ESCORT_SEA
	elif iRole == iExploreSea:
		return UnitAITypes.UNITAI_EXPLORE_SEA
	elif iRole == iExplore:
		return UnitAITypes.UNITAI_EXPLORE
	elif iRole == iSkirmish:
		return UnitAITypes.UNITAI_COLLATERAL
	elif iRole == iWork:
		return UnitAITypes.UNITAI_WORKER

	return UnitAITypes.NO_UNITAI

# used: RFCUtils
def isUnitOfRole(iUnit, iRole):
	unit = infos.unit(iUnit)
	iCombatType = unit.getUnitCombatType()
	iDomainType = unit.getDomainType()

	if iRole == iBase:
		return base_unit(iUnit) == iMilitia
	elif iRole == iDefend:
		return (iCombatType == UnitCombatTypes.UNITCOMBAT_ARCHER and unit.getCityDefenseModifier() > 0) or iCombatType == UnitCombatTypes.UNITCOMBAT_GUN or base_unit(iUnit) == iMilitia
	elif iRole in [iAttack, iCityAttack]:
		return iCombatType in [UnitCombatTypes.UNITCOMBAT_MELEE, UnitCombatTypes.UNITCOMBAT_GUN]
	elif iRole == iCounter:
		return iCombatType == UnitCombatTypes.UNITCOMBAT_MELEE and unit.getUnitCombatModifier(UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY) > 0
	elif iRole in [iShock, iShockCity]:
		return iCombatType == UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY and iUnit != iWarElephant or iUnit == iKeshik
	elif iRole == iHarass:
		return iCombatType == UnitCombatTypes.UNITCOMBAT_LIGHT_CAVALRY and not iUnit == iKeshik
	elif iRole == iWorkerSea:
		return iDomainType == DomainTypes.DOMAIN_SEA and unit.getCombat() == 0
	elif iRole == iSettle:
		return unit.isFound()
	elif iRole in [iSettleSea, iAssaultSea, iFerry]:
		return unit.getCargoSpace() > 0
	elif iRole in [iAttackSea, iEscort, iExploreSea]:
		return iDomainType == DomainTypes.DOMAIN_SEA
	elif iRole == iExplore:
		return unit.isNoBadGoodies()
	elif iRole in [iSiege, iCitySiege]:
		return iCombatType == UnitCombatTypes.UNITCOMBAT_SIEGE
	elif iRole == iSkirmish:
		return iCombatType in [UnitCombatTypes.UNITCOMBAT_ARCHER, UnitCombatTypes.UNITCOMBAT_GUN] and unit.getCollateralDamage() > 0
	elif iRole == iLightEscort:
		return iDomainType == DomainTypes.DOMAIN_SEA and unit.getWithdrawalProbability() > 0
	elif iRole == iWork:
		return unit.getWorkRate() > 0 and unit.getCombat() == 0 and not unit.isSlave()
	
	raise Exception("Unexpected unit role: %d" % iRole)
	
def canCreateUnit(iPlayer, iUnit):
	if iUnit in dNeverTrain[iPlayer]:
		return False
	
	if iUnit in dAlwaysTrain[iPlayer]:
		return True
	
	if not player(iPlayer).isHuman() and iUnit in dAIAlwaysTrain[iPlayer]:
		return True
	
	return player(iPlayer).canTrain(iUnit, False, False)

# used: RFCUtils, Rise
def getUnitForRole(iPlayer, iRole, bUnique=True):
	roleMetric = lambda unit: (infos.unit(unit).getCombat(), infos.unit(unit).getCityAttackModifier(), bUnique == (base_unit(unit) != unit))
	possibleUnits = infos.units().where(lambda unit: canCreateUnit(iPlayer, unit)).where(lambda unit: isUnitOfRole(unit, iRole))
	
	if not bUnique:
		possibleUnits = possibleUnits.map(base_unit)
	
	iBestUnit = possibleUnits.maximum(roleMetric)
	return (iBestUnit, getRoleAI(iRole, iPlayer))

# used: RFCUtils, Rise
def getUnitsForRole(iPlayer, iRole, bUnique=True):
	iUnit, iUnitAI = getUnitForRole(iPlayer, iRole, bUnique=bUnique)
	units = [(iUnit, iUnitAI)]
	
	if iRole == iSettleSea:
		units.append(getUnitForRole(iPlayer, iSettle, bUnique=bUnique))
		
		for _ in range(infos.unit(iUnit).getCargoSpace()-1):
			units.append(getUnitForRole(iPlayer, iDefend, bUnique=bUnique))
	
	elif iRole == iAssaultSea:
		for _ in range(infos.unit(iUnit).getCargoSpace()):
			units.append(getUnitForRole(iPlayer, iAttack, bUnique=bUnique))
	
	return units

# used: AIWars, History, RFCUtils, Rise, Stability
def createRoleUnits(iPlayer, location, units, iExperience=0, bCreateSettlers=True):
	created = CreatedUnits.none()
	for iRole, iAmount in units:
		if bCreateSettlers or iRole != iSettle:
			created += createRoleUnit(iPlayer, location, iRole, iAmount, iExperience)
	return created

# used: AIWars, Congresses, History, RFCUtils
def createRoleUnit(iPlayer, location, iRole, iAmount=1, iExperience=0):
	created = CreatedUnits.none()
	location = getRoleLocation(iRole, location)
	if iRole == iSettle:
		created += createSettlers(iPlayer, iAmount)
	elif iRole == iMissionary:
		created += createMissionaries(iPlayer, iAmount)
	else:
		for _ in range(iAmount):
			for iUnit, iUnitAI in getUnitsForRole(iPlayer, iRole):
				if iUnit is not None and location is not None:
					iRoleExperience = iExperience + dStartingExperience[iPlayer].get(iRole, 0)
					created += makeUnits(iPlayer, iUnit, location, 1, iUnitAI).experience(iRoleExperience)
	return created
	
# used: Congresses, History, RFCUtils, Rise, Stability
def completeCityFlip(tPlot, iPlayer, iOwner, iCultureChange, bBarbarianDecay = True, bBarbarianConversion = False, bAlwaysOwnPlots = False, bFlipUnits = False, bPermanentCultureChange = True, bCreateGarrisons = True):
	plot = plot_(tPlot)
	
	if bPermanentCultureChange:
		cultureManager(plot, iCultureChange, iPlayer, iOwner, bBarbarianDecay, bBarbarianConversion, bAlwaysOwnPlots)
	
	if bFlipUnits: 
		plotUnits = units.at(plot).owner(iOwner)
		flippingUnits = plotUnits.where(lambda unit: not is_minor(unit) or (not unit.isAnimal() and not unit.isFound())).grouped(CyUnit.getUnitType)
		removedUnits = plotUnits.where(lambda unit: not unit.isCargo())
		
		for unit in removedUnits:
			unit.kill(False, -1)
	else:
		pushOutGarrisons(plot, iOwner)
		relocateSeaGarrisons(plot, iOwner)
	
	flippedCity = flipCity(plot, False, False, iPlayer, [iOwner])
	
	if flippedCity:
		flippedCity.setOccupationTimer(0)
	
	if bFlipUnits:
		for iUnit, typeUnits in flippingUnits:
			makeUnits(iPlayer, iUnit, plot, len(typeUnits))
	elif bCreateGarrisons:
		createGarrisons(plot, iPlayer, 2)
	
	plot.setRevealed(team(iPlayer).getID(), True, False, -1)
	
	return flippedCity


def updateStartingCulture():
	capital_city = capital(active())
	if not capital_city:
		return
	
	for plot in plots.surrounding(capital_city, radius=capital_city.getCultureLevel()):
		plot.updateCulture()
		
# used: Stability
def isGreatBuilding(iBuilding):
	if isWorldWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True

	if isTeamWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True

	if isNationalWonderClass(infos.building(iBuilding).getBuildingClassType()):
		return True

	# Regular building
	return True
	
# used: History, RFCUtils, Rules, Stability
def relocateCapital(iPlayer, tile):
	if not tile:
		return

	newCapital = city(tile)
	if not newCapital or newCapital.getOwner() != player(iPlayer).getID():
		return
		
	oldCapital = player(iPlayer).getCapitalCity()
	if location(oldCapital) == location(newCapital):
		return
	
	oldCapital.setHasRealBuilding(iPalace, False)
	newCapital.setHasRealBuilding(iPalace, True)
	
	events.fireEvent("capitalMoved", newCapital)
	
# used: Rise
def createSettlers(iPlayer, iTargetCities, bGrantCapital=True):
	capital = plots.capital(iPlayer)

	iNumCities = cities.birth(iPlayer).count()
	iNumSettlers = iTargetCities - iNumCities
	
	if bGrantCapital and not city(capital):
		iNumSettlers = max(iNumSettlers, 1)
	
	return makeUnits(iPlayer, unique_unit(iPlayer, iSettler), capital, iNumSettlers)
		
# used: Rise
def createMissionaries(iPlayer, iNumUnits, iReligion=None):
	if not iReligion:
		iReligion = player(iPlayer).getStateReligion()
		
	if iReligion < 0:
		iNumUnits = 0
		
	if not game.isReligionFounded(iReligion):
		iNumUnits = 0
	
	return makeUnits(iPlayer, missionary(iReligion), plots.capital(iPlayer), iNumUnits)
	
def exclusive(iCiv, *civs):
	return iCiv in civs and any(player(iOtherCiv).isExisting() for iOtherCiv in civs if iCiv != iOtherCiv)
	
# used: CvScreensInterface, Stability
# TODO: should move to stability
def canRespawn(iCiv):
	# only dead civ needs to check for resurrection
	if player(iCiv).isAlive():
		return False
	
	# cannot respawn if it has not spawned yet
	if until(year(dBirth[iCiv])) > 0:
		return False
		
	if data.civs[iCiv].iLastTurnAlive > turn() - turns(20):
		return False
	
	# check if the civ can be reborn at this date
	if none(year().between(iStart, iEnd) for iStart, iEnd in dResurrections[iCiv]):
		return False
				
	# Thailand cannot respawn when Khmer is alive and vice versa
	if exclusive(iCiv, iKhmer, iThailand):
		return False
	
	# Rome cannot respawn when Italy is alive and vice versa
	if exclusive(iCiv, iRome, iItaly):
		return False
	
	# Greece cannot respawn when Byzantium is alive and vice versa
	if exclusive(iCiv, iGreece, iByzantium):
		return False

	if exclusive(iCiv, iMacedon, iByzantium):
		return False
	
	# Iran cannot respawn if Persia is alive and vice versa
	if exclusive(iCiv, iPersia, iIran):
		return False
	
	if exclusive(iCiv, iParthia, iIran):
		return False
	
	# Mexico cannot respawn if Aztecs are alive and vice versa
	if exclusive(iCiv, iAztecs, iMexico):
		return False
	
	# India cannot respawn when Mughals are alive (not vice versa -> Pakistan)
	if iCiv == iIndia and player(iTimurids).isAlive():
		return False
	
	# Exception during Japanese UHV
	if player(iJapan).isHuman() and year().between(1920, 1945):
		if iCiv in [iChina, iChinaS, iKorea, iMalays, iJava, iThailand]:
			return False
		
	# Ottoman respawn if
	# 1) they have been alive before
	# 2A) they didn't have the conditions to spawn initially, but now one of their "parent civs" has or had conquered the area
	if iCiv == iOttomans:
		if data.civs[iOttomans].iLastTurnAlive > 0:
			return True
		if cities.regions(rAnatolia, rCaucasus).none(lambda city: 
			iTurks in [city.getCivilizationType(), city.getPreviousCiv()] or 
			iMongols in [city.getCivilizationType(), city.getPreviousCiv()] or
			iTimurids in [city.getCivilizationType(), city.getPreviousCiv()]):
			return False
		
	# Qin (China) cannot respawn if Xia (Zhou) is alive and vice-versa
	if exclusive(iCiv, iChina, iXia):
		return False
			
	return True
	
# used: CvScreensInterface, MapDrawer, RFCUtils
def canEverRespawn(iCiv, iGameTurn = None):
	if iGameTurn is None:
		iGameTurn = turn()
		
	return any(turn(iEnd) > iGameTurn for _, iEnd in dResurrections[iCiv])
	
# used: Barbs
def evacuate(iPlayer, tPlot):
	for plot in plots.surrounding(tPlot):
		for unit in units.at(plot).notowner(iPlayer):
			target = plots.surrounding(plot, radius=2).without(tPlot).where(lambda p: isFree(unit.getOwner(), p, bNoEnemyUnit=True, bCanEnter=True)).random()
			move(unit, target)

# used: Rise
def expelUnits(iPlayer, area, excluded_area = None):
	if excluded_area is None:
		excluded_area = area

	for plot in area:
		for iOwner, ownerUnits in units.at(plot).notowner(iPlayer).grouped(lambda unit: unit.getOwner()):
			ownerUnits = ownerUnits.where(lambda unit: not unit.isNone() and not unit.isCargo())
			landUnits, seaUnits = ownerUnits.split(lambda unit: unit.getDomainType() != DomainTypes.DOMAIN_SEA)
		
			possibleDestinations = cities.owner(iOwner).without(excluded_area.cities())
			
			if landUnits:
				moveDomainUnits(iPlayer, iOwner, landUnits, possibleDestinations.closest(plot))
			
			if seaUnits:
				moveDomainUnits(iPlayer, iOwner, seaUnits, possibleDestinations.coastal().closest(plot))
				
# used: RFCUtils
def moveDomainUnits(iPlayer, iOwner, units, destination):
	if not is_minor(iOwner) and destination:
		for unit in units:
			move(unit, destination)
		
		message(iOwner, "TXT_KEY_MESSAGE_ATTACKERS_EXPELLED", len(units), adjective(iPlayer), destination.getName())
	
	else:
		for unit in units:
			unit.kill(False, -1)

# used: CvScreensInterface, CvPlatyBuilderScreen
# TODO: should be civ based not player based
def toggleStabilityOverlay(iPlayer = -1):
	global bStabilityOverlay
	bReturn = bStabilityOverlay
	removeStabilityOverlay()

	if bReturn:
		return

	if iPlayer == -1:
		iPlayer = active()

	bStabilityOverlay = True
	CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", True)

	iTeam = player(iPlayer).getTeam()

	engine = CyEngine()

	bDebug = game.isDebugMode()

	# othercivs = civs.major().without(iPlayer).where(lambda iCiv: player(iCiv).isAlive() or canEverRespawn(iCiv))

	# apply the highlight
	for plot in plots.all().land():
		if bDebug or plot.isRevealed(iTeam, False):
			if not plot.isPeak() and not plot.isWater():
				if plot.isPlayerCore(iPlayer):
					iPlotType = iCoreArea
				elif plot.getPlayerSettlerValue(iPlayer) > 0:
					iPlotType = iHistoricalArea
				elif plot.getPlayerWarValue(iPlayer) > 1:
					iPlotType = iConquestArea
				else:
					iPlotType = iForeignArea
			
				szColor = lStabilityColors[iPlotType]
				engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000 + iPlotType, szColor, 0.7)

				
# used: CvScreensInterface, RFCUtils, CvPlatyBuilderScreen
def removeStabilityOverlay():
	global bStabilityOverlay
	engine = CyEngine()
	# clear the highlight
	for i in range(50):
		engine.clearAreaBorderPlots(1000+i)
	bStabilityOverlay = False
	CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).setState("StabilityOverlay", False)
	
# used: CvPediaBuilding
def getAdvisorString(iBuilding):
	iAdvisor = infos.building(iBuilding).getAdvisorType()
	
	dAdvisors = defaultdict({
		0 : 'Military',
		1 : 'Religious',
		2 : 'Economy',
		3 : 'Science',
		4 : 'Culture',
		5 : 'Growth',
	}, default='')
	
	return dAdvisors[iAdvisor]
	
# used: RFCUtils
def isGreatPeopleBuilding(iBuilding):
	return any(infos.unit(iUnit).getBuildings(iBuilding) for iUnit in lGreatPeopleUnits)
	
# used: CvPediaMain
def getBuildingCategory(iBuilding):
	'0 = Building'
	'1 = Religious Building'
	'2 = Unique Building'
	'3 = Great People Building'
	'4 = National Wonder'
	'5 = World Wonder'

	BuildingInfo = infos.building(iBuilding)
	if BuildingInfo.getReligionType() > -1:
		return 1
	elif isWorldWonderClass(BuildingInfo.getBuildingClassType()):
		return 5
	else:
		iBuildingClass = BuildingInfo.getBuildingClassType()
		iDefaultBuilding = infos.buildingClass(iBuildingClass).getDefaultBuildingIndex()
		if isNationalWonderClass(iBuildingClass):
			return 4
		elif isGreatPeopleBuilding(iBuilding):
			return 3
		else:
			if iDefaultBuilding > -1 and iDefaultBuilding != iBuilding:
				if infos.building(iBuilding).isGraphicalOnly():
					return 0
				return 2
			else:
				if infos.building(iBuilding).isGraphicalOnly():
					return -1
				return 0
				
# used: CvPediaLeader, CvPediaMain
def getLeaderCiv(iLeader):
	return next(iCiv for iCiv in range(iNumCivs) if infos.civ(iCiv).isLeaders(iLeader))
	
# used: Rules
def freeCargo(identifier, tile):
	transportUnits, cargoUnits = units.at(tile).owner(identifier).split(lambda unit: unit.cargoSpace() > 0 and unit.specialCargo() == -1)
	
	iTotalSpace = transportUnits.sum(CyUnit.cargoSpace)
	iTotalCargo = cargoUnits.land().count()
	
	return iTotalSpace - iTotalCargo
	
# used: Rules
def captureUnit(pLosingUnit, pWinningUnit, iUnit, iChance):
	if pLosingUnit.isAnimal(): 
		return
	
	if pLosingUnit.getDomainType() != DomainTypes.DOMAIN_LAND: 
		return
	
	if infos.unit(pLosingUnit).getCombat() == 0: 
		return
	
	iPlayer = pWinningUnit.getOwner()
	
	if rand(100) < iChance:
		unitAI = UnitAITypes.UNITAI_WORKER
		if iUnit not in [iSlave, iWorker, iAztecSlave]:
			unitAI = UnitAITypes.UNITAI_ATTACK

		makeUnit(iPlayer, iUnit, pWinningUnit, unitAI)
		message(pWinningUnit.getOwner(), 'TXT_KEY_UP_ENSLAVE_WIN', sound='SND_REVOLTEND', event=1, button=infos.unit(iUnit).getButton(), color=8, location=pWinningUnit)
		message(pLosingUnit.getOwner(), 'TXT_KEY_UP_ENSLAVE_LOSE', sound='SND_REVOLTEND', event=1, button=infos.unit(iUnit).getButton(), color=7, location=pWinningUnit)
		
		events.fireEvent("enslave", iPlayer, pLosingUnit)

# used: Stability
def flipOrRelocateGarrison(city, iNumDefenders):
	lRelocatedUnits = []
	lFlippedUnits = []
	
	for plot in plots.surrounding(city, radius=2).where(lambda p: not p.isCity() or location(p) == location(city)):
		for unit in units.at(plot).owner(city.getOwner()).domain(DomainTypes.DOMAIN_LAND):
			if unit.canFight() and len(lFlippedUnits) < iNumDefenders:
				lFlippedUnits.append(unit)
			else:
				lRelocatedUnits.append(unit)
					
	return lFlippedUnits, lRelocatedUnits
		
# used: Stability
def relocateGarrisonToCore(city):
	relocateUnitsToCore(city.getOwner(), plots.surrounding(city, radius=2).where(lambda p: not p.isCity() or at(p, city)).units().owner(city.getOwner()))
	
# used: RFCUtils, Stability
def getLocalGarrison(city):
	return plots.surrounding(city, radius=2).where(lambda p: not p.isCity() or at(p, city)).units().owner(city.getOwner()).domain(DomainTypes.DOMAIN_LAND)
	
# used: RFCUtils
def flipUnit(unit, iNewOwner, plot):
	if location(unit) >= (0, 0):
		iUnitType = unit.getUnitType()
		unit.kill(False, -1)
		makeUnit(iNewOwner, iUnitType, plot)
	
# used: Congresses, Stability
def relocateUnitsToCore(iPlayer, lUnits, iArmyPercent = 100, exceptions = []):
	coreCities = cities.core(iPlayer).without(exceptions).owner(iPlayer)
	coastalCities = coreCities.coastal() or cities.owner(iPlayer).without(exceptions).coastal()
	if not coreCities:
		killUnits(lUnits)
		return
	
	for iType, typeUnits in units.of(lUnits).where(lambda unit: unit.plot() and unit.plot().isOwned()).by_type().items():
		movedUnits, removedUnits = typeUnits.percentage_split(iArmyPercent)
		destinations = infos.unit(iType).getDomainType() == DomainTypes.DOMAIN_SEA and coastalCities or coreCities
		
		for city, movedUnits in movedUnits.divide(destinations):
			for unit in movedUnits:
				move(unit, city)
			
		for unit in removedUnits:
			unit.kill(-1, False)
				
# used: Stability
def flipOrCreateDefenders(iNewOwner, units, tPlot, iNumDefenders):
	for unit in units:
		flipUnit(unit, iNewOwner, tPlot)

	if len(units) < iNumDefenders and active() != iNewOwner:
		createRoleUnit(iNewOwner, tPlot, iDefend, iNumDefenders - len(units))
		
# used: Congresses, Stability
def killUnits(lUnits):
	for unit in units.of(lUnits).where(lambda unit: not unit.isCargo()):
		if location(unit) >= (0, 0):
			unit.kill(False, barbarian())
			
# used: RFCUtils, Rise
def ensureDefenders(iPlayer, tPlot, iNumDefenders):
	defenders = units.at(tPlot).owner(iPlayer).where(lambda unit: isUnitOfRole(unit, iDefend))
	iNumRequired = max(0, iNumDefenders - defenders.count())
	return createRoleUnit(iPlayer, tPlot, iDefend, iNumRequired)
	
# used: CvDawnOfMan
def getDawnOfManText(iPlayer):
	iScenario = scenario()
	baseKey = 'TXT_KEY_DOM_%s' % str(name(iPlayer).replace(' ', '_').upper())
	
	fullKey = baseKey
	if iScenario == i600AD: fullKey += "_600AD"
	elif iScenario == i1700AD: fullKey += "_1700AD"
	
	return text_if_exists(fullKey, otherwise=baseKey)
	
# used: History, Periods, DynamicCivs, Victory
def isControlled(iPlayer, area, iMinCities=1):
	iTotalCities = area.cities().count()
	iPlayerCities = area.cities().owner(iPlayer).count()
	
	if iPlayerCities < iTotalCities: return False
	if iPlayerCities < iMinCities: return False
	
	return True
		
# used: Scenarios, VictoryGoals, Wonders
def getBuildingCity(iBuilding, bEffect = True):
	if game.getBuildingClassCreatedCount(infos.building(iBuilding).getBuildingClassType()) == 0:
		return None
		
	if bEffect:
		return cities.all().building_effect(iBuilding).first()
		
	return cities.all().building(iBuilding).first()
	
# used: BUG/UnitGrouper.py, CvRFCEventHandler
def getDefaultGreatPerson(iGreatPersonType):
	if iGreatPersonType in dFemaleGreatPeople.values():
		return dict((v, k) for k, v in dFemaleGreatPeople.items())[iGreatPersonType]
	return iGreatPersonType

# used: History, Scenarios
def findSeaPlots(tile, iRange, iCiv):
	"""Searches a sea plot that isn't occupied by a unit and isn't a civ's territory surrounding the starting coordinates"""
	return plots.surrounding(tile, radius=iRange).sea().where(lambda p: not p.isUnit()).where(lambda p: p.getOwner() in [-1, slot(iCiv)]).random()

# used: Rise, Stability
def getPrevalentReligion(area, iStateReligionPlayer=None):
	religions = infos.religions().where(lambda iReligion: not infos.religion(iReligion).isLocal())
	
	religionCount = lambda iReligion: area.cities().religion(iReligion).count()
	stateReligionCount = lambda iReligion: area.cities().notowner(iStateReligionPlayer).where(lambda city: player(city).getStateReligion() == iReligion).count()
	previousStateReligionCount = lambda iReligion: area.cities().owner(iStateReligionPlayer).where(lambda city: slot(Civ(city.getPreviousCiv())) >= 0 and player(Civ(city.getPreviousCiv())).getStateReligion() == iReligion).count()
	
	found = find_max(religions, lambda iReligion: religionCount(iReligion) + stateReligionCount(iReligion) + previousStateReligionCount(iReligion))
	
	if found.value > 0:
		return found.result
	
	return -1

# used: DynamicCivs, Periods
# simplified: this is a simple string check
# just make sure the names correspond to the names given by the civ...
def isCurrentCapital(iPlayer, *names):
	capital = player(iPlayer).getCapitalCity()
	if not capital: return False
	return any(capital.getName() == name for name in names)

# used: Rise, Scenarios
def convertSurroundingPlotCulture(iPlayer, plots):
	for plot in plots:
		if plot.isOwned() and plot.isPlayerCore(plot.getOwner()) and not plot.isPlayerCore(iPlayer): continue
		if not plot.isCity():
			convertPlotCulture(plot, iPlayer, 100, False)

# used: CvPlatyBuilderScreen
def paintPlots(plots, index=1000, color="COLOR_CYAN"):
	engine.clearAreaBorderPlots(1000)
	for plot in plots:
		engine.fillAreaBorderPlotAlt(plot.getX(), plot.getY(), 1000, "COLOR_CYAN", 0.7)

# used: Shortcuts
def startObserverMode(iTurns):
	data.iBeforeObserverSlot = active()
	iObserverSlot = player(iHarappa).isAlive() and slot(iPolynesia) or slot(iHarappa)
	
	makeUnit(iObserverSlot, iCatapult, (0, 0))
	
	game.setActivePlayer(iObserverSlot, False)
	game.setAIAutoPlay(iTurns)
	
# used: Shortcuts
def endObserverMode():
	if data.iBeforeObserverSlot != -1:
		if player(data.iBeforeObserverSlot).isAlive():
			game.setActivePlayer(data.iBeforeObserverSlot, False)
			data.iBeforeObserverSlot = -1
		else:
			makeUnit(active(), iCatapult, (0, 0))

def breakObserverMode(message = None):
	if data.iBeforeObserverSlot == -1:
		return
	
	game.setAIAutoPlay(0)
	events.fireEvent("autoplayEnded")
	
	if message:
		show(message)

# used: Congresses
def isIsland(tile):
	return plot(tile).area().getNumTiles() == 1


def getImprovementBuild(iImprovement):
	if iImprovement < 0:
		return None
		
	iPredecessor = next(i for i in infos.improvements() if infos.improvement(i).getImprovementUpgrade() == iImprovement)
	if iPredecessor is not None:
		return getImprovementBuild(iPredecessor)
	
	return next(iBuild for iBuild in infos.builds() if infos.build(iBuild).getImprovement() == iImprovement)


# used: Rise
def possibleSpawnsBetween(origin, target, iDistance):
	return (
		plots.rectangle(origin, target)
			.expand(1)
			.land()
			.passable()
			.where(lambda p: p.getOwner() in [plot(origin).getOwner(), plot(target).getOwner(), -1])
			.where(lambda p: map.getArea(p.getArea()).getNumCities() > 0)
			.where(lambda p: distance(p, target) >= iDistance)
			.where(lambda p: not units.at(p).atwar(origin.getOwner()))
			.where(lambda p: not cities.surrounding(p).notowner(origin.getOwner()))
	)


# used: Slots, Collapse
def resetRevealedOwner(iPlayer):
	for plot in plots.all():
		if not plot.isRevealed(game.getActiveTeam(), False) and plot.getRevealedOwner(game.getActiveTeam(), False) == iPlayer:
			plot.setRevealedOwner(game.getActiveTeam(), slot(iIndependent))


# used: Minors
def isDefensiveBuilding(iBuilding):
	if isWonder(iBuilding):
		return False

	building = infos.building(iBuilding)
	return building.getDefenseModifier() > 0 or building.getBombardDefenseModifier() > 0 or building.getUnignorableBombardDefenseModifier() > 0


# used: Collapse
def removeBuildings(city):
	for iBuilding in infos.buildings():
		if city.isHasRealBuilding(iBuilding):
			if not isWonder(iBuilding):
				if infos.building(iBuilding).getFreeStartEra() < 0 or infos.building(iBuilding).getFreeStartEra() > player(city).getCurrentEra():
					city.setHasRealBuilding(iBuilding, False)


# used: Birth
def downgradeAreaCottages(iPlayer, area):
	for plot in area.owner(iPlayer):
		iImprovement = plot.getImprovementType()
		
		if iImprovement == iTown:
			plot.setImprovementType(iVillage)
		elif iImprovement == iVillage:
			plot.setImprovementType(iHamlet)
		elif iImprovement == iHamlet:
			plot.setImprovementType(iCottage)
		elif iImprovement == iCottage:
			plot.setImprovementType(-1)
		
		plot.setUpgradeProgress(0)


# used: Rules
def downgradeCityCottages(city):
	for plot in plots.city_radius(city):
		if plot.getOwner() == city.getOwner():
			if plot.getWorkingCity() == city or plot.getWorkingCity() is None:
				iImprovement = plot.getImprovementType()
				
				if iImprovement == iTown:
					plot.setImprovementType(iVillage)
				elif iImprovement == iVillage:
					plot.setImprovementType(iHamlet)
				elif iImprovement == iHamlet:
					plot.setImprovementType(iCottage)
				elif iImprovement == iCottage:
					plot.setImprovementType(-1)
				
				plot.setUpgradeProgress(0)