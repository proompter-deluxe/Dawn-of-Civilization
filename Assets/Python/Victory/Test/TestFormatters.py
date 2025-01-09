from Formatters import *
from Goals import *
from Requirements import *

from TestVictoryCommon import *


class TestTextProcessing(ExtendedTestCase):
	
	def test_number_word_a(self):
		result = number_word(1)
		
		self.assertEqual(result, "a")
	
	def test_number_word_two(self):
		result = number_word(2)
		
		self.assertEqual(result, "two")
	
	def test_number_word_ten(self):
		result = number_word(10)
		
		self.assertEqual(result, "ten")
	
	def test_number_word_twenty(self):
		result = number_word(20)
		
		self.assertEqual(result, "20")
	
	def test_ordinal_word_first(self):
		self.assertEqual(ordinal_word(1), "first")
	
	def test_ordinal_word_100th(self):
		self.assertEqual(ordinal_word(100), "100th")
	
	def test_plural(self):
		result = plural("word")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_s(self):
		result = plural("words")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_y(self):
		result = plural("library")
		
		self.assertEqual(result, "libraries")
	
	def test_plural_ends_with_ch(self):
		self.assertEqual(plural("church"), "churches")
	
	def test_plural_ends_with_sh(self):
		self.assertEqual(plural("marsh"), "marshes")
	
	def test_plural_ends_with_man(self):
		self.assertEqual(plural("swordsman"), "swordsmen")
	
	def test_plural_irregular(self):
		self.assertEqual(plural("Ship of the Line"), "Ships of the Line")
		self.assertEqual(plural("Great Statesman"), "Great Statesmen")
		self.assertEqual(plural("cathedral of your state religion"), "cathedrals of your state religion")

	def test_format_articles(self):
		self.assertEqual(format_articles("The Internet"), "the Internet")
		self.assertEqual(format_articles("the Internet"), "the Internet")
		self.assertEqual(format_articles("Swordsman"), "Swordsman")
	
	def test_capitalize(self):
		self.assertEqual(capitalize("hello"), "Hello")
	
	def test_capitalize_multiple_words(self):
		self.assertEqual(capitalize("hello world"), "Hello world")
	
	def test_capitalize_already_capital(self):
		self.assertEqual(capitalize("Hello World"), "Hello World")
	
	def test_capitalize_single_character(self):
		self.assertEqual(capitalize("a"), "A")
	
	def test_capitalize_empty(self):
		self.assertEqual(capitalize(""), "")
	
	def test_in_area(self):
		self.assertEqual(in_area("this is a sentence", plots.rectangle((10, 10), (20, 20)).named("Test Area")), "this is a sentence in Test Area")
	
	def test_in_area_none(self):
		self.assertEqual(in_area("this is a sentence", None), "this is a sentence")
	
	def test_format_date_turn_before(self):
		self.assertEqual(format_date_turn(-1000, False), "1000 BC")
	
	def test_format_date_turn_after(self):
		self.assertEqual(format_date_turn(1000, False), "1000 AD")
	
	def test_format_date_turn(self):
		self.assertEqual(format_date_turn(1000, True), "1000 AD (Turn 270)")
	
	def test_remove_articles(self):
		self.assertEqual(remove_articles("the Mediterranean"), "Mediterranean")


class StringProgress(object):

	def progress(self, evaluator):
		return "string"


class ListProgress(object):

	def progress(self, evaluator):
		return ["one", "two", "three"]


