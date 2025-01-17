from Core import *

from Events import events, handler


### Unit spawn functions ###

def getStartingUnits(iPlayer):
	return [(iRole, iAmount) for iRole, iAmount in dStartingUnits[iPlayer].items() if iRole != iWork]

def getAIStartingUnits(iPlayer):
	return dExtraAIUnits[iPlayer].items()
	
def getAdditionalUnits(iPlayer):
	return dAdditionalUnits[iPlayer].items()

def getHumanStartingUnits(iPlayer):
	return dHumanStartingUnits[iPlayer].items()

def getSpecificAdditionalUnits(iPlayer):
	return dSpecificAdditionalUnits[iPlayer].items()

def getSpecificAIStartingUnits(iPlayer):
	return dSpecificAIStartingUnits[iPlayer].items()

### Tech preference functions ###

def getTechPreferences(iPlayer):
	dPreferences = defaultdict({}, 0)
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = dPreferences[iPrereqTech]
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	player(iPlayer).resetTechPreferences()

	for iTech, iValue in dPreferences.items():
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.resetBuildingClassPreferences()
	
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingClassPreference(infos.building(iBuilding).getBuildingClassType(), iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingClassPreference(infos.building(iWonder).getBuildingClassType(), iDefaultPreference)


### General functions ###
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	initPlayerTechPreferences(iPlayer)
	initBuildingPreferences(iPlayer)
	

### Civilization starting attributes ###

class Civilization(object):

	def __init__(self, iCiv, **kwargs):
		self.iCiv = iCiv
	
		self.iLeader = kwargs.get("iLeader")
		self.iGold = kwargs.get("iGold")
		self.iStateReligion = kwargs.get("iStateReligion")
		self.iAdvancedStartPoints = kwargs.get("iAdvancedStartPoints")
		
		self.lCivics = kwargs.get("lCivics", [])
		self.lEnemies = kwargs.get("lEnemies", []) + [iNative, iBarbarian]
		
		self.dAttitudes = kwargs.get("dAttitudes", {})
		
		self.sLeaderName = kwargs.get("sLeaderName")
		
		self.techs = kwargs.get("techs", techs.none())
	
	@property
	def player(self):
		return player(self.iCiv)
	
	@property
	def team(self):
		return team(self.player.getTeam())
	
	@property
	def info(self):
		return infos.civ(self.iCiv)
	
	def isPlayable(self):
		return self.info.getStartingYear() != 0
	
	def apply(self):
		if not self.player.isHuman():
			if self.iLeader is not None:
				self.player.setLeader(self.iLeader)
		
			if self.sLeaderName is not None:
				self.player.setLeaderName(text(self.sLeaderName))
		
		if self.iGold is not None:
			self.player.changeGold(scale(self.iGold))
		
		if self.iStateReligion is not None:
			iOldStateReligion = self.player.getStateReligion()
			iNewStateReligion = self.iStateReligion
			
			if iNewStateReligion == iProtestantism and not game.isReligionFounded(iProtestantism):
				iNewStateReligion = iCatholicism
			
			if iNewStateReligion == iCatholicism and not game.isReligionFounded(iCatholicism):
				iNewStateReligion = iOrthodoxy
			
			if game.isReligionFounded(iNewStateReligion) or self.canFoundReligion(iNewStateReligion):
				self.player.setLastStateReligion(iNewStateReligion)
				events.fireEvent("playerChangeStateReligion", self.player.getID(), iNewStateReligion, iOldStateReligion)
		
		if self.techs:
			for iTech in self.techs:
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)
			
			self.player.setStartingEra(self.player.getCurrentEra())
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
			
		for iEnemy in self.lEnemies:
			iEnemyPlayer = slot(iEnemy)
			if iEnemyPlayer >= 0 and self.iCiv != iEnemy:
				team(self.player.getTeam()).declareWar(iEnemyPlayer, False, WarPlanTypes.WARPLAN_TOTAL)
		
		for iCiv, iAttitude in self.dAttitudes.items():
			self.player.AI_changeAttitudeExtra(slot(iCiv), iAttitude)
	
	def canFoundReligion(self, iReligion):
		return infos.religion(iReligion).getTechPrereq() in self.techs
	
	def advancedStart(self):
		if self.iAdvancedStartPoints is not None:
			self.player.setAdvancedStartPoints(scale(self.iAdvancedStartPoints))
			
			if not self.player.isHuman():
				self.player.AI_doAdvancedStart()

