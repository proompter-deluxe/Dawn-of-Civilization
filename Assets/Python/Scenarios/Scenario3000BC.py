from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iMasonry, iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iBabylonia,
		techs=techs.of(iPottery, iPastoralism, iAgriculture, iMythology, iProperty)
	),
	Civilization(
		iHarappa,
		techs=techs.of(iMining, iPottery, iAgriculture, iPastoralism, iTanning)
	),
	Civilization(
		iNative,
		techs=techs.of(iTanning, iMythology)
	),
	Civilization(
		iIndependent2
	),
	Civilization(
		iIndependent
	),
]

lTribalVillages = [
	((121, 42), (129, 48)), # South China
	((71, 56), (78, 61)), # Balkans
	((80, 51), (87, 55)), # Anatolia
]


def createStartingUnits():
	makeUnit(iBabylonia, iWorker, plots.capital(iBabylonia))

	if not player(iBabylonia).isHuman():
		makeUnit(iBabylonia, iSettler, plots.capital(iBabylonia))
		makeUnit(iBabylonia, iMilitia, plots.capital(iBabylonia))

scenario3000BC = Scenario(
	iStartYear = -3000,
	fileName = "RFC_3000BC",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	createStartingUnits = createStartingUnits,
)
