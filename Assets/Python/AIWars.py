from Core import *
from RFCUtils import *

from Events import handler
from Resurrection import getResurrectionTechs


### Constants ###

iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iRomeCarthageYear = -220
tRomeCarthageTL = (60, 44)
tRomeCarthageBR = (70, 49)

tRomeSpainTL = (56, 48)
tRomeSpainBR = (61, 53)

iRomeGreeceYear = -150
tRomeGreeceTL = (74, 49)
tRomeGreeceBR = (78, 55)

iRomeMesopotamiaYear = -75
tRomeMesopotamiaTL = (82, 44)
tRomeMesopotamiaBR = (90, 50)

iRomeAnatoliaYear = -100
tRomeAnatoliaTL = (79, 51)
tRomeAnatoliaBR = (88, 55)

iRomeCeltiaYear = -60
tRomeCeltiaTL = (56, 55)
tRomeCeltiaBR = (67, 62)

iRomeEgyptYear = -10
tRomeEgyptTL = (76, 40)
tRomeEgyptBR = (82, 45)

iRomeBritainYear = 50
tRomeBritainTL = (55, 62)
tRomeBritainBR = (59, 67)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestRomeCarthageInSpain = (22, iRome, iCarthage, tRomeSpainTL, tRomeSpainBR, 3, iRomeCarthageYear, 10)
tConquestRomeCarthage = (0, iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 4, iRomeCarthageYear + 10, 30)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 3, iRomeAnatoliaYear, 20)
tConquestRomeCelts = (3, iRome, iCelts, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
tConquestRomeEgypt = (4, iRome, iEgypt, tRomeEgyptTL, tRomeEgyptBR, 3, iRomeEgyptYear, 10)
tConquestRomeBritain = (21, iRome, iCelts, tRomeBritainTL, tRomeBritainBR, 2, iRomeBritainYear, 20)

iAlexanderYear = -330
tGreeceAnatoliaTL = (79, 51) 
tGreeceAnatoliaBR = (86, 53) # ignore the top 2 rows of Anatolia
tGreeceLevantTL = (83, 44)
tGreeceLevantBR = (86, 51)
tGreeceMesopotamiaTL = (86, 44)
tGreeceMesopotamiaBR = (90, 50)
tGreeceEgyptTL = (76, 40)
tGreeceEgyptBR = (82, 45)
tGreecePersiaTL = (91, 43)
tGreecePersiaBR = (97, 52)

tConquestGreeceAnatolia = (19, iGreece, iPersia, tGreeceAnatoliaTL, tGreeceAnatoliaBR, 10, iAlexanderYear, 10)
tConquestGreeceLevant = (20, iGreece, iPersia, tGreeceLevantTL, tGreeceLevantBR, 10, iAlexanderYear + 1, 20)
tConquestGreeceEgypt = (6, iGreece, iEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 10, iAlexanderYear + 2, 20)
tConquestGreeceMesopotamia = (5, iGreece, iPersia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 10, iAlexanderYear + 3, 20)
tConquestGreecePersia = (7, iGreece, iPersia, tGreecePersiaTL, tGreecePersiaBR, 10, iAlexanderYear + 4, 30)

iCholaSumatraYear = 1030
tCholaSumatraTL = (115, 26)
tCholaSumatraBR = (121, 31)

# currently inactive
tConquestCholaSumatra = (8, iDravidia, iMalays, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1200
tSpainMoorsTL = (55, 48)
tSpainMoorsBR = (60, 51)

tConquestSpainMoors = (9, iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 1, iSpainMoorsYear, 10)

iTurksPersiaYear = 1000
tTurksPersiaTL = (91, 43)
tTurksPersiaBR = (98, 52)

iTurksAnatoliaYear = 1100
tTurksAnatoliaTL = (80, 51)
tTurksAnatoliaBR = (87, 55)

tConquestTurksPersia = (10, iTurks, iArabia, tTurksPersiaTL, tTurksPersiaBR, 4, iTurksPersiaYear, 20)
tConquestTurksAnatolia = (11, iTurks, iByzantium, tTurksAnatoliaTL, tTurksAnatoliaBR, 5, iTurksAnatoliaYear, 20)

iEnglandIrelandYear = 1200
tEnglandIrelandTL = (52, 64)
tEnglandIrelandBR = (54, 67)

tConquestEnglandIreland = (12, iEngland, iCelts, tEnglandIrelandTL, tEnglandIrelandBR, 2, iEnglandIrelandYear, 10)

iMongolsPersiaYear = 1220
tMongolsPersiaTL = (91, 43)
tMongolsPersiaBR = (98, 52)

tConquestMongolsPersia = (13, iMongols, iTurks, tMongolsPersiaTL, tMongolsPersiaBR, 7, iMongolsPersiaYear, 10)

iChinaIndiesYear = -240
tChinaIndiesTL = (118, 49)
tChinaIndiesBR = (128, 56)

tConquestChinaIndependents = (14, iChina, iIndependent, tChinaIndiesTL, tChinaIndiesBR, 3, iChinaIndiesYear, 20)

iFranceCrusadesYear = 1090
iHolyRomeCrusadesYear = 1190
iEnglandCrusadesYear = 1190

tHolyLandTL = (84, 44)
tHolyLandBR = (85, 51)

tConquestFranceCrusades = (15, iFrance, iArabia, tHolyLandTL, tHolyLandBR, 2, iFranceCrusadesYear, 10)
tConquestHolyRomeCrusades = (16, iHolyRome, iMamluks, tHolyLandTL, tHolyLandBR, 1, iHolyRomeCrusadesYear, 5)
tConquestEnglandCrusades = (17, iEngland, iMamluks, tHolyLandTL, tHolyLandBR, 1, iEnglandCrusadesYear, 5)

iSuiUnificationYear = 588
tSouthChinaTL = (124, 43)
tSouthChinaBR = (131, 50)

tConquestSuiUnification = (18, iChina, iChinaS, tSouthChinaTL, tSouthChinaBR, 3, iSuiUnificationYear, 10)

iArabCarthageConquestYear = 690
tTunisiaTL = (66, 44)
tTunisiaBR = (69, 48)

tConquestArabiaCarthage = (23, iArabia, iPhoenicia, tTunisiaTL, tTunisiaBR, 3, iArabCarthageConquestYear, 10)

iArabPersiaConquestYear = 650
tArabsPersiaTL = (92, 43)
tArabsPersiaBR = (95, 50)

tConquestArabiaPersia = (24, iArabia, iPersia, tArabsPersiaTL, tArabsPersiaBR, 3, iArabPersiaConquestYear, 10)

iArabSindConquestYear = 710
tArabsSindTL = (98, 42)
tArabsSindBR = (102, 47)

tConquestArabiaSind = (25, iArabia, iKushans, tArabsSindTL, tArabsSindBR, 2, iArabSindConquestYear, 15)

lConquests = [
	tConquestRomeCarthageInSpain,
	tConquestRomeCarthage, 
	tConquestRomeGreece, 
	tConquestRomeAnatolia, 
	tConquestRomeCelts, 
	tConquestRomeEgypt,
	tConquestRomeBritain,
	tConquestGreeceAnatolia,
	tConquestGreeceLevant,
	tConquestGreeceMesopotamia, 
	tConquestGreeceEgypt, 
	tConquestGreecePersia, 
	#tConquestSpainMoors, # --> now that Moors have Almoravid barbarians to contend with, we don't need this
	tConquestTurksPersia, 
	tConquestTurksAnatolia, 
	tConquestEnglandIreland,
	tConquestMongolsPersia,
	tConquestChinaIndependents,
	tConquestFranceCrusades,
	tConquestHolyRomeCrusades,
	tConquestEnglandCrusades,
	tConquestSuiUnification,
	tConquestArabiaCarthage,
	tConquestArabiaPersia,
	tConquestArabiaSind
]


@handler("GameStart")
def setup():
	iTurn = year(-600)
	if scenario() == i600AD:  #late start condition
		iTurn = year(900)
	elif scenario() == i1700AD:
		iTurn = year(1720)
	data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly-iMinIntervalEarly)


@handler("BeginGameTurn")
def restorePeaceMinors(iGameTurn):
	if iGameTurn > turns(50):
		iMinor = players.independent().periodic(20)
		if iMinor:
			restorePeaceHuman(iMinor, False)
			
		iMinor = players.independent().periodic(60)
		if iMinor:
			restorePeaceAI(iMinor, False)


@handler("BeginGameTurn")
def startMinorWars(iGameTurn):
	if iGameTurn > turns(50):	
		iMinor = players.independent().periodic(13)
		if iMinor:
			minorWars(iMinor)


@handler("BeginGameTurn")
def checkConquests():
	# if this gets much bigger, convert to dict
	for tConquest in lConquests:
		if tConquest[0] == tConquestGreeceLevant[0]:
			# before "Alexander" can conquer the Levant, he has to conquer Anatolia
			checkConquest(tConquest, tConquestGreeceAnatolia)
		elif tConquest[0] == tConquestGreeceEgypt[0] or tConquest[0] == tConquestGreeceMesopotamia[0] :
			# before "Alexander" can conquer Egypt or Mesopotamia, he has to conquer the Levant
			checkConquest(tConquest, tConquestGreeceLevant)
		elif tConquest[0] == tConquestGreecePersia[0]:
			# before "Alexander" can conquer Persia, he has to conquer Mesopotamia
			checkConquest(tConquest, tConquestGreeceMesopotamia)
		elif tConquest[0] == tConquestHolyRomeCrusades[0] or tConquest[0] == tConquestEnglandCrusades[0]:
			# Don't launch "Third Crusade" if Holy Land still firmly under French control
			checkConquest(tConquest, tConquestFranceCrusades, True)
		elif tConquest[0] == tConquestRomeAnatolia[0]:
			# Rome needs Greece before Anatolia
			checkConquest(tConquest, tConquestRomeGreece)
		elif tConquest[0] == tConquestRomeCarthage[0]:
			# Rome needs Spain before attacking North Africa
			checkConquest(tConquest, tConquestRomeCarthageInSpain)
		elif tConquest[0] == tConquestArabiaSind[0]:
			checkConquest(tConquest, tConquestArabiaPersia)
		else:
			checkConquest(tConquest)
		
		
@handler("BeginGameTurn")
def checkWarPlans(iGameTurn):		
	if iGameTurn == data.iNextTurnAIWar:
		planWars(iGameTurn)


@handler("BeginGameTurn")
def checkTargetMinors():
	targetMinors()


@handler("BeginGameTurn")
def increaseAggressionLevels():
	for iLoopPlayer in players.major():
		data.players[iLoopPlayer].iAggressionLevel = dAggressionLevel[iLoopPlayer] + rand(2)


@handler("techAcquired")	
def forgetMemory(iTech, iTeam, iPlayer):
	if year() <= year(1700):
		return

	if iTech in [iPsychology, iTelevision]:
		pPlayer = player(iPlayer)
		for iLoopPlayer in players.major().without(iPlayer):
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR, -1)
			
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)