lCivilizations = [
	# this doesn't do anything because it is set in Scenario3000BC
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iMasonry, iPottery, iAgriculture, iMythology)
	),
	# this doesn't do anything because it is set in Scenario3000BC
	Civilization(
		iBabylonia,
		techs=techs.of(iPottery, iPastoralism, iAgriculture, iMythology, iProperty)
	),
	# this doesn't do anything because it is set in Scenario3000BC
	Civilization(
		iHarappa,
		techs=techs.of(iMining, iPottery, iAgriculture, iPastoralism, iTanning)
	),
	# this doesn't do anything because it is set in Scenario3000BC
	Civilization(
		iMinoans,
		techs=techs.of(iPastoralism, iPottery, iAgriculture, iSailing, iTanning)
	),
	Civilization(
		iXia,
		iGold=50,
		lCivics=[iDespotism],
		techs=techs.column(2).without(iSailing, iSeafaring, iSmelting, ).including(iProperty, iCeremony)
	),
	Civilization(
		iHittites,
		iGold=40,
		lCivics=[iMonarchy, iSlavery],
		techs=techs.column(2).without(iRiding, iSeafaring).including(iAlloys)
	),
	Civilization(
		iNubia,
		iGold=100,
		lCivics=[iSlavery, iDeification],
		lEnemies=[iEgypt],
		techs=techs.column(1).including(iMasonry, iSmelting, iProperty, iCeremony, iDivination)
	),
	Civilization(
		iAssyria,
		lCivics=[iDespotism, iSlavery, iDeification],
		techs=techs.column(2).without(iRiding, iSeafaring).including(iWriting)
	),
	Civilization(
		iShu,
		iGold=50,
		lCivics=[iDespotism, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys).without(iRiding, iSeafaring)
	),
	Civilization(
		iPhoenicia,
		iGold=200,
		iAdvancedStartPoints=90,
		lCivics=[iRepublic, iSlavery],
		techs=techs.column(2).including(iAlloys, iWriting, iShipbuilding)
	),
	Civilization(
		iPolynesia,
		techs=techs.of(iTanning, iMythology, iSailing, iSeafaring)
	),
	Civilization(
		iGreece,
		iGold=100,
		lCivics=[iRepublic, iSlavery, iDeification],
		techs=techs.column(3).including(iBloomery)
	),
	Civilization(
		iPersia,
		iGold=200,
		iAdvancedStartPoints=200,
		iStateReligion=iZoroastrianism,
		lCivics=[iMonarchy, iManorialism, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iPriesthood, iMathematics, iContract).without(iSeafaring, iShipbuilding)
	),
	Civilization(
		iIndia,
		iGold=80,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy],
		techs=techs.column(3).including(iBloomery, iPriesthood, iMathematics).without(iSeafaring, iShipbuilding)
	),
	Civilization(
		iCelts,
		techs=techs.column(2).including(iAlloys),
		lCivics=[iMonarchy],
	),
	Civilization(
		iVietnam,
		iGold=50,
		lCivics=[iMonarchy, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys),
	),
	Civilization(
		iMacedon,
		iGold=50,
		iAdvancedStartPoints=100,
		lCivics=[iMonarchy, iRedistribution, iSlavery, iDeification, iStratocracy],
		techs=techs.column(3).including(iBloomery, iMathematics).without(iShipbuilding)
	),
	Civilization(
		iChina,
		iGold=250,
		iAdvancedStartPoints=100,
		lCivics=[iDespotism, iSlavery, iRedistribution, iHegemony],
		techs=techs.column(4).including(iGeneralship).without(iShipbuilding, iNavigation)
	),
	Civilization(
		iRome,
		iGold=200,
		iAdvancedStartPoints=300,
		lCivics=[iRepublic, iSlavery, iCitizenship, iRedistribution, iHegemony],
		techs=techs.column(4).including(iGeneralship, iLaw).without(iRiding, iShipbuilding, iNavigation)
	),
	Civilization(
		iArmenia,
		iGold=100,
		iAdvancedStartPoints=60,
		lCivics=[iMonarchy, iRedistribution, iSlavery],
		techs=techs.column(4).including(iGeneralship).without(iNavigation)
	),
	Civilization(
		iParthia,
		iGold=100,
		iAdvancedStartPoints=120,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(4).including(iGeneralship, iCurrency).without(iShipbuilding, iNavigation)
	),
	Civilization(
		iMaya,
		iGold=100,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(1).including(iProperty, iMasonry, iSmelting, iCeremony).without(iSailing)
	),
	Civilization(
		iDravidia,
		iGold=200,
		iAdvancedStartPoints=80,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iMathematics, iContract, iPriesthood)
	),
	Civilization(
		iEthiopia,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iClergy],
		lEnemies=[iNubia],
		techs=techs.column(2).including(iAlloys, iWriting, iCalendar, iPriesthood)
	),
	Civilization(
		iToltecs,
		iGold=50,
		lCivics=[iRedistribution, iDeification],
		techs=techs.column(2).including(iConstruction, iArithmetics).without(iSeafaring)
	),
	Civilization(
		iKushans,
		iGold=100,
		iAdvancedStartPoints=120,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iSyncretism, iHegemony],
		techs=techs.column(4).including(iGeneralship, iCurrency, iPhilosophy).without(iNavigation)
	),
	Civilization(
		iKorea,
		iGold=200,
		iAdvancedStartPoints=60,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCasteSystem, iRedistribution, iSyncretism],
		techs=techs.column(4).without(iNavigation).including(iPhilosophy)
	),
	Civilization(
		iKhmer,
		iGold=50,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(4).without(iNavigation).including(iEngineering)
	),
	Civilization(
		iChinaS,
		iGold=150,
		iAdvancedStartPoints=60,
		iStateReligion=iTaoism,
		lCivics=[iMonarchy, iCasteSystem, iRedistribution, iSyncretism, iHegemony],
		lEnemies=[iChina, iIndependent, iIndependent2],
		techs=techs.column(5).including(iArtisanry, iScholarship, iAlchemy)
	),
	Civilization(
		iMali,
		iGold=200,
		lCivics=[iDespotism, iSlavery, iMerchantTrade],
		techs=techs.column(3).including(iMathematics, iContract, iCurrency, iLiterature, iPriesthood)
	),
	Civilization(
		iByzantium,
		iGold=400,
		iAdvancedStartPoints=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iMonarchy, iCitizenship, iSlavery, iRedistribution, iClergy, iThalassocracy],
		techs=techs.column(5).including(iArchitecture, iPolitics, iEthics)
	),
	Civilization(
		iSpain,
		iGold=100,
		lCivics=[iMonarchy, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).without(iScholarship, iArchitecture)
	),
	Civilization(
		iFrance,
		iGold=200,
		lCivics=[iMonarchy, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).without(iScholarship, iArchitecture)
	),
	Civilization(
		iMalays,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(5).including(iEthics).without(iGeneralship, iEngineering)
	),
	Civilization(
		iJapan,
		iGold=100,
		iAdvancedStartPoints=60,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iCasteSystem, iRedistribution, iDeification, iThalassocracy],
		techs=techs.column(5).including(iNobility, iSteel, iArchitecture, iArtisanry)
	),
	Civilization(
		iNorse, 
		iGold=150,
		lCivics=[iElective, iSlavery, iMerchantTrade, iThalassocracy],
		techs=techs.column(6).without(iScholarship, iEthics)
	),
	Civilization(
		iTurks,
		iGold=100,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(5).including(iNobility, iSteel).without(iEngineering, iPhilosophy, iShipbuilding, iNavigation)
	),
	Civilization(
		iArabia,
		iGold=300,
		iAdvancedStartPoints=150,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).including(iAlchemy, iTheology).without(iPolitics)
	),
	Civilization(
		iTibet,
		iGold=50,
		iAdvancedStartPoints=25,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iMerchantTrade, iMonasticism],
		techs=techs.column(5).including(iNobility, iScholarship, iEthics)
	),
	Civilization(
		iKhazars,
		iGold=100,
		iStateReligion=iJudaism,
		iAdvancedStartPoints=25,
		lCivics=[iElective, iSlavery, iMerchantTrade],
		techs=techs.column(5).including(iNobility, iSteel).without(iEngineering, iPhilosophy, iNavigation)
	),
	Civilization(
		iBulgaria,
		iGold=50,
		iAdvancedStartPoints=25,
		lEnemies=[iByzantium],
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(5).including(iNobility, iSteel).without(iWriting, iLiterature, iPriesthood, iEngineering, iAesthetics, iLaw, iPhilosophy, iNavigation)
	),
	Civilization(
		iJava,
		iGold=300,
		iAdvancedStartPoints=100,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(6).without(iNobility, iPolitics, iScholarship)
	),
	Civilization(
		iMoors,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).including(iMachinery, iAlchemy, iTheology)
	),
	Civilization(
		iEngland,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iTheology, iCivilService)
	),
	Civilization(
		iHolyRome,
		iGold=150,
		iAdvancedStartPoints=150,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iTheocracy, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).including(iFeudalism, iTheology)
	),
	Civilization(
		iBurma,
		iGold=100,
		iAdvancedStartPoints=80,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iHegemony],
		techs=techs.column(6).including(iTheology)
	),
	Civilization(
		iNigeria,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade],
		techs=techs.column(4).including(iCurrency).without(iShipbuilding, iNavigation)
	),
	Civilization(
		iRus,
		iGold=200,
		iAdvancedStartPoints=50,
		lCivics=[iElective, iMerchantTrade],
		techs=techs.column(6).including(iGuilds).without(iScholarship)
	),
	Civilization(
		iMamluks,
		iGold=300,
		iAdvancedStartPoints=60,
		iStateReligion=iShia,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iClergy, iTheocracy, iHegemony],
		techs=techs.column(6).including(iTheology, iDoctrine)
	),
	Civilization(
		iSwahili,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iShia,
		lCivics=[iElective, iCitizenship, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(6).including(iAlchemy)
	),
	Civilization(
		iGhorids,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(6).including(iFeudalism, iTheology, iDoctrine).without(iShipbuilding, iNavigation)
	),
	Civilization(
		iPoland,
		iGold=100,
		iAdvancedStartPoints=80,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFeudalism, iFortification, iCivilService, iTheology)
	),
	Civilization(
		iPortugal,
		iGold=200,
		iAdvancedStartPoints=60,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(7).including(iCommune, iPatronage)
	),
	Civilization(
		iInca,
		iGold=700,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iDeification],
		techs=techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood).without(iSeafaring, iRiding, iShipbuilding)
	),
	Civilization(
		iItaly,
		iGold=350,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iRepublic, iCitizenship, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7).including(iCommune, iPaper, iCompass, iDoctrine)
	),
	Civilization(
		iMongols,
		iGold=250,
		iAdvancedStartPoints=50,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(7).including(iPaper, iCompass).without(iTheology)
	),
	Civilization(
		iAztecs,
		iGold=200,
		iAdvancedStartPoints=30,
		lCivics=[iMonarchy, iCitizenship, iSlavery, iRedistribution, iDeification, iHegemony],
		techs=techs.column(4).including(iGeneralship, iAesthetics, iCurrency, iLaw).without(iSeafaring, iRiding, iShipbuilding, iCement, iNavigation)
	),
	Civilization(
		iThailand,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iThalassocracy],
		techs=techs.column(8).without(iCompass, iDoctrine)
	),
	Civilization(
		iSweden,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iProtestantism,
		lCivics=[iElective, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(8)
	),
	Civilization(
		iRussia,
		iGold=300,
		iAdvancedStartPoints=200,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8)
	),
	Civilization(
		iOttomans,
		iGold=300,
		iAdvancedStartPoints=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(7).including(iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder)
	),
	Civilization(
		iCongo,
		iGold=300,
		lCivics=[iElective, iSlavery, iRedistribution],
		techs=techs.column(6).including(iMachinery, iCivilService, iGuilds, iTheology)
	),
	Civilization(
		iTimurids,
		iGold=800,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iRegulatedTrade, iSyncretism, iHegemony],
		techs=techs.column(7).including(iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder)
	),
	Civilization(
		iIroquois,
		iGold=20,
		techs=techs.of(iTanning, iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iIran,
		iGold=600,
		iAdvancedStartPoints=100,
		iStateReligion=iShia,
		lEnemies=[iTimurids],
		lCivics=[iMonarchy, iTheocracy, iManorialism, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(9).including(iFirearms).without(iCartography, iFinance, iHumanities, iPrinting, iJudiciary)
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iAdvancedStartPoints=200,
		iStateReligion=iProtestantism,
		lCivics=[iRepublic, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iColonialism],
		techs=techs.column(10).including(iCombinedArms, iUrbanPlanning)
	),
	Civilization(
		iGermany,
		iGold=800,
		iAdvancedStartPoints=200,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(11).without(iGeography, iCivilLiberties)
	),
	Civilization(
		iAmerica,
		iGold=2000,
		iAdvancedStartPoints=300,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iIsolationism],
		techs=techs.column(12).including(iRepresentation, iChemistry, iBiology)
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iMexico,
		iGold=500,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iZulu,
		iGold=100,
		techs=techs.column(2).including(iAlloys),
		lCivics=[iMonarchy, iSlavery, iDeification],
	),
	Civilization(
		iColombia,
		iGold=750,
		iAdvancedStartPoints=150,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iAdvancedStartPoints=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iConstitution, iSlavery, iFreeEnterprise, iClergy, iColonialism],
		techs=techs.column(12).including(iRepresentation, iNationalism, iBiology)
	),
	Civilization(
		iCanada,
		iGold=1000,
		iAdvancedStartPoints=250,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(13).including(iBallistics, iEngine, iRailroad, iJournalism)
	),
]

