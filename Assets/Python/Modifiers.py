from Consts import *
from RFCUtils import *
from Events import *

def getModifier(iPlayer, iModifier):
	if iPlayer in lCivOrder:
		return tModifiers[iModifier][iPlayer]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iArabia]:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	player(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iPlayer, iModifier))
	
def updateModifiers(iPlayer):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iModifier)


@handler("playerCivAssigned")
def init(iPlayer, iCivilization):
	updateModifiers(iPlayer)
	
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iArabia]:
		adjustModifiers(iPlayer)
	
	player(iPlayer).updateMaintenance()


@handler("BeginGameTurn")
def updateLateModifiers(iGameTurn):			
	if scenario() == i3000BC and iGameTurn == year(600):
		for iPlayer in players.major().where(lambda p: dBirth[p] < dBirth[iArabia]):
			adjustInflationModifier(iPlayer)
		

### Modifier types ###

iNumModifiers = 14
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierColonyMaintenance,
iModifierCitiesMaintenance, iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, 
iModifierBuildingCost, iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Modifiers (by civilization!) ###



dCultureMods = CivDict({
	iEgypt: 90,
	iBabylonia: 80,
	iHarappa: 80,
	iChina: 80,
	iHittites: 80,
	iNubia: 80,
	iGreece: 100,
	iMacedon: 100,
	iAssyria: 80,
	iIndia: 80,
	iCarthage: 100,
	iPolynesia: 100,
	iPersia: 100,
	iCelts: 80,
	iMaya: 100,
	iRome: 100,
	iDravidia: 100,
	iEthiopia: 90,
	iToltecs: 100,
	iKushans: 100,
	iKorea: 100,
	iKhmer: 120,
	iChinaS: 80,
	iMali: 130,
	iByzantium: 100,
	iBulgaria: 120,
	iFrance: 160,
	iMalays: 120,
	iJapan: 110,
	iSpain: 125,
	iNorse: 130,
	iTurks: 120,
	iArabia: 100,
	iMamluks: 100,
	iTibet: 120,
	iMoors: 125,
	iJava: 120, 
	iEngland: 130,
	iHolyRome: 150,
	iBurma: 120,
	iRus: 120,
	iVietnam: 100,
	iSwahili: 110,
	iPoland: 110,
	iPortugal: 140,
	iInca: 140,
	iItaly: 150,
	iMongols: 135,
	iAztecs: 140,
	iMughals: 120,
	iThailand: 130,
	iSweden: 130,
	iRussia: 130,
	iOttomans: 150,
	iCongo: 130,
	iIran: 135,
	iNetherlands: 165,
	iGermany: 150,
	iAmerica: 140,
	iArgentina: 130,
	iMexico: 140,
	iColombia: 140,
	iBrazil: 140,
	iCanada: 140,
	iIndependent: 20,
	iIndependent2: 20,
	iNative: 20,
	iBarbarian: 30,
}, default=100)

dUnitUpkeepMods = CivDict({
	iEgypt: 135,
	iBabylonia: 120,
	iHarappa: 200,
	iChina: 125,
	iHittites: 110,
	iNubia: 130,
	iGreece: 115,
	iMacedon: 110,
	iAssyria: 100,
	iIndia: 135,
	iCarthage: 115,
	iPolynesia: 100,
	iPersia: 110,
	iCelts: 110,
	iMaya: 110,
	iRome: 100,
	iDravidia: 100,
	iEthiopia: 115,
	iToltecs: 110,
	iKushans: 100,
	iKorea: 110,
	iKhmer: 90,
	iChinaS: 135,
	iMali: 100,
	iByzantium: 110,
	iBulgaria: 100,
	iFrance: 100,
	iMalays: 100,
	iJapan: 100,
	iSpain: 110,
	iNorse: 90,
	iTurks: 100,
	iArabia: 120,
	iMamluks: 150,
	iTibet: 110,
	iMoors: 110,
	iJava: 120, 
	iEngland: 100,
	iHolyRome: 100,
	iBurma: 100,
	iRus: 100,
	iVietnam: 100,
	iSwahili: 100,
	iPoland: 100,
	iPortugal: 100,
	iInca: 100,
	iItaly: 100,
	iMongols: 75,
	iAztecs: 90,
	iMughals: 115,
	iThailand: 90,
	iSweden: 80,
	iRussia: 100,
	iOttomans: 120,
	iCongo: 90,
	iIran: 110,
	iNetherlands: 90,
	iGermany: 75,
	iAmerica: 80,
	iArgentina: 80,
	iMexico: 90,
	iColombia: 90,
	iBrazil: 80,
	iCanada: 75,
	iIndependent: 50,
	iIndependent2: 50,
	iNative: 100,
	iBarbarian: 100,
}, default=100)