@handler("changeWar")
def resetAggressionLevel(bWar, iTeam, iOtherTeam):
	if bWar and not is_minor(iTeam) and not is_minor(iOtherTeam):
		data.players[iTeam].iAggressionLevel = 0
		data.players[iOtherTeam].iAggressionLevel = 0

		
def checkConquest(tConquest, tPrereqConquest = (), bInvertPrereqConquestCondition = False, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return
		
	if player(iPlayer).isHuman():
		return
		
	if not player(iPlayer).isExisting() and iCiv != iTurks: 
		return
	
	if team(iPlayer).isAVassal():
		return
	
	if not iID in data.lConquest:
		data.lConquest[iID] = False

	if data.lConquest[iID]:
		return

	iStartTurn = year(iYear) + turns(data.iSeed % 10 - 5)
	
	if turn() == iStartTurn - turns(5):
		warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR)
	
	if turn() < player(iCiv).getLastBirthTurn() + turns(3): 
		return
	
	if not (iStartTurn <= turn() <= iStartTurn + turns(iIntervalTurns)):
		return
		
	iPreferredTarget = slot(iPreferredTargetCiv)

	if iPreferredTarget >= 0 and player(iPreferredTarget).isExisting() and team(iPreferredTarget).isVassal(iPlayer):
		return
	
	if tPrereqConquest and not bInvertPrereqConquestCondition and not isConquered(tPrereqConquest):
		#message(active(), 'Failing to start conquest from %s1 because prereq conquest not met.', name(iPlayer))
		return

	if tPrereqConquest and bInvertPrereqConquestCondition and isConquered(tPrereqConquest):
		#message(active(), 'INVERTED CONQUEST CONDITION: Failing to start conquest from %s1 because prereq conquest is met.', name(iPlayer))
		return
	
	#if iCiv == iSpain and (iPreferredTarget < 0 or player(iPreferredTarget).isHuman()):
	#	return
	
	spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iWarPlan)
	data.lConquest[iID] = True


def warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR):
	text = text_if_exists("TXT_KEY_MESSAGE_CONQUERORS_%s_%s" % (infos.civ(iCiv).getIdentifier(), infos.civ(iPreferredTargetCiv).getIdentifier()), adjective(iPlayer), otherwise="TXT_KEY_MESSAGE_CONQUERORS_GENERIC")
	conquerorCities = cities.owner(iPlayer)
	
	for iTarget, targetCities in cities.rectangle(tTL, tBR).notowner(iPlayer).grouped(CyCity.getOwner):
		message(iTarget, str(text), color=iRed, location=targetCities.closest_all(conquerorCities), button=infos.civ(iCiv).getButton())


def isConquered(tConquest):
	iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest
	
	iPlayer = slot(iCiv)
	iNumMinorCities = 0
	lAreaCities = cities.rectangle(tTL, tBR)

	# if empty, assume conquered
	if len(lAreaCities) == 0: return True

	for city in lAreaCities:
		if city.getOwner() in players.minor(): iNumMinorCities += 1
		elif city.getOwner() != iPlayer: return False
		
	if 2 * iNumMinorCities > len(lAreaCities): return False
	
	return True


def conquerorWar(iPlayer, iTarget, iWarPlan):
	# reset at war counters because this is essentially a renewed war, will avoid cheap peace out of the conquerors
	if team(iPlayer).isAtWar(team(iTarget).getID()):
		team(iPlayer).AI_setAtWarCounter(team(iTarget).getID(), 0)
		team(iTarget).AI_setAtWarCounter(team(iPlayer).getID(), 0)
		
		team(iPlayer).AI_setWarPlan(team(iTarget).getID(), iWarPlan)
		
	# otherwise declare war
	else:
		declareWar(iPlayer, iTarget, iWarPlan)

	
def spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	
	if not player(iPlayer).isExisting():
		for iTech in getResurrectionTechs(iPlayer):
			team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
			
	targetPlots = plots.rectangle(tTL, tBR)
			
	targetCities = cities.rectangle(tTL, tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iPlayer))))
	owners = set(city.getOwner() for city in targetCities)
	
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isExisting():
		conquerorWar(iPlayer, iPreferredTarget, iWarPlan)
			
	for iOwner in owners:
		conquerorWar(iPlayer, iOwner, iWarPlan)
		message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iPlayer))
		message(active(), 'TXT_KEY_UP_CONQUESTS_TARGET_ALL', name(iPlayer), name(iOwner))
	
	iExtra = 0
	if iEra >= iMedieval:
		iExtra += 1

	for city in targetCities:	
		if not player(iPlayer).isHuman():
			# we want to be sure that the AI can fund these conquerors for at least a few turns
			player(iPlayer).changeGold(20)
		
		tPlot = findNearestLandPlot(city, iPlayer)
		
		if iCiv == iGreece:
			makeUnits(iPlayer, iCatapult, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iHoplite, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCompanion, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iArcher, tPlot, 1)
		else:
			dConquestUnits = {
				iCityAttack: 2 + iExtra,
				iCitySiege: 2 + iExtra,
				iDefend: 1,
			}
			createRoleUnits(iPlayer, tPlot, dConquestUnits.items())

		if iCiv in [iSpain, iEngland, iHolyRome, iFrance, iPoland, iPortugal, iItaly, iNorse, iRus, iRussia, iSweden]:
			createRoleUnit(iPlayer, tPlot, iShockCity, 2)
			createRoleUnit(iPlayer, tPlot, iCounter, 2)
			
		if iCiv in [iTurks, iMongols]:
			createRoleUnit(iPlayer, tPlot, iShockCity, 2)