### Starting units ###

dStartingUnits = CivDict({
	iAssyria: {
		iSettle: 1,
		iWork: 2,
		iBase: 1,
		iDefend: 3,
		iCounter: 4,
		iSiege: 4,
	},
	iXia: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
	},
	iShu: {
		iSettle: 1,
		iShock: 1,
		iDefend: 1,
		iBase: 1,
	},
	iHittites: {
		iSettle: 1,
		iWork: 1,
		iBase: 1,
		iAttack: 1,
		iShock: 2,
	},
	iNubia: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iBase: 2,
	},
	iGreece: {
		iSettle: 1,
		iWork: 2,
		iSettleSea: 2,
		iDefend: 1,
		iCounter: 1,
		iWorkerSea: 1,
	},
	iIndia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 4,
		iCounter: 2,
		iAttack: 1,
		iShock: 3,
	},
	iPhoenicia: {
		iSettle: 1,
		iWork: 3,
		iDefend: 1,
		iCounter: 1,
		iSettleSea: 1,
		iFerry: 1,
		iEscort: 1,
	},
	iPolynesia: {
		iSettle: 1,
		iSettleSea: 1,
		iWorkerSea: 1,
	},
	iPersia: {
		iSettle: 7,
		iWork: 3,
		iShock: 5,
		iSiege: 3,
		iCounter: 6,
	},
	iMacedon: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iCounter: 1,
		iShock: 2,
		iSiege: 1,
	},
	iCelts: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iAttack: 4,
		iExplore: 1,
	},
	iChina: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iSiege: 3,
		iCityAttack: 4,
		iCounter: 3,
		iShockCity: 2,
	},
	iRome: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iAttack: 8,
		iSiege: 4,
		iSettleSea: 1,
		iFerry: 1,
		iWorkerSea: 1,
	},
	iArmenia : {
		iSettle: 1,
		iWork: 1,
		iDefend: 3,
		iAttack: 1,
		iShock: 1,
		iCounter: 1,
	},
	iParthia : {
		iSettle: 2,
		iWork: 2,
		iDefend: 4,
		iAttack: 2,
		iShock: 3,
		iSiege: 2,
	},
	iMaya: {
		iSettle: 1,
		iWork: 1,
		iSkirmish: 2,
	},
	iDravidia: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 2,
		iDefend: 1,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
		# 1 War Elephant
	},
	iEthiopia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 2,
		iAttack: 1,
		iWorkerSea: 1,
		iEscort: 1,
		# 1 Shotelai
	},
	iToltecs: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iAttack: 2,
	},
	iKushans: {
		iSettle: 3,
		iWork: 3,
		iDefend: 2,
		iShockCity: 4,
		iCityAttack: 2,
		iSkirmish: 2,
		iCitySiege: 2,
	},
	iKorea: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iAttack: 1,
		iShock: 1,
		iMissionary: 1,
	},
	iKhmer: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iAttack: 1,
		iMissionary: 1,
		iWorkerSea: 1,
	},
	iChinaS: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 3,
		iCounter: 2,
		iMissionary: 1,
		iSiege: 2,
	},
	iMali: {
		iSettle: 1,
		iWork: 1,
		iSkirmish: 3,
	},
	iNigeria: {
		iSettle: 1,
		iDefend: 1,
		iCounter: 1,
		iShock: 2,
		iWork: 1,
	},
	iByzantium: {
		iSettle: 4,
		iWork: 2,
		iAttack: 4,
		iCounter: 2,
		iMissionary: 1,
		iFerry: 2,
		iEscort: 2,
	},
	iFrance: {
		iSettle: 3,
		iWork: 2,
		iDefend: 4,
		iCounter: 3,
		iAttack: 3,
		iSiege: 1,
		iShock: 1,
		iMissionary: 2,
	},
	iMalays: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 2,
		iWorkerSea: 1,
		iDefend: 1,
		iAttack: 1,
		iMissionary: 2,
		iEscort: 1,
	},
	iJapan: {
		iSettle: 3,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 2,
	},
	iNorse: {
		iSettle: 1,
		iWork: 2,
		iSettleSea: 2,
		iDefend: 2,
		iExplore: 1,
		iAssaultSea: 2,
		iWorkerSea: 2,
	},
	iTurks: {
		iSettle: 6,
		iWork: 3,
		iDefend: 4,
		iHarass: 9,
		iExplore: 1,
	},
	iArabia: {
		iSettle: 2,
		iWork: 5,
		iDefend: 1,
		iShock: 4,
		iAttack: 5,
		iHarass: 2,
		iSiege: 3,
	},
	iTibet: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iHarass: 4,
		iMissionary: 1,
	},
	iKhazars: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iCounter: 1,
		iHarass: 2,
		iShock: 4,
		iMissionary: 2,
	},
	iMoors: {
		iSettle: 2,
		iWork: 1,
		iDefend: 1,
		iAttack: 2,
		iCounter: 2,
		iHarass: 2,
		iMissionary: 2,
		iWorkerSea: 1,
		iFerry: 1,
		iEscort: 1,
		# if human Spain or Moors: 1 Crossbowman
	},
	iJava : {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iCityAttack: 2,
		iFerry: 2,
		iEscort: 2,
		iWorkerSea: 1,
		iMissionary: 1,
	},
	iSpain: {
		iSettle: 2,
		iWork: 2,
		iDefend: 2,
		iMissionary: 1,
	},
	iBulgaria: {
		iSettle: 3,
		iWork: 2,
		iDefend: 4,
		iAttack: 1,
		iHarass: 5,
	},
	iEngland: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iShockCity: 1,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
		iFerry: 1,
	},
	iHolyRome: {
		iSettle: 4,
		iWork: 2,
		iDefend: 3,
		iCityAttack: 3,
		iShockCity: 3,
		iCitySiege: 4,
		iMissionary: 1,
	},
	iBurma: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iCounter: 2,
		iAttack: 2,
		iMissionary: 1,
	},
	iVietnam: {
		iSettle: 2,
		iDefend: 1,
	},
	iRus: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iAttack: 3,
		iCounter: 1,
	},
	iSwahili: {
		iSettle: 1,
		iWork: 3,
		iWorkerSea: 2,
		iDefend: 1,
		iSkirmish: 2,
		iExploreSea: 1,
		iSettleSea: 2,
		iMissionary: 1,
	},
	iMamluks: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iShock: 6,
		iAttack: 4,
		iSiege: 4,
		iMissionary: 2,
	},
	iGhorids: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iShockCity: 4,
		iCounter: 3,
		iSiege: 2,
		iMissionary: 3,
	},
	iPoland: {
		iSettle: 2,
		iWork: 2,
		iDefend: 1,
		iAttack: 2,
		iShock: 2,
		iSiege: 1,
		iMissionary: 1,
	},
	iPortugal: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 1,
		iDefend: 4,
		iCounter: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iEscort: 2,
	},
	iInca: {
		iSettle: 1,
		iWork: 4,
		iCityAttack: 4,
		iDefend: 2,
		# if not human: 1 Settler
	},
	iItaly: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iCounter: 2,
		iMissionary: 1,
		iWorkerSea: 1,
		iFerry: 1,
		iEscort: 1,
	},
	iMongols: {
		iSettle: 3,
		iWork: 4,
		iDefend: 4,
		iAttack: 3,
		iHarass: 5,
		iShock: 8,
		iSiege: 4,
		iExplore: 2,
	},
	iAztecs: {
		iSettle: 1,
		iWork: 2,
		iAttack: 4,
		iDefend: 2,
		iWorkerSea: 2,
	},
	iTimurids: {
		iSettle: 3,
		iWork: 2,
		iDefend: 6,
		iCityAttack: 6,
		iHarass: 6,
		iSiege: 8,
		iMissionary: 2,
	},
	iThailand: {
		iSettle: 1,
		iWork: 2,
		iCounter: 2,
		iShock: 2,
		iMissionary: 1,
	},
	iSweden: {
		iSettle: 2,
		iWork: 3,
		iCounter: 3,
		iDefend: 2,
		iAttack: 2,
		iMissionary: 2,
		iSettleSea: 1,
		iEscort: 2,
		iWorkerSea: 1,
	},
	iRussia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 4,
		iAttack: 3,
		iCounter: 4,
		iSiege: 3,
		iHarass: 2,
		iExplore: 2,
		iMissionary: 3,
	},
	iOttomans: {
		iSettle: 3,
		iWork: 3,
		iAttack: 4,
		iDefend: 2,
		iShock: 3,
		iSiege: 4,
		iMissionary: 2,
		iHarass: 3,
	},
	iCongo: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
		iExplore: 1,
	},
	iIroquois: {
		iExplore: 1,
		iSettle: 1,
		iWork: 2,
		iBase: 1,
		iDefend: 3,
	},
	iIran: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 3,
	},
	iNetherlands: {
		iSettle: 2,
		iSettleSea: 2,
		iWork: 2,
		iAttack: 6,
		iCounter: 2,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iExploreSea: 2,
	},
	iGermany: {
		iSettle: 4,
		iWork: 2,
		iAttack: 3,
		iDefend: 2,
		iSiege: 3,
		iMissionary: 2,
	},
	iAmerica: {
		iSettle: 6,
		iWork: 4,
		iSkirmish: 2,
		iAttack: 4,
		iSiege: 2,
		iExplore: 1,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 1,
	},
	iArgentina: {
		iSettle: 2,
		iWork: 2,
		iAttack: 1,
		iDefend: 2,
		iSiege: 2,
		iMissionary: 1,
		iFerry: 1,
		iEscort: 2,
	},
	iMexico: {
		iSettle: 7,
		iWork: 3,
		iShock: 4,
		iDefend: 4,
		iAttack: 2,
		iSkirmish: 2,
		iMissionary: 1,
	},
	iZulu: {
		iSettle: 1,
		iDefend: 1,
		iCounter: 3,
	},
	iColombia: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 1,
		iFerry: 1,
		iAttackSea: 1,
	},
	iBrazil: {
		iSettle: 5,
		iWork: 3,
		iSkirmish: 3,
		iDefend: 3,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 3,
	},
	iCanada: {
		iSettle: 5,
		iWork: 3,
		iShock: 3,
		iDefend: 5,
		iMissionary: 1,
		iFerry: 2,
		iEscort: 1,
		iLightEscort: 1,
	}
}, {})