dResearchCostMods = CivDict({
	iEgypt: 150,
	iBabylonia: 140,
	iHarappa: 125,
	iChina: 120,
	iHittites: 125,
	iNubia: 130,
	iGreece: 150,
	iMacedon: 120,
	iAssyria: 120,
	iIndia: 130,
	iCarthage: 125,
	iPolynesia: 200,
	iPersia: 125,
	iCelts: 150,
	iMaya: 125,
	iRome: 120,
	iDravidia: 120,
	iEthiopia: 120,
	iToltecs: 135,
	iKushans: 110,
	iKorea: 110,
	iKhmer: 90,
	iChinaS: 110,
	iMali: 100,
	iByzantium: 140,
	iBulgaria: 100,
	iFrance: 90,
	iMalays: 100,
	iJapan: 110,
	iSpain: 80,
	iNorse: 100,
	iTurks: 120,
	iArabia: 140,
	iMamluks: 125,
	iTibet: 90,
	iMoors: 100,
	iJava: 110, 
	iEngland: 80,
	iHolyRome: 100,
	iBurma: 90,
	iRus: 90,
	iVietnam: 90,
	iSwahili: 110,
	iPoland: 80,
	iPortugal: 85,
	iInca: 80,
	iItaly: 70,
	iMongols: 90,
	iAztecs: 80,
	iMughals: 125,
	iThailand: 100,
	iSweden: 80,
	iRussia: 80,
	iOttomans: 120,
	iCongo: 85,
	iIran: 110,
	iNetherlands: 80,
	iGermany: 70,
	iAmerica: 75,
	iArgentina: 70,
	iMexico: 90,
	iColombia: 90,
	iBrazil: 80,
	iCanada: 70,
	iIndependent: 125,
	iIndependent2: 125,
	iNative: 125,
	iBarbarian: 110,
}, default=100)

dDistanceMaintenanceMods = CivDict({
	iEgypt: 150,
	iBabylonia: 110,
	iHarappa: 120,
	iChina: 120,
	iHittites: 120,
	iNubia: 100,
	iGreece: 110,
	iMacedon: 110,
	iAssyria: 100,
	iIndia: 120,
	iCarthage: 80,
	iPolynesia: 50,
	iPersia: 90,
	iCelts: 60,
	iMaya: 100,
	iRome: 70,
	iDravidia: 95,
	iEthiopia: 100,
	iToltecs: 150,
	iKushans: 100,
	iKorea: 120,
	iKhmer: 80,
	iChinaS: 120,
	iMali: 80,
	iByzantium: 120,
	iBulgaria: 100,
	iFrance: 90,
	iMalays: 80,
	iJapan: 95,
	iSpain: 70,
	iNorse: 70,
	iTurks: 60,
	iArabia: 120,
	iMamluks: 120,
	iTibet: 120,
	iMoors: 85,
	iJava: 110, 
	iEngland: 70,
	iHolyRome: 85,
	iBurma: 90,
	iRus: 90,
	iVietnam: 110,
	iSwahili: 80,
	iPoland: 90,
	iPortugal: 80,
	iInca: 60,
	iItaly: 70,
	iMongols: 75,
	iAztecs: 70,
	iMughals: 130,
	iThailand: 80,
	iSweden: 90,
	iRussia: 75,
	iOttomans: 110,
	iCongo: 80,
	iIran: 100,
	iNetherlands: 70,
	iGermany: 80,
	iAmerica: 60,
	iArgentina: 50,
	iMexico: 70,
	iColombia: 70,
	iBrazil: 80,
	iCanada: 70,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 100,
	iBarbarian: 20,
}, default=100)

