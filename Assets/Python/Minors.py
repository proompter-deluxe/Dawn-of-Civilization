# coding: utf-8

from Core import *
from Core import periodic as core_periodic
from RFCUtils import *
from Events import handler
from Locations import *

def periodic(iTurns, seed):
	return (turn() + hash(seed)) % turns(iTurns) == 0


def best_civ_of_group(iGroup):
	return civs.of(*dTechGroups[iGroup]).alive().maximum(lambda c: player(c).getScoreHistory(turn()))


def best_civ_of_same_tech_group(iCiv):
	iTechGroup = next(iGroup for iGroup in dTechGroups if iCiv in dTechGroups[iGroup])
	return best_civ_of_group(iTechGroup)


def add_city_buildings(tile, iCiv):
	city(tile).rebuild(player(iCiv).getCurrentEra())
	return
		
	for iDefensiveBuilding in infos.buildings().where(isDefensiveBuilding):
		if player(iCiv).canConstruct(iDefensiveBuilding, False, False, False):
			city(tile).setHasRealBuilding(iDefensiveBuilding, True)


def is_new_world_discovered(_):
	return True in data.dFirstContactConquerors.values()


def is_free_of_civ(iCiv):
	def func(barbarians):
		return iCiv not in cities.rectangle(barbarians.area).owners()
	
	return func


class MinorCity(object):

	def __init__(self, iYear, iOwner, tile, name, iPopulation=1, iCiv=None, iCulture=0, bIgnoreRuins=False, units={}, buildings=[], bUnique=True, adjective=None, condition=lambda: True):
		self.iYear = iYear
		self.iOwner = iOwner
		self.tile = tile
		self.name = name
		self.iPopulation = iPopulation
		self.iCiv = iCiv
		self.iCulture = iCulture
		self.bIgnoreRuins = bIgnoreRuins
		self.units = units
		self.buildings = buildings
		self.bUnique = bUnique
		self.adjective = adjective
		self.condition = condition
	
	def check(self):
		if self.canFound():
			self.found()
		
		city = city_(self.tile)
		if not city:
			return
		
		if not is_minor(city.getOwner()):
			return
		
		if self.every(10):
			self.add_unit()
		
		if self.every(25):
			self.add_buildings()
	
	def canFound(self):
		if not self.bIgnoreRuins and plot(self.tile).getImprovementType() == iCityRuins:
			return False
	
		if year() < year(self.iYear):
			return False
		
		if year() >= year(self.iYear) + turns(10):
			return False
		
		if not self.condition():
			return False
		
		if not isFree(self.iOwner, self.tile, bNoCity=True, bNoCulture=True) and not isFree(self.iOwner, self.tile, bNoCity=True, iCityDistance=2):
			return False
		
		return True
		
	def get_tech_civ(self):
		if self.iCiv is None or since(year(dBirth[self.iCiv])) < 0:
			return self.iOwner
		
		if slot(self.iCiv) >= 0:
			return self.iCiv
		
		lNeighbours = dNeighbours[self.iCiv]
		lTechGroup = next(lTechGroupCivs for iTechGroup, lTechGroupCivs in dTechGroups.items() if self.iCiv in lTechGroupCivs)
		
		lValidCivs = [iCiv for iCiv in set(lNeighbours) & set(lTechGroup) if self.iCiv != iCiv and since(year(dBirth[self.iCiv])) >= 0 and slot(iCiv) >= 0 and infos.civ(iCiv).getImpact() >= infos.civ(self.iCiv).getImpact()]

		if not lValidCivs:
			return self.iOwner
		
		return sorted(lValidCivs, key=lambda iCiv: abs(year(dBirth[iCiv]) - year(dBirth[self.iCiv])))[0]
	
	def found(self):
		iOwnerPlayer = slot(self.iOwner)
		x, y = location(self.tile)
		
		convertPlotCulture(self.tile, iOwnerPlayer, 100, bOwner=True)
		expelUnits(iOwnerPlayer, plots.surrounding(x, y))
		
		player(iOwnerPlayer).found(x, y)
		founded = city(x, y)
		
		if founded:
			iTechEra = player(self.get_tech_civ()).getCurrentEra()
			
			founded.setName(self.name, False)
			founded.setPopulation(self.iPopulation)
			
			if plot(x, y).getRegionID() not in lAfrica:
				founded.setCulture(founded.getOwner(), scale(self.iCulture) + iTechEra * scale(100), True)
			
			self.add_buildings()
			self.create_units()
			
	def every(self, iTurns):
		return periodic(iTurns, self)
	
	def get_units(self):
		iUnitCiv = self.get_tech_civ()
		bUnique = self.bUnique and self.iCiv == iUnitCiv
		
		for iRole, iNumUnits in self.units.items():
			for iUnit, iUnitAI in getUnitsForRole(iUnitCiv, iRole, bUnique=bUnique):
				if iUnit is None:
					iUnit = iMilitia
				
				if not bUnique:
					iUnit = base_unit(iUnit)
				
				yield iUnit, iNumUnits, iUnitAI
	
	def make_units(self, iUnit, iUnitAI, iNumUnits=1):
		for unit in units.at(self.tile).where(lambda unit: unit.upgradeAvailable(unit.getUnitType(), infos.unit(iUnit).getUnitClassType(), 0)).limit(iNumUnits):
			unit.kill(False, -1)
		
		city = city_(self.tile)
		if not city:
			return
	
		created_units = makeUnits(city.getOwner(), iUnit, self.tile, iNumUnits, iUnitAI)
		
		if self.adjective:
			created_units.adjective(self.adjective)
	
	def create_units(self):
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			if self.is_human_proximity():
				iNumUnits += 1
			
			self.make_units(iUnit, iUnitAI, iNumUnits)
	
	def add_unit(self):
		if units.surrounding(self.tile).atwar(city(self.tile).getOwner()):
			return
	
		iTechCiv = self.get_tech_civ()
	
		for iUnit, iNumUnits, iUnitAI in self.get_units():
			if units.surrounding(self.tile).type(iUnit).count() < iNumUnits + max(0, player(iTechCiv).getCurrentEra() - 1):
				self.make_units(iUnit, iUnitAI)
	
	def add_buildings(self):
		iTechCiv = self.get_tech_civ()
		add_city_buildings(self.tile, iTechCiv)
		
		for iBuilding in self.buildings:
			city(self.tile).setHasRealBuilding(iBuilding, True)
	
	def is_human_proximity(self):
		return plot(self.tile).getRegionID() == plot(dCapitals[active()]).getRegionID() or plot(self.tile).getPlayerWarValue(active()) >= 5


NUM_BARBARIAN_TYPES = 8
(ANIMALS, NOMADS, MINORS, INVADERS, CLOSE_INVADERS, NATIVES, SEA_INVADERS, PIRATES) = range(NUM_BARBARIAN_TYPES)