class TestProgressFormatter(ExtendedTestCase):

	def setUp(self):
		self.progress = ProgressFormatter()
		
		self.string_progress = StringProgress()
		self.list_progress = ListProgress()
		
		self.evaluator = SelfEvaluator(self.iPlayer)
	
	def test_get_row_size(self):
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 2), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 3), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 4), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 5), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 6), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 7), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 8), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 9), 3)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 10), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 11), 4)
		self.assertEqual(self.progress.get_row_size([self.string_progress] * 12), 4)
	
	def test_get_item_progress_single(self):
		self.assertEqual(self.progress.get_item_progress([self.string_progress] * 5, self.evaluator), ["string"] * 5)
	
	def test_get_item_progress_list(self):
		self.assertEqual(self.progress.get_item_progress([self.list_progress], self.evaluator), [])
	
	def test_format_items(self):
		self.assertEqual(list(self.progress.format_items([self.string_progress] * 5, self.evaluator)), ["string string string", "string string"])

	def test_format_items_list(self):
		self.assertEqual(list(self.progress.format_items([self.list_progress], self.evaluator)), [])
	
	def test_format_list(self):
		self.assertEqual(list(self.progress.format_list([self.list_progress] * 2, self.evaluator)), ["one", "two", "three", "one", "two", "three"])
	
	def test_format_list_string(self):
		self.assertEqual(list(self.progress.format_list([self.string_progress] * 3, self.evaluator)), [])
	
	def test_format_with_list(self):
		self.assertEqual(self.progress.format([self.list_progress] * 2, self.evaluator), ["one", "two", "three", "one", "two", "three"])
	
	def test_format_with_string(self):
		self.assertEqual(self.progress.format([self.string_progress] * 5, self.evaluator), ["string string string", "string string"])
	
	def test_format_mixed(self):
		self.assertEqual(self.progress.format([self.string_progress] * 5 + [self.list_progress], self.evaluator), ["one", "two", "three", "string string string", "string string"])


class TestDescription(ExtendedTestCase):
	
	def setUp(self):
		self.description = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
	
	def test_repr(self):
		self.assertEqual(repr(self.description), "Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three'))")
	
	def test_str(self):
		self.assertEqual(str(self.description), "Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three'))")
	
	def test_format(self):
		self.assertEqual(self.description.format(), "three Libraries")
	
	def test_matches(self):
		identical = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		different_key = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		different_arguments = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "three")
		
		self.assertEqual(self.description.matches(identical), False)
		self.assertEqual(self.description.matches(different_key), False)
		self.assertEqual(self.description.matches(different_arguments), False)
	
	def test_unwrap(self):
		self.assertEqual(self.description.unwrap(), [self.description])


class TestWrappedDescription(ExtendedTestCase):
	
	def setUp(self):
		self.wrapped = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		self.description = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", self.wrapped, "your capital")

	def test_repr(self):
		self.assertEqual(repr(self.description), "WrappedDescription(key=TXT_KEY_VICTORY_DESC_BUILD_IN_CITY, description=Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three')), arguments=('your capital',))")
	
	def test_str(self):
		self.assertEqual(str(self.description), "WrappedDescription(key=TXT_KEY_VICTORY_DESC_BUILD_IN_CITY, description=Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three')), arguments=('your capital',))")
	
	def test_format(self):
		self.assertEqual(self.description.format(), "build three Libraries in your capital")
	
	def test_matches(self):
		identical = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), "your capital")
		different_description = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four"), "your capital")
		different_key = WrappedDescription("TXT_KEY_VICTORY_DESC_HAVE", Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), "your capital")
		different_arguments = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), "another capital")
		different_type = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
	
		self.assertEqual(self.description.matches(identical), True)
		self.assertEqual(self.description.matches(different_description), True)
		self.assertEqual(self.description.matches(different_key), False)
		self.assertEqual(self.description.matches(different_arguments), False)
		self.assertEqual(self.description.matches(different_type), False)
	
	def test_unwrap(self):
		self.assertEqual(self.description.unwrap(), [self.description])