dExtraAIUnits = CivDict({
	iAssyria : {
		iCounter: 2,
		iDefend: 2,
		iSiege: 3,
	},
	iHittites : {
		iAttack: 1,
		iShock: 2,
		iSettler: 1,
		iBase: 1,
	},
	iChina : {
		iSettle: 2,
		iSiege: 4,
		iCityAttack: 7,
		iShockCity: 4,
		iCounter: 2,
		iDefend: 2,
	},
	iPhoenicia: {
		iSettleSea: 2,
		iEscort: 1,
	},
	iGreece: {
		iSettleSea: 2,
		iWork: 2,
		iWorkerSea: 4,
		iEscort: 1,
	},
	iIndia : {
		iShock: 1,
		iAttack: 1,
		iDefend: 1,
	},
	iRome: {
		iWork: 3,
	},
	iJapan: {
		iDefend: 2,
		iAttack: 1,
	},
	iDravidia: {
		iShock: 1,
		iMissionary: 1,
	},
	iKushans: {
		iShockCity: 4,
		iCityAttack: 2,
		iSiege: 3,
	},
	iKorea: {
		iCounter: 2,
		iDefend: 2,
	},
	iByzantium: {
		iAttack: 3,
		iSiege: 1,
	},
	iFrance: {
		iAttack: 7,
		iDefend: 3,
		iSiege: 1,
		iShock: 2,
	},
	iMalays: {
		iDefend: 2,
	},
	iNorse: {
		iExploreSea: 1,
	},
	iJava: {
		iCityAttack: 2,
	},
	iArabia: {
		iShock: 3,
		iAttack: 2,
		iHarass: 3,
		iCounter: 1,
		iSiege: 3,
		iWork: 3,
	},
	iBulgaria: {
		iAttack: 1,
		iHarass: 2,
		iDefend: 2,
		iSiege: 1,
		iWork: 2,
	},
	iMoors: {
		iAttack: 2,
		iSiege: 2,
		iHarass: 3,
		iDefend: 1,
	}, 
	iHolyRome: {
		iSettle: 1,
		iDefend: 1,
	},
	iEngland: {
		iWork: 2,
	},
	iPoland: {
		iCounter: 2,
	},
	iMongols: {
		iDefend: 3,
		iAttack: 3,
		iShock: 14,
		iSiege: 8,
		iHarass: 7,
		iExplore: 2,
	},
	iInca: {
		iCityAttack: 2,
		iSettle: 1,
	},
	iOttomans: {
		iAttack: 4,
		iShock: 1,
		iSiege: 3,
	},
	iRussia: {
		iWork: 6,
		iShock: 2,
	},
	iTimurids: {
		iWork: 1,
		iCityAttack: 4,
		iHarass: 4,
		iSiege: 7,
		iMissionary: 1,
	},
	iAztecs: {
		iSiege: 2,
	},
	iIran: {
		iAttack: 6,
		iSiege: 3,
	},
	iGermany: {
		iAttack: 10,
		iSiege: 5,
	},
	iAmerica: {
		iDefend: 4,
		iWork: 8,
		iSettle: 4,
	},
	iArgentina: {
		iDefend: 3,
		iShock: 2,
		iSiege: 2,
	},
	iBrazil: {
		iDefend: 1,
	}
}, {})