dColonyMaintenanceMods = CivDict({
	iEgypt: 150,
	iBabylonia: 150,
	iHarappa: 150,
	iChina: 150,
	iHittites: 150,
	iNubia: 150,
	iGreece: 150,
	iMacedon: 150,
	iAssyria: 150,
	iIndia: 100,
	iCarthage: 100,
	iPolynesia: 100,
	iPersia: 100,
	iCelts: 100,
	iMaya: 150,
	iRome: 100,
	iDravidia: 100,
	iEthiopia: 150,
	iToltecs: 150,
	iKushans: 150,
	iKorea: 150,
	iKhmer: 150,
	iChinaS: 150,
	iMali: 100,
	iBulgaria: 100,
	iByzantium: 150,
	iFrance: 60,
	iMalays: 100,
	iJapan: 80,
	iSpain: 55,
	iNorse: 80,
	iTurks: 100,
	iArabia: 150,
	iMamluks: 100,
	iTibet: 150,
	iMoors: 150,
	iJava: 150, 
	iEngland: 50,
	iHolyRome: 90,
	iBurma: 150,
	iRus: 150,
	iVietnam: 100,
	iSwahili: 100,
	iPoland: 100,
	iPortugal: 70,
	iInca: 100,
	iItaly: 80,
	iMongols: 150,
	iAztecs: 100,
	iMughals: 150,
	iThailand: 150,
	iSweden: 80,
	iRussia: 100,
	iOttomans: 100,
	iCongo: 150,
	iIran: 150,
	iNetherlands: 60,
	iGermany: 75,
	iAmerica: 90,
	iArgentina: 100,
	iMexico: 100,
	iColombia: 100,
	iBrazil: 100,
	iCanada: 100,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 100,
	iBarbarian: 20,
}, default=100)

dCitiesMaintenanceMods = CivDict({
	iEgypt: 120,
	iBabylonia: 135,
	iHarappa: 125,
	iChina: 125,
	iHittites: 125,
	iNubia: 145,
	iGreece: 125,
	iMacedon: 120,
	iAssyria: 100,
	iIndia: 150,
	iCarthage: 120,
	iPolynesia: 100,
	iPersia: 85,
	iCelts: 120,
	iMaya: 115,
	iRome: 60,
	iDravidia: 100,
	iEthiopia: 115,
	iToltecs: 160,
	iKushans: 100,
	iKorea: 130,
	iKhmer: 100,
	iChinaS: 125,
	iMali: 90,
	iByzantium: 120,
	iBulgaria: 100,
	iFrance: 90,
	iMalays: 100,
	iJapan: 110,
	iSpain: 50,
	iNorse: 75,
	iTurks: 90,
	iArabia: 130,
	iMamluks: 120,
	iTibet: 120,
	iMoors: 75,
	iJava: 100, 
	iEngland: 75,
	iHolyRome: 75,
	iBurma: 100,
	iRus: 80,
	iVietnam: 100,
	iSwahili: 70,
	iPoland: 75,
	iPortugal: 85,
	iInca: 80,
	iItaly: 80,
	iMongols: 75,
	iAztecs: 85,
	iMughals: 110,
	iThailand: 100,
	iSweden: 80,
	iRussia: 60,
	iOttomans: 120,
	iCongo: 90,
	iIran: 100,
	iNetherlands: 80,
	iGermany: 75,
	iAmerica: 70,
	iArgentina: 50,
	iMexico: 85,
	iColombia: 85,
	iBrazil: 80,
	iCanada: 60,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 100,
	iBarbarian: 30,
}, default=100)

