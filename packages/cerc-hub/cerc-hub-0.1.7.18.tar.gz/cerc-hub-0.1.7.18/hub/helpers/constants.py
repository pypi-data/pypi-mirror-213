"""
Constant module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

# universal constants

KELVIN = 273.15
WATER_DENSITY = 1000  # kg/m3
WATER_HEAT_CAPACITY = 4182  # J/kgK

AIR_DENSITY = 1.293  # kg/m3
AIR_HEAT_CAPACITY = 1005.2  # J/kgK


# converters
HOUR_TO_MINUTES = 60
MINUTES_TO_SECONDS = 60
HOUR_TO_SECONDS = 3600
METERS_TO_FEET = 3.28084
BTU_H_TO_WATTS = 0.29307107
KILO_WATTS_HOUR_TO_JULES = 3600000
GALLONS_TO_QUBIC_METERS = 0.0037854117954011185

# time
SECOND = 'second'
MINUTE = 'minute'
HOUR = 'hour'
DAY = 'day'
WEEK = 'week'
MONTH = 'month'
YEAR = 'year'

# day types
MONDAY = 'monday'
TUESDAY = 'tuesday'
WEDNESDAY = 'wednesday'
THURSDAY = 'thursday'
FRIDAY = 'friday'
SATURDAY = 'saturday'
SUNDAY = 'sunday'
HOLIDAY = 'holiday'
WINTER_DESIGN_DAY = 'winter_design_day'
SUMMER_DESIGN_DAY = 'summer_design_day'
WEEK_DAYS = 'Weekdays'
WEEK_ENDS = 'Weekends'
ALL_DAYS = 'Alldays'

DAYS_A_MONTH = {'monday': [5, 4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 5],
                'tuesday': [5, 4, 4, 4, 5, 4, 5, 4, 4, 5, 4, 4],
                'wednesday': [5, 4, 4, 4, 5, 4, 4, 5, 4, 5, 4, 4],
                'thursday': [4, 4, 5, 4, 5, 4, 4, 5, 4, 4, 5, 4],
                'friday': [4, 4, 5, 4, 4, 5, 4, 5, 4, 4, 5, 4],
                'saturday': [4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 5],
                'sunday': [4, 4, 4, 5, 4, 4, 5, 4, 5, 4, 4, 5],
                'holiday': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

DAYS_A_YEAR = {'monday': 51,
               'tuesday': 50,
               'wednesday': 50,
               'thursday': 50,
               'friday': 50,
               'saturday': 52,
               'sunday': 52,
               'holiday': 10}

# data types
ANY_NUMBER = 'any_number'
FRACTION = 'fraction'
ON_OFF = 'on_off'
TEMPERATURE = 'temperature'
HUMIDITY = 'humidity'
CONTROL_TYPE = 'control_type'
CONTINUOUS = 'continuous'
DISCRETE = 'discrete'
CONSTANT = 'constant'
INTERNAL_GAINS = 'internal_gains'

# surface types
WALL = 'Wall'
GROUND_WALL = 'Ground wall'
GROUND = 'Ground'
ATTIC_FLOOR = 'Attic floor'
ROOF = 'Roof'
INTERIOR_SLAB = 'Interior slab'
INTERIOR_WALL = 'Interior wall'
VIRTUAL_INTERNAL = 'Virtual internal'
WINDOW = 'Window'
DOOR = 'Door'
SKYLIGHT = 'Skylight'

# functions and usages
RESIDENTIAL = 'residential'
SINGLE_FAMILY_HOUSE = 'single family house'
MULTI_FAMILY_HOUSE = 'multifamily house'
ROW_HOUSE = 'row house'
MID_RISE_APARTMENT = 'mid rise apartment'
HIGH_RISE_APARTMENT = 'high rise apartment'
OFFICE_AND_ADMINISTRATION = 'office and administration'
SMALL_OFFICE = 'small office'
MEDIUM_OFFICE = 'medium office'
LARGE_OFFICE = 'large office'
COURTHOUSE = 'courthouse'
FIRE_STATION = 'fire station'
PENITENTIARY = 'penitentiary'
POLICE_STATION = 'police station'
POST_OFFICE = 'post office'
LIBRARY = 'library'
EDUCATION = 'education'
PRIMARY_SCHOOL = 'primary school'
PRIMARY_SCHOOL_WITH_SHOWER = 'school with shower'
SECONDARY_SCHOOL = 'secondary school'
UNIVERSITY = 'university'
LABORATORY_AND_RESEARCH_CENTER = 'laboratory and research centers'
STAND_ALONE_RETAIL = 'stand alone retail'
HOSPITAL = 'hospital'
OUT_PATIENT_HEALTH_CARE = 'out-patient health care'
HEALTH_CARE = 'health care'
RETIREMENT_HOME_OR_ORPHANAGE = 'retirement home or orphanage'
COMMERCIAL = 'commercial'
STRIP_MALL = 'strip mall'
SUPERMARKET = 'supermarket'
RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD = 'retail shop without refrigerated food'
RETAIL_SHOP_WITH_REFRIGERATED_FOOD = 'retail shop with refrigerated food'
RESTAURANT = 'restaurant'
QUICK_SERVICE_RESTAURANT = 'quick service restaurant'
FULL_SERVICE_RESTAURANT = 'full service restaurant'
HOTEL = 'hotel'
HOTEL_MEDIUM_CLASS = 'hotel medium class'
SMALL_HOTEL = 'small hotel'
LARGE_HOTEL = 'large hotel'
DORMITORY = 'dormitory'
EVENT_LOCATION = 'event location'
CONVENTION_CENTER = 'convention center'
HALL = 'hall'
GREEN_HOUSE = 'green house'
INDUSTRY = 'industry'
WORKSHOP = 'workshop'
WAREHOUSE = 'warehouse'
WAREHOUSE_REFRIGERATED = 'warehouse refrigerated'
SPORTS_LOCATION = 'sports location'
SPORTS_ARENA = 'sports arena'
GYMNASIUM = 'gymnasium'
MOTION_PICTURE_THEATRE = 'motion picture theatre'
MUSEUM = 'museum'
PERFORMING_ARTS_THEATRE = 'performing arts theatre'
TRANSPORTATION = 'transportation'
AUTOMOTIVE_FACILITY = 'automotive facility'
PARKING_GARAGE = 'parking garage'
RELIGIOUS = 'religious'
NON_HEATED = 'non-heated'
DATACENTER = 'datacenter'

LIGHTING = 'Lights'
OCCUPANCY = 'Occupancy'
APPLIANCES = 'Appliances'
HVAC_AVAILABILITY = 'HVAC Avail'
INFILTRATION = 'Infiltration'
VENTILATION = 'Ventilation'
COOLING_SET_POINT = 'ClgSetPt'
HEATING_SET_POINT = 'HtgSetPt'
EQUIPMENT = 'Equipment'
ACTIVITY = 'Activity'
PEOPLE_ACTIVITY_LEVEL = 'People Activity Level'
DOMESTIC_HOT_WATER = 'Domestic Hot Water'
HEATING = 'Heating'
COOLING = 'Cooling'
ELECTRICITY = 'Electricity'
RENEWABLE = 'Renewable'
WOOD = 'Wood'
GAS = 'Gas'
DIESEL = 'Diesel'
COAL = 'Coal'
AIR = 'Air'
WATER = 'Water'
GEOTHERMAL = 'Geothermal'
DISTRICT_HEATING_NETWORK = 'District Heating'
GRID = 'Grid'
ONSITE_ELECTRICITY = 'Onsite Electricity'
PHOTOVOLTAIC = 'Photovoltaic'
BOILER = 'Boiler'
HEAT_PUMP = 'Heat Pump'
BASEBOARD = 'Baseboard'
CHILLER = 'Chiller'

# Geometry
EPSILON = 0.0000001

# HVAC types
ONLY_HEATING = 'Heating'
ONLY_COOLING = 'Colling'
ONLY_VENTILATION = 'Ventilation'
HEATING_AND_VENTILATION = 'Heating and ventilation'
COOLING_AND_VENTILATION = 'Cooling and ventilation'
HEATING_AND_COLLING = 'Heating and cooling'
FULL_HVAC = 'Heating and cooling and ventilation'

# Floats
MAX_FLOAT = float('inf')
MIN_FLOAT = float('-inf')

# Tools
SRA = 'sra'
INSEL_MEB = 'insel meb'

# Costs units
CURRENCY_PER_SQM = 'currency/m2'
CURRENCY_PER_CBM = 'currency/m3'
CURRENCY_PER_KW = 'currency/kW'
CURRENCY_PER_KWH = 'currency/kWh'
CURRENCY_PER_MONTH = 'currency/month'
CURRENCY_PER_LITRE = 'currency/l'
CURRENCY_PER_KG = 'currency/kg'
CURRENCY_PER_CBM_PER_HOUR = 'currency/(m3/h)'
PERCENTAGE = '%'

# Costs chapters
SUPERSTRUCTURE = 'B_shell'
ENVELOPE = 'D_services'
ALLOWANCES_OVERHEAD_PROFIT = 'Z_allowances_overhead_profit'