dHumanStartingUnits = CivDict({
	iMacedon : {
		iCounter: 4,
		iShock: 1,
		iSiege: 2,
	},
	iRome : {
		iAttack: 3,
	},
	iPersia : {
		iCounter: 2,
		iShock: 1,
		iSiege: 1,
	},
}, {})

dAdditionalUnits = CivDict({
	iGreece: {
		iCounter: 2,
	},
	iRome: {
		iAttack: 4,
	},
	iJapan: {
		iDefend: 2,
		iAttack: 2,
	},
	iEthiopia: {
		iDefend: 2,
		# 2 Shotelai
	},
	iKorea: {
		iShock: 2,
		iDefend: 2,
	},
	iMaya: {
		iDefend: 2,
		iAttack: 2,
	},
	iByzantium: {
		iAttack: 1,
		iCounter: 2,
	},
	iFrance: {
		iDefend: 3,
		iAttack: 3,
	},
	iNorse: {
		# 3 Huscarls
	},
	iTurks: {
		iHarass: 4,
	},
	iTibet: {
		iHarass: 2,
	},
	iKhazars: {
		iShock: 2,
	},
	iBulgaria: {
		iDefend: 2,
		iHarass: 2,
	},
	iSpain: {
		iDefend: 3,
		iAttack: 3,
	},
	iEngland: {
		iDefend: 3,
		iAttack: 3,
	},
	iHolyRome: {
		iDefend: 3,
		iAttack: 3,
	},
	iPoland: {
		iDefend: 2,
		iShock: 2,
	},
	iPortugal: {
		iDefend: 3,
		iCounter: 3,
	},
	iItaly: {
		iDefend: 2,
		iCounter: 2,
	},
	iMongols: {
		iDefend: 2,
		iHarass: 2,
		iShock: 4,
	},
	iTimurids: {
		iShock: 2,
		iHarass: 4,
	},
	iThailand: {
		iCounter: 2,
		iShock: 2,
	},
	iRussia: {
		iAttack: 4,
		iDefend: 3,
	},
	iOttomans: {
		iDefend: 3,
		iHarass: 3,
	},
	iIran: {
		iAttack: 2,
		iHarass: 1,
		iSiege: 1,
	},
	iNetherlands: {
		iAttack: 3,
		iCounter: 3,
	},
	iGermany: {
		iAttack: 5,
		iSiege: 3,
	},
	iAmerica: {
		iAttack: 3,
		iSkirmish: 3,
		iSiege: 3,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 4,
	},
	iMexico: {
		iShock: 4,
		iSiege: 2,
	},
	iColombia: {
		iAttack: 4,
		iSkirmish: 4,
		iSiege: 2,
	},
	iBrazil: {
		iAttack: 3,
		iSkirmish: 2,
		iSiege: 2,
	},
	iCanada: {
		iAttack: 4,
		iShock: 2,
		iSiege: 2,
	},
}, {})