dCivicUpkeepMods = CivDict({
	iEgypt: 130,
	iBabylonia: 110,
	iHarappa: 100,
	iChina: 120,
	iHittites: 110,
	iNubia: 125,
	iGreece: 110,
	iMacedon: 115,
	iAssyria: 110,
	iIndia: 140,
	iCarthage: 70,
	iPolynesia: 80,
	iPersia: 75,
	iCelts: 120,
	iMaya: 80,
	iRome: 75,
	iDravidia: 80,
	iEthiopia: 80,
	iToltecs: 100,
	iKushans: 80,
	iKorea: 85,
	iKhmer: 100,
	iChinaS: 100,
	iMali: 80,
	iByzantium: 120,
	iBulgaria: 100,
	iFrance: 80,
	iMalays: 100,
	iJapan: 80,
	iSpain: 75,
	iNorse: 80,
	iTurks: 110,
	iArabia: 110,
	iMamluks: 110,
	iTibet: 80,
	iMoors: 90,
	iJava: 100, 
	iEngland: 70,
	iHolyRome: 70,
	iBurma: 100,
	iRus: 80,
	iVietnam: 80,
	iSwahili: 80,
	iPoland: 70,
	iPortugal: 80,
	iInca: 60,
	iItaly: 60,
	iMongols: 60,
	iAztecs: 60,
	iMughals: 100,
	iThailand: 80,
	iSweden: 70,
	iRussia: 80,
	iOttomans: 90,
	iCongo: 80,
	iIran: 80,
	iNetherlands: 70,
	iGermany: 60,
	iAmerica: 50,
	iArgentina: 50,
	iMexico: 70,
	iColombia: 70,
	iBrazil: 75,
	iCanada: 75,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 100,
	iBarbarian: 70,
}, default=100)

dHealthMods = CivDict({
	iEgypt: 1,
	iBabylonia: 1,
	iHarappa: 1,
	iChina: 1,
	iHittites: 1,
	iNubia: 2,
	iGreece: 3,
	iMacedon: 2,
	iAssyria: 1,
	iIndia: 1,
	iCarthage: 3,
	iPolynesia: 3,
	iPersia: 3,
	iCelts: 1,
	iMaya: 3,
	iRome: 3,
	iDravidia: 2,
	iEthiopia: 3,
	iToltecs: 3,
	iKushans: 3,
	iKorea: 2,
	iKhmer: 3,
	iChinaS: 1,
	iMali: 2,
	iBulgaria: 2,
	iByzantium: 3,
	iFrance: 2,
	iMalays: 3,
	iJapan: 2,
	iSpain: 2,
	iNorse: 3,
	iTurks: 2,
	iArabia: 2,
	iMamluks: 2,
	iTibet: 3,
	iMoors: 2,
	iJava: 2, 
	iEngland: 2,
	iHolyRome: 2,
	iBurma: 3,
	iRus: 2,
	iVietnam: 3,
	iSwahili: 2,
	iPoland: 2,
	iPortugal: 2,
	iInca: 3,
	iItaly: 2,
	iMongols: 3,
	iAztecs: 3,
	iMughals: 4,
	iThailand: 4,
	iSweden: 2,
	iRussia: 2,
	iOttomans: 4,
	iCongo: 4,
	iIran: 3,
	iNetherlands: 3,
	iGermany: 3,
	iAmerica: 3,
	iArgentina: 3,
	iMexico: 3,
	iColombia: 3,
	iBrazil: 3,
	iCanada: 3,
	iIndependent: 0,
	iIndependent2: 0,
	iNative: 0,
	iBarbarian: 0,
}, default=2)