def declareWar(iPlayer, iTarget, iWarPlan):
	if team(iPlayer).isVassal(iTarget):
		team(iPlayer).setVassal(iTarget, False, False)
		
	team(iPlayer).declareWar(iTarget, True, iWarPlan)


def planWars(iGameTurn):
	# skip if there is a world war
	if iGameTurn > year(1500):
		iCivsAtWar = 0
		for iLoopPlayer in players.major():
			if team(iLoopPlayer).getAtWarCount(True) > 0:
				iCivsAtWar += 1
		if 100 * iCivsAtWar / game.countCivPlayersAlive() > 50:
			data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)
			return

	iAttackingPlayer = determineAttackingPlayer()
	iTargetPlayer = determineTargetPlayer(iAttackingPlayer)
	
	if iAttackingPlayer is None:
		return

	data.players[iAttackingPlayer].iAggressionLevel = 0
	
	if iTargetPlayer == -1:
		return
		
	if team(iAttackingPlayer).canDeclareWar(iTargetPlayer):
		team(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
	
	data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)


def targetMinors():
	for iPlayer in players.major().ai().existing().periodic_iter(10):
		if players.major().existing().any(lambda p: team(iPlayer).isAtWar(player(p).getTeam())):
			continue
	
		if players.major().existing().any(lambda p: team(iPlayer).AI_getWarPlan(player(p).getTeam()) != WarPlanTypes.NO_WARPLAN):
			continue
		
		for city in cities.all().where(is_minor).revealed(iPlayer):
			if team(iPlayer).isAtWar(city.getTeam()):
				continue
		
			if plot(city).getPlayerSettlerValue(iPlayer) >= 10 or plot(city).getPlayerWarValue(iPlayer) >= 6:
				declareWar(iPlayer, city.getOwner(), WarPlanTypes.WARPLAN_LIMITED)
				break


def determineAttackingPlayer():
	return players.major().existing().where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


def possibleTargets(iPlayer):
	return players.major().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))