dSpecificAIStartingUnits = CivDict({
	iByzantium: {
		iTagmata: 4,
	},
	iTimurids: {
		iKeshik: 10,
	}
}, {})

dStartingExperience = CivDict({
	iCelts: {
		iAttack: 2,
	},
	iKushans: {
		iCityAttack: 3,
		iShockCity: 3,
		iCitySiege: 2,
	},
	iTimurids: {
		iCityAttack: 2,
		iShockCity: 2,
		iSiege: 2,
	},
	iGermany: {
		iAttack: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iMexico: {
		iShock: 2,
		iDefend: 2,
		iAttack: 2,
		iSkirmish: 2,
	},
	iColombia: {
		iAttack: 2,
		iSkirmish: 2,
		iSiege: 2,
	},
}, {})

dAlwaysTrain = CivDict({
	iGreece: [iHoplite],
	iMacedon: [iPhalanx],
	iPhoenicia: [iNumidianCavalry],
	iDravidia: [iWarElephant],
	iArabia: [iMobileGuard, iGhazi],
	iAztecs: [iJaguar],
	iOttomans: [iJanissary, iGreatBombard],
	iMexico: [iGrenadier],
	iColombia: [iAlbionLegion],
	iBrazil: [iGrenadier],
	iNigeria: [iHausaCavalry],
	iZulu: [iImpi],
}, [])

dAIAlwaysTrain = CivDict({
	iMoors: [iCrossbowman],
	iTurks: [iMamlukCavalry],
}, [])

dNeverTrain = CivDict({
	iCongo: [iCrossbowman],
	iNigeria: [iCrossbowman],
}, [])

def createSpecificUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	
	if iCiv == iKorea:
		makeUnit(iPlayer, iConfucianMissionary, tile)
	elif iCiv == iPersia:
		makeUnits(iPlayer, iZoroastrianMissionary, tile, 2)
	elif iCiv == iDravidia:
		makeUnit(iPlayer, iWarElephant, tile)
	elif iCiv == iEthiopia:
		makeUnit(iPlayer, iShotelai, tile)
	elif iCiv == iMalays:
		makeUnit(iPlayer, iHinduMissionary, tile)
	elif iCiv == iJava:
		makeUnit(iPlayer, iBuddhistMissionary, tile)
	elif iCiv == iColombia:
		makeUnits(iPlayer, iAlbionLegion, tile, 5).experience(2)
	elif iCiv == iParthia:
		makeUnits(iPlayer, iHorseArcher, tile, 5)
	elif iCiv == iFrance:
		makeUnits(iPlayer, iAxeman, tile, 6)
	elif iCiv == iTimurids:
		makeUnits(iPlayer, iKeshik, tile, 12)
	elif iCiv == iRus:
		makeUnits(iPlayer, iHuscarl, tile, 3)

dSpecificAdditionalUnits = CivDict({
	iEthiopia: {
		iShotelai: 2,
	},
	iNorse: {
		iHuscarl: 3,
	},
	iMoors: {
		iCamelArcher: 2,
	},
}, {})


### Tech Preferences ###

dTechPreferences = {
	iEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		iNavigation: 20,
		iShipbuilding: 20,
		iArithmetics: 20,
		
		iAlloys: -20,
		iBloomery: -50,
		iRiding: -50,
	},
	iBabylonia : {
		iWriting: 30,
		iContract: 30,
		iCalendar: 30,
		iMasonry: 20,
		iProperty: 20,
		iDivination: 20,
		iConstruction: 20,
		iArithmetics: 20,
	
		iMathematics: -50,
		iLiterature: -50,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
	},
	iHarappa : {
		iMasonry: 30,
		iDivination: 10,
		
		iAlloys: -50,
		iMasonry: -30,
		iCalendar: -30,
		iTanning: -10,
	},
	iAssyria : {
		iMasonry: 40,
		iLeverage: 40,
		iAlloys: 30,
		iCeremony: 20,
		iWriting: 20,
		iArithmetics: 20,
		
		iRiding: -40,
		iSeafaring: -20,
	},
	iChina : {
		iAesthetics: 20,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		iLaw: 25,
		iMedicine: 25,
		iGeneralship: 15,
		iStatecraft: 15,
		iLabourUnions: 20,
		
		iMachineTools: -20,
		iReplaceableParts: -20,
		iBallistics: -30,
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,
		iCartography: -40,
		iEconomics: -20,
	},
	iChinaS : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		iStatecraft: 15,
		iLabourUnions: 15,
		iNationalism: 15,

		iMachineTools: -20,
		iReplaceableParts: -20,
		iBallistics: -30,
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,
		iCartography: -40,
		iEconomics: -20,
	},
	iShu : {
		iAesthetics: 20,
		iContract: 20,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		iStatecraft: 15,
		iLabourUnions: 15,
		iNationalism: 15,

		iMachineTools: -20,
		iReplaceableParts: -20,
		iBallistics: -30,
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,
		iCartography: -40,
		iEconomics: -20,
	},
	iXia : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		iStatecraft: 15,
		iLabourUnions: 15,
		iNationalism: 15,

		iMachineTools: -20,
		iReplaceableParts: -20,
		iBallistics: -30,
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,
		iCartography: -40,
		iEconomics: -20,
	},
	iTurks: {
		iMachineTools: -20,
		iReplaceableParts: -20,
		iBallistics: -30,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
	},
	iHittites: {
		iBloomery: 50,
		iContract: 20,
		iConstruction: 20,
	},
	iNubia: {
		iPriesthood: 20,
		iEthics: 20,
	},
	iGreece : {
		iPhilosophy: 50,
		iPriesthood: 40,
		iLiterature: 40,
		iMathematics: 40,
		iNavigation: 40,
		iBloomery: 40,
		iCalendar: 20,
		iWriting: 20,
		iShipbuilding: 20,
		iMedicine: 20,
		iAesthetics: 20,
		
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
		iArtisanry: -20,
	},
	iMinoans : {
		iArithmetics: 40,
		iLiterature: 20,
		iNavigation: 40,
		iWriting: 20,
		iShipbuilding: 20,
		
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
		iBloomery: -10,
	},
	iMacedon : {
		iGeneralship: 40,
		iCalendar: 20,
		iMedicine: 20,
		iAesthetics: 20,
		
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iPhoenicia : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iPersia : {
		iTheology: -40,
	},
	iParthia : {
		iTheology: -40,
	},
	iCelts : {
		iEthics: 20,
		iBloomery: 20,
	},
	iRome : {	
		iCurrency: 30,
		iLaw: 20,
		iPolitics: 20,
		iEngineering: 15,
		iArchitecture: 15,
		iAlchemy: 15,

		iFeudalism: -10,
		iSteel: -10,
		iTheology: -30,
	},
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iDravidia : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iToltecs : {
		iMathematics: 30,
		iWriting: 20,
		iCalendar: 20,
		iContract: 20,
	},
	iKushans : {
		iAesthetics: 20,
		iEngineering: 20,
		iArchitecture: 20,
		iMedicine: 20,
	},
	iKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iByzantium : {
		iNobility: 10,
		iAlchemy: 10,

		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iMali : {
		iScholarship: 40,
		iDoctrine: 30,
	},
	iNigeria : {
		iDoctrine: 10,
	},
	iFrance : {
		iReplaceableParts: 15,
		iExploration: 20,
		iLogistics: 15,
		iPatronage: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iFeudalism: 15,
		iChemistry: 15,
		iSociology: 15,
		iFission: 12,
	},
	iMalays : {
		iEcology: 40,
		iCompass: 30,
		iPolitics: 20,
		iArtisanry: 20,
	},
	iJapan : {
		iFeudalism: 40,
		iFortification: 40,
		iRobotics: 40,
	
		iOptics: -40,
		iExploration: -40,
		iFirearms: -30,
		iMachinery: -20,
		iGuilds: -20,
		iGeography: -20,
		iReplaceableParts: -20,
		iScientificMethod: -20,
	},
	iNorse : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
		iCompass: -30,
	},
	iMamluks : {
		iFinance: -50,
		iCompanies: -50,
		iCartography: -30,
		iExploration: -30,
	},
	iTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iKhazars : {
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
		iCompass: -30,
	},
	iJava : {
		iPolitics: 30,
		iGunpowder: 30,
		iCompass: 20,
		iCivilService: 20,
	
		iExploration: -20,
	},
	iMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
		iPrinting: -20,
	},
	iSpain : {
		iFeudalism: 100,
		iMachinery: 100,
		iCartography: 30,
		iExploration: 30,
		iCompass: 50,
		iFirearms: 15,
		iPatronage: 30,
		iGuilds: 15,
		iGunpowder: 15,
		iPrinting: 15,
		iEconomics: -10,
		iHeritage: 15,
	},
	iEngland : {
		iExploration: 20,
		iFirearms: 20,
		iReplaceableParts: 30,
		iLogistics: 15,
		iAcademia: 25,
		iCivilLiberties: 25,
		iEducation: 15,
		iGuilds: 15,
		iChemistry: 15,
		iPrinting: 15,
	},
	iHolyRome : {
		iPrinting: 40,
		iAcademia: 50,
		iFirearms: 20,
		iLogistics: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
		iEconomics: -10,
	},
	iBurma : {
		iLogistics: 20,
		iCombinedArms: 20,
	},
	iRus : {
		iCompass: 30,
		iCommune: 20,
	},
	iBulgaria : {
		iOptics: -5,
	},
	iGhorids : {
		iScholarship: 30,
		iAlchemy: 30,
		iHeritage: 20,
		iFinance: -50,
		iFirearms: -30,
		iCompanies: -50,
		iPaper: -20,
		iCompass: -30,
		iCartography: -30,
		iExploration: -30,
	},
	iVietnam : {
		iPrinting: 20,
		iHeritage: 20,
		iStatecraft: 20,
		iLabourUnions: 20,
	},
	iSwahili : {
		iCompass: 30,
		iFortification: 20,
		
		iCartography: -40,
	},
	iPoland : {
		iGeography: -15,
		iCombinedArms: 45,
		iCivilLiberties: 15,
		iSocialContract: 15,
	},
	iPortugal : {
		iCartography: 100,
		iExploration: 100,
		iCompass: 100,
		iFirearms: 25,
		iCompanies: 30,
		iPatronage: 30,
		iAssemblyLine: -5,
	},
	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,
	},
	iItaly : {
		iRadio: 20,
		iPsychology: 20,
		iFinance: 25,
		iOptics: 25,
		iPatronage: 30,
		iHumanities: 3^0,
		iAcademia: 25,
		iFission: 12,
	},
	iTimurids : {
		iHumanities: 20,
		iPhilosophy: 15,
		iEducation: 15,
		iPaper: 15,
		iPatronage: 15,
		iEngineering: 15,
	
		iReplaceableParts: -15,
		iCombinedArms: -15,
		iScientificMethod: -30,
		iExploration: -30,
	},
	iMongols : {
		iGunpowder: 40,
		iLogistics: 30,
		iStatecraft: 20,
		iPrinting: 20,
		
		iExploration: -100,
		iOptics: -100,
		iFirearms: -20,
		iCombinedArms: -20,
	},
	iAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iSweden : {
		iCombinedArms: 25,
		iFirearms: 25,
		iLogistics: 25,
		iRefining: 30,
		iCivilLiberties: 20,
		iBiology: 20,
		iAcademia: 20,
	},
	iRussia : {
		iMacroeconomics: 30,
		iCombinedArms: 20,
		iReplaceableParts: 15,
		iHeritage: 20,
		iPatronage: 15,
		iUrbanPlanning: 20,
		iFission: 12,
		
		iPhilosophy: -20,
		iPrinting: -20,
		iCivilLiberties: -20,
		iSocialContract: -20,
		iRepresentation: -20,
	},
	iOttomans : {
		iGunpowder: 25,
		iFirearms: 30,
		iCombinedArms: 20,
		iJudiciary: 20,
	},
	iThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iNetherlands : {
		iAcademia: 30,
		iExploration: 50,
		iFirearms: 20,
		iOptics: 50,
		iGeography: 25,
		iHydraulics: 20,
		iReplaceableParts: 30,
		iLogistics: 25,
		iEconomics: 30,
		iCivilLiberties: 30,
		iHumanities: 30,
		iChemistry: 15,
	},
	iGermany : {
		iEngine: 20,
		iBallistics: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iEgypt: -15,
	iBabylonia: -40,
	iGreece: -15,
	iMacedon: -15,
	iIndia: -15,
	iRome: -20,
	iArabia: -15,
	iMamluks: -15,
	iJava: -15,
	iFrance: -12,
	iKhmer: -15,
	iEngland: -12,
	iRussia: -12,
	iThailand: -15,
	iCongo: -20,
	iNetherlands: -12,
	iAmerica: -12,
}