dUnitCostMods = CivDict({
	iEgypt: 125,
	iBabylonia: 140,
	iHarappa: 200,
	iChina: 130,
	iHittites: 100,
	iNubia: 130,
	iGreece: 115,
	iMacedon: 95,
	iAssyria: 120,
	iIndia: 120,
	iCarthage: 90,
	iPolynesia: 100,
	iPersia: 120,
	iCelts: 100,
	iMaya: 105,
	iRome: 80,
	iDravidia: 85,
	iEthiopia: 90,
	iToltecs: 110,
	iKushans: 100,
	iKorea: 90,
	iKhmer: 90,
	iChinaS: 130,
	iMali: 90,
	iByzantium: 120,
	iBulgaria: 85,
	iFrance: 90,
	iMalays: 100,
	iJapan: 90,
	iSpain: 90,
	iNorse: 85,
	iTurks: 100,
	iArabia: 100,
	iMamluks: 110,
	iTibet: 110,
	iMoors: 110,
	iJava: 110, 
	iEngland: 100,
	iHolyRome: 90,
	iBurma: 80,
	iRus: 90,
	iVietnam: 90,
	iSwahili: 100,
	iPoland: 80,
	iPortugal: 90,
	iInca: 100,
	iItaly: 110,
	iMongols: 80,
	iAztecs: 100,
	iMughals: 100,
	iThailand: 90,
	iSweden: 80,
	iRussia: 90,
	iOttomans: 100,
	iCongo: 70,
	iIran: 90,
	iNetherlands: 90,
	iGermany: 75,
	iAmerica: 85,
	iArgentina: 80,
	iMexico: 85,
	iColombia: 85,
	iBrazil: 85,
	iCanada: 85,
	iIndependent: 300,
	iIndependent2: 300,
	iNative: 150,
	iBarbarian: 140,
}, default=100)

dWonderCostMods = CivDict({
	iEgypt: 80,
	iBabylonia: 80,
	iHarappa: 120,
	iChina: 120,
	iHittites: 100,
	iNubia: 80,
	iGreece: 80,
	iMacedon: 90,
	iAssyria: 80,
	iIndia: 100,
	iCarthage: 90,
	iPolynesia: 100,
	iPersia: 85,
	iCelts: 120,
	iMaya: 90,
	iRome: 100,
	iDravidia: 100,
	iEthiopia: 100,
	iToltecs: 100,
	iKushans: 110,
	iKorea: 100,
	iKhmer: 90,
	iChinaS: 120,
	iMali: 90,
	iByzantium: 110,
	iBulgaria: 85,
	iFrance: 70,
	iMalays: 90,
	iJapan: 100,
	iSpain: 90,
	iNorse: 90,
	iTurks: 120,
	iArabia: 90,
	iMamluks: 90,
	iTibet: 100,
	iMoors: 85,
	iJava: 80, 
	iEngland: 90,
	iHolyRome: 100,
	iBurma: 100,
	iRus: 90,
	iVietnam: 100,
	iSwahili: 100,
	iPoland: 100,
	iPortugal: 90,
	iInca: 80,
	iItaly: 80,
	iMongols: 90,
	iAztecs: 80,
	iMughals: 80,
	iThailand: 90,
	iSweden: 100,
	iRussia: 100,
	iOttomans: 90,
	iCongo: 100,
	iIran: 85,
	iNetherlands: 100,
	iGermany: 90,
	iAmerica: 70,
	iArgentina: 70,
	iMexico: 90,
	iColombia: 90,
	iBrazil: 90,
	iCanada: 80,
	iIndependent: 150,
	iIndependent2: 150,
	iNative: 150,
	iBarbarian: 100,
}, default=100)