class Barbarians(object):

	SPAWN_LIMITS = {
		ANIMALS: 3,
		NOMADS: 3,
		MINORS: 5,
		NATIVES: 3,
		PIRATES: 3,
	}
	
	SPAWN_NOTIFICATIONS = {
		ANIMALS: "TXT_KEY_BARBARIAN_NOTIFICATION_ANIMALS",
		NOMADS: "TXT_KEY_BARBARIAN_NOTIFICATION_NOMADS",
		MINORS: "TXT_KEY_BARBARIAN_NOTIFICATION_MINORS",
		INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_INVADERS",
		CLOSE_INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_INVADERS",
		NATIVES: "TXT_KEY_BARBARIAN_NOTIFICATION_NATIVES",
		SEA_INVADERS: "TXT_KEY_BARBARIAN_NOTIFICATION_SEA_INVADERS",
		PIRATES: "TXT_KEY_BARBARIAN_NOTIFICATION_PIRATES"
	}

	def __init__(self, iStart, iEnd, units, area, iInterval, pattern, iOwner=iBarbarian, target_area=None, adjective=None, iAlternativeCiv=None, promotions=None, condition=None):
		self.iStart = iStart
		self.iEnd = iEnd
		self.units = units
		self.area = area
		self.iInterval = iInterval
		self.pattern = pattern
		self.iOwner = iOwner
		self.target_area = target_area
		self.adjective = adjective
		self.iAlternativeCiv = iAlternativeCiv
		self.promotions = promotions
		self.condition = condition
		
		if self.target_area is None:
			self.target_area = area
	
	def __repr__(self):
		return "%s barbarians: %s" % (text(self.adjective), format_separators(self.units.keys(), ", ", text("TXT_KEY_AND"), format=lambda iUnit: infos.unit(iUnit).getText()))
	
	def spawn_data(self):
		data = {
			"iStart": self.iStart,
			"iEnd": self.iEnd,
			"units": self.units,
			"iInterval": self.iInterval,
		}
		return data
	
	def check(self):
		if self.can_spawn():
			self.spawn()
	
	def can_spawn(self):
		if self.iAlternativeCiv is not None and player(self.iAlternativeCiv).isExisting():
			return False
		
		if self.condition is not None and not self.condition(self):
			return False
	
		if not (year(self.iStart) <= year() <= year(self.iEnd)):
			return False
		
		if not self.every():
			return False
	
		if self.pattern in [NOMADS, INVADERS, CLOSE_INVADERS, SEA_INVADERS]:
			if not self.valid_targets():
				return False
		
		if self.spawn_limit():
			return False
		
		if self.pattern == MINORS:
			if plots.rectangle(self.area).land().all(lambda p: p.isOwned() and not owner(p, self.get_owner())):
				return False
	
		return True
	
	def every(self):
		return periodic(self.iInterval, self)
	
	def is_targeted(self):
		if self.pattern != INVADERS:
			return False
		
		if cities.rectangle(self.target_area).owner(active()).count() < cities.rectangle(self.target_area).count():
			return False
		
		if year() < year(dFall[civ(active())]):
			return False
		
		return True
	
	def spawn(self):
		lSpawnPlots = self.get_spawn_plots()
		
		# only naval units on first pass, then only land units
		for iUnit, plot in zip(self.get_spawn_units(), lSpawnPlots):
			if infos.unit(iUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				self.spawnUnit(iUnit, plot)

		for iUnit, plot in zip(self.get_spawn_units(), lSpawnPlots):
			if infos.unit(iUnit).getDomainType() != DomainTypes.DOMAIN_SEA:
				self.spawnUnit(iUnit, plot)
		
		for plot in lSpawnPlots:
			if self.can_notify(plot):
				self.notify(plot)

	def spawnUnit(self, iUnit, plot):
		unit = makeUnit(self.get_owner(), iUnit, plot, self.get_unit_ai(iUnit, plot))
					
		data.units[unit].spawn_data = self.spawn_data()
					
		if self.adjective:
			set_unit_adjective(unit, self.adjective)
					
		if self.promotions:
			for iPromotion in self.promotions:
				unit.setHasPromotion(iPromotion, True)
	
	def get_owner(self):
		if self.pattern == MINORS:
			minor_city = cities.rectangle(self.area).where(lambda city: is_minor(city.getOwner())).first()
			if minor_city:
				return civ(minor_city.getOwner())
		
		return self.iOwner
	
	def valid_targets(self):
		return cities.rectangle(self.target_area).any(lambda city: not is_minor(city.getOwner()))
	
	def count_existing(self, iUnit):
		return units.owner(self.iOwner).type(iUnit).where(lambda unit: data.units[unit].spawn_data == self.spawn_data()).count()
	
	def spawn_limit(self):
		iLimit = self.SPAWN_LIMITS.get(self.pattern)
		
		if iLimit is None:
			return False
			
		for iUnit, iNumUnits in self.units.items():
			if self.count_existing(iUnit) >= iLimit * iNumUnits:
				return True
		
		return False
	
	def get_units(self):
		for iUnit, iNumUnits in self.units.items():
			if self.is_targeted():
				iNumUnits += 1
			
			yield iUnit, iNumUnits
		
	def get_spawn_units(self):
		return sum(([iUnit] * iNumUnits for iUnit, iNumUnits in self.get_units()), [])
	
	def get_spawn_plots(self):
		spawn_area = plots.rectangle(self.area).passable().where(self.valid_spawn)
		iNumUnits = sum(self.units.values())
		
		if not spawn_area:
			return []
		
		if self.pattern == MINORS:
			minor_city = spawn_area.cities().owner(self.get_owner()).random()
			if minor_city:
				return [minor_city] * iNumUnits
			
			return [spawn_area.random()] * iNumUnits
		
		elif self.pattern in [INVADERS, CLOSE_INVADERS, SEA_INVADERS]:
			return [spawn_area.random()] * iNumUnits
		
		else:
			return spawn_area.sample(iNumUnits)
	
	def get_unit_ai(self, iUnit, plot):
		if plot.isCity():
			return UnitAITypes.UNITAI_CITY_DEFENSE
	
		if self.pattern == PIRATES:
			return UnitAITypes.UNITAI_PIRATE_SEA
		
		elif self.pattern == ANIMALS:
			return UnitAITypes.UNITAI_ANIMAL
		
		elif self.pattern == SEA_INVADERS:
			if infos.unit(iUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
				return UnitAITypes.UNITAI_ASSAULT_SEA
		
		return UnitAITypes.UNITAI_ATTACK
	
	@staticmethod
	def valid_unit_spawn_terrain(plot, iUnit):
		if infos.unit(iUnit).getTerrainImpassable(plot.getTerrainType()) and not plot.isOwned():
			return False
		
		if plot.getFeatureType() >= 0 and infos.unit(iUnit).getFeatureImpassable(plot.getFeatureType()):
			return False
		
		return True
	
	def valid_spawn_terrain(self, plot):
		return all(self.valid_unit_spawn_terrain(plot, iUnit) for iUnit in self.units)
	
	def valid_spawn(self, plot):
		if plot.getBirthProtected() >= 0:
			return False
	
		if not self.valid_spawn_terrain(plot):
			return False
	
		if self.pattern in [SEA_INVADERS, PIRATES]:
			if plot.getTerrainType() not in [iCoast, iArcticCoast]:
				return False
			
			if map.getArea(plot.getArea()).isLake():
				return False
				
		else:
			if plot.isWater():
				return False
		
			if map.getArea(plot.getArea()).getNumCities() == 0:
				return False
		
		if units.at(plot).notowner(self.get_owner()):
			return False
			
		if self.pattern == CLOSE_INVADERS:
			if plot.isCity():
				return False
		elif cities.surrounding(plot):
			return False
		
		if self.pattern in [ANIMALS, NOMADS, MINORS, PIRATES]:
			if plot.isOwned():
				return False
		
		if self.pattern == ANIMALS:
			if cities.surrounding(plot, radius=3):
				return False
		
		if self.pattern == INVADERS:
			if not plots.surrounding(plot).where(lambda p: p.getOwner() != plot.getOwner() or p.isWater()):
				return False
		
		return True
	
	def can_notify(self, plot):
		if turn() <= self.iStart + turns(self.iInterval):
			if plot.isVisible(player().getTeam(), False):
				closest = closestCity(plot, owner=active(), same_continent=not plot.isWater(), coastal_only=plot.isWater())
				if closest and distance(plot, closest) <= 5:
					return True
		
		return False
	
	def notify(self, plot):
		adjective_text = text_if_exists(self.adjective, otherwise="TXT_KEY_ADJECTIVE_BARBARIAN")
		unit = infos.unit(self.units.items()[0][0])
		
		message(active(), self.SPAWN_NOTIFICATIONS[self.pattern], adjective_text, iColor=iRed, button=unit.getButton(), location=plot)


minor_cities = [
	MinorCity(-2800, iIndependent2, tSusa, "Shushan", iPopulation=1, iCiv=iBabylonia, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_ELAMITE"),
	# MinorCity(-3000, iIndependent, (90, 45), "Unug", iPopulation=1, iCiv=iBabylonia, units={iDefend: 2}, iCulture=10, adjective="TXT_KEY_ADJECTIVE_SUMERIAN"),
	MinorCity(-2100, iIndependent2, (85, 50), "Ugarit", iPopulation=1, iCiv=iBabylonia, units={iDefend: 1, iWork: 1}, iCulture=15, adjective="TXT_KEY_ADJECTIVE_MARIOTE"),
	#MinorCity(-2050, iIndependent, (118, 49), "Sanxingdui", iPopulation=2, iCiv=iChina, units={iDefend: 1, iBase: 1}, adjective="TXT_KEY_ADJECTIVE_SHU"),
	#MinorCity(-1830, iBarbarian, (124, 52), "Daliang", iPopulation=2, iCiv=iChina, units={iDefend: 1, iBase: 1}, adjective="TXT_KEY_ADJECTIVE_WEI"),
	MinorCity(-1830, iBarbarian, (126, 53), "Linzi", iPopulation=1, iCiv=iChina, units={iBase: 2}, adjective="TXT_KEY_ADJECTIVE_QI"),
	MinorCity(-2200, iIndependent2, tJerusalem, "Yerushalayim", iPopulation=1, iCiv=iBabylonia, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_ISRAELITE"),
	MinorCity(-2000, iIndependent, (85, 47), "Sur", iPopulation=1, iCiv=iBabylonia, units={iDefend: 1, iCounter: 1}, adjective="TXT_KEY_CIV_PHOENICIA_ADJECTIVE"),
	MinorCity(-1200, iBarbarian, (72, 55), "Daorson", iPopulation=2, iCiv=iMinoans, units={iDefend: 2, iAttack: 1}, adjective="TXT_KEY_ADJECTIVE_ILLYRIAN"),
	MinorCity(-1200, iIndependent2, (89, 53), "Tushpa", iPopulation=2, iCiv=iHittites, units={iDefend: 3, iCounter: 2}, adjective="TXT_KEY_ADJECTIVE_ARMENIAN"),
	MinorCity(-1000, iBarbarian, tDelhi, "Indraprastha", iPopulation=1, iCiv=iHarappa, units={iDefend: 1, iCounter: 1}, bIgnoreRuins=True, condition=lambda: not player(iHarappa).isHuman(), adjective="TXT_KEY_ADJECTIVE_VEDIC"),
	MinorCity(-1000, iBarbarian, tVaranasi, "Kashika", iPopulation=1, iCiv=iHarappa, units={iDefend: 1, iCounter: 1}, bIgnoreRuins=True, condition=lambda: not player(iHarappa).isHuman(), adjective="TXT_KEY_ADJECTIVE_VEDIC"),
	MinorCity(-1000, iBarbarian, (85, 50), "Kinalua", iPopulation=1, iCiv=iHittites, units={iDefend: 1, iCounter: 1}, iCulture=15, adjective="TXT_KEY_ADJECTIVE_NEO_HITTITE"),
	MinorCity(-910, iIndependent2, (80, 52), "Sfard", iPopulation=2, iCiv=iHittites, units={iDefend: 1, iCounter: 1}, condition=lambda: not player(iHittites).isHuman(), adjective="TXT_KEY_ADJECTIVE_LYDIAN"),
	MinorCity(-900, iBarbarian, (119, 44), "Kunming", iPopulation=1, iCiv=iShu, units={iDefend: 2, iCounter: 2}, adjective="TXT_KEY_ADJECTIVE_QIANG"),
	MinorCity(-850, iBarbarian, (119, 55), "Qiang", iPopulation=2, iCiv=iChina, units={iShock: 3}, adjective="TXT_KEY_ADJECTIVE_QIANG"),
	MinorCity(-810, iIndependent2, tCarthage, "Qart-Hadasht", iPopulation=3, iCiv=iPhoenicia, units={iDefend: 2, iCounter: 2, iWork: 2}, condition=lambda: not player(iPhoenicia).isExisting(), adjective="TXT_KEY_CIV_PHOENICIA_ADJECTIVE"),
	MinorCity(-800, iIndependent, (100, 55), u"Smárkath", iPopulation=1, iCiv=iAssyria, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SOGDIAN"),
	MinorCity(-750, iIndependent2, tTrebizond, "Trapezous", iPopulation=2, iCiv=iGreece, units={iDefend: 1}, condition=lambda: player(iGreece).isExisting() and not player(iGreece).isHuman(),  adjective="TXT_KEY_CIV_GREECE_ADJECTIVE"),
	MinorCity(-680, iIndependent, (92, 50), "Hagmatana", iPopulation=3, iCiv=iAssyria, units={iDefend: 2, iShock: 2}, iCulture=15, adjective="TXT_KEY_ADJECTIVE_MEDIAN"),
	MinorCity(-600, iIndependent, (97, 53), "Margu", iPopulation=1, iCiv=iPersia, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SOGDIAN"),
	MinorCity(-650, iIndependent2, tGades, "Gadir", iPopulation=2, iCiv=iPhoenicia, units={iDefend: 1, iCounter:1, iWork: 1}, condition=lambda: not player(iPhoenicia).isHuman(), adjective="TXT_KEY_CIV_PHOENICIA_ADJECTIVE"),
	MinorCity(-650, iIndependent, tPella, "Aigai", iPopulation=2, iCiv=iGreece, units={iDefend: 1, iCounter:1, iWork: 1}, adjective="TXT_KEY_CIV_MACEDON_ADJECTIVE"), 
	MinorCity(-600, iBarbarian, (125, 43), "Panyu", iPopulation=2, iCiv=iShu, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_NANYUE"),
	MinorCity(-600, iBarbarian, (128, 48), "Kuaiji", iPopulation=2, iCiv=iShu, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_NANYUE"),
	MinorCity(-600, iBarbarian, (60, 50), "Mastia", iPopulation=2, iCiv=iCelts, units={iDefend: 1, iCounter:1}, adjective="TXT_KEY_ADJECTIVE_CELTIBERIAN"),
	MinorCity(-580, iIndependent2, (123, 39), "Indrapura", iPopulation=2, iCiv=iShu, units={iDefend: 2, iSkirmish: 1}, adjective="TXT_KEY_ADJECTIVE_CHAM"),
	MinorCity(-500, iIndependent2, (68, 53), "Roma", iPopulation=3, iCiv=iGreece, units={iDefend: 1, iCounter: 2, iWork: 1}, adjective="TXT_KEY_CIV_ROME_ADJECTIVE"),
	MinorCity(-500, iNative, (19, 41), "Danibaan", iPopulation=2, iCiv=iMaya, units={iSkirmish: 1}, adjective="TXT_KEY_ADJECTIVE_ZAPOTEC"),
	MinorCity(-490, iBarbarian, (66, 57), "Melpum", iPopulation=2, iCiv=iCelts, units={iHarass: 2}, adjective="TXT_KEY_ADJECTIVE_CELTIC"),
	MinorCity(-280, iBarbarian, (57, 52), "Vaccaei", iPopulation=1, iCiv=iCelts, units={iSkirmish: 1}, iCulture=1, adjective="TXT_KEY_ADJECTIVE_CELTIBERIAN"),
	MinorCity(-250, iBarbarian, (60, 47), "Shigan", iPopulation=2, iCiv=iPhoenicia, units={iShock: 4}, adjective="TXT_KEY_ADJECTIVE_BERBER"),
	MinorCity(-150, iIndependent2, (112, 57), "Jiaohe", iPopulation=1, iCiv=iChina, units={iHarass: 1}, adjective="TXT_KEY_ADJECTIVE_TOCHARIAN"),
	MinorCity(-75, iIndependent, (105, 55), "Kash", iPopulation=2, iCiv=iKushans, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_UIGHUR"),
	MinorCity(-50, iIndependent2, (58, 64), "Londinion", iPopulation=2, iCiv=iCelts, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_CELTIC"),
	MinorCity(50, iBarbarian, (76, 58), "Sarmizegetusa", iPopulation=2, iCiv=iCelts, units={iDefend: 1, iAttack: 2}, adjective="TXT_KEY_ADJECTIVE_DACIAN"),
	MinorCity(300, iIndependent2, (89, 37), "San'a", iPopulation=2, iCiv=iEthiopia, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_YEMENI"),
	MinorCity(400, iIndependent2, (118, 45), "Dali", iPopulation=4, iCiv=iChina, units={iDefend: 3, iShock: 1}, adjective="TXT_KEY_ADJECTIVE_BAI"),
	MinorCity(470, iBarbarian, (65, 62), "Eresburg", iPopulation=2, iCiv=iCelts, units={iDefend: 2, iAttack: 4}, adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	MinorCity(500, iIndependent2, (123, 25), "Sunda Kelapa", iPopulation=3, iCiv=iMalays, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_SUNDANESE"),
	MinorCity(500, iBarbarian, (69, 56), "Venexia", iPopulation=5, iCiv=iRome, units={iDefend: 3}, adjective="TXT_KEY_ADJECTIVE_VENETIAN"),
	MinorCity(500, iBarbarian, (54, 54), "Bracara", iPopulation=2, iCiv=iRome, units={iDefend: 3}, adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	MinorCity(550, iIndependent, tMecca, "Yathrib", iPopulation=2, iCiv=iPersia, units={iDefend: 1, iHarass: 2}, adjective="TXT_KEY_CIV_ARABIA_ADJECTIVE"),
	MinorCity(570, iBarbarian, (72, 59), "Vienna", iPopulation=2, iCiv=iRome, units={iHarass: 5}, adjective="TXT_KEY_ADJECTIVE_AVAR"),
	MinorCity(610, iIndependent, (95, 39), "Nizwa", iPopulation=2, iCiv=iPersia, units={iDefend: 2}, adjective="TXT_KEY_CIV_ARABIA_ADJECTIVE"),
	MinorCity(650, iIndependent2, (66, 65), "Bornhoved", iPopulation=2, iCiv=iCelts, units={iAttack: 2}, adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	MinorCity(700, iNative, (34, 22), "Tiwanaku", iPopulation=1, iCiv=iInca, adjective="TXT_KEY_ADJECTIVE_AYMARA"),
	MinorCity(700, iIndependent2, (71, 36), "Njimi", iPopulation=1, iCiv=iArabia, units={iHarass: 1}, adjective="TXT_KEY_ADJECTIVE_KANURI"),
	#MinorCity(750, iIndependent, (91, 60), "Atil", iPopulation=2, iCiv=iTurks, units={iHarass: 3}, adjective="TXT_KEY_ADJECTIVE_KHAZAR"),
	MinorCity(800, iNative, (30, 34), u"Bacatá", iPopulation=1, iCiv=iInca, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_MUISCA"),
	MinorCity(800, iIndependent, (57, 69), u"Sgàin", iPopulation=2, iCiv=iFrance, units={iDefend: 2, iCounter: 1}, buildings=[iWalls], adjective="TXT_KEY_ADJECTIVE_SCOTTISH"),
	MinorCity(840, iIndependent, (54, 65), u"Áth Cliath", iPopulation=1, iCiv=iCelts, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_IRISH"),
	MinorCity(860, iBarbarian, (76, 59), u"Kolozsvár", iPopulation=3, iCiv=iTurks, units={iHarass: 3}, adjective="TXT_KEY_ADJECTIVE_MAGYAR"),
	MinorCity(860, iIndependent2, (82, 68), u"Holmgarðr", iPopulation=1, iCiv=iRus, units={iDefend: 2}, condition=lambda: not player(iRus).isExisting() and not player(iNorse).isHuman(), adjective="TXT_KEY_CIV_RUS_ADJECTIVE"),
	MinorCity(880, iIndependent, (81, 62), u"Kænugarðr", iPopulation=1, iCiv=iRus, units={iDefend: 2}, condition=lambda: not player(iRus).isExisting(), adjective="TXT_KEY_CIV_RUS_ADJECTIVE"),
	MinorCity(900, iNative, (27, 28), u"Túcume", iPopulation=1, iCiv=iInca, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	MinorCity(900, iNative, (28, 25), "Chan Chan", iPopulation=2, iCiv=iInca, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	MinorCity(900, iIndependent, (87, 29), "Muqdisho", iPopulation=3, iCiv=iSwahili, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	MinorCity(900, iNative, (79, 18), "Zimbabwe", iPopulation=2, units={iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	MinorCity(1000, iBarbarian, (92, 66), "Qazan", iPopulation=2, iCiv=iTurks, units={iHarass: 2}, adjective="TXT_KEY_ADJECTIVE_BULGAR"),
	MinorCity(1000, iBarbarian, (78, 65), "Vil'na", iPopulation=2, iCiv=iPoland, units={iHarass: 3, iDefend: 1}, adjective="TXT_KEY_ADJECTIVE_LITHUANIAN"),
	MinorCity(1000, iNative, (67, 34), "Kano", iPopulation=2, iCiv=iMali, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_HAUSA"),
	MinorCity(1100, iIndependent, (144, 33), "Nan Madol", iPopulation=1),
	MinorCity(1150, iNative, (15, 44), "Ts'intsuntsani", iPopulation=3, iCiv=iToltecs, units={iDefend: 1, iHarass: 2}, bIgnoreRuins=True, adjective="TXT_KEY_ADJECTIVE_PUREPECHA"),
	MinorCity(1180, iIndependent, (66, 31), "Edo", iPopulation=3, iCiv=iMali, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_EDO"),
	MinorCity(1350, iIndependent2, (81, 32), "Bonga", iPopulation=3, iCiv=iEthiopia, units={iDefend: 3}),
	MinorCity(1585, iNative, (74, 23), "Mwimbele", iPopulation=1, units={iSkirmish: 2}, adjective="TXT_KEY_ADJECTIVE_LUBA"),
	MinorCity(1610, iNative, (89, 18), "Antananarivo", iPopulation=1, units={iDefend: 2}, adjective="TXT_KEY_ADJECTIVE_MALAGASY"),
	MinorCity(1635, iBarbarian, (109, 58), "Ghulja", iPopulation=3, iCiv=iTurks, units={iDefend: 2, iHarass: 3}, condition=lambda: not player(iMongols).isExisting(), adjective="TXT_KEY_ADJECTIVE_DZUNGAR"),
	MinorCity(1635, iBarbarian, (119, 61), "Qara Qorum", iPopulation=2, iCiv=iMongols, units={iDefend: 2, iHarass: 3}, condition=lambda: not player(iMongols).isExisting(), adjective="TXT_KEY_ADJECTIVE_MONGOL"),
]

barbarians = [
	Barbarians(-3000, -850, {iBear: 1}, ((65, 62), (132, 73)), 5, ANIMALS),
	Barbarians(-3000, -850, {iWolf: 1}, ((65, 62), (132, 73)), 5, ANIMALS),
	Barbarians(-3000, -1500, {iPanther: 1}, ((54, 11), (84, 41)), 8, ANIMALS),
	Barbarians(-3000, -1500, {iLion: 1}, ((54, 11), (84, 41)), 8, ANIMALS),
	Barbarians(-1500, -850, {iPanther: 1}, ((69, 11), (81, 26)), 8, ANIMALS),
	Barbarians(-1500, -850, {iLion: 1}, ((69, 11), (81, 26)), 8, ANIMALS),
	Barbarians(-3000, -850, {iPanther: 1}, ((101, 33), (113, 45)), 10, ANIMALS),
	Barbarians(-3000, -850, {iLion: 1}, ((101, 33), (113, 45)), 10, ANIMALS),
	Barbarians(-3000, -1500, {iWarrior: 2}, ((79, 56), (103, 62)), 8, NOMADS, target_area=((83, 44), (104, 51)), adjective="TXT_KEY_ADJECTIVE_INDO_EUROPEAN"),
	Barbarians(-2000, -1500, {iWarrior: 2}, ((120, 42), (129, 50)), 7, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(-1800, -1400, {iWarrior: 2}, ((90, 47), (93, 51)), 9, INVADERS, adjective="TXT_KEY_ADJECTIVE_KASSITE"),
	Barbarians(-1800, -1400, {iChariot: 1}, ((82, 44), (84, 45)), 6, INVADERS, target_area=((77, 39), (80, 44)), adjective="TXT_KEY_ADJECTIVE_HYKSOS"),
	Barbarians(-1750, -1300, {iChariot: 2}, ((85, 50), (91, 57)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HURRIAN"),
	Barbarians(-1600, -1000, {iChariot: 1}, ((73, 37), (77, 43)), 9, NOMADS, target_area=((77, 37), (80, 44)), adjective="TXT_KEY_ADJECTIVE_TJEHENU", promotions=(iDesertAdaptation,)),
	Barbarians(-1500, -550, {iWarrior: 1, iSkirmisher: 1}, ((120, 42), (129, 50)), 7, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(-1500, -670, {iChariot: 2}, ((79, 56), (103, 62)), 8, NOMADS, target_area=((83, 44), (104, 51)), adjective="TXT_KEY_ADJECTIVE_IRANIAN"),
	# Barbarians(-1100, -300, {iAxeman: 2}, ((120, 42), (129, 50)), 12, MINORS, adjective="TXT_KEY_ADJECTIVE_SHU"),
	Barbarians(-1500, -500, {iArcher: 1}, ((105, 39), (111, 43)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_GIRIJAN"),
	Barbarians(-1600, -1100, {iChariot: 4}, ((98, 49), (102, 52)), 4, INVADERS, target_area=((99, 41), (105, 48)), adjective="TXT_KEY_ADJECTIVE_VEDIC", promotions=(iMobility, iDesertAdaptation)),
	Barbarians(-1400, -800, {iChariot: 2}, ((115, 54), (129, 59)), 12, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_HU", promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(-1270, -1180, {iGalley: 2, iSpearman: 1, iAxeman: 1, iSacredBand: 1, iMycenaeanMyrmidon: 1}, ((68, 45), (73, 53)), 1, SEA_INVADERS, target_area=((75, 44), (85, 54)), adjective="TXT_KEY_ADJECTIVE_SEA_PEOPLES"),
	Barbarians(-1270, -1160, {iVulture: 2}, ((90, 47), (93, 51)), 7, INVADERS, adjective="TXT_KEY_ADJECTIVE_KASSITE"),
	Barbarians(-900, -650, {iChariot: 1, iWarrior: 2}, ((117, 53), (119, 56)), 7, INVADERS, target_area=((118, 52), (121, 54)), adjective="TXT_KEY_ADJECTIVE_QIANG"),
	#Barbarians(-1000, -100, {iSkirmisher: 1, iAxeman: 1}, ((120, 42), (129, 50)), 7, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(-1200, -600, {iSkirmisher: 1}, ((84, 44), (88, 52)), 7, NOMADS, target_area=((84, 44), (91, 52)), adjective="TXT_KEY_ADJECTIVE_ARAMEAN"),
	Barbarians(-1250, -950, {iLightSwordsman: 1, iAxeman: 1, iSpearman: 1}, ((79, 51), (82, 54)), 5, INVADERS, target_area=((79, 51), (84, 55)), adjective="TXT_KEY_ADJECTIVE_PHRYGIAN"),
	Barbarians(-1100, -780, {iHorseman: 2, iAxeman: 1}, ((85, 54), (92, 60)), 9, INVADERS, target_area=((79, 51), (84, 55)), adjective="TXT_KEY_ADJECTIVE_CIMMERIAN"),
	Barbarians(-1000, 400, {iMedjay: 1}, ((78, 35),	(82, 40)), 8, MINORS, iAlternativeCiv=iNubia, adjective="TXT_KEY_ADJECTIVE_NUBIAN"),
	Barbarians(-800, -300, {iChariot: 2}, ((115, 54), (129, 59)), 12, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_HU", promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(-400, -100, {iHorseman: 2}, ((78, 57), (102, 63)), 8, NOMADS, target_area=((79, 51), (83, 55)), adjective="TXT_KEY_ADJECTIVE_SCYTHIAN"),
	# Barbarians(-650, -50, {iGallicWarrior: 1}, ((56, 55), (75, 61)), 6, INVADERS, target_area=((64, 49), (79, 57))),
	# Barbarians(-650, -50, {iAxeman: 1}, ((69, 56), (78, 61)), 8, INVADERS, target_area=((73, 49), (84, 55)), adjective="TXT_KEY_ADJECTIVE_GALATIAN"),
	Barbarians(-650, -50, {iLightSwordsman: 1}, ((54, 50), (58, 54)), 12, INVADERS, target_area=((54, 48), (62, 54)), adjective="TXT_KEY_ADJECTIVE_CELTIBERIAN"),
	Barbarians(-500, 200, {iSkirmisher: 1}, ((105, 39), (111, 43)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_GIRIJAN"),
	Barbarians(-500, 0, {iAxeman: 1}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(-400, 200, {iNumidianCavalry: 1}, ((57, 43), (66, 47)), 9, NOMADS, target_area=((57, 43), (70, 48))),
	Barbarians(-400, 700, {iSkirmisher: 1}, ((80, 36), (84, 41)), 12, INVADERS, adjective="TXT_KEY_ADJECTIVE_BLEMMYES"),
	Barbarians(-400, 300, {iCamelRider: 1}, ((73, 37), (77, 43)), 9, NOMADS, target_area=((77, 37), (82, 45)), adjective="TXT_KEY_ADJECTIVE_LIBYAN"),
	Barbarians(-400, -150, {iHorseArcher: 3}, ((96, 42), (105, 49)), 9, INVADERS, target_area=((98, 42), (112, 49)), adjective="TXT_KEY_ADJECTIVE_INDO_SCYTHIAN"),
	Barbarians(-350, 200, {iLightSwordsman: 1}, ((113, 47), (117, 54)), 10, MINORS, adjective="TPXT_KEY_ADJECTIVE_TIBETAN"),
	Barbarians(-300, 90, {iHorseArcher: 3}, ((113, 55), (128, 62)), 8, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_XIONGNU", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(-350, 200, {iLightSwordsman: 1}, ((113, 47), (117, 54)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_XIRONG"),
	Barbarians(-300, 300, {iCamelRider: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(-250, 300, {iAxeman: 1}, ((64, 59), (75, 65)), 8, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	Barbarians(-250, 300, {iAxeman: 1}, ((64, 59), (75, 65)), 10, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	# Barbarians(-250, -100, {iHorseArcher: 3, iSavaran: 3, iCatapult: 2, iSwordsman: 2, iArcher: 2}, ((95, 49), (97, 51)), 4, CLOSE_INVADERS, target_area=((87, 45), (91, 50)), adjective="TXT_KEY_CIV_PERSIA_PARTHIAN", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(-200, 100, {iHolkan: 1}, ((19, 38), (25, 44)), 7, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	Barbarians(-200, 200, {iWarGalley: 1}, ((59, 44), (84, 54)), 8, PIRATES),
	Barbarians(-200, 300, {iCamelRider: 1}, ((56, 39), (71, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(-200, 700, {iWarElephant: 1}, ((103, 37), (118, 42)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(-200, 700, {iWarGalley: 1}, ((84, 22), (95, 37)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	#Barbarians(-100, 150, {iSkirmisher: 1, iLightSwordsman: 1}, ((120, 42), (129, 48)), 9, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"), # reduce intensity during "Han golden age"
	Barbarians(-100, 400, {iHorseArcher: 2}, ((79, 58), (88, 63)), 8, NOMADS, target_area=((65, 50), (84, 58)), adjective="TXT_KEY_ADJECTIVE_SARMATIAN"),
	Barbarians(-50, 700, {iWarGalley: 1}, ((54, 42), (69, 50)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(0, 200, {iAxeman: 2}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(0, 800, {iPendekar: 2}, ((116, 37), (119, 43)), 10, NATIVES, target_area=((64, 56), (72, 65)), adjective="TXT_KEY_ADJECTIVE_MON"),
	Barbarians(50, 250, {iHorseArcher: 1, iAxeman: 1}, ((117, 53), (119, 56)), 6, INVADERS, target_area=((118, 52), (121, 54)), adjective="TXT_KEY_ADJECTIVE_QIANG"),
	Barbarians(50, 100, {iHorseArcher: 3}, ((125, 60), (131, 63)), 6, NOMADS, target_area=((123, 55), (129, 61)), adjective="TXT_KEY_ADJECTIVE_XIANBEI", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(100, 500, {iHorseArcher: 3}, ((113, 55), (131, 63)), 7, NOMADS, target_area=((117, 46), (129, 61)), adjective="TXT_KEY_ADJECTIVE_XIANBEI", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(100, 450, {iSwordsman: 3, iAxeman: 2}, ((64, 59), (75, 65)), 3, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_GERMANIC"),
	Barbarians(100, 600, {iHolkan: 1}, ((19, 38), (25, 44)), 6, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	#Barbarians(150, 450, {iSkirmisher: 1, iLightSwordsman: 2}, ((120, 42), (129, 48)), 6, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"), # intensify during crisis period (although it should be fully settled by now)
	Barbarians(200, 1100, {iSwordsman: 1}, ((113, 47), (117, 54)), 10, MINORS, target_area=((112, 57), (123, 56)), adjective="TXT_KEY_ADJECTIVE_TIBETAN"),
	Barbarians(175, 205, {iLightSwordsman: 2, iSwordsman: 1, iSkirmisher: 1, iCatapult: 1}, ((123, 50), (127, 55)), 1, CLOSE_INVADERS, target_area=((121, 49), (127, 53)), adjective="TXT_KEY_ADJECTIVE_YELLOW_TURBAN"),
	Barbarians(175, 205, {iLightSwordsman: 2, iSwordsman: 1, iSkirmisher: 1, iCatapult: 1}, ((123, 50), (127, 55)), 1, CLOSE_INVADERS, target_area=((121, 49), (127, 53)), adjective="TXT_KEY_ADJECTIVE_YELLOW_TURBAN"),
	Barbarians(200, 500, {iSwordsman: 2}, ((101, 37), (112, 45)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_HINDI"),
	Barbarians(200, 400, {iSwordsman: 3, iAxeman: 2}, ((64, 58), (79, 65)), 3, INVADERS, target_area=((57, 51), (79, 61)), adjective="TXT_KEY_ADJECTIVE_GOTHIC"),
	Barbarians(300, 600, {iCamelArcher: 3}, ((56, 39), (73, 44)), 6, INVADERS, target_area=((60, 45), (69, 45)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(300, 600, {iCamelArcher: 2}, ((71, 39), (76, 44)), 6, INVADERS, target_area=((77, 40), (81, 44)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(300, 1500, {iCamelArcher: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(340, 440, {iSwordsman: 3, iAxeman: 4, iCatapult: 1}, ((59, 59), (65, 65)), 3, INVADERS, target_area=((59, 55), (66, 63)), iAlternativeCiv=iFrance, adjective="TXT_KEY_ADJECTIVE_FRANKISH"),
	Barbarians(330, 430, {iSwordsman: 3, iSavaran: 2, iCatapult: 1}, ((64, 59), (75, 65)), 3, INVADERS, target_area=((58, 52), (71, 62)), adjective="TXT_KEY_ADJECTIVE_VANDAL"),
	Barbarians(350, 540, {iSwordsman: 2, iHorseArcher: 1, iAxeman: 2, iCatapult: 1}, ((66, 53), (73, 66)), 3, INVADERS, target_area=((65, 51), (70, 57)), adjective="TXT_KEY_ADJECTIVE_OSTROGOTHIC"),
	Barbarians(340, 420, {iSwordsman: 3, iAxeman: 2, iCatapult: 1}, ((65, 60), (70, 64)), 3, INVADERS, target_area=((54, 49), (62, 58)), iAlternativeCiv=iSpain, adjective="TXT_KEY_ADJECTIVE_VISIGOTHIC"),
	Barbarians(350, 460, {iOghuz: 5, iCatapult: 1, iSwordsman: 1}, ((61, 57), (77, 62)), 2, INVADERS, target_area=((57, 51), (71, 61)), adjective="TXT_KEY_ADJECTIVE_HUNNIC", promotions=(iMobility,)),
	Barbarians(350, 540, {iOghuz: 5}, ((93, 53), (100, 60)), 1, INVADERS, target_area=((92, 44), (102, 52)), adjective="TXT_KEY_ADJECTIVE_HUNA", iAlternativeCiv=iTurks, promotions=(iMobility, iDesertAdaptation, iSteppeAdaptation)), # Hephtalites
	Barbarians(350, 600, {iDogSoldier: 1}, ((11, 44), (19, 51)), 10, NOMADS, iOwner=iNative, target_area=((14, 40), (23, 45)), adjective="TXT_KEY_ADJECTIVE_NAHUA"),
	Barbarians(400, 550, {iGalley: 2, iSwordsman: 4}, ((62, 46), (71, 50)), 2, SEA_INVADERS, target_area=((62, 46), (71, 55)), adjective="TXT_KEY_ADJECTIVE_VANDAL"),
	Barbarians(400, 1000, {iSkirmisher: 2, iSwordsman: 1}, ((120, 42), (129, 48)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_YUE"),
	Barbarians(400, 1200, {iSwordsman: 2}, ((118, 43), (122, 47)), 12, MINORS, adjective="TXT_KEY_ADJECTIVE_BAI"),
	Barbarians(500, 800, {iHorseArcher: 2}, ((105, 54), (123, 61)), 12, NOMADS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_UIGHUR", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(400, 900, {iHorseArcher: 3}, ((113, 55), (128, 62)), 9, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_KHITAN", promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(500, 900, {iOghuz: 3}, ((98, 55), (123, 62)), 8, NOMADS, target_area=((94, 52), (128, 61)), adjective="TXT_KEY_ADJECTIVE_TURKIC", promotions=(iSteppeAdaptation,)),
	Barbarians(500, 1000, {iSkirmisher: 1}, ((137, 56), (140, 62)), 16, NATIVES, target_area=((134, 49), (140, 55)), adjective="TXT_KEY_ADJECTIVE_EMISHI"),
	Barbarians(500, 1800, {iNativeRaider: 2, iNativeArcher: 1, iNativeWarrior: 2}, ((62, 24), (77, 33)), 16, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_BANTU"),
	Barbarians(500, 1900, {iNativeRaider: 2}, ((69, 19), (78, 32)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_BANTU"),
	Barbarians(540, 660, {iSwordsman: 3, iAxeman: 2}, ((69, 57), (72, 60)), 2, INVADERS, target_area=((67, 50), (71, 53)), adjective="TXT_KEY_CIV_ITALY_LOMBARD"),	
	Barbarians(530, 630, {iHorseArcher: 4, iSwordsman: 2}, ((70, 57), (80, 62)), 4, INVADERS, target_area=((65, 52), (72, 59)), adjective="TXT_KEY_ADJECTIVE_AVAR", promotions=(iMobility,)),
	Barbarians(480, 610, {iSwordsman: 3, iAxeman: 2}, ((68, 60), (77, 65)), 6, INVADERS, target_area=((74, 49), (76, 52)), iAlternativeCiv=iBulgaria, adjective="TXT_KEY_ADJECTIVE_SLAVIC"),
	Barbarians(550, 850, {iSwordsman: 3, iAxeman: 2}, ((71, 61), (77, 65)), 7, INVADERS, target_area=((62, 55), (64, 70)), adjective="TXT_KEY_ADJECTIVE_SLAVIC"),
	Barbarians(600, 1000, {iHolkan: 1}, ((19, 38), (25, 44)), 4, NATIVES, adjective="TXT_KEY_ADJECTIVE_MAYA"),
	Barbarians(600, 900, {iDogSoldier: 1, iJaguar: 2}, ((11, 44), (19, 51)), 14, NOMADS, iOwner=iNative, target_area=((14, 40), (23, 45)), adjective="TXT_KEY_ADJECTIVE_NAHUA"),
	Barbarians(600, 1100, {iSkirmisher: 1}, ((54, 33), (57, 38)), 12, NATIVES, iOwner=iNative, target_area=((57, 32), (64, 39)), adjective="TXT_KEY_ADJECTIVE_FULA"),
	Barbarians(560, 610, {iKonnik: 2}, ((78, 57), (82, 61)), 2, NOMADS, target_area=((74, 52), (79, 56)), iAlternativeCiv=iBulgaria, adjective="TXT_KEY_ADJECTIVE_BULGAR", promotions=(iMobility,)),
	#Barbarians(650, 950, {iHorseArcher: 3}, ((85, 57), (92, 63)), 7, NOMADS, target_area=((86, 50), (91, 54)), adjective="TXT_KEY_ADJECTIVE_KHAZAR"),
	Barbarians(700, 1500, {iCamelArcher: 1}, ((56, 39), (76, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(700, 1600, {iHeavyGalley: 1}, ((54, 42), (69, 50)), 8, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(700, 1700, {iHeavyGalley: 1}, ((84, 22), (95, 37)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_SOMALI"),
	Barbarians(750, 950, {iLongship: 1, iAxeman: 2}, ((53, 48), (63, 72)), 6, SEA_INVADERS, adjective="TXT_KEY_ADJECTIVE_VIKING"),
	Barbarians(800, 1200, {iLongbowman: 2, iWarElephant: 1}, ((116, 37), (119, 43)), 8, INVADERS, target_area=((118, 34), (124, 39)), adjective="TXT_KEY_ADJECTIVE_TAI"),
	Barbarians(800, 1100, {iHeavySwordsman: 1}, ((113, 50), (120, 56)), 8, INVADERS, target_area=((112, 57), (123, 56)), adjective="TXT_KEY_ADJECTIVE_TANGUT", condition=is_free_of_civ(iTibet)),
	Barbarians(820, 880, {iHorseArcher: 2}, ((82, 60), (90, 64)), 2, INVADERS, target_area=((65, 57), (72, 61)), adjective="TXT_KEY_ADJECTIVE_MAGYAR"),
	Barbarians(850, 1100, {iHorseArcher: 3}, ((82, 60), (90, 64)), 6, NOMADS, target_area=((73, 49), (84, 66)), adjective="TXT_KEY_ADJECTIVE_PECHENEG"),
	Barbarians(900, 1100, {iKeshik: 4}, ((117, 56), (131, 63)), 6, INVADERS, target_area=((118, 49), (129, 61)), adjective="TXT_KEY_ADJECTIVE_JURCHEN", promotions=(iDesertAdaptation,)),
	Barbarians(900, 1200, {iKonnik: 3}, ((89, 62), (93, 66)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_BULGAR"),
	Barbarians(900, 1150, {iOghuz: 3}, ((92, 53), (112, 65)), 6, NOMADS, target_area=((91, 45), (102, 58)), adjective="TXT_KEY_ADJECTIVE_TURKIC", promotions=(iSteppeAdaptation,)),
	Barbarians(900, 1150, {iSkirmisher: 1}, ((25, 24), (29, 29)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	Barbarians(900, 1100, {iJaguar: 4}, ((11, 44), (19, 51)), 5, INVADERS, iOwner=iNative, target_area=((14, 40), (23, 45)), adjective="TXT_KEY_ADJECTIVE_NAHUA"),
	Barbarians(900, 1200, {iKeshik: 2, iHorseArcher: 2}, ((105, 53), (119, 59)), 6, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_KHITAN", promotions=(iDesertAdaptation, iSteppeAdaptation), condition=is_free_of_civ(iTibet)),
	Barbarians(950, 1100, {iLongship: 1, iHuscarl: 2}, ((53, 48), (63, 72)), 8, SEA_INVADERS, adjective="TXT_KEY_ADJECTIVE_VIKING"),
	Barbarians(1000, 1200, {iHorseArcher: 2}, ((101, 41), (105, 46)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_RAJPUT"),
	Barbarians(1000, 1280, {iAxeman: 2}, ((74, 64), (80, 69)), 10, MINORS, adjective="TXT_KEY_ADJECTIVE_BALTIC"),
	Barbarians(1050, 1400, {iAxeman: 1}, ((75, 17), (80, 23)), 10, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	Barbarians(1050, 1180, {iCamelArcher: 3, iHeavySwordsman: 3, iTrebuchet: 1}, ((56, 39), (58, 49)), 2, CLOSE_INVADERS, target_area=((56, 44), (58, 49)), adjective="TXT_KEY_ADJECTIVE_ALMORAVID", promotions=(iDesertAdaptation,)),
	Barbarians(1100, 1350, {iHorseArcher: 2}, ((115, 38), (120, 45)), 12, INVADERS, adjective="TXT_KEY_ADJECTIVE_SHAN"),
	Barbarians(1100, 1250, {iMamlukCavalry: 1, iHorseArcher: 2}, ((82, 60), (105, 63)), 9, NOMADS, target_area=((73, 49), (84, 66)), adjective="TXT_KEY_ADJECTIVE_CUMAN"),
	Barbarians(1150, 1400, {iAucac: 1}, ((25, 24), (29, 29)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_CHIMU"),
	Barbarians(1200, 1500, {iLancer: 3}, ((101, 41), (105, 46)), 8, MINORS, adjective="TXT_KEY_ADJECTIVE_RAJPUT"),
	Barbarians(1200, 1500, {iHorseArcher: 2}, ((85, 57), (95, 67)), 10, INVADERS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR", iAlternativeCiv=iKhazars),
	Barbarians(1200, 1500, {iLongbowman: 1}, ((87, 69), (96, 74)), 15, NATIVES, adjective="TXT_KEY_ADJECTIVE_KOMI"),
	Barbarians(1200, 1550, {iLongbowman: 2}, ((58, 31), (64, 35)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_AKAN"),
	Barbarians(1200, 1500, {iKeshik: 2}, ((92, 58), (103, 65)), 10, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_NOGAI", iAlternativeCiv=iMongols, promotions=(iSteppeAdaptation,)),
	Barbarians(1200, 1500, {iKeshik: 3}, ((116, 57), (127, 66)), 8, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_MONGOL", iAlternativeCiv=iMongols, promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(1200, 1700, {iFarari: 1}, ((61, 34), (66, 38)), 16, INVADERS, iOwner=iNative, target_area=((54, 33), (66, 39)), adjective="TXT_KEY_ADJECTIVE_SONGHAI"),
	Barbarians(1250, 1450, {iHeavyGalley: 2}, ((125, 44), (134, 57)), 18, PIRATES, adjective="TXT_KEY_ADJECTIVE_WOKOU"),
	Barbarians(1300, 1550, {iJaguar: 2}, ((13, 41), (17, 46)), 12, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_PUREPECHA"),
	Barbarians(1300, 1600, {iDogSoldier: 2}, ((11, 44), (19, 51)), 8, INVADERS, iOwner=iNative, target_area=((13, 41), (19, 47)), adjective="TXT_KEY_ADJECTIVE_CHICHIMECA"),
	Barbarians(1300, 1800, {iHeavySwordsman: 1}, ((54, 33), (58, 38)), 12, NATIVES, adjective="TXT_KEY_ADJECTIVE_WOLOF"),
	Barbarians(1400, 1550, {iKeshik: 1}, ((96, 62), (108, 69)), 10, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR", iAlternativeCiv=iKhazars),
	Barbarians(1400, 1700, {iHeavySwordsman: 1}, ((75, 17), (80, 23)), 10, MINORS, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_SHONA"),
	Barbarians(1400, 1800, {iNativeRaider: 1}, ((71, 11), (81, 17)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_NGUNI"),
	Barbarians(1400, 1550, {iArcher: 2}, ((21, 49), (27, 54)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MUSCOGEE"),
	Barbarians(1415, 1550, {iGhazi: 2, iBombard: 1, iMobileGuard: 1}, ((86, 31), (88, 33)), 5, CLOSE_INVADERS, target_area=((82, 33), (85, 36)), iAlternativeCiv=iArabia, adjective="TXT_KEY_ADJECTIVE_ADAL", promotions=(iDesertAdaptation,)),
	Barbarians(1400, 1650, {iKeshik: 2}, ((105, 58), (115, 64)), 8, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_OIRAT", iAlternativeCiv=iMongols, promotions=(iDesertAdaptation,)),
	Barbarians(1450, 1600, {iSkirmisher: 1}, ((33, 12), (34, 16)), 15, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MAPUCHE"),
	Barbarians(1450, 1700, {iGalleass: 2}, ((125, 44), (134, 57)), 12, PIRATES, adjective="TXT_KEY_ADJECTIVE_WOKOU"),
	Barbarians(1450, 1600, {iArcher: 2}, ((29, 58), (33, 62)), 8, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_ALGONQUIN"),
	Barbarians(1490, 1600, {iKeshik: 4}, ((92, 58), (103, 65)), 5, NOMADS, target_area=((94, 52), (101, 57)), adjective="TXT_KEY_CIV_UZBEKS_ADJECTIVE", iAlternativeCiv=iTurks, promotions=(iDesertAdaptation, iSteppeAdaptation)),
	Barbarians(1500, 1650, {iLongbowman: 1}, ((29, 58), (33, 62)), 8, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_ALGONQUIN", condition=is_new_world_discovered),
	Barbarians(1500, 1650, {iGalleass: 1}, ((114, 27), (128, 35)), 8, PIRATES),
	Barbarians(1480, 1650, {iOromoWarrior: 2}, ((80, 29), (88, 32)), 6, CLOSE_INVADERS, iOwner=iNative, target_area=((80, 32), (85, 36)), promotions=(iDesertAdaptation,)),
	Barbarians(1500, 1650, {iCuirassier: 3}, ((116, 57), (127, 66)), 8, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_MONGOL", iAlternativeCiv=iMongols, promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(1500, 1750, {iCuirassier: 2}, ((85, 57), (95, 67)), 12, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR", promotions=(iSteppeAdaptation,), iAlternativeCiv=iKhazars),
	Barbarians(1500, 1750, {iArcher: 1}, ((40, 17), (47, 26)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_TUPI"),
	Barbarians(1500, 1800, {iCamelGunner: 1}, ((56, 39), (76, 44)), 9, NOMADS, target_area=((54, 34), (76, 48)), adjective="TXT_KEY_ADJECTIVE_BERBER"),
	Barbarians(1500, 1800, {iCamelGunner: 1}, ((86, 38), (91, 45)), 10, NOMADS, target_area=((77, 39), (91, 50)), adjective="TXT_KEY_ADJECTIVE_BEDOUIN"),
	Barbarians(1550, 1800, {iCuirassier: 1}, ((96, 62), (108, 69)), 10, NOMADS, target_area=((80, 59), (95, 70)), adjective="TXT_KEY_ADJECTIVE_TATAR", promotions=(iSteppeAdaptation,), iAlternativeCiv=iKhazars),
Barbarians(1500, 1650, {iLongbowman: 2}, ((21, 49), (27, 54)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MUSCOGEE", condition=is_new_world_discovered),
	Barbarians(1500, 1850, {iCuirassier: 2}, ((92, 57), (109, 64)), 10, NOMADS, target_area=((92, 60), (113, 70)), adjective="TXT_KEY_ADJECTIVE_KAZAKH", promotions=(iSteppeAdaptation,), iAlternativeCiv=iTurks),
	Barbarians(1550, 1900, {iArquebusier: 2}, ((58, 31), (64, 35)), 10, NATIVES, adjective="TXT_KEY_ADJECTIVE_ASHANTI"),
	Barbarians(1550, 1750, {iCuirassier: 2}, ((124, 58), (132, 64)), 6, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_MANCHU"),
	Barbarians(1550, 1650, {iCuirassier: 3, iBombard: 2, iArquebusier: 2}, ((124, 58), (132, 64)), 3, INVADERS, target_area=((117, 46), (129, 59)), iAlternativeCiv=iChina, adjective="TXT_KEY_ADJECTIVE_MANCHU"),
	Barbarians(1600, 1800, {iPombos: 2}, ((70, 20), (77, 25)), 10, INVADERS, iOwner=iNative, target_area=((69, 21), (77, 30)), adjective="TXT_KEY_ADJECTIVE_CHOKWE"),
	Barbarians(1600, 1800, {iPrivateer: 1}, ((23, 39), (38, 47)), 5, PIRATES),
	Barbarians(1600, 1850, {iCorsair: 1}, ((54, 42), (69, 50)), 8, PIRATES, adjective="TXT_KEY_ADJECTIVE_BARBARY"),
	Barbarians(1600, 1900, {iPistolier: 1}, ((32, 10), (37, 15)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MAPUCHE", condition=is_new_world_discovered),
	# Barbarians(1600, 1850, {iMohawk: 1}, ((23, 55), (32, 61)), 8, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_IROQUOIS", condition=is_new_world_discovered),
	Barbarians(1650, 1900, {iPrivateer: 1}, ((114, 27), (128, 35)), 8, PIRATES),
	Barbarians(1650, 1850, {iArquebusier: 2}, ((21, 49), (27, 54)), 12, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_MUSCOGEE", condition=is_new_world_discovered),
	Barbarians(1650, 1740, {iCuirassier: 4}, ((105, 53), (116, 62)), 10, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_DZUNGAR", iAlternativeCiv=iMongols, promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(1700, 1900, {iMountedBrave: 1}, ((14, 56), (23, 62)), 12, NOMADS, iOwner=iNative, target_area=((15, 51), (26, 62)), adjective="TXT_KEY_ADJECTIVE_SIOUX", condition=is_new_world_discovered),
	Barbarians(1720, 1850, {iCuirassier: 2}, ((58, 33), (69, 38)), 8, INVADERS, adjective="TXT_KEY_ADJECTIVE_FULA"),
	Barbarians(1740, 1800, {iHussar: 4}, ((105, 53), (116, 62)), 10, INVADERS, target_area=((117, 46), (129, 59)), adjective="TXT_KEY_ADJECTIVE_DZUNGAR", iAlternativeCiv=iMongols, promotions=(iDesertAdaptation, iSteppeAdaptation,)),
	Barbarians(1800, 1900, {iPikeman: 2}, ((71, 11), (81, 17)), 10, NATIVES, iOwner=iNative, adjective="TXT_KEY_ADJECTIVE_ZULU"),
	Barbarians(1800, 1900, {iMountedBrave: 1}, ((12, 62), (22, 65)), 12, NOMADS, iOwner=iNative, target_area=((15, 57), (26, 66)), adjective="TXT_KEY_ADJECTIVE_CREE"),
	Barbarians(1800, 1900, {iMountedBrave: 1}, ((13, 50), (20, 56)), 9, NOMADS, iOwner=iNative, target_area=((15, 51), (26, 62)), adjective="TXT_KEY_ADJECTIVE_COMANCHE"),
]


@handler("BeginGameTurn")
def onBeginGameTurn():
	for minor_city in minor_cities:
		minor_city.check()
	
	for barbarian in barbarians:
		barbarian.check()
	
	maintainFallenCivilizations()


@handler("unitBuilt")
def assignMinorUnitAdjective(city, unit):
	if not is_minor(city.getOwner()):
		return

	minor_city_adjective = next(minor_city.adjective for minor_city in minor_cities if at(city, minor_city.tile))
	if minor_city_adjective:
		set_unit_adjective(unit, minor_city_adjective)
	

@handler("BeginGameTurn")
def fragmentIndependents():
	if year() >= year(50) and core_periodic(15):
		iLargestMinor = players.independent().maximum(lambda p: player(p).getNumCities())
		iSmallestMinor = players.independent().minimum(lambda p: player(p).getNumCities())
		if player(iLargestMinor).getNumCities() > 2 * player(iSmallestMinor).getNumCities():
			for city in cities.owner(iLargestMinor).sample(3):
				completeCityFlip(city, iSmallestMinor, iLargestMinor, 50, bBarbarianDecay=False, bBarbarianConversion=True, bAlwaysOwnPlots=True, bFlipUnits=True)


@handler("BeginGameTurn")
def checkMinorTechs():
	iMinor = players.civs(iIndependent, iIndependent2, iNative).existing().periodic(8)
	if iMinor:
		updateMinorTechs(iMinor, barbarian())


def maintainFallenCivilizations():
	fallen_civs = civs.major().past_birth().notalive().where(canEverRespawn)
	
	for iFallenCiv in fallen_civs:
		if periodic(20, iFallenCiv):
			fallen_cities = cities.respawn(iFallenCiv).where(is_minor)
			
			if fallen_cities:
				iTechCiv = best_civ_of_same_tech_group(iFallenCiv)
				if iTechCiv < 0:
					iTechCiv = iFallenCiv
				
				if slot(iTechCiv) < 0:
					continue
				
				iNumDesiredUnits = 2 + player(iTechCiv).getCurrentEra() / 2
				bUnique = iFallenCiv == iTechCiv
				iDefender, iDefenseAI = getUnitForRole(iTechCiv, iDefend, bUnique=bUnique)
				
				for city in fallen_cities:
					add_city_buildings(city, iTechCiv)
					
					iNumCurrentUnits = units.at(city).where(CyUnit.canFight).count()
					if iNumCurrentUnits < iNumDesiredUnits:
						makeUnits(city.getOwner(), iDefender, city, iNumDesiredUnits-iNumCurrentUnits, iDefenseAI)
				