dBuildingPreferences = {
	iEgypt : {
		iPyramids: 100,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,

		iPalaceOfMinos: -30,
		iOracle: -20,
	},
	iBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: 0,
		iGreatSphinx: 0,
		
		iOracle: -60,
		iPalaceOfMinos: -30,
	},
	iHarappa : {
		iPyramids: 0,
		iGreatSphinx: 0,

		iPalaceOfMinos: -30,
		iOracle: -40,
	},
	iAssyria : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,

		iPyramids: 0,
		iGreatSphinx: 0,

		iPalaceOfMinos: -30,
		iOracle: -30,
	},
	iChina : {
		iGreatWall: 80,
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 30,
		iTerracottaArmy: 30,
		iPorcelainTower: 30,
		
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iChinaS : {
		iForbiddenPalace: 20,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 50,
		iTerracottaArmy: 30,
		iPorcelainTower: 50,
		iGreatWall: -30,
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iShu : {
		iForbiddenPalace: 20,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 50,
		iTerracottaArmy: 30,
		iPorcelainTower: 50,
		iGreatWall: -30,
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iXia : {
		iForbiddenPalace: 20,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 50,
		iTerracottaArmy: 30,
		iPorcelainTower: 50,
		iGreatWall: -30,
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iVietnam: {
		iGreatWall: -30,	
	},
	iNubia: {
		iPalaceOfMinos: -20,
		iOracle: -20,
		iHangingGardens: -20,
		iIshtarGate: -20,
	},
	iMinoans: {
		iPalaceOfMinos: 50,

		iOracle: -20,
		iGreatCothon: -50,
	},
	iGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,

		iPyramids: -100,
		iGreatCothon: -100,
	},

	iMacedon : {
		iColossus: 15,
		iTempleOfArtemis: 15,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		
		iPyramids: -100,
		iGreatCothon: -100,
	},
	iIndia : {
		iKhajuraho: 30,
		iIronPillar: 30,
		iVijayaStambha: 30,
		iNalanda: 30,
		iLotusTemple: 30,
		iTajMahal: 20,
		iWatPreahPisnulok: 20,
		iShwedagonPaya: 20,
		iHarmandirSahib: 20,
		iJetavanaramaya: 20,
		iSalsalBuddha: 20,
		iPotalaPalace: 20,
		iBorobudur: 15,
		iPrambanan: 15,
		
		iParthenon: -30,
		iStatueOfZeus: -20,
	},
	iPhoenicia : {
		iGreatCothon: 30,
		iGreatLighthouse: 15,
		iColossus: 15,
		
		iPyramids: -50,
	},
	iPolynesia : {
		iMoaiStatues: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iRome : {
		iSaintPeters: 40,
		iFlavianAmphitheatre: 30,
		iAquaAppia: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iMaya : {
		iTempleOfKukulkan: 40,
	},
	iDravidia : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iEthiopia : {
		iMonolithicChurch: 40,
	},
	iToltecs : {
		iPyramidOfTheSun: 30,
	},
	iKushans : {
		iSalsalBuddha: 30,
		iNalanda: 20,
		iKhajuraho: 20,
	},
	iKorea : {
		iCheomseongdae: 30,
		
		iShwedagonPaya: 0,
		iPrambanan: 0,
		iBorobudur: 0,
	},
	iKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iMali : {
		iUniversityOfSankore: 40,
		iGreatAdobeMosque: 40,
	},
	iByzantium : {
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		
		iNotreDame: -20,
		iSistineChapel: -20,
		iSaintSophia: -50,
	},
	iFrance : {
		iTradingCompanyBuilding: 40,
		iNotreDame: 40,
		iEiffelTower: 30,
		iVersailles: 30,
		iLouvre: 30,
		iTriumphalArch: 30,
		iMetropolitain: 30,
		iCERN: 30,
		iKrakDesChevaliers: 30,
		iChannelTunnel: 30,
		iPalaceOfNations: 20,
		iBerlaymont: 20,
		iLargeHadronCollider: 20,
		iITER: 20,
		iSaintPeters: 20,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iMalays : {
		iGardensByTheBay: 40,
		iPrambanan: 20,
		iBorobudur: 20,
	},
	iJapan : {
		iItsukushimaShrine: 50,
		iHimejiCastle: 50,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iBorobudur: 0,
		iPrambanan: 0,
		iShwedagonPaya: 0,
		iGreatWall: -100,
	},
	iTurks : {
		iGurEAmir: 20,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
		
		iShwedagonPaya: -30,
	},
	iNorse : {
		iNobelPrize: 20,
		iGlobalSeedVault: 30,
		iCERN: 15,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iArabia: {
		iSpiralMinaret: 40,
		iDomeOfTheRock: 40,
		iHouseOfWisdom: 40,
		iBurjKhalifa: 40,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
	},
	iMamluks: {
		iBurjKhalifa: 40,
		iAlamut: 30,
	},
	iTibet : {
		iPotalaPalace: 40,
		iLouvre: -10,
	},
	iMoors : {
		iMezquita: 100,
		
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
	},
	iJava : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 30,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iSpain : {
		iEscorial: 30,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iSagradaFamilia: 30,
		iSaintPeters: 20,
		iCristoRedentor: 20,
		iWembley: 20,
		iIberianTradingCompanyBuilding: 20,
		iTorreDeBelem: 15,
		iNotreDame: 15,
		iMezquita: 15,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iOxfordUniversity: 30,
		iWembley: 30,
		iWestminsterPalace: 30,
		iTrafalgarSquare: 30,
		iBellRockLighthouse: 30,
		iCrystalPalace: 30,
		iChannelTunnel: 30,
		iBletchleyPark: 20,
		iAbbeyMills: 20,
		iMetropolitain: 20,
		iNationalGallery: 20,
		iKrakDesChevaliers: 20,
		iHarbourOpera: 20,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iHolyRome : {
		iSaintThomasChurch: 30,
		iSaintPeters: 20,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iBurma : {
		iShwedagonPaya: 50,
		iWatPreahPisnulok: 20,
		iEmeraldBuddha: 20,
	},
	iRus : {
		iSaintSophia: 40,
		iSaintBasilsCathedral: 20,
		iKremlin: 20,
	},
	iPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iPortugal : {
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
		iMountAthos: -20,
		iHagiaSophia: -20,
	},
	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iItaly : {
		iSaintPeters: 40,
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
		iMountAthos: -20,
	},
	iMongols : {
		iSilverTreeFountain: 40,
	},
	iRussia : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
	},
	iOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iTimurids : {
		iGurEAmir: 40,
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iGhorids: {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iSweden : {
		iNobelPrize: 30,
		iGlobalSeedVault: 20,
	},
	iIran: {
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
		iBourse: 40,
		iDeltaWorks: 40,
		iAtomium: 30,
		iBerlaymont: 30,
		iNationalGallery: 20,
		iWembley: 20,
		iCERN: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
		iMetropolitain: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	}
}