dBuildingCostMods = CivDict({
	iEgypt: 110,
	iBabylonia: 110,
	iHarappa: 100,
	iChina: 100,
	iHittites: 100,
	iNubia: 110,
	iGreece: 100,
	iMacedon: 100,
	iAssyria: 110,
	iIndia: 110,
	iCarthage: 90,
	iPolynesia: 50,
	iPersia: 110,
	iCelts: 120,
	iMaya: 90,
	iRome: 80,
	iDravidia: 70,
	iEthiopia: 100,
	iToltecs: 120,
	iKushans: 100,
	iKorea: 85,
	iKhmer: 100,
	iChinaS: 100,
	iMali: 80,
	iByzantium: 110,
	iBulgaria: 85,
	iFrance: 85,
	iMalays: 90,
	iJapan: 80,
	iSpain: 90,
	iNorse: 90,
	iTurks: 100,
	iArabia: 100,
	iMamluks: 100,
	iTibet: 80,
	iMoors: 90,
	iJava: 100, 
	iEngland: 90,
	iHolyRome: 85,
	iBurma: 100,
	iRus: 90,
	iVietnam: 90,
	iSwahili: 80,
	iPoland: 80,
	iPortugal: 80,
	iInca: 70,
	iItaly: 80,
	iMongols: 80,
	iAztecs: 80,
	iMughals: 85,
	iThailand: 80,
	iSweden: 80,
	iRussia: 90,
	iOttomans: 80,
	iCongo: 80,
	iIran: 80,
	iNetherlands: 80,
	iGermany: 70,
	iAmerica: 70,
	iArgentina: 70,
	iMexico: 80,
	iColombia: 80,
	iBrazil: 75,
	iCanada: 80,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 150,
	iBarbarian: 100,
}, default=100)

dInflationRateMods = CivDict({
	iEgypt: 130,
	iBabylonia: 130,
	iHarappa: 130,
	iChina: 120,
	iHittites: 130,
	iNubia: 140,
	iGreece: 150,
	iMacedon: 130,
	iAssyria: 125,
	iIndia: 140,
	iCarthage: 130,
	iPolynesia: 130,
	iPersia: 130,
	iCelts: 140,
	iMaya: 125,
	iRome: 130,
	iDravidia: 110,
	iEthiopia: 130,
	iToltecs: 125,
	iKushans: 120,
	iKorea: 95,
	iKhmer: 100,
	iChinaS: 120,
	iMali: 115,
	iByzantium: 130,
	iBulgaria: 100,
	iFrance: 90,
	iMalays: 100,
	iJapan: 80,
	iSpain: 90,
	iNorse: 70,
	iTurks: 90,
	iArabia: 140,
	iMamluks: 120,
	iTibet: 100,
	iMoors: 100,
	iJava: 100, 
	iEngland: 70,
	iHolyRome: 70,
	iBurma: 90,
	iRus: 100,
	iVietnam: 90,
	iSwahili: 90,
	iPoland: 70,
	iPortugal: 80,
	iInca: 80,
	iItaly: 85,
	iMongols: 90,
	iAztecs: 80,
	iMughals: 120,
	iThailand: 75,
	iSweden: 70,
	iRussia: 80,
	iOttomans: 100,
	iCongo: 75,
	iIran: 85,
	iNetherlands: 85,
	iGermany: 70,
	iAmerica: 65,
	iArgentina: 60,
	iMexico: 65,
	iColombia: 65,
	iBrazil: 60,
	iCanada: 60,
	iIndependent: 95,
	iIndependent2: 95,
	iNative: 95,
	iBarbarian: 95,
}, default=100)