def determineTargetPlayer(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	lPotentialTargets = []
	dTargetValues = defaultdict({}, 0)

	# determine potential targets
	for iLoopPlayer in possibleTargets(iPlayer):
		pLoopPlayer = player(iLoopPlayer)
		tLoopPlayer = team(iLoopPlayer)
		
		if iLoopPlayer == iPlayer: continue
		
		# requires live civ and past contact
		if not pLoopPlayer.isExisting(): continue
		if not tPlayer.isHasMet(iLoopPlayer): continue
		
		# no masters or vassals
		if tPlayer.isVassal(iLoopPlayer): continue
		if tLoopPlayer.isVassal(iPlayer): continue
		
		# not already at war
		if tPlayer.isAtWar(iLoopPlayer): continue
		
		# birth protected
		if pLoopPlayer.isBirthProtected(): continue
		
		lPotentialTargets.append(iLoopPlayer)
		
	if not lPotentialTargets: 
		return -1
		
	# iterate the map for all potential targets
	for plot in plots.all():
		iOwner = plot.getOwner()
		if iOwner in lPotentialTargets:
			dTargetValues[iOwner] += plot.getPlayerWarValue(iPlayer)
				
	# hard to attack with lost contact
	for iLoopPlayer in lPotentialTargets:
		if not pPlayer.canContact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 8
		
	# normalization
	iMaxValue = max(dTargetValues.values())
	if iMaxValue == 0: 
		return -1
	
	for iLoopPlayer in lPotentialTargets:
		dTargetValues[iLoopPlayer] *= 500
		dTargetValues[iLoopPlayer] /= iMaxValue
		
	for iLoopPlayer in lPotentialTargets:
		iLoopCiv = civ(iLoopPlayer)
	
		# randomization
		if dTargetValues[iLoopPlayer] <= iThreshold:
			dTargetValues[iLoopPlayer] += rand(100)
		else:
			dTargetValues[iLoopPlayer] += rand(300)
		
		# balanced by attitude
		iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
		if iAttitude > 0:
			dTargetValues[iLoopPlayer] /= 2 * iAttitude
			
		# exploit plague
		if data.players[iLoopPlayer].iPlagueCountdown > 0 or data.players[iLoopPlayer].iPlagueCountdown < -10:
			if turn() > player(iLoopPlayer).getLastBirthTurn() + turns(20):
				dTargetValues[iLoopPlayer] *= 3
				dTargetValues[iLoopPlayer] /= 2
	
		# determine master
		iMaster = master(iLoopPlayer)
				
		# master attitudes
		if iMaster >= 0:
			iAttitude = player(iMaster).AI_getAttitude(iLoopPlayer)
			if iAttitude > 0:
				dTargetValues[iLoopPlayer] /= 2 * iAttitude
		
		# peace counter
		if not tPlayer.isAtWar(iLoopPlayer):
			iCounter = min(7, max(1, tPlayer.AI_getAtPeaceCounter(iLoopPlayer)))
			if iCounter <= 7:
				dTargetValues[iLoopPlayer] *= 20 + 10 * iCounter
				dTargetValues[iLoopPlayer] /= 100
				
		# defensive pact
		if tPlayer.isDefensivePact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 4
			
		# consider power
		iOurPower = tPlayer.getPower(True)
		iTheirPower = team(iLoopPlayer).getPower(True)
		if iOurPower > 2 * iTheirPower:
			dTargetValues[iLoopPlayer] *= 2
		elif 2 * iOurPower < iTheirPower:
			dTargetValues[iLoopPlayer] /= 2
			
		# spare smallish civs
		if iLoopCiv in [iNetherlands, iPortugal, iItaly]:
			dTargetValues[iLoopPlayer] *= 4
			dTargetValues[iLoopPlayer] /= 5
			
		# no suicide
		if iCiv == iNetherlands:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				dTargetValues[iLoopPlayer] /= 2
		elif iCiv == iPortugal:
			if iLoopCiv == iSpain:
				dTargetValues[iLoopPlayer] /= 2
		elif iCiv == iItaly:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				dTargetValues[iLoopPlayer] /= 2
				
	return dict_max(dTargetValues)
				

def getNextInterval(iGameTurn):
	if iGameTurn > year(1600):
		iMinInterval = iMinIntervalLate
		iMaxInterval = iMaxIntervalLate
	else:
		iMinInterval = iMinIntervalEarly
		iMaxInterval = iMaxIntervalEarly
		
	iMinInterval = turns(iMinInterval)
	iMaxInterval = turns(iMaxInterval)
	
	return rand(iMinInterval, iMaxInterval)