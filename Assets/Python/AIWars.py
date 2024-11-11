from Core import *
from RFCUtils import *
from Locations import *

from Events import handler
from Resurrection import getResurrectionTechs

### Constants ###

iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iRomeCarthageYear = -200
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
tRomeAnatoliaBR = (84, 55)

iRomeCeltiaYear = -60
tRomeCeltiaTL = (56, 55)
tRomeCeltiaBR = (67, 62)

iRomeLevantYear = -75
iRomeEgyptYear = -10

iRomeBritainYear = 50
tRomeBritainTL = (55, 62)
tRomeBritainBR = (59, 67)

iAlexanderYear = -335
tGreeceAnatoliaTL = (79, 51) 
tGreeceAnatoliaBR = (86, 53) # ignore the top 2 rows of Anatolia
tLevantTL = (83, 44)
tLevantBR = (86, 51)
tGreeceMesopotamiaTL = (86, 44)
tGreeceMesopotamiaBR = (90, 50)
tEgyptTL = (76, 40)
tEgyptBR = (82, 45)
tGreecePersiaTL = (91, 43)
tGreecePersiaBR = (97, 52)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestMacedonAnatolia = (19, iMacedon, iPersia, tGreeceAnatoliaTL, tGreeceAnatoliaBR, 2, iAlexanderYear, 10)
tConquestMacedonLevant = (20, iMacedon, iPhoenicia, tLevantTL, tLevantBR, 3, iAlexanderYear, 20)
tConquestMacedonEgypt = (6, iMacedon, iEgypt, tEgyptTL, tEgyptBR, 2, iAlexanderYear, 20)
tConquestMacedonMesopotamia = (5, iMacedon, iPersia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 3, iAlexanderYear, 20)
tConquestMacedonPersia = (7, iMacedon, iPersia, tGreecePersiaTL, tGreecePersiaBR, 4, iAlexanderYear, 20)

