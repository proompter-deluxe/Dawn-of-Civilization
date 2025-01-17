from Core import *
from Locations import *
from RFCUtils import *
from Events import handler


### CONSTANTS ###

dRelocatedCapitals = {
	(iHolyRome, iRenaissance): tVienna,
	(iJapan, iIndustrial): tTokyo,
	(iItaly, iIndustrial): tRome,
}


### CITY ACQUIRED ###

@handler("cityAcquired")
def resetSlaves(iOwner, iPlayer, city):
	if player(iPlayer).canUseSlaves():
		freeSlaves(city, iPlayer)
	else:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		

@handler("cityAcquired")
def resetAdminCenter(iOwner, iPlayer, city):
	if city.isCapital() and city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)


@handler("cityAcquired")
def restoreCapital(iOwner, iPlayer, city):
	if player(iPlayer).isHuman() or is_minor(iPlayer):
		return
	
	capital = plots.capital(iPlayer)
	
	if data.civs[civ(iPlayer)].iResurrections > 0 or player(iPlayer).getPeriod() != -1:
		capital = plots.respawnCapital(iPlayer)
		
	if at(city, capital):
		relocateCapital(iPlayer, city)


@handler("cityAcquired")
def resetNationalWonders(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade:
		for iNationalWonder in range(iNumBuildings):
			if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
				city.setHasRealBuilding(iNationalWonder, False)


@handler("cityAcquired")
def spreadTradingCompanyCulture(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade and civ(iPlayer) in lTradingCompanyCivs and city.getRegionID() in lAsia + lSubSaharanAfrica:
		for plot in plots.surrounding(city):
			if location(plot) == location(city):
				convertPlotCulture(plot, iPlayer, 51, False)
			elif plot.isCity():
				pass
			elif distance(plot, city) == 1:
				convertPlotCulture(plot, iPlayer, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(plot, iPlayer, 15, False)


@handler("cityAcquired")
def downgradeCottages(iOwner, iPlayer, city, bConquest, bTrade):
	if bConquest and player(iPlayer).getCurrentEra() <= iRenaissance:
		downgradeCityCottages(city)

# purge Great People when a city falls to independents, barbarians or natives, prior to Renaissance era
@handler("cityAcquired")
def purgeGreatPeople(iOwner, iPlayer, city, bConquest, bTrade):
	if bConquest and civ(iPlayer) in [iBarbarian, iIndependent, iIndependent2, iNative] and player(iOwner).getCurrentEra() >= iRenaissance:
		for iGreatPerson in lGreatSpecialists:
			city.setFreeSpecialistCount(iGreatPerson, 0)


### CITY ACQUIRED AND KEPT ###
	
@handler("cityAcquiredAndKept")
def spreadCultureOnConquest(iPlayer, city):
	for plot in plots.surrounding(city):
		if at(plot, city):
			convertTemporaryCulture(plot, iPlayer, 25, False)
		elif civ(plot) == city.getPreviousCiv():
			convertTemporaryCulture(plot, iPlayer, 50, True)
		else:
			convertTemporaryCulture(plot, iPlayer, 25, True)


### CITY BUILT ###

@handler("cityBuilt")
def clearMinorCulture(city):
	for iMinor in players.minor():
		plot(city).setCulture(iMinor, 0, True)


@handler("cityBuilt")
def spreadCulture(city):
	if not is_minor(city):
		spreadMajorCulture(city.getOwner(), location(city))


@handler("cityBuilt")
def updateFoundValues(city):
	if not is_minor(city):
		player(city).AI_updateFoundValues(False)


@handler("cityBuilt")
def createColonialDefenders(city):
	iPlayer = city.getOwner()
	# only grant extras in the colonial era
	if not player(iPlayer).isHuman() and player(iPlayer).getCurrentEra() >= iRenaissance:
		if civ(iPlayer) in dCivGroups[iCivGroupEurope] and city.getRegionID() not in lEurope:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


@handler("cityBuilt")
def americanPioneerAbility(city):
	iPlayer = city.getOwner()
	if civ(iPlayer) == iAmerica:
		if city.getRegionID() in lNorthAmerica:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return

	if civ(winningUnit) == iAztecs:
		captureUnit(losingUnit, winningUnit, iAztecSlave, 50)
		return
	
	if civ(losingUnit) == iNative and winningUnit.getUnitType() == iBandeirante and player(winningUnit).canUseSlaves():
		captureUnit(losingUnit, winningUnit, iSlave, 100)
		return
	
	# enslave natives if your civic is slavery or colonialism regardless of era
	if civ(losingUnit) == iNative:
		if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
			captureUnit(losingUnit, winningUnit, iSlave, 50)
		return
	
	# Nigeria UP: can always capture slaves from any civ at 25% rate (natives still at 50%)
	if civ(winningUnit) == iNigeria:
		if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
			captureUnit(losingUnit, winningUnit, iSlave, 25)
		return

	# also enslave barbarians but at a lesser rate
	if civ(losingUnit) == iBarbarian:
		if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
			captureUnit(losingUnit, winningUnit, iSlave, 15)
		return

@handler("combatResult")
def zuluUniquePower(winningUnit, losingUnit):
	# Zulu UP: 25% chance to create a friendly copy of a defeated unit
	if civ(winningUnit) == iZulu:
		captureUnit(losingUnit, winningUnit, losingUnit.getUnitType(), 25)

@handler("combatResult")
def mayanHolkanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iHolkan:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city and distance(winningUnit, city) <= 10:
				iFood = scale(5)
				city.changeFood(iFood)
				
				message(iWinner, 'TXT_KEY_MAYA_HOLKAN_EFFECT', adjective(losingUnit), losingUnit.getName(), iFood, city.getName())
				
				events.fireEvent("combatFood", iWinner, winningUnit, iFood)


### REVOLUTION ###

@handler("revolution")
def validateSlaves(iPlayer):
	if not player(iPlayer).canUseSlaves():
		if player(iPlayer).getImprovementCount(iSlavePlantation) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlavePlantation):
				plot.setImprovementType(iPlantation)
		
		if player(iPlayer).getImprovementCount(iSlaveMine) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlaveMine):
				plot.setImprovementType(iMine)
		
		for city in cities.owner(iPlayer):
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) == iSlave):
			slave.kill(False, iPlayer)


