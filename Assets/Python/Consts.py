# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
from DataStructures import *
from CoreTypes import *

gc = CyGlobalContext()

iWorldX = 150
iWorldY = 80

iNumPlayers = gc.getMAX_PLAYERS()

# civilizations, not players
# also increment iNUmCivs in DrawMaps.py (and add the civ identifier in the list as well)
# also increment NUM_CIVS in CvRhyes.h
iNumCivs = 76
(iAmerica, iArabia, iArgentina, iArmenia, iAssyria, iAztecs, iBabylonia, iBrazil, iBulgaria, iBurma, iByzantium, iCanada, 
iPhoenicia, iCelts, iChina, iChinaS, iColombia, iDravidia, iEgypt, iEngland, iEthiopia, iFrance, iGermany, iGhorids,
iGreece, iHarappa, iHittites, iHolyRome, iInca, iIndia, iIran, iIroquois, iItaly, iJapan, iJava, iKhazars,
iKhmer, iCongo, iKorea, iKushans, iMacedon, iMalays, iMali, iMamluks, iMaya, iMexico, iMinoans, iMongols, iMoors, 
iNetherlands, iNorse, iNubia, iOttomans, iParthia, iPersia, iPoland, iPolynesia, iPortugal, 
iRome, iRus, iRussia, iSpain, iSwahili, iSweden, iThailand, iTibet, iTimurids, iToltecs, 
iTurks, iVietnam, iZulu, iIndependent, iIndependent2, iNative, iMinor, iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

lBirthOrder = [
	iEgypt,
	iBabylonia,
	iHarappa,
	iMinoans,
	iChina,
	iHittites,
	iNubia,
	iAssyria,
	iPhoenicia,
	iPolynesia,
	iGreece,
	iPersia,
	iIndia,
	iCelts,
	iMacedon,
	iMaya,
	iRome,
	iArmenia,
	iDravidia,
	iEthiopia,
	iParthia,
	iToltecs,
	iKushans,
	iKorea,
	iKhmer,
	iChinaS,
	iMali,
	iByzantium,
	iFrance,
	iMalays,
	iJapan,
	iSpain,
	iNorse,
	iTurks,
	iArabia,
	iTibet,
	iKhazars,
	iBulgaria,
	iJava,
	iMoors,
	iEngland,
	iHolyRome,
	iBurma,
	iRus,
	iMamluks,
	iVietnam,
	iSwahili,
	iGhorids,
	iPoland,
	iPortugal,
	iInca,
	iItaly,
	iMongols,
	iAztecs,
	iThailand,
	iSweden,
	iRussia,
	iOttomans,
	iTimurids,
	iCongo,
	iIroquois,
	iIran,
	iNetherlands,
	iGermany,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada
]

lCivOrder = lBirthOrder + [
	iIndependent,
	iIndependent2,
	iNative,
	iBarbarian
]

# used in: Congresses, DynamicCivs, Plague, RFCUtils, UniquePowers, Victory
# a civilisation can be in multiple civ groups
iNumCivGroups = 6
(iCivGroupEurope, iCivGroupAsia, iCivGroupMiddleEast, iCivGroupMediterranean, iCivGroupAfrica, iCivGroupAmerica) = range(iNumCivGroups)

dCivGroups = {
iCivGroupEurope : [iGreece, iRome, iCelts, iByzantium, iFrance, iNorse, iSpain, iEngland, iHolyRome, iRus, iItaly, iPoland, iPortugal, iSweden, iRussia, iNetherlands, iGermany, iBulgaria, iMacedon, iArmenia],
iCivGroupAsia : [iIndia, iChina, iChinaS, iHarappa, iPolynesia, iPersia, iJapan, iDravidia, iKushans, iKorea, iKhmer, iMalays, iJava, iTibet, iBurma, iVietnam, iMongols, iTimurids, iThailand, iRussia, iTurks, iGhorids, iKhazars],
iCivGroupMiddleEast : [iEgypt, iBabylonia, iAssyria, iHittites, iPersia, iKushans, iByzantium, iArabia, iMoors, iSwahili, iOttomans, iPhoenicia, iTurks, iIran, iMamluks, iParthia],
iCivGroupMediterranean : [iEgypt, iGreece, iPhoenicia, iRome, iByzantium, iFrance, iArabia, iMoors, iSpain, iPortugal, iItaly, iOttomans, iMamluks, iMacedon, iMinoans],
iCivGroupAfrica : [iEgypt, iNubia, iPhoenicia, iEthiopia, iMali, iMoors, iSwahili, iCongo, iMamluks],
iCivGroupAmerica : [iMaya, iToltecs, iInca, iAztecs, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iIroquois],
}

# used in: Stability
# tech groups share techs within each other on respawn
iNumTechGroups = 4
(iTechGroupWestern, iTechGroupMiddleEast, iTechGroupFarEast, iTechGroupNativeAmerica) = range(iNumTechGroups)

dTechGroups = {
iTechGroupWestern : [iRome, iGreece, iCelts, iByzantium, iFrance, iNorse, iSpain, iEngland, iHolyRome, iRus, iPoland, iPortugal, iItaly, iSweden, iRussia, iNetherlands, iGermany, iAmerica, iArgentina, iMexico, iColombia, iBrazil, iCanada, iBulgaria, iMacedon],
iTechGroupMiddleEast : [iEgypt, iBabylonia, iHarappa, iAssyria, iHittites, iNubia, iIndia, iPhoenicia, iPersia, iEthiopia, iKushans, iMali, iArabia, iMoors, iSwahili, iOttomans, iTimurids, iDravidia, iCongo, iTurks, iIran, iMamluks, iArmenia, iParthia, iMinoans, iGhorids],
iTechGroupFarEast : [iChina, iChinaS, iKorea, iKhmer, iMalays, iJapan, iJava, iTibet, iBurma, iVietnam, iMongols, iThailand, iKhazars],
iTechGroupNativeAmerica : [iPolynesia, iMaya, iToltecs, iInca, iAztecs, iIroquois],
}

lBioNewWorld = [iMaya, iToltecs, iInca, iAztecs, iIroquois]

#for messages
iDuration = 14
iWhite = 0
iRed = 7
iGreen = 8
iBlue = 9
iLightBlue = 10
iYellow = 11
iDarkPink = 12
iLightRed = 20
iPurple = 25
iCyan = 44
iBrown = 55
iOrange = 88
iTan = 90
iLime = 100

lNeighbours = [
	(iEgypt, iBabylonia),
    (iEgypt, iMinoans),
	(iEgypt, iAssyria),
	(iEgypt, iHittites),
	(iEgypt, iNubia),
	(iEgypt, iGreece),
	(iEgypt, iPersia),
	(iEgypt, iPhoenicia),
	(iEgypt, iRome),
	(iEgypt, iEthiopia),
	(iEgypt, iByzantium),
	(iEgypt, iArabia),
	(iEgypt, iMoors),
	(iEgypt, iOttomans),
	(iBabylonia, iAssyria),
	(iBabylonia, iHittites),
	(iBabylonia, iGreece),
	(iBabylonia, iPersia),
	(iBabylonia, iTurks),
	(iBabylonia, iArabia),
	(iBabylonia, iOttomans),
	(iBabylonia, iMongols),
	(iBabylonia, iPhoenicia),
	(iBabylonia, iByzantium),
	(iBabylonia, iIran),
	(iHarappa, iIndia),
	(iHarappa, iPersia),
	(iHarappa, iDravidia),
	(iHarappa, iKushans),
	(iHarappa, iTibet),
	(iHarappa, iTimurids),
	(iHarappa, iIran),
	(iAssyria, iHittites),
	(iAssyria, iPhoenicia),
	(iAssyria, iGreece),
	(iAssyria, iPersia),
	(iAssyria, iByzantium),
	(iAssyria, iTurks),
	(iAssyria, iArabia),
	(iAssyria, iOttomans),
	(iAssyria, iIran),
	(iChina, iVietnam),
	(iChina, iKushans),
	(iChina, iJapan),
	(iChina, iKorea),
	(iChina, iTurks),
	(iChina, iTibet),
	(iChina, iMongols),
	(iChinaS, iVietnam),
	(iChinaS, iJapan),
	(iChinaS, iKorea),
	(iChinaS, iTibet),
	(iChinaS, iBurma),
	(iChinaS, iMongols),
	(iHittites, iGreece),
	(iHittites, iPhoenicia),
	(iHittites, iPersia),
	(iHittites, iCelts),
	(iHittites, iByzantium),
	(iHittites, iArabia),
	(iHittites, iOttomans),
	(iHittites, iIran),
	(iGreece, iPersia),
	(iPhoenicia, iGreece),
	(iGreece, iRome),
	(iGreece, iCelts),
	(iGreece, iByzantium),
	(iGreece, iOttomans),
	(iGreece, iItaly),
	(iPersia, iIndia),
	(iIndia, iDravidia),
	(iIndia, iKushans),
	(iIndia, iMalays),
	(iIndia, iTibet),
	(iIndia, iJava),
	(iIndia, iKhmer),
	(iIndia, iBurma),
	(iIndia, iTimurids),
	(iIndia, iIran),
	(iPhoenicia, iRome),
	(iPhoenicia, iSpain),
	(iPhoenicia, iMali),
	(iPhoenicia, iPersia),
	(iPhoenicia, iArabia),
	(iPhoenicia, iMoors),
	(iPhoenicia, iOttomans),
	(iPhoenicia, iItaly),
	(iNubia, iEthiopia),
	(iNubia, iArabia),
	(iPersia, iRome),
	(iPersia, iKushans),
	(iPersia, iTurks),
	(iPersia, iByzantium),
	(iPersia, iOttomans),
	(iPersia, iMongols),
	(iPersia, iTimurids),
	(iPersia, iRussia),
	(iPersia, iIran),
	(iCelts, iRome),
	(iCelts, iNorse),
	(iCelts, iSpain),
	(iCelts, iFrance),
	(iCelts, iEngland),
	(iCelts, iHolyRome),
	(iCelts, iGermany),
	(iRome, iSpain),
	(iRome, iByzantium),
	(iRome, iFrance),
	(iRome, iHolyRome),
	(iRome, iItaly),
	(iRome, iGermany),
	(iRome, iMoors),
	(iDravidia, iKushans),
	(iDravidia, iMalays),
	(iDravidia, iJava),
	(iDravidia, iKhmer),
	(iDravidia, iBurma),
	(iDravidia, iTimurids),
	(iEthiopia, iArabia),
	(iEthiopia, iSwahili),
	(iToltecs, iAztecs),
	(iToltecs, iAmerica),
	(iToltecs, iMexico),
	(iToltecs, iColombia),
	(iKushans, iTurks),
	(iKushans, iMongols),
	(iKushans, iTimurids),
	(iKushans, iIran),
	(iKorea, iMongols),
	(iKorea, iJapan),
	(iKhmer, iMalays),
	(iKhmer, iJava),
	(iKhmer, iBurma),
	(iKhmer, iVietnam),
	(iKhmer, iThailand),
	(iMali, iMoors),
	(iMali, iCongo),
	(iMaya, iToltecs),
	(iMaya, iAztecs),
	(iMaya, iMexico),
	(iMaya, iColombia),
	(iByzantium, iTurks),
	(iByzantium, iArabia),
	(iByzantium, iRus),
	(iByzantium, iMongols),
	(iByzantium, iRussia),
	(iByzantium, iOttomans),
	(iByzantium, iIran),
	(iFrance, iNorse),
	(iFrance, iEngland),
	(iFrance, iHolyRome),
	(iFrance, iNetherlands),
	(iFrance, iItaly),
	(iFrance, iGermany),
	(iMalays, iJava),
	(iMalays, iVietnam),
	(iMalays, iThailand),
	(iJapan, iMongols),
	(iNorse, iEngland),
	(iNorse, iHolyRome),
	(iNorse, iRus),
	(iNorse, iPoland),
	(iNorse, iSweden),
	(iNorse, iRussia),
	(iNorse, iNetherlands),
	(iNorse, iGermany),
	(iBulgaria, iRus),
	(iBulgaria, iByzantium),
	(iBulgaria, iHolyRome),
	(iBulgaria, iItaly),
	(iBulgaria, iPoland),
	(iTurks, iTibet),
	(iTurks, iArabia),
	(iTurks, iRus),
	(iTurks, iMongols),
	(iTurks, iTimurids),
	(iTurks, iOttomans),
	(iTurks, iIran),
	(iArabia, iMoors),
	(iArabia, iSwahili),
	(iArabia, iMongols),
	(iArabia, iOttomans),
	(iArabia, iIran),
	(iTibet, iBurma),
	(iTibet, iMongols),
	(iTibet, iTimurids),
	(iMoors, iSpain),
	(iMoors, iPortugal),
	(iJava, iThailand),
	(iSpain, iFrance),
	(iSpain, iPortugal),
	(iSpain, iItaly),
	(iEngland, iNetherlands),
	(iHolyRome, iItaly),
	(iHolyRome, iPoland),
	(iHolyRome, iSweden),
	(iHolyRome, iNetherlands),
	(iHolyRome, iGermany),
	(iRus, iPoland),
	(iRus, iMongols),
	(iRus, iSweden),
	(iRus, iRussia),
	(iRus, iOttomans),
	(iVietnam, iBurma),
	(iVietnam, iThailand),
	(iBurma, iThailand),
	(iPoland, iSweden),
	(iPoland, iRussia),
	(iPoland, iGermany),
	(iInca, iArgentina),
	(iInca, iColombia),
	(iInca, iBrazil),
	(iMongols, iRussia),
	(iMongols, iOttomans),
	(iMongols, iIran),
	(iAztecs, iAmerica),
	(iAztecs, iMexico),
	(iAztecs, iColombia),
	(iTimurids, iIran),
	(iSweden, iRussia),
	(iSweden, iGermany),
	(iRussia, iOttomans),
	(iRussia, iGermany),
	(iOttomans, iIran),
	(iAmerica, iMexico),
	(iAmerica, iCanada),
	(iArgentina, iBrazil),
	(iMexico, iColombia),
	(iArabia, iMamluks),
	(iMamluks, iOttomans),
	(iTurks, iMamluks),
	(iPersia, iMamluks),
	(iMamluks, iMongols),
	(iGreece, iMacedon),
	(iHittites, iMacedon),
	(iPersia, iMacedon),
	(iMacedon, iRome),
	(iIroquois, iAmerica),
	(iIroquois, iCanada),
	(iPersia, iArmenia),
	(iMacedon, iArmenia),
	(iArmenia, iIran),
	(iArmenia, iTurks),
	(iArmenia, iOttomans),
    (iMinoans, iGreece),
    (iPersia, iParthia),
    (iParthia, iKushans),
    (iGhorids, iTurks),
    (iGhorids, iTimurids),
    (iGhorids, iIndia),
    (iGhorids, iKushans),
	(iGhorids, iArabia),
    (iKhazars, iRus),
	(iKhazars, iRussia),
	(iKhazars, iArmenia),
    (iKhazars, iTurks),
]

lInfluences = [
	(iEgypt, iEngland),
	(iBabylonia, iRome),
	(iBabylonia, iArabia),
	(iIndia, iEngland),
    (iPhoenicia, iRome),
	(iPhoenicia, iCelts),
	(iPhoenicia, iByzantium),
	(iPhoenicia, iTurks),
	(iPhoenicia, iIran),
	(iPersia, iArabia),
	(iPersia, iSwahili),
	(iRome, iOttomans),
	(iMaya, iSpain),
	(iDravidia, iEngland),
	(iDravidia, iSwahili),
	(iDravidia, iNetherlands),
	(iVietnam, iJapan),
	(iVietnam, iFrance),
	(iVietnam, iAmerica),
	(iKhmer, iJapan),
	(iMalays, iJapan),
	(iMalays, iPortugal),
	(iMalays, iNetherlands),
	(iJava, iJapan),
	(iJava, iNetherlands),
	(iArabia, iBabylonia),
	(iArabia, iGreece),
	(iArabia, iPersia),
	(iSpain, iArabia),
	(iSpain, iOttomans),
	(iEngland, iBurma),
	(iHolyRome, iOttomans),
	(iInca, iSpain),
	(iItaly, iOttomans),
	(iAztecs, iSpain),
	(iTimurids, iEngland),
	(iOttomans, iRome),
	(iThailand, iJapan),
	(iCongo, iPortugal),
	(iNetherlands, iSpain),
	(iAmerica, iEngland),
	(iAmerica, iFrance),
	(iAmerica, iNetherlands),
	(iArgentina, iSpain),
	(iMexico, iSpain),
	(iMexico, iFrance),
	(iColombia, iSpain),
	(iBrazil, iPortugal),
	(iBrazil, iCongo),
	(iCanada, iFrance),
	(iCanada, iEngland),
	(iMamluks, iItaly),
	(iIroquois, iEngland),
	(iIroquois, iFrance),
	(iIroquois, iNetherlands),
	(iIroquois, iNorse),
    (iParthia, iMacedon),
    (iHittites, iMinoans),
	(iGhorids, iByzantium),
	(iKhazars, iMongols),
    (iKhazars, iParthia),
    (iKhazars, iKushans),
]

dBirth = CivDict({
iEgypt : -3000,
iBabylonia : -3000,
iHarappa : -3000,
iMinoans : -3000,
iChina : -2070,
iHittites : -1800,
iNubia : -1650,
iAssyria : -1450,
iPhoenicia : -1100,
iPolynesia : -1000,
iGreece : -900,
iPersia : -660,
iIndia : -650,
iCelts : -600,
iMacedon: -475,
iMaya : -400,
iRome : -338,
iArmenia: -320,
iDravidia : -300,
iEthiopia : -290,
iParthia : -240,
iToltecs : -200,
iKushans : -135,
iKorea : -50,
iKhmer : 50,
iChinaS: 200,
iMali : 300,
iByzantium : 330,
iFrance : 496,
iMalays : 500,
iJapan : 525,
iSpain : 526,
iNorse : 551,
iTurks : 552,
iArabia : 634,
iTibet : 630,
iKhazars: 640,
iBulgaria: 670,
iJava : 716,
iMoors : 720,
iEngland : 820,
iHolyRome : 840,
iBurma : 849,
iRus : 880,
iMamluks: 909, # Fatimids in Tunisia
iVietnam : 938,
iSwahili : 957,
iGhorids: 977,
iPoland : 1025,
iPortugal : 1130,
iInca : 1150,
iItaly : 1167,
iMongols : 1190,
iAztecs : 1195,
iThailand : 1238,
iSweden : 1252,
iRussia : 1263,
iOttomans : 1280,
iTimurids : 1370,
iCongo : 1390,
iIroquois: 1450,
iIran : 1505,
iNetherlands : 1580,
iGermany : 1700,
iAmerica : 1776,
iArgentina : 1810,
iMexico : 1810,
iColombia : 1814,
iBrazil : 1822,
iCanada : 1867,
}, -3000)

lBirthCivs = dBirth.keys()

dFall = CivDict({
iEgypt : -1150, # Egypt never regained its relevance after the Bronze Age Collapse
iBabylonia : -1155, # Neo-Babylonia was a short lived affair, it can exist if Babylonia respawns, but it shouldn't be super stable
iHarappa : -1700,
iAssyria : -631, # end of Ashurbanipal's reign
iHittites : -1180,
iPhoenicia: -150,
iNubia : -150,
iChina: 1170,
iChinaS: 580,
iIndia : 1150,
iPolynesia : 1200,
iPersia : -300,
iCelts : 1169,
iRome : 550,
iGreece: -50,
iMacedon: -50,
iMaya : 900,
iDravidia : 1770,
iEthiopia : 960,
iToltecs : 950,
iKushans : 375,
iMalays : 1511,
iKorea : 1255,
iKhmer : 1200,
iMali : 1600,
iByzantium : 1200,
iTurks : 1150,
iArabia : 1000,
iBulgaria: 1250,
iKhazars: 970,
iTibet : 1500,
iMoors : 1150,
iJava: 1645, # the decline of Sultanate of Mataram started then, even if the end was in 1755
iBurma : 1885,
iRus : 1300,
iSwahili : 1513,
iPoland : 1650,
iInca : 1533,
iMamluks: 1382, # the "Circassian" period is often considered a decline
iMongols : 1368,
iAztecs : 1600, # decline after the historical conquest, because we want to give the AI time to discover and conquer the Aztecs
iTimurids : 1640,
iCongo : 1800,
iIroquois : 1770,
iArmenia : 1050,
iMinoans: -1130,
iParthia: 650,
iGhorids: 1400,
}, 2020)

# Leoreth: determine neighbour lists from pairwise neighbours for easier lookup
dNeighbours = dictFromEdges(lBirthCivs, lNeighbours)

# Leoreth: determine influence lists from pairwise influences for easier lookup
dInfluences = dictFromEdges(lBirthCivs, lInfluences)

dResurrections = CivDict({
iEgypt : [(-3000, -100)], # can revive as Ptolemaic dynasty
iBabylonia : [(-3000, -1450), (-700, -630)],
iAssyria : [(-1450, -650), (910, 1200)],
iChina : [(580, 1127), (1600, 2020)],
iChinaS : [(910, 1550), (1850, 1920)],
iHittites : [(-840, -670)],
iNubia : [(500, 1500)],
iGreece : [(-900, -500), (1800, 2020)],
iIndia : [(330, 480), (1600, 1800), (1940, 2020)],
iPhoenicia : [(-800,-300), (1000, 1500), (1950, 2020)],
iPersia : [(910, 1000)],
iCelts : [(400, 1150), (1850, 2020)],
iRome : [(-338, 450)],
iMaya : [(0, 800)],
iDravidia : [(300, 1650)],
iEthiopia : [(1270, 1520), (1750, 1880), (1940, 2020)],
iKorea : [(1800, 2020)],
iKhmer : [(1950, 2020)],
iMali : [(1340, 1590)],
iByzantium : [(1100, 1280)],
iFrance : [(1700, 2020)],
iMalays : [(500, 1500), (1940, 2020)],
iJapan : [(1800, 2020)],
iNorse : [(1520, 2020)],
iTurks : [(870, 980), (1505, 1700), (1980, 2020)],
iArabia : [(1900, 2020)],
iBulgaria: [(1200, 1400), (1848,2020)],
iKhazars: [(1300, 1550)],
iMoors : [(1220, 1750), (1940, 2020)], # Marinids / Ziyanids
iJava : [(720, 1650), (1940, 2020)],
iSpain : [(1150, 1300), (1700, 2020)],
iEngland : [(1700, 2020)],
iHolyRome : [(1800, 2020)],
iBurma : [(850, 1885), (1950, 2020)],
iRus : [(1970, 2020)],
iVietnam : [(950, 2020)],
iSwahili : [(1960, 2020)],
iPoland : [(1920, 2020)],
iPortugal : [(1700, 2020)],
iInca : [(1800, 1930)],
iItaly : [(1820, 2020)],
iMongols : [(1350, 1650), (1910, 2020)],
iTimurids : [(1526, 1630), (1940, 2020)],
iThailand : [(1700, 2020)],
iSweden : [(1250, 2020)],
iRussia : [(1280, 1550), (1700, 2020)],
iOttomans : [(1505, 2020)],
iIran : [(1505, 2020)],
iNetherlands : [(1700, 2020)],
iGermany : [(1840, 2020)],
iAmerica : [(1776, 2020)],
iArgentina : [(1810, 2020)],
iMexico : [(1810, 2020)],
iColombia : [(1810, 2020)],
iBrazil : [(1820, 2020)],
iCanada : [(1867, 2020)],
iMamluks : [(920, 1250), (1800, 2020)],
iMacedon : [(-400, -150)],
iArmenia : [(50, 1050), (1870, 2020)],
iMinoans : [(-3000, -1300)],
iParthia : [(200, 550)],
iGhorids : [(1220, 1400)]
}, [])

dAggressionLevel = CivDict({
iBabylonia : 1,
iChina : 2,
iChinaS : 2,
iHittites : 3,
iNubia : 1,
iGreece : 1,
iAssyria : 3,
iPersia : 3,
iCelts : 1,
iRome : 3,
iMaya : 1,
iDravidia : 1,
iToltecs: 1,
iKushans : 1,
iKhmer : 2,
iByzantium : 1,
iFrance : 1,
iJapan : 1,
iNorse : 2,
iTurks : 2,
iArabia : 2,
iTibet : 1,
iBulgaria: 2,
iKhazars: 2,
iMoors : 1,
iJava : 1,
iSpain : 2,
iEngland : 1,
iHolyRome : 1,
iBurma : 2,
iVietnam : 1,
iPoland : 1,
iInca : 1,
iMongols : 3,
iAztecs : 2,
iTimurids : 1,
iSweden : 1,
iRussia : 1,
iOttomans : 2,
iIran : 1,
iGermany : 2,
iAmerica : 2,
iColombia : 2,
iMexico : 1,
iArgentina : 1,
iMamluks: 2,
iMacedon: 3,
iIroquois: 2,
iArmenia: 1,
iParthia: 2,
iMinoans: 1,
iGhorids: 2,
}, 0)

dWarOnFlipProbability = CivDict({
iEgypt: 20,
iBabylonia: 50,
iHarappa: 50,
iAssyria: 50,
iChina: 40,
iChinaS: 70,
iHittites: 50,
iNubia: 20,
iGreece: 50,
iIndia: 20,
iPhoenicia: 20,
iPolynesia: 20,
iPersia: 70,
iCelts: 20,
iRome: 20,
iMaya: 20,
iDravidia: 20,
iEthiopia: 20,
iToltecs: 20,
iKushans: 30,
iMalays: 30,
iKorea: 20,
iKhmer: 20,
iMali: 30,
iByzantium: 20,
iFrance: 20,
iJapan: 20,
iNorse: 20,
iTurks: 50,
iArabia: 20,
iTibet: 20,
iBulgaria: 20,
iKhazars: 20,
iJava: 20,
iMoors: 20,
iSpain: 20,
iEngland: 50,
iHolyRome: 20,
iBurma: 40,
iRus: 20,
iVietnam: 20,
iSwahili: 20,
iPoland: 60,
iPortugal: 60,
iInca: 30,
iItaly: 40,
iMongols: 30,
iAztecs: 50,
iTimurids: 50,
iThailand: 20,
iSweden : 30,
iRussia: 50,
iOttomans: 30,
iCongo: 20,
iIran: 20,
iNetherlands: 60,
iGermany: 20,
iAmerica: 50,
iArgentina: 40,
iMexico: 40,
iColombia: 40,
iBrazil: 40,
iCanada: 40,
iMamluks: 50,
iMacedon: 50,
iIroquois: 20,
iArmenia: 50,
iMinoans: 30,
iParthia: 60,
iGhorids: 50,
}, 0)

# the probability out of 100 (and other factors like "Nationalism")
# that once every 10 turns, the civ is cleared for respawn
dResurrectionProbability = CivDict({
iEgypt : 75,
iBabylonia : 40,
iHarappa : 0,
iAssyria : 85,
iChina : 100,
iChinaS : 50,
iHittites : 40,
iNubia : 20,
iGreece : 75,
iIndia : 50,
iPhoenicia : 85,
iPolynesia : 40,
iPersia : 70,
iCelts : 50,
iRome : 65,
iMaya : 30,
iDravidia : 10,
iEthiopia : 80,
iMalays : 60,
iKorea : 80,
iKhmer : 60,
iMali : 30,
iByzantium : 65,
iFrance : 100,
iJapan : 100,
iNorse : 60,
iTurks : 85,
iArabia : 100,
iTibet : 60,
iBulgaria: 60,
iKhazars: 70,
iMoors : 70,
iJava : 65,
iSpain : 100,
iEngland : 100,
iHolyRome : 80,
iBurma : 60,
iVietnam : 60,
iRus: 60,
iSwahili: 40,
iPoland : 65,
iPortugal : 100,
iInca : 70,
iItaly : 100,
iMongols : 80,
iAztecs : 70,
iTimurids : 80,
iThailand : 100,
iSweden : 100,
iRussia : 100,
iOttomans : 100,
iCongo : 20,
iIran : 100,
iNetherlands : 100,
iGermany : 100,
iAmerica : 100,
iArgentina : 100,
iMexico : 100,
iColombia : 80,
iBrazil : 100,
iCanada : 100,
iMamluks : 70,
iMacedon : 70,
iIroquois : 0,
iArmenia : 65,
iParthia : 85,
iMinoans : 50,
iGhorids : 60,
})

dPatienceThreshold = CivDict({
iEgypt : 30,
iBabylonia : 30,
iHarappa : 30,
iAssyria : 25,
iChina : 30,
iChinaS : 30,
iHittites : 30,
iNubia : 30,
iGreece : 35,
iIndia : 50,
iPhoenicia : 35,
iPolynesia : 50,
iPersia : 30,
iCelts : 25,
iRome : 25,
iMaya : 35,
iDravidia : 45,
iEthiopia : 20,
iToltecs : 20,
iKushans : 25,
iMalays : 40,
iKorea : 25,
iKhmer : 30,
iMali : 35,
iByzantium : 25,
iFrance : 20,
iJapan : 25,
iNorse : 30,
iTurks : 30,
iArabia : 30,
iTibet : 50,
iBulgaria: 30,
iKhazars: 30,
iMoors : 20,
iJava : 30,
iSpain : 20,
iEngland : 20,
iHolyRome : 20,
iBurma : 30,
iRus : 20,
iVietnam : 20,
iSwahili : 40,
iPoland : 20,
iPortugal : 30,
iInca : 35,
iItaly : 25,
iMongols : 20,
iAztecs : 30,
iTimurids : 35,
iThailand : 30,
iSweden : 30,
iRussia : 30,
iOttomans : 35,
iCongo : 20,
iIran : 30,
iNetherlands : 30,
iGermany : 20,
iAmerica : 30,
iArgentina : 40,
iMexico : 40,
iColombia : 30,
iBrazil : 40,
iCanada : 40,
iMamluks: 20,
iMacedon: 30,
iIroquois: 30,
iArmenia: 30,
iParthia: 30,
iMinoans: 30,
iGhorids: 35,
}, 100)

dMaxColonistsPreIndustrial = CivDict({
iSweden : 1,
iSpain : 8,
iFrance : 8,
iEngland : 7,
iPortugal : 7, 
iNetherlands : 6,
})

dMaxColonistsIndustrial = CivDict({
iFrance : 3,
iEngland : 6,
iPortugal : 2, 
iNetherlands : 2,
iGermany : 3
})

# initialise religion variables to religion indices from XML
iNumReligions = 11
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism, iShia) = range(iNumReligions)