dGreatPeopleThresholdMods = CivDict({
	iEgypt: 140,
	iBabylonia: 140,
	iHarappa: 140,
	iChina: 125,
	iHittites: 140,
	iNubia: 140,
	iGreece: 140,
	iMacedon: 120,
	iAssyria: 140,
	iIndia: 125,
	iCarthage: 120,
	iPolynesia: 120,
	iPersia: 110,
	iCelts: 140,
	iMaya: 100,
	iRome: 110,
	iDravidia: 110,
	iEthiopia: 110,
	iToltecs: 120,
	iKushans: 100,
	iKorea: 110,
	iKhmer: 90,
	iChinaS: 125,
	iMali: 80,
	iByzantium: 120,
	iBulgaria: 80,
	iFrance: 70,
	iMalays: 90,
	iJapan: 90,
	iSpain: 75,
	iNorse: 90,
	iTurks: 90,
	iArabia: 80,
	iMamluks: 80,
	iTibet: 90,
	iMoors: 75,
	iJava: 100, 
	iEngland: 75,
	iHolyRome: 80,
	iBurma: 90,
	iRus: 90,
	iVietnam: 90,
	iSwahili: 80,
	iPoland: 80,
	iPortugal: 75,
	iInca: 70,
	iItaly: 65,
	iMongols: 70,
	iAztecs: 70,
	iMughals: 75,
	iThailand: 80,
	iSweden: 75,
	iRussia: 80,
	iOttomans: 80,
	iCongo: 85,
	iIran: 80,
	iNetherlands: 70,
	iGermany: 65,
	iAmerica: 65,
	iArgentina: 70,
	iMexico: 80,
	iColombia: 80,
	iBrazil: 80,
	iCanada: 75,
	iIndependent: 100,
	iIndependent2: 100,
	iNative: 100,
	iBarbarian: 100,
}, default=100)

dGrowthThresholdMods = CivDict({
	iEgypt: 150,
	iBabylonia: 150,
	iHarappa: 150,
	iChina: 150,
	iHittites: 150,
	iNubia: 150,
	iGreece: 130,
	iMacedon: 130,
	iAssyria: 150,
	iIndia: 150,
	iCarthage: 120,
	iPolynesia: 120,
	iPersia: 130,
	iCelts: 150,
	iMaya: 110,
	iRome: 120,
	iDravidia: 110,
	iEthiopia: 100,
	iToltecs: 120,
	iKushans: 120,
	iKorea: 110,
	iKhmer: 80,
	iChinaS: 150,
	iMali: 75,
	iBulgaria: 85,
	iByzantium: 90,
	iFrance: 80,
	iMalays: 100,
	iJapan: 90,
	iSpain: 80,
	iNorse: 80,
	iTurks: 80,
	iArabia: 80,
	iMamluks: 80,
	iTibet: 90,
	iMoors: 90,
	iJava: 100, 
	iEngland: 70,
	iHolyRome: 80,
	iBurma: 90,
	iRus: 80,
	iVietnam: 120,
	iSwahili: 80,
	iPoland: 80,
	iPortugal: 80,
	iInca: 70,
	iItaly: 70,
	iMongols: 75,
	iAztecs: 70,
	iMughals: 70,
	iThailand: 75,
	iSweden: 80,
	iRussia: 80,
	iOttomans: 70,
	iCongo: 75,
	iIran: 70,
	iNetherlands: 75,
	iGermany: 70,
	iAmerica: 70,
	iArgentina: 70,
	iMexico: 70,
	iColombia: 70,
	iBrazil: 70,
	iCanada: 70,
	iIndependent: 125,
	iIndependent2: 125,
	iNative: 125,
	iBarbarian: 125,
}, default=100)

tModifiers = (dCultureMods, dUnitUpkeepMods, dResearchCostMods, dDistanceMaintenanceMods, dColonyMaintenanceMods, dCitiesMaintenanceMods, dCivicUpkeepMods, dHealthMods, dUnitCostMods, dWonderCostMods, dBuildingCostMods, dInflationRateMods, dGreatPeopleThresholdMods, dGrowthThresholdMods)

dLateScenarioModifiers = {
iModifierUnitUpkeep : 90,
iModifierDistanceMaintenance : 85,
iModifierCitiesMaintenance : 80,
iModifierCivicUpkeep : 90,
iModifierInflationRate : 85,
iModifierGreatPeopleThreshold : 85,
iModifierGrowthThreshold : 80,
}

# a repeat of the civDict defaults, hopefully refactored out later
tDefaults = (100, 100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)