tConquestRomeCarthageInSpain = (22, iRome, iPhoenicia, tRomeSpainTL, tRomeSpainBR, 3, iRomeCarthageYear, 10)
tConquestRomeCarthage = (0, iRome, iPhoenicia, tRomeCarthageTL, tRomeCarthageBR, 4, iRomeCarthageYear + 20, 30)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iMacedon, tRomeAnatoliaTL, tRomeAnatoliaBR, 2, iRomeAnatoliaYear, 15)
tConquestRomeLevant = (28, iRome, iMacedon, tLevantTL, tLevantBR, 2, iRomeLevantYear, 10)
tConquestRomeCelts = (3, iRome, iCelts, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
tConquestRomeEgypt = (4, iRome, iEgypt, tEgyptTL, tEgyptBR, 3, iRomeEgyptYear, 10)
tConquestRomeBritain = (21, iRome, iCelts, tRomeBritainTL, tRomeBritainBR, 2, iRomeBritainYear, 20)

iCholaSumatraYear = 1030
tCholaSumatraTL = (115, 26)
tCholaSumatraBR = (121, 31)

# currently inactive
tConquestCholaSumatra = (8, iDravidia, iMalays, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1200
tSpainMoorsTL = (55, 48)
tSpainMoorsBR = (60, 51)

tConquestSpainMoors = (9, iSpain, iMoors, tSpainMoorsTL, tSpainMoorsBR, 1, iSpainMoorsYear, 10)

iTurksPersiaYear = 1040
tTurksPersiaTL = (91, 43)
tTurksPersiaBR = (98, 52)

iTurksAnatoliaYear = 1100
tTurksAnatoliaTL = (81, 51)
tTurksAnatoliaBR = (92, 55)

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

iMongolsBaghdadYear = 1260
tMongolsBaghdadTL = (88, 43)
tMongolsBaghdadBR = (90, 49)

tConquestMongolsBaghdad = (38, iMongols, iArabia, tMongolsBaghdadTL, tMongolsBaghdadBR, 2, iMongolsBaghdadYear, 5)

iChinaIndiesYear = -240
tChinaIndiesTL = (118, 49)
tChinaIndiesBR = (128, 56)

tConquestChinaIndependents = (14, iChina, iIndependent, tChinaIndiesTL, tChinaIndiesBR, 3, iChinaIndiesYear, 20)

iFranceCrusadesYear = 1090
iHolyRomeCrusadesYear = 1190
iEnglandCrusadesYear = 1190

tConquestFranceCrusades = (15, iFrance, iArabia, tLevantTL, tLevantBR, 2, iFranceCrusadesYear, 10)
tConquestHolyRomeCrusades = (16, iHolyRome, iMamluks, tLevantTL, tLevantBR, 1, iHolyRomeCrusadesYear, 5)
tConquestEnglandCrusades = (17, iEngland, iMamluks, tLevantTL, tLevantBR, 1, iEnglandCrusadesYear, 5)

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

iAssyriaLevantConquestYear = -800

tConquestAssyriaLevant = (26, iAssyria, iPhoenicia, tLevantTL, tLevantBR, 2, iAssyriaLevantConquestYear, 5)

iPersiaLydiaConquestYear = -550
tPersiaLydiaTL = (80, 51)
tPersiaLydiaBR = (84, 55)

tConquestPersiaLydia = (27, iPersia, iHittites, tPersiaLydiaTL, tPersiaLydiaBR, 2, iPersiaLydiaConquestYear, 5)

tCarthageTL = (66, 47)
tCarthageBR = (67, 48)
iByzantiumCarthageConquestYear = 530
tConquestByzantiumCarthage = (29, iByzantium, iBarbarian, tCarthageTL, tCarthageBR, 1, iByzantiumCarthageConquestYear, 5)

tSicilyTL = (69, 48)
tSicilyBR = (71, 52)
tConquestByzantiumSicily = (30, iByzantium, iBarbarian, tSicilyTL, tSicilyBR, 2, iByzantiumCarthageConquestYear + 5, 5)

tConquestByzantiumAndalusia = (31, iByzantium, iBarbarian, tSpainMoorsTL, tSpainMoorsBR, 1, iByzantiumCarthageConquestYear + 5, 5)

# dummy conquest intended for validating if Egypt can be conquered
iPersiaLevantConquestYear = -600
tConquestPersiaLevant= (32, iPersia, iPhoenicia, tLevantTL, tLevantBR, 2, iPersiaLevantConquestYear, 5)

iPersiaEgyptConquestYear = -525

tConquestPersiaEgypt = (33, iPersia, iEgypt, tEgyptTL, tEgyptBR, 2, iPersiaEgyptConquestYear, 10)

iCarthageInSpainYear = -240
tCarthageSpainTL = (56, 48)
tCarthageSpainBR = (60, 51)
tConquestCarthageInSpain = (34, iPhoenicia, iIndependent2, tCarthageSpainTL, tCarthageSpainBR, 3, iCarthageInSpainYear, 5)

iHannibalInItalyYear = -220
tHannibalInItalyTL = (65, 57)
tHannibalInItalyBR = (67, 57)
tConquestHannibalInItaly = (35, iPhoenicia, iRome, tHannibalInItalyTL, tHannibalInItalyBR, 1, iHannibalInItalyYear, 10)

# used for checking a precondition
tDummyConquestRomeHoldingRome= (36, iRome, iBarbarian, tRome, tRome, 1, -3000, 10)


iParthiaMesopotamiaYear = 220
tConquestParthiaMesopotamia = (37, iParthia, iRome, tLevantTL, tGreeceMesopotamiaBR, 3, iParthiaMesopotamiaYear, 10)

iFatamidEgyptYear = 969
tConquestFatamidEgypt = (38, iMamluks, iArabia, tEgyptTL, tEgyptBR, 2, iFatamidEgyptYear, 10)

lConquests = [
	tConquestRomeCarthageInSpain,
	tConquestRomeCarthage, 
	tConquestRomeGreece, 
	tConquestRomeAnatolia,
	tConquestRomeLevant, 
	tConquestRomeCelts, 
	tConquestRomeEgypt,
	tConquestRomeBritain,
	tConquestMacedonAnatolia,
	tConquestMacedonLevant,
	tConquestMacedonMesopotamia, 
	tConquestMacedonEgypt, 
	tConquestMacedonPersia, 
	#tConquestSpainMoors, # --> now that Moors have Almoravid barbarians to contend with, we don't need this
	tConquestTurksPersia, 
	tConquestTurksAnatolia, 
	tConquestEnglandIreland,
	tConquestMongolsPersia,
	tConquestChinaIndependents,
	#tConquestFranceCrusades, # if re-enabled make sure to not trigger on top of Catholic lands
	#tConquestHolyRomeCrusades, # if re-enabled make sure to not trigger on top of Catholic lands
	#tConquestEnglandCrusades, # if re-enabled make sure to not trigger on top of Catholic lands
	tConquestSuiUnification,
	tConquestArabiaCarthage,
	tConquestArabiaPersia,
	tConquestArabiaSind,
	tConquestAssyriaLevant,
	tConquestPersiaLydia,
	tConquestByzantiumCarthage,
	tConquestByzantiumSicily,
	tConquestByzantiumAndalusia,
	tConquestPersiaLevant,
	tConquestPersiaEgypt,
	tConquestCarthageInSpain,
	tConquestHannibalInItaly,
	tConquestParthiaMesopotamia,
	tConquestFatamidEgypt,
	tConquestMongolsBaghdad,
]

dConquestChecker = {
	tConquestMacedonLevant[0]: lambda tConquest: checkConquest(tConquest, tConquestMacedonAnatolia),
	tConquestMacedonEgypt[0]: lambda tConquest: checkConquest(tConquest, tConquestMacedonLevant),
	tConquestMacedonMesopotamia[0]: lambda tConquest: checkConquest(tConquest, tConquestMacedonLevant),
	tConquestMacedonPersia[0]: lambda tConquest: checkConquest(tConquest, tConquestMacedonMesopotamia),
	tConquestRomeAnatolia[0]: lambda tConquest: checkConquest(tConquest, tConquestRomeGreece),
	tConquestRomeLevant[0]: lambda tConquest: checkConquest(tConquest, tConquestRomeGreece),
	tConquestRomeEgypt[0]: lambda tConquest: checkConquest(tConquest, tConquestRomeGreece),
	tConquestRomeCarthage[0]: lambda tConquest: checkConquest(tConquest, tConquestRomeCarthageInSpain),
	tConquestRomeBritain[0]: lambda tConquest: checkConquest(tConquest, tConquestRomeCelts),
	tConquestArabiaSind[0]: lambda tConquest: checkConquest(tConquest, tConquestArabiaPersia),
	tConquestByzantiumCarthage[0]: lambda tConquest: checkByzantiumConquestOfCarthage(tConquest),
	tConquestByzantiumSicily[0]: lambda tConquest: checkByzantiumIfCarthageOwned(tConquest),
	tConquestByzantiumAndalusia[0]: lambda tConquest: checkByzantiumIfCarthageOwned(tConquest),
	tConquestPersiaEgypt[0]: lambda tConquest: checkConquest(tConquest, tConquestPersiaLevant),
	tConquestHannibalInItaly[0]: lambda tConquest: checkConquest(tConquest, tConquestCarthageInSpain),
	tConquestRomeGreece[0]: lambda tConquest: checkConquest(tConquest, tDummyConquestRomeHoldingRome),
	tConquestRomeCelts[0]: lambda tConquest: checkConquest(tConquest, tDummyConquestRomeHoldingRome),
	tConquestMongolsBaghdad[0]: lambda tConquest: checkConquest(tConquest, tConquestMongolsPersia),
}

def checkByzantiumConquestOfCarthage(tConquest):
	if player(iByzantium).isAlive() and len(cities.region(rMaghreb).owner(iRome)) == 0 and len(cities.region(rMaghreb).owner(iPhoenicia)) == 0: 
		checkConquest(tConquest)

def checkByzantiumIfCarthageOwned(tConquest):
	if not player(iRome).isAlive(): 
		checkConquest(tConquest, tConquestByzantiumCarthage)

@handler("BeginGameTurn")
def checkConquests():
	for tConquest in lConquests:
		iID = tConquest[0]
		if not iID in data.dHasConquestHappened:
			data.dHasConquestHappened[iID] = False

		if not data.dHasConquestHappened[iID]:
			if iID in dConquestChecker: 
				dConquestChecker[iID](tConquest)
			else:
				checkConquest(tConquest)	

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
	
	if not iID in data.dHasConquestHappened:
		data.dHasConquestHappened[iID] = False

	if data.dHasConquestHappened[iID]:
		return

	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return
		
	if player(iPlayer).isHuman():
		return
		
	if not player(iPlayer).isExisting() and iCiv != iTurks: 
		return
	
	if team(iPlayer).isAVassal():
		return

	iStartTurn = year(iYear) + turns(data.iSeed % 6 - 3)
	
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
	data.dHasConquestHappened[iID] = True


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
		elif city.getOwner() != iPlayer and not team(city).isVassal(iPlayer): return False
		
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
	if iEra >= iMedieval or iCiv == iArabia:
		iExtra = 1

	tPlotLast = None
	
	for city in targetCities:	
		if not player(iPlayer).isHuman():
			# we want to be sure that the AI can fund these conquerors for at least a few turns
			player(iPlayer).changeGold(20)
		
		tPlot = findNearestLandPlot(city, iPlayer)
		tPlotLast = tPlot
		
		if iCiv == iMacedon:
			makeUnits(iPlayer, iCatapult, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iPhalanx, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCompanion, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)

			# if Macedon happens to control Greece proper, give them volunteers
			# otherwise give them mercenaries
			if civ(plot(tAthens)) == iMacedon:
				lUnits = makeUnits(iPlayer, iHoplite, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			else:
				lUnits = makeUnits(iPlayer, iHoplite, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
				lUnits.promotion(infos.type("PROMOTION_MERCENARY"))

			# Tyre gets extra attackers, since it's a tough nut to crack and the site of a famous siege
			if location(city) == tTyre:
				makeUnits(iPlayer, iCatapult, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
				makeUnits(iPlayer, iHoplite, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		# Hannibalic army composition
		elif iCiv == iPhoenicia:
			lUnits  = makeUnits(iPlayer, iCatapult, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits += makeUnits(iPlayer, iSacredBand, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits += makeUnits(iPlayer, iOathsworn, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits += makeUnits(iPlayer, iHoplite, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits += makeUnits(iPlayer, iNumidianCavalry, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits += makeUnits(iPlayer, iWarElephant, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			lUnits.promotion(infos.type("PROMOTION_MERCENARY"))

		elif iCiv in [iSpain, iEngland, iHolyRome, iFrance, iItaly, iParthia]:
			dConquestUnits = {
				iCityAttack: 1 + iExtra,
				iCitySiege: 2 + iExtra,
				iDefend: 1,
				iShockCity: min(iExtra * 2, 2),
				iCounter: 1,
			}
			lUnits = createRoleUnits(iPlayer, tPlot, dConquestUnits.items())
			lUnits.promotion(infos.type("PROMOTION_CITY_RAIDER1"))
		else:
			dConquestUnits = {
				iCityAttack: 2 + iExtra,
				iCitySiege: 2 + 2 * iExtra,
				iDefend: 1,
			}
			lUnits = createRoleUnits(iPlayer, tPlot, dConquestUnits.items())
			lUnits.promotion(infos.type("PROMOTION_CITY_RAIDER1"))
	
			if iCiv in [iTurks, iMongols]:
				createRoleUnit(iPlayer, tPlot, iShockCity, 2)
				createRoleUnit(iPlayer, tPlot, iHarass, 2)

			# Shia conquerors get free missionary
			if pPlayer.getStateReligion() == iShia:
				makeUnits(iPlayer, iShiaMissionary, tPlot, 1)

	# if human, select to orient player
	if pPlayer.isHuman():
		conquerorUnit = units.at(tPlotLast).owner(iPlayer).last()
		if conquerorUnit:
			interface.selectUnit(conquerorUnit, True, False, False)
		


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