#Persecution preference
tPersecutionPreference = (
(iHinduism, iBuddhism, iTaoism, iConfucianism, iZoroastrianism, iIslam, iShia, iProtestantism, iCatholicism, iOrthodoxy), # Judaism
(iIslam, iShia, iProtestantism, iCatholicism, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Orthodoxy
(iIslam, iShia, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Catholicism
(iIslam, iShia, iCatholicism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism, iConfucianism), # Protestantism
(iShia, iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iTaoism, iConfucianism, iZoroastrianism, iBuddhism), # Islam (Sunni)
(iIslam, iShia, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iConfucianism, iBuddhism), # Hinduism
(iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iTaoism, iIslam, iShia, iConfucianism, iHinduism), # Buddhism
(iIslam, iShia, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iTaoism), # Confucianism
(iIslam, iShia, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iZoroastrianism, iHinduism, iBuddhism, iConfucianism), # Taoism
(iIslam, iShia, iCatholicism, iProtestantism, iOrthodoxy, iJudaism, iBuddhism, iHinduism, iTaoism, iConfucianism), # Zoroastrianism
(iIslam, iHinduism, iProtestantism, iCatholicism, iOrthodoxy, iJudaism, iTaoism, iConfucianism, iZoroastrianism, iBuddhism), # Shia
)

# pagan religions
iNumPaganReligions = 19
(iAnunnaki, iAsatru, iAtua, iBaalism, iBon, iDruidism, iInti, iMazdaism, iMugyo, iOlympianism, 
iPesedjet, iRodnovery, iShendao, iShinto, iTengri, iTeotlMaya, iTeotlAztec, iVedism, iYoruba) = range(iNumPaganReligions)

iPaganVictory = iNumReligions
iSecularVictory = iNumReligions + 1

# corporations
iNumCorporations = 11
(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry, iHanseaticLeague, iKnightsTemplar) = range(iNumCorporations)

# initialise tech variables to unit indices from XML

iNumTechs = 141
(iTanning, iMining, iPottery, iPastoralism, iAgriculture, iMythology, iSailing,
iSmelting, iMasonry, iLeverage, iProperty, iCeremony, iDivination, iSeafaring,
iAlloys, iConstruction, iRiding, iArithmetics, iWriting, iCalendar, iShipbuilding,
iBloomery, iCement, iMathematics, iContract, iLiterature, iPriesthood, iNavigation,
iGeneralship, iEngineering, iAesthetics, iCurrency, iLaw, iPhilosophy, iMedicine,
iNobility, iSteel, iArchitecture, iArtisanry, iPolitics, iScholarship, iEthics,
iFeudalism, iFortification, iMachinery, iAlchemy, iGuilds, iCivilService, iTheology,
iCommune, iCropRotation, iPaper, iCompass, iPatronage, iEducation, iDoctrine,
iGunpowder, iCompanies, iFinance, iCartography, iHumanities, iPrinting, iJudiciary,
iFirearms, iLogistics, iExploration, iOptics, iAcademia, iStatecraft, iHeritage,
iCombinedArms, iEconomics, iGeography, iScientificMethod, iUrbanPlanning, iCivilLiberties, iHorticulture,
iReplaceableParts, iHydraulics, iPhysics, iGeology, iMeasurement, iSociology, iSocialContract,
iMachineTools, iThermodynamics, iMetallurgy, iChemistry, iBiology, iRepresentation, iNationalism,
iBallistics, iEngine, iRailroad, iElectricity, iRefrigeration, iLabourUnions, iJournalism,
iPneumatics, iAssemblyLine, iRefining, iFilm, iMicrobiology, iConsumerism, iCivilRights,
iInfrastructure, iFlight, iSynthetics, iRadio, iPsychology, iMacroeconomics, iSocialServices,
iAviation, iRocketry, iFission, iElectronics, iTelevision, iPowerProjection, iGlobalism,
iRadar, iSpaceflight, iNuclearPower, iLaser, iComputers, iTourism, iEcology,
iAerodynamics, iSatellites, iSuperconductors, iRobotics, iTelecommunications, iRenewableEnergy, iGenetics,
iSupermaterials, iFusion, iNanotechnology, iAutomation, iBiotechnology,
iUnifiedTheory, iArtificialIntelligence,
iTranshumanism) = range(iNumTechs)

# initialise unit variables to unit indices from XML

iNumUnits = 239
(iLion, iBear, iPanther, iWolf, iSettler, iCityBuilder, iPioneer, iWorker, iRomanWorker, iPunjabiWorker, iLabourer, 
iMadeireiro, iScout, iExplorer, iBandeirante, iSpy, iReligiousPersecutor, iJewishMissionary, iOrthodoxMissionary, iCatholicMissionary, iProtestantMissionary, 
iIslamicMissionary, iShiaMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary, iZoroastrianMissionary, iWarrior, iNativeWarrior, iMilitia, iAxeman, 
iLightSwordsman, iMycenaeanMyrmidon, iVulture, iDogSoldier, iOathsworn, iSwordsman, iJaguar, iLegion, iComitatus, iGallicWarrior, iPendekar, iAucac, 
iShotelai, iHeavySwordsman, iSamurai, iHuscarl, iGhazi, iDruzhina, iPombos, iSpearman, iPhalanx, iAzmaru, iHoplite, 
iSacredBand, iImmortal, iNativeRaider, iHeavySpearman, iGhuridVeteranSpears, iTagmata, iKyundaw, iPikeman, iLandsknecht, iArquebusier, iFirelancer, iTercio, 
iStrelets, iJanissary, iOromoWarrior, iQizilbash, iMohawkCatholic, iMohawkProtestant, iMusketeer, iRedcoat, iCarolean, iFusilier, iRifleman, 
iMehalSefari, iGrenadier, iRocketeer, iGrenzer, iAlbionLegion, iAntiTank, iInfantry, iSamInfantry, iMobileSam, iMarine, 
iNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iAsharittuBowman, iMedjay, iNativeArcher, iSkirmisher, iVishap, iHolkan, iAtlatl, 
iKelebolo, iLongbowman, iPatiyodha, iRattanArcher, iCrossbowman, iNaffatun, iChokonu, iBalestriere, iChariot, iWarChariot, iHuluganni, 
iCidainh, iHorseman, iCompanion, iNumidianCavalry, iAsvaka, iCamelRider, iHorseArcher, iKonnik, iMangudai, iKhampa, iOghuz, 
iCamelArcher, iLancer, iMamlukCavalry, iVaru, iSavaran, iFarari, iMobileGuard, iKeshik, iCataphract, iChangSuek, iPistolier, 
iHakkapeliitta, iMountedBrave, iCamelGunner, iCuirassier, iGendarme, iConquistador, iWingedHussar, iSowar, iHussar, iCossack, 
iLlanero, iDragoon, iCassay, iGrenadierCavalry, iCavalry, iRural, iWarElephant, iBallistaElephant, iTank, iPanzer, 
iMainBattleTank, iGunship, iCatapult, iSiegeRam, iBallista, iTrebuchet, iBombard, iSiegeEngineer, iHwacha, iLantaka, iSiegeElephant, 
iGreatBombard, iCannon, iGribeauval, iArtillery, iMachineGun, iHowitzer, iMobileArtillery, iWorkboat, iGalley, iWaka, 
iBireme, iWarGalley, iHeavyGalley, iDromon, iLongship, iCog, iDharani, iDhow, iGalleass, iDjong, 
iKobukson, iLanternas, iCaravel, iCarrack, iGalleon, iFluyt, iPrivateer, iCorsair, iFrigate, iShipOfTheLine, 
iManOfWar, iSteamship, iIronclad, iTorpedoBoat, iCruiser, iTransport, iDestroyer, iCorvette, iBattleship, iMissileCruiser, 
iStealthDestroyer, iSubmarine, iNuclearSubmarine, iCarrier, iSupercarrier, iBiplane, iFighter, iZero, iJetFighter, iBomber, 
iFlyingFortress, iStealthBomber, iGuidedMissile, iDrone, iNuclearBomber, iICBM, iSatellite, iGreatProphet, iGreatArtist, iGreatScientist, 
iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iArgentineGreatGeneral, iGreatSpy, iFemaleGreatProphet, iFemaleGreatArtist, iFemaleGreatScientist, iFemaleGreatMerchant, 
iFemaleGreatEngineer, iFemaleGreatStatesman, iFemaleGreatGeneral, iFemaleGreatSpy, iSlave, iAztecSlave) = range(iNumUnits)

lGreatPeopleUnits = [iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant, iGreatEngineer, iGreatStatesman, iGreatGeneral, iGreatSpy]

dFemaleGreatPeople = {
iGreatProphet : iFemaleGreatProphet,
iGreatArtist : iFemaleGreatArtist,
iGreatScientist : iFemaleGreatScientist,
iGreatMerchant : iFemaleGreatMerchant,
iGreatEngineer : iFemaleGreatEngineer,
iGreatStatesman : iFemaleGreatStatesman,
iGreatGeneral : iFemaleGreatGeneral,
iGreatSpy : iFemaleGreatSpy,
}


iNumUnitRoles = 23
(iBase, iDefend, iAttack, iCounter, iShock, iHarass, iCityAttack, iWorkerSea, iSettle, iSettleSea, 
iAttackSea, iAssaultSea, iFerry, iEscort, iExplore, iShockCity, iSiege, iCitySiege, iExploreSea, iSkirmish, 
iLightEscort, iWork, iMissionary) = range(iNumUnitRoles)

# Promotions
iDesertAdaptation = 82
iSteppeAdaptation = 83
iMobility = 47

iNumBonuses = 54
(iAluminium, iAmber, iCamel, iCitrus, iCoal, iCopper, iDates, iHorse, iIron, iMarble,
iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab, iDeer, iFish,
iPig, iPotato, iRice, iSheep, iWheat, iCocoa, iCoffee, iCotton, iDye, iFur,
iGems, iGold, iIncense, iIvory, iJade, iMillet, iObsidian, iOlives, iOpium, iPearls,
iRareEarths, iRubber, iSalt, iSilk, iSilver, iSpices, iSugar, iTea, iTobacco, iWine,
iWhales, iSoccer, iSongs, iMovies) = range(iNumBonuses)

iNumBonusVarieties = 19
(iDyeCochineal, iDyeMurex, iDyeHenna, iSpicesCinnamon, iSpicesNutmeg, iSpicesSaffron, iSpicesVanilla, iGemsTurquoise, iGemsDiamonds, iGemsRuby, iGemsSapphire, 
iGemsEmeralds, iSheepLlama, iSheepBlack, iCowBrown, iPigFurry, iIvoryAfrican, iCitrusOranges, iCrabShrimp) = range(iNumBonuses, iNumBonuses + iNumBonusVarieties)

# if you increase this, increment BEGIN_WONDERS	in CvRhyes.h
iNumBuildings = 151
(iPalace, iChineseUniquePowerPalace, iIroquoisAssemblyHall, iBarracks, iSlaveBarracks, iHellenisticColony, iKalliu, iSoldattorp, iIkhanda, iGranary, iAnaktora, iCommandery, iTannery, iLonghouse, iPaganTemple, iWeaver, iStan, iMbwadi, 
iMonument, iObelisk, iMenhir, iStele, iCandi, iEdict, iMalae, iMudbrickPyramid, iTotemPole, iWalls, iMountainWatch,
iDun, iStable, iPoloField, iOrtege, iLibrary, iEdubba, iTaixue, iKyaung, iCalmecac, iHarbor, iAqueduct, 
iQanat, iBaray, iNoria, iStepwell, iTheatre, iOdeon, iWaterPuppetTheatre, iHippodrome, iPavilion, iArena, 
iBallCourt, iCharreadaArena, iSambadrome, iGarden, iLighthouse, iKhazarTradePost, iGudang, iTradingPost, iJeweller, iGlassmaker, iObsidianWorkshop, 
iMarket, iForum, iCaravanserai, iWangara, iFloatingMarket, iJail, iDivan, iKatorga, iBath, iReservoir, 
iHammam, iForge, iBloomeryBuilding, iArtStudio, iCastle, iQalaat, iCitadel, iIslandFort, iPharmacy, iAlchemist, 
iGrocer, iPostOffice, iTambo, iWharf, iVolok, iCoffeehouse, iSalon, iBank, iConstabulary, iMountedPolice, iCustomsHouse, 
iFeitoria, iUniversity, iSeowon, iGompa, iCivicSquare, iGopuram, iRathaus, iSejmik, iSewer, iStarFort, 
iEstate, iMausoleum, iHacienda, iDrydock, iLevee, iPolder, iObservatory, iWarehouse, iCourthouse, iExchequer, 
iFactory, iAssemblyPlant, iZaibatsu, iDistillery, iPark, iBagh, iCoalPlant, iRailwayStation, iLaboratory, iAbattoir, 
iColdStoragePlant, iGrainSilo, iNewsPress, iIndustrialPark, iCinema, iHospital, iSupermarket, iPublicTransportation, iDepartmentStore, iMall, 
iBroadcastTower, iIntelligenceAgency, iElectricalGrid, iAirport, iBunker, iBombShelters, iHydroPlant, iSecurityBureau, iStadium, iContainerTerminal, 
iNuclearPlant, iSupercomputer, iHotel, iRecyclingCenter, iLogisticsCenter, iSolarPlant, iFiberNetwork, iAutomatedFactory, iVerticalFarm) = range(iNumBuildings)

iNumReligiousBuildings = 44
iFirstReligiousBuilding = iNumBuildings
iNumBuildings += iNumReligiousBuildings
(iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iCatholicTemple, iCatholicCathedral, 
iCatholicMonastery, iCatholicShrine, iProtestantTemple, iProtestantCathedral, iProtestantMonastery, iProtestantShrine, iIslamicTemple, iIslamicCathedral, iIslamicMonastery, iIslamicShrine, iShiaTemple, iShiaCathedral, iShiaMonastery, iShiaShrine, 
iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, 
iConfucianMonastery, iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral, iZoroastrianMonastery, iZoroastrianShrine) = range(iFirstReligiousBuilding, iNumBuildings)

iNumNationalWonders = 19
iFirstNationalWonder = iNumBuildings
iNumBuildings += iNumNationalWonders
(iAcademy, iAdministrativeCenter, iManufactory, iArmoury, iMuseum, iStockExchange, iTradingCompanyBuilding, iIberianTradingCompanyBuilding, iNationalMonument, iNationalTheatre, 
iNationalGallery, iNationalCollege, iMilitaryAcademy, iSecretService, iIronworks, iRedCross, iNationalPark, iCentralBank, iSpaceport) = range(iFirstNationalWonder, iNumBuildings)

iNumGreatWonders = 139 # different from DLL constant because that includes national wonders
iFirstWonder = iNumBuildings
iNumBuildings += iNumGreatWonders
(iGreatSphinx, iPyramids, iOracle, iGreatWall, iIshtarGate, iPalaceOfMinos, iTerracottaArmy, iHangingGardens, iGreatCothon, iDujiangyan, iApadanaPalace, 
iColossus, iStatueOfZeus, iGreatMausoleum, iParthenon, iPyramidOfTheSun, iTempleOfArtemis, iGreatLighthouse, iMoaiStatues, iFlavianAmphitheatre, iAquaAppia, 
iAlKhazneh, iTempleOfKukulkan, iMachuPicchu, iGreatLibrary, iFloatingGardens, iGondeshapur, iJetavanaramaya, iNalanda, iTheodosianWalls, iHagiaSophia, iSaintPeters,
iBorobudur, iMezquita, iShwedagonPaya, iMountAthos, iIronPillar, iPrambanan, iSalsalBuddha, iCheomseongdae, iHimejiCastle, iGrandCanal, 
iWatPreahPisnulok, iKhajuraho, iGreatAdobeMosque, iSpiralMinaret, iDomeOfTheRock, iHouseOfWisdom, iKrakDesChevaliers, iMonolithicChurch, iUniversityOfSankore, iNotreDame, 
iOldSynagogue, iSaintSophia, iSilverTreeFountain, iSantaMariaDelFiore, iAlamut, iSanMarcoBasilica, iSistineChapel, iPorcelainTower, iTopkapiPalace, iKremlin, 
iSaintThomasChurch, iVijayaStambha, iGurEAmir, iRedFort, iTajMahal, iForbiddenPalace, iVersailles, iBlueMosque, iEscorial, iTorreDeBelem, 
iPotalaPalace, iOxfordUniversity, iHarmandirSahib, iSaintBasilsCathedral, iBourse, iItsukushimaShrine, iImageOfTheWorldSquare, iLouvre, iEmeraldBuddha, iShalimarGardens, 
iTrafalgarSquare, iHermitage, iGuadalupeBasilica, iSaltCathedral, iAmberRoom, iStatueOfLiberty, iBrandenburgGate, iAbbeyMills, iBellRockLighthouse, iChapultepecCastle, 
iEiffelTower, iWestminsterPalace, iTriumphalArch, iMenloPark, iCrystalPalace, iTsukijiFishMarket, iBrooklynBridge, iHollywood, iEmpireStateBuilding, iLasLajasSanctuary, 
iPalaceOfNations, iMoleAntonelliana, iNeuschwanstein, iFrontenac, iWembley, iLubyanka, iCristoRedentor, iMetropolitain, iNobelPrize, iGoldenGateBridge, 
iBletchleyPark, iSagradaFamilia, iCERN, iItaipuDam, iGraceland, iCNTower, iPentagon, iUnitedNations, iCrystalCathedral, iMotherlandCalls, 
iBerlaymont, iWorldTradeCenter, iAtomium, iIronDome, iHarbourOpera, iLotusTemple, iGlobalSeedVault, iGardensByTheBay, iBurjKhalifa, iHubbleSpaceTelescope, 
iChannelTunnel, iSkytree, iOrientalPearlTower, iDeltaWorks, iSpaceElevator, iLargeHadronCollider, iITER) = range(iFirstWonder, iNumBuildings)

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

#Civics
iNumCivics = 42
(iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty, iDemocracy,
iPersonalism, iCitizenship, iVassalage, iTheocracy, iBureaucracy, iStratocracy, iConstitution,
iTraditionalism, iSlavery, iManorialism, iCasteSystem, iIndividualism, iTotalitarianism, iEgalitarianism,
iReciprocity, iRedistribution, iMerchantTrade, iRegulatedTrade, iFreeEnterprise, iCentralPlanning, iPublicWelfare,
iAnimism, iDeification, iClergy, iSyncretism, iMonasticism, iFanaticism, iSecularism,
iKinship, iThalassocracy, iHegemony, iIsolationism, iColonialism, iNationhood, iMultilateralism) = range(iNumCivics)

iNumCivicCategories = 6
(iCivicsGovernment, iCivicsLegitimacy, iCivicsSociety, iCivicsEconomy, iCivicsReligion, iCivicsTerritory) = range(iNumCivicCategories)

#Specialists
iNumSpecialists = 19
(iSpecialistCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistStatesman,
iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy, 
iSpecialistResearchSatellite, iSpecialistCommercialSatellite, iSpecialistMilitarySatellite, 
iSpecialistSlave) = range(iNumSpecialists)

lGreatSpecialists = [iSpecialistGreatProphet, iSpecialistGreatArtist, iSpecialistGreatScientist, iSpecialistGreatMerchant, iSpecialistGreatEngineer, iSpecialistGreatStatesman, iSpecialistGreatGeneral, iSpecialistGreatSpy]

#Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)
StabilityLevelTexts = ["TXT_KEY_STABILITY_COLLAPSING", "TXT_KEY_STABILITY_UNSTABLE", "TXT_KEY_STABILITY_SHAKY", "TXT_KEY_STABILITY_STABLE", "TXT_KEY_STABILITY_SOLID"]

#Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)
StabilityTypesTexts = ["TXT_KEY_STABILITY_CATEGORY_EXPANSION", "TXT_KEY_STABILITY_CATEGORY_ECONOMY", "TXT_KEY_STABILITY_CATEGORY_DOMESTIC", "TXT_KEY_STABILITY_CATEGORY_FOREIGN", "TXT_KEY_STABILITY_CATEGORY_MILITARY"]

#Stability Parameters
iNumStabilityParameters = 23
(iParameterCorePeriphery, iParameterAdministration, iParameterSeparatism, iParameterRecentExpansion, iParameterRazedCities, iParameterIsolationism,	# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,								# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,								# Domestic
iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterNationhood, iParameterTheocracy, iParameterMultilateralism,			# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)						# Military

#Regions
iNumRegions = 87
(rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland,
rBaltics, rSweden, rRuthenia, rPonticSteppe, rEuropeanArctic, rUrals, rAnatolia, rCaucasus, rLevant, rMesopotamia,
rArabia, rEgypt, rNubia, rMaghreb, rPersia, rKhorasan, rTransoxiana, rSindh, rPunjab, rRajputana,
rHindustan, rBengal, rDeccan, rDravida, rIndochina, rIndonesia, rPhilippines, rSouthChina, rNorthChina, rKorea,
rJapan, rTibet, rTarimBasin, rMongolia, rManchuria, rAmur, rCentralAsianSteppe, rSiberia, rAustralia, rOceania,
rEthiopia, rHornOfAfrica, rSwahiliCoast, rGreatLakes, rZambezi, rMadagascar, rCape, rKalahari, rCongo, rGuinea, 
rSahel, rSahara, rAtlanticSeaboard, rDeepSouth, rMidwest, rGreatPlains, rAridoamerica, rCalifornia, rCascadia, rOntario, 
rQuebec, rMaritimes, rAmericanArctic, rCaribbean, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, 
rSouthernCone, rAntarctica, rHinduKush, rDenmark, rNorway, rCrimea, rYemenOman) = range(iNumRegions)

iNumWaterRegions = 85
(rMediterraneanSea, rBlackSea, rCaspianSea, rBalticSea, rNorthSea, rAtlanticOcean, rCaribbeanSea, rGulfOfMexico, rHudsonBay, rArcticOcean,
rRedSea, rArabianSea, rPersianGulf, rGulfOfBengal, rIndianOcean, rAustralasianSea, rSouthChinaSea, rEastChinaSea, rSeaOfJapan, rSeaOfOkhotsk, 
rBeringSea, rPacificOcean, rSouthernOcean, rVanern, rVattern, rInari, rPaijanne, rOulu, rSaimaa, rPeipus, 
rLadoga, rOnega, rVan, rSevan, rUrmia, rAralSea, rTengiz, rBalkhash, rIssykKul, rAlakol, 
rZaysan, rUvs, rKhovsgol, rBaikal, rTaymyr, rHulun, rQinghai, rLopNur, rSiling, rDongting, 
rPoyang, rTai, rTonleSap, rSetoInlandSea, rEyre, rChad, rTana, rTurkana, rNyanza, rMwitanzege, 
rRweru, rTanganyika, rMweru, rBangweulu, rRukwa, rMalawi, rGreatBear, rTidee, rAthabasca, rReindeer, 
rDubawt, rBaker, rWinnipeg, rSuperior, rMichigan, rHuron, rErie, rLakeOntario, rMistassini, rLobstick, 
rGreatSalt, rNicaragua, rTiticaca, rMarChiquita, rKhanka) = range(100, 100 + iNumWaterRegions)

lEuropeProper = [rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rBaltics, rDenmark, rNorway, rSweden, rRuthenia, rCrimea]
lEuropeAsia = [rEuropeanArctic, rUrals, rSiberia, rPonticSteppe]
lMiddleEast = [rAnatolia, rCaucasus, rLevant, rMesopotamia, rArabia, rPersia, rKhorasan, rTransoxiana, rYemenOman, rHinduKush]
lIndia = [rSindh, rPunjab, rRajputana, rHindustan, rBengal, rDeccan, rDravida]
lEastAsia = [rIndochina, rIndonesia, rPhilippines, rSouthChina, rNorthChina, rKorea, rJapan, rTibet, rTarimBasin, rMongolia, rManchuria, rAmur, rCentralAsianSteppe]
lNorthAfrica = [rEgypt, rNubia, rMaghreb]
lSubSaharanAfrica = [rEthiopia, rHornOfAfrica, rSwahiliCoast, rGreatLakes, rZambezi, rMadagascar, rCape, rKalahari, rCongo, rGuinea, rSahel, rSahara]
lSouthAmerica = [rNewGranada, rAndes, rAmazonia, rBrazil, rSouthernCone]
lCentralAmerica = [rCaribbean, rMesoamerica, rCentralAmerica]
lNorthAmerica = [rAtlanticSeaboard, rDeepSouth, rMidwest, rGreatPlains, rAridoamerica, rCalifornia, rCascadia, rOntario, rQuebec, rMaritimes, rAmericanArctic]
lOceania = [rAustralia, rOceania]

lEurope = lEuropeProper + lEuropeAsia
lAfrica = lNorthAfrica + lSubSaharanAfrica
lAsia = lMiddleEast + lIndia + lEastAsia
lAmerica = lSouthAmerica + lCentralAmerica + lNorthAmerica

lNewWorld = lAmerica + lOceania

#Projects

iNumProjects = 21
(iManhattanProject, iTheInternet, iHumanGenome, iSDI, iGPS, iISS, iBallisticMissile, iFirstSatellite, iManInSpace, iLunarLanding,
iGoldenRecord, iMarsMission, iLunarColony, iInterstellarProbe, iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter) = range(iNumProjects)

lMarsBaseComponents = [iMarsFraming, iMarsPowerSource, iMarsExtractor, iMarsHabitat, iMarsHydroponics, iMarsLaboratory, iMarsControlCenter]

#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iGlobal, iDigital) = range (iNumEras)

# Culture

iNumCultureLevels = 7
(iCultureLevelNone, iCultureLevelPoor, iCultureLevelFledgling, iCultureLevelDeveloping, iCultureLevelRefined, iCultureLevelInfluential, iCultureLevelLegendary) = range(iNumCultureLevels)


#Improvements

iNumImprovements = 32
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iPaddyField, iFishingBoats, iHarvestBoats, iOceanFishery, iWhalingBoats, 
iMine, iSlaveMine, iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, iSlavePlantation, iQuarry, iPasture, 
iCamp, iWell, iOffshorePlatform, iOrchard, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve, 
iMarinePreserve, iSolarCollector) = range(iNumImprovements)

iNumRoutes = 4
(iRouteRoad, iRouteRailroad, iRouteRomanRoad, iRouteHighway) = range(iNumRoutes)

#feature & terrain

iNumFeatures = 12
(iSeaIce, iJungle, iOasis, iFloodPlains, iForest, iMud, iCape, iIslands, iRainforest, iFallout, 
iTaiga, iSavanna) = range(iNumFeatures)

iNumTerrains = 19
(iGrass, iPlains, iDesert, iTundra, iSnow, iCoast, iOcean, iTerrainPeak, iTerrainHill, iMarsh, 
iLagoon, iArcticCoast, iSemidesert, iSteppe, iMoorland, iSaltFlat, iSaltLake, iAtoll, iTerrainSavanna) = range(iNumTerrains)

#Plague
iImmunity = 20

# Victory
iVictoryPaganism = 10
iVictorySecularism = 11


#leaders
iNumLeaders = 151
(iLeaderBarbarian, iNativeLeader, iIndependentLeader, iRamesses, iCleopatra, iSargon, iHammurabi, iWentAntu,
iAshurbanipal, iNasirAlDawla, iQinShiHuang, iTaizong, iHongwu, iMao, iSunQuan, iGaozong, iChiangKaishek, iMursili, iPericles, iAlexanderTheGreat, iGeorge, iAsoka, 
iChandragupta, iShivaji, iGandhi, iHiram, iHannibal, iAbuFaris, iTaharqa, iAhoeitu, iCyrus, iDarius, iMithridates, iKhosrow, 
iBrennus, iJuliusCaesar, iAugustus, iPacal, iRajendra, iKrishnaDevaRaya, iEzana, iZaraYaqob, iMenelik, iTopiltzin, 
iKanishka, iWangKon, iSejong, iSuryavarman, iMansaMusa, iJustinian, iBasil, iCharlemagne, iLouis, iNapoleon, 
iDeGaulle, iSriJayanasa, iTunPerak, iKammu, iOdaNobunaga, iMeiji, iRagnar, iChristian, iGerhardsen, iBumin, 
iAlpArslan, iTamerlane, iHarun, iAlMuizz, iSaladin, iBaibars, iNasser, iSimeon, iSongtsen, iLobsangGyatso, iRahman, iYaqub, iHayamWuruk, iSuharto, 
iIsabella, iPhilip, iFranco, iAlfred, iElizabeth, iVictoria, iChurchill, iBarbarossa, iCharles, iFrancis, 
iAnawrahta, iBayinnaung, iYaroslav, iLeLoi, iDawud, iCasimir, iSobieski, iPilsudski, iWalesa, iAfonso, 
iJoao, iMaria, iHuaynaCapac, iCastilla, iLorenzo, iCavour, iMussolini, iGenghisKhan, iKublaiKhan, iMontezuma, 
iTughluq, iAkbar, iBhutto, iNaresuan, iMongkut, iGustav, iIvan, iPeter, iCatherine, iAlexanderI, 
iStalin, iMehmed, iSuleiman, iAtaturk, iMbemba, iAbbas, iKhomeini, iWillemVanOranje, iWilliam, iFrederick, 
iBismarck, iHitler, iWashington, iLincoln, iRoosevelt, iSanMartin, iPeron, iJuarez, iSantaAnna, iCardenas, 
iBolivar, iPedro, iVargas, iMacDonald, iTrudeau, iBoudica, iHiawatha, iTigranes, iAshot, iAndranik, iAriadne, iAgamemnon, iBulan) = range(iNumLeaders)

dResurrectionLeaders = CivDict({
	iChina : iHongwu,
	iChinaS: iGaozong,
	iIndia : iShivaji,
})

# update DLL constants when this changes
iNumPeriods = 27
(iPeriodMing, iPeriodMaratha, iPeriodModernGreece, iPeriodCarthage, iPeriodInsularCelts,
iPeriodVijayanagara, iPeriodByzantineConstantinople, iPeriodSeljuks, iPeriodMeiji, iPeriodDenmark, 
iPeriodNorway, iPeriodUzbeks, iPeriodSaudi, iPeriodMorocco, iPeriodSpain, iPeriodAustria, 
iPeriodYuan, iPeriodPeru, iPeriodLateInca, iPeriodModernItaly, iPeriodPakistan, 
iPeriodOttomanConstantinople, iPeriodModernGermany, iPeriodTunisia, iPeriodMughals, iPeriodModernIndia, iPeriodUkraine) = range(iNumPeriods)

iNumImpacts = 5
(iImpactMarginal, iImpactLimited, iImpactSignificant, iImpactCritical, iImpactPlayer) = range(iNumImpacts)

lTradingCompanyCivs = [iSpain, iFrance, iEngland, iPortugal, iNetherlands]
lLateColonyCivs = lTradingCompanyCivs + [iGermany]

lMongolCivs = [iPersia, iByzantium, iTurks, iArabia, iRus, iMamluks, iAssyria, iParthia, iKushans, iMacedon, iArmenia, iGhorids, iKhazars]

(i3000BC, i600AD, i1700AD) = range(3)

# Stability overlay and editor
iNumPlotStabilityTypes = 4
(iCoreArea, iHistoricalArea, iConquestArea, iForeignArea) = range(iNumPlotStabilityTypes)
lStabilityColors = ["COLOR_CYAN", "COLOR_GREEN", "COLOR_YELLOW", "COLOR_RED"]
lPresetValues = [3, 20, 90, 200, 500, 700]

iMaxWarValue = 12
lWarMapColors = ["COLOR_RED", "COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_PLAYER_DARK_GREEN", "COLOR_BLUE"]

lReligionMapColors = ["COLOR_PLAYER_ORANGE", "COLOR_YELLOW", "COLOR_GREEN", "COLOR_CYAN"]
lReligionMapTexts = ["TXT_KEY_CULTURELEVEL_NONE", "TXT_KEY_WB_RELIGIONMAP_MINORITY", "TXT_KEY_WB_RELIGIONMAP_PERIPHERY", "TXT_KEY_WB_RELIGIONMAP_HISTORICAL", "TXT_KEY_WB_RELIGIONMAP_CORE"]

lNetworkEvents = {
	"CHANGE_COMMERCE_PERCENT" :	1200,
}

newline = "[NEWLINE]"
bullet = "[ICON_BULLET]"
event_bullet = "INTERFACE_EVENT_BULLET"
event_cancel = "INTERFACE_BUTTONS_CANCEL"