### UNIT BUILT ###

@handler("unitBuilt")
def moveSlavesToNewWorld(city, unit):
	if base_unit(unit) == iSlave and city.getRegionID() in lEurope + [rMaghreb, rAnatolia] and not city.isHuman():	
		colony = cities.owner(iPlayer).regions(*(lAmerica + lSubSaharanAfrica)).random()
		if colony:
			move(unit, colony)


### CAPITAL MOVED ###

@handler("capitalMoved")
def resetAdminCenterOnPalaceBuilt(city):
	if city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)



### PLOT FEATURE REMOVED ###


@handler("plotFeatureRemoved")
def brazilianMadeireiroAbility(plot, city, iFeature):
	dFeatureGold = defaultdict({
		iForest : 15,
		iSavanna : 15,
		iJungle : 20,
		iRainforest : 20,
	}, 0)
	
	if civ(plot) == iBrazil:
		iGold = dFeatureGold[iFeature]
		
		if iGold > 0:
			player(plot).changeGold(iGold)
			message(plot.getOwner(), 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def checkImmigration(iGameTurn):
	if iGameTurn < year(dBirth[iAmerica]) + turns(5):
		return

	data.iImmigrationTimer -= 1
	
	if data.iImmigrationTimer == 0:
		immigration()
		data.iImmigrationTimer = turns(3 + rand(5))


### TECH ACQUIRED ###

@handler("techAcquired")
def relocateCapitals(iTech, iTeam, iPlayer):
	if not player(iPlayer).isHuman():
		iCiv = civ(iPlayer)
		iEra = infos.tech(iTech).getEra()
		if (iCiv, iEra) in dRelocatedCapitals:
			relocateCapital(iPlayer, dRelocatedCapitals[iCiv, iEra])


### END GAME TURN ###

@handler("EndGameTurn")
def startTimedConquests():
	for iConqueror, tPlot in data.lTimedConquests:
		colonialConquest(iConqueror, tPlot)
	
	data.lTimedConquests = []


### BEGIN PLAYER TURN ###

@handler("setPlayerAlive")
def updateLastTurnAlive(iPlayer, bAlive):
	if turn() == scenarioStartTurn():
		return

	if not bAlive and not (player(iPlayer).isHuman() and autoplay()):
		data.civs[civ(iPlayer)].iLastTurnAlive = game.getGameTurn()


### IMPLEMENTATIONS ###

def isBribableUnit(iPlayer, unit):
	if not unit.canFight():
		return False
	
	if unit.isInvisible(player(iPlayer).getTeam(), False):
		return False
	
	if unit.getDomainType() != DomainTypes.DOMAIN_LAND:
		return False
	
	return True


def getPossibleBribes(iPlayer, location):
	iTreasury = player(iPlayer).getGold()
	targets = [(unit, infos.unit(unit).getProductionCost() * 3 / 2) for unit in units.at(location).owner(iBarbarian)]
	return [(unit, iCost) for unit, iCost in targets if isBribableUnit(iPlayer, unit) and iCost <= iTreasury]


def canBribeUnits(spy):
	if not player(spy).canHurry(1):
		return False
	
	if plot(spy).isOwned() and plot(spy).getOwner() != spy.getOwner():
		return False

	if spy.getMoves() >= spy.maxMoves(): 
		return False
		
	if not getPossibleBribes(spy.getOwner(), location(spy)):
		return False
	
	return True


def applyUnitBribes(iChoice, iPlayer, x, y):
	targets = getPossibleBribes(iPlayer, (x, y))
	unit, iCost = targets[iChoice]
	
	newUnit = makeUnit(iPlayer, unit.getUnitType(), closestCity(unit, owner=iPlayer))
	player(iPlayer).changeGold(-iCost)

	unit.kill(False, -1)
	
	if newUnit:
		interface.selectUnit(newUnit, True, True, False)


def doUnitBribes(spy):
	# only once per turn
	spy.finishMoves()
			
	# launch popup
	bribePopup = unit_bribe_popup.launcher()
	
	for unit, iCost in getPossibleBribes(spy.getOwner(), location(spy)):
		bribePopup.text().applyUnitBribes(unit.getName(), unit.currHitPoints(), unit.maxHitPoints(), iCost, button=unit.getButton())
	
	x, y = location(spy)
	bribePopup.cancel().launch(spy.getOwner(), x, y)


def getImmigrationValue(city):
	iFoodDifference = city.foodDifference(False)
	iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
	
	iValue = 0
	
	iValue += max(0, iHappinessDifference)
	iValue += max(0, iFoodDifference / 2)
	iValue += city.getPopulation() / 2
	
	if city.getRegionID() in lNorthAmerica:
		iValue += 5
	
	if iValue > 0:
		iValue += rand(0, 2)
	
	return iValue
	
	
def getEmigrationValue(city):
	iFoodDifference = city.foodDifference(False)
	iHappinessDifference = city.happyLevel() - city.unhappyLevel(0)
	
	iValue = 0
	
	iValue -= min(0, iHappinessDifference)
	iValue -= min(0, iFoodDifference / 2)
	
	if iValue > 0:
		iValue += city.getPopulation() / 5
		iValue += rand(0, 2)
	
	return iValue


def immigration():
	sourcePlayers = players.major().existing().where(lambda p: player(p).getCapitalCity().getRegionID() not in lNewWorld).where(lambda p: cities.owner(p).any(lambda city: getEmigrationValue(city) > 0))
	targetPlayers = players.major().existing().where(lambda p: player(p).getCapitalCity().getRegionID() in lNewWorld).where(lambda p: cities.owner(p).any(lambda city: getImmigrationValue(city) > 0))
	
	iNumMigrations = min(sourcePlayers.count(), targetPlayers.count())
	
	sourceCities = sourcePlayers.cities().where(lambda city: city.getRegionID() not in lNewWorld).where(lambda city: city.getPopulation() > 1).highest(iNumMigrations, getEmigrationValue)
	targetCities = targetPlayers.cities().regions(*lNewWorld).highest(iNumMigrations, getImmigrationValue)
	
	for sourceCity, targetCity in zip(sourceCities, targetCities):
		iPopulation = 1
		if sourceCity.getPopulation() >= 9:
			iPopulation += 1
	
		sourceCity.changePopulation(-iPopulation)
		targetCity.changePopulation(iPopulation)
			
		# extra cottage growth for target city's vicinity
		for pCurrent in plots.surrounding(targetCity, radius=2):
			if pCurrent.getWorkingCity() == targetCity:
				pCurrent.changeUpgradeProgress(turns(10))
					
		# migration brings culture
		targetPlot = plot(targetCity)
		iTargetPlayer = targetCity.getOwner()
		iSourcePlayer = sourceCity.getOwner()
		
		iCultureChange = targetPlot.getCulture(iTargetPlayer) / targetCity.getPopulation()
		targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)
		
		iCultureChange = targetCity.getCulture(iTargetPlayer) / targetCity.getPopulation()
		targetCity.changeCulture(iSourcePlayer, iCultureChange, False)
		
		# chance to spread religions in source city
		lReligions = [iReligion for iReligion in range(iNumReligions) if sourceCity.isHasReligion(iReligion) and not targetCity.isHasReligion(iReligion)]
		if player(iSourcePlayer).getStateReligion() in lReligions:
			lReligions.append(player(iSourcePlayer).getStateReligion())
		
		if rand(1, 4) <= len(lReligions):
			targetCity.setHasReligion(random_entry(lReligions), True, True, True)
					
		# notify affected players
		message(iSourcePlayer, 'TXT_KEY_UP_EMIGRATION', sourceCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=sourceCity)
		message(iTargetPlayer, 'TXT_KEY_UP_IMMIGRATION', targetCity.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=targetCity)

		events.fireEvent("immigration", sourceCity, targetCity, iPopulation, iCultureChange)


### POPUPS ###

unit_bribe_popup = popup.text("TXT_KEY_BRIBE_UNITS_POPUP") \
						.selection(applyUnitBribes, "TXT_KEY_BRIBE_UNITS_BUTTON") \
						.cancel("TXT_KEY_BRIBE_UNITS_BUTTON_NONE") \
						.build()