class TestCombinedDescription(ExtendedTestCase):
	
	def setUp(self):
		self.first = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		self.second = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four")
		self.third = Description("TXT_KEY_VICTORY_DESC_COUNT", "Markets", "five")
		
		self.description = CombinedDescription([self.first, self.second, self.third])
	
	def test_repr(self):
		self.assertEqual(repr(self.description), "CombinedDescription([Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three')), Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Granaries', 'four')), Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Markets', 'five'))])")
	
	def test_str(self):
		self.assertEqual(str(self.description), "CombinedDescription([Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Libraries', 'three')), Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Granaries', 'four')), Description(key=TXT_KEY_VICTORY_DESC_COUNT, arguments=('Markets', 'five'))])")
	
	def test_format(self):
		self.assertEqual(self.description.format(), "three Libraries, four Granaries and five Markets")
	
	def test_matches(self):
		identical = CombinedDescription([Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Markets", "five")])
		different = CombinedDescription([Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Walls", "two")])
		
		self.assertEqual(self.description.matches(identical), False)
		self.assertEqual(self.description.matches(different), False)
	
	def test_unwrap(self):
		self.assertEqual(self.description.unwrap(), [self.first, self.second, self.third])


class TestCombineDescriptions(ExtendedTestCase):
	
	def test_combine_descriptions(self):
		first = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		second = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four")
		third = Description("TXT_KEY_VICTORY_DESC_COUNT", "Markets", "five")
		
		self.assertEqual(combine_descriptions([first, second, third]), CombinedDescription([first, second, third]))
	
	def test_combine_single_description(self):
		description = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		
		self.assertEqual(combine_descriptions([description]), description)
	
	def test_combine_wrapped_matching(self):
		wrapped_first = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_first, "your capital")
		
		wrapped_second = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four")
		second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_second, "your capital")
		
		self.assertEqual(combine_descriptions([first, second]), WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", CombinedDescription([wrapped_first, wrapped_second]), "your capital"))
	
	def test_combine_wrapped_not_matching(self):
		wrapped_first = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_first, "your capital")
		
		wrapped_second = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four")
		second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_second, "another capital")
		
		self.assertEqual(combine_descriptions([first, second]), CombinedDescription([first, second]))
	
	def test_combine_wrapped_nested_matching(self):
		nested_wrapped_first = Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three")
		wrapped_first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", nested_wrapped_first, "your capital")
		first = WrappedDescription("TXT_KEY_VICTORY_SUFFIX", wrapped_first, "in 1000 AD")
		
		nested_wrapped_second = Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four")
		wrapped_second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", nested_wrapped_second, "your capital")
		second = WrappedDescription("TXT_KEY_VICTORY_SUFFIX", wrapped_second, "in 1000 AD")
		
		self.assertEqual(combine_descriptions([first, second]), WrappedDescription("TXT_KEY_VICTORY_SUFFIX", WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", CombinedDescription([nested_wrapped_first, nested_wrapped_second]), "your capital"), "in 1000 AD"))
	
	def test_combine_wrapped_nested_not_matching(self):
		nested_wrapped_first = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		wrapped_first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", nested_wrapped_first, "your capital")
		first = WrappedDescription("TXT_KEY_VICTORY_SUFFIX", wrapped_first, "in 1000 AD")
		
		nested_wrapped_second = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four")
		wrapped_second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", nested_wrapped_second, "another capital")
		second = WrappedDescription("TXT_KEY_VICTORY_SUFFIX", wrapped_second, "in 1000 AD")
		
		self.assertEqual(combine_descriptions([first, second]), WrappedDescription("TXT_KEY_VICTORY_SUFFIX", CombinedDescription([wrapped_first, wrapped_second]), "in 1000 AD"))
	
	def test_combine_wrapped_combined_and_wrapped(self):
		wrapped_first = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_first, "your capital")
		
		wrapped_second_1 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four")
		wrapped_second_2 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Markets", "five")
		wrapped_second = CombinedDescription([wrapped_second_1, wrapped_second_2])
		second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_second, "your capital")
		
		self.assertEqual(combine_descriptions([first, second]), WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", CombinedDescription([wrapped_first, wrapped_second_1, wrapped_second_2]), "your capital"))
	
	def test_combine_wrapped_combined_and_combined(self):
		wrapped_first_1 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Walls", "two")
		wrapped_first_2 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		wrapped_first = CombinedDescription([wrapped_first_1, wrapped_first_2])
		first = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_first, "your capital")
		
		wrapped_second_1 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four")
		wrapped_second_2 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Markets", "five")
		wrapped_second = CombinedDescription([wrapped_second_1, wrapped_second_2])
		second = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped_second, "your capital")
		
		self.assertEqual(combine_descriptions([first, second]), WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", CombinedDescription([wrapped_first_1, wrapped_first_2, wrapped_second_1, wrapped_second_2]), "your capital"))

	def test_combine_wrapped_single(self):
		wrapped = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		description = WrappedDescription("TXT_KEY_VICTORY_DESC_BUILD_IN_CITY", wrapped, "your capital")
		
		self.assertEqual(combine_descriptions([description]), description)
	
	def test_combine_combined(self):
		wrapped_first_1 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Walls", "two")
		wrapped_first_2 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		first = CombinedDescription([wrapped_first_1, wrapped_first_2])
		
		wrapped_second_1 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four")
		wrapped_second_2 = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Markets", "five")
		second = CombinedDescription([wrapped_first_1, wrapped_first_2])
		
		self.assertEqual(combine_descriptions([first, second]), CombinedDescription([first, second]))
	
	def test_combine_combined_single(self):
		wrapped_first = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Libraries", "three")
		wrapped_second = Description("TXT_KEY_VICTORY_DESC_CITY_BUILDING_COUNT", "Granaries", "four")
		description = CombinedDescription([wrapped_first, wrapped_second])
		
		self.assertEqual(combine_descriptions([description]), description)
	

class TestCombineEntries(ExtendedTestCase):
	
	def test_requirements(self):
		first = BuildingCount(iLibrary, 3)
		second = BuildingCount(iGranary, 4)
		third = BuildingCount(iMarket, 5)
		
		self.assertEqual(combine_entries([first, second, third]), CombinedDescription([Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Markets", "five")]))
	
	def test_goals(self):
		first = Goal([BuildingCount(iLibrary, 3).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		second = Goal([BuildingCount(iGranary, 4).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		third = Goal([BuildingCount(iMarket, 5).create()], "TXT_KEY_VICTORY_DESC_HAVE", 0)
		
		self.assertEqual(combine_entries([first, second, third]), WrappedDescription("TXT_KEY_VICTORY_DESC_HAVE", CombinedDescription([Description("TXT_KEY_VICTORY_DESC_COUNT", "Libraries", "three"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Granaries", "four"), Description("TXT_KEY_VICTORY_DESC_COUNT", "Markets", "five")])))


class TestGenerateDescription(ExtendedTestCase):
	
	def setUp(self):
		self.requirements = [
			CitySpecialistCount(CapitalCityArgument().named("your capital"), iSpecialistGreatArtist, 3),
			CitySpecialistCount(CapitalCityArgument().named("your capital"), iSpecialistGreatMerchant, 4),
			CitySpecialistCount(CapitalCityArgument().named("your capital"), iSpecialistGreatScientist, 5),
		]
		self.goals = [Goal([requirement.create()], "TXT_KEY_VICTORY_DESC_SETTLE", 0) for requirement in self.requirements]
		
		self.requirement_descs = [
			Description("TXT_KEY_VICTORY_DESC_CITY_SPECIALIST_COUNT", "your capital", "Great Artists", "three"),
			Description("TXT_KEY_VICTORY_DESC_CITY_SPECIALIST_COUNT", "your capital", "Great Merchants", "four"),
			Description("TXT_KEY_VICTORY_DESC_CITY_SPECIALIST_COUNT", "your capital", "Great Scientists", "five"),
		]
		self.goal_descs = [WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", desc, "your capital") for desc in self.requirements]
		
	def test_generate_description_requirements(self):
		self.assertEqual(generate_description(self.requirements, "TXT_KEY_VICTORY_DESC_SETTLE", ["your capital"], [], None), WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", CombinedDescription(self.requirement_descs), "your capital"))
	
	def test_generate_description_requirements_suffix(self):
		self.assertEqual(generate_description(self.requirements, "TXT_KEY_VICTORY_DESC_SETTLE", ["your capital"], ["in 1000 AD"], None), WrappedDescription("TXT_KEY_VICTORY_SUFFIX", WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", CombinedDescription(self.requirement_descs), "your capital"), "in 1000 AD"))
	
	def test_generate_description_requirements_required(self):
		self.assertEqual(generate_description(self.requirements, "TXT_KEY_VICTORY_DESC_SETTLE", ["your capital"], [], 2), WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", WrappedDescription("TXT_KEY_VICTORY_REQUIRED_OUT_OF", CombinedDescription(self.requirement_descs), "two"), "your capital"))
	
	def test_generate_description_goals(self):
		self.assertEqual(generate_description(self.goals, None, ["your capital"], [], None), WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", CombinedDescription(self.requirement_descs)))

	def test_generate_description_goals_suffix(self):
		self.assertEqual(generate_description(self.goals, None, ["your capital"], ["in 1000 AD"], None), WrappedDescription("TXT_KEY_VICTORY_SUFFIX", WrappedDescription("TXT_KEY_VICTORY_DESC_SETTLE", CombinedDescription(self.requirement_descs)), "in 1000 AD"))
	

test_cases = [
	TestTextProcessing,
	TestProgressFormatter,
	TestDescription,
	TestWrappedDescription,
	TestCombinedDescription,
	TestCombineDescriptions,
	TestCombineEntries,
	TestGenerateDescription,
]
