
json_scenario_1_zipcodestack = """
{
	"message": "You used all your monthly requests. Please upgrade your plan at https://app.zipcodestack.com/subscription"
}
"""

json_scenario_2_zipcodebase = """
{
	"query": {
		"city": "not existing city",  <--- Not existing city
		"state": null,
		"country": "CZ"
	},
	"results": []  <--- No data
}
"""

json_scenario_2_zipcodestack = """
{
	"query": {
		"codes": [
		"00000"  <--- Not existing ZIP code
		],
		"country": "CZ"
	},
	"results": {}  <--- No data
}
"""

# For visibility the API structure from zipcodebase.com
json_api_structure_zipcodebase = """
{
	"query": {
		"city": "zlin",
		"state": null,
		"country": "CZ"
	},
	"results": [
		"760 01",
		"760 07",
	]
}
"""

# For visibility the API structure from zipcodestack.com 
json_api_structure_zipcodestack = """
{
  "query": {
    "codes": [
      "25163",
      "11000",
      "14021"
    ],
    "country": "CZ"
  },
  "results": {
    "25163": [
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9333,
        "longitude": 14.6667,
        "city": "Vidovice",
        "state": "Středočeský kraj",
        "city_en": "Vidovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.7,
        "city": "Menčice",
        "state": "Středočeský kraj",
        "city_en": "Menčice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Svojšovice",
        "state": "Středočeský kraj",
        "city_en": "Svojšovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9667,
        "longitude": 14.65,
        "city": "Otice",
        "state": "Středočeský kraj",
        "city_en": "Otice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9667,
        "longitude": 14.6833,
        "city": "Všestary",
        "state": "Středočeský kraj",
        "city_en": "Všestary",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.65,
        "city": "Všechromy",
        "state": "Středočeský kraj",
        "city_en": "Všechromy",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6833,
        "city": "Strančice",
        "state": "Středočeský kraj",
        "city_en": "Strančice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6333,
        "city": "Předboř",
        "state": "Středočeský kraj",
        "city_en": "Předboř",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9333,
        "longitude": 14.6667,
        "city": "Kunice",
        "state": "Středočeský kraj",
        "city_en": "Kunice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Sklenka",
        "state": "Středočeský kraj",
        "city_en": "Sklenka",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Kašovice",
        "state": "Středočeský kraj",
        "city_en": "Kašovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      }
    ],
    "11000": [
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Josefov",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Josefov",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3333,
        "longitude": 15.9167,
        "city": "Josefov",
        "state": "Hlavní město Praha",
        "city_en": "Josefov",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.4,
        "longitude": 16.1667,
        "city": "Staré Město",
        "state": "Hlavní město Praha",
        "city_en": "Staré Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Nové Město",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Nové Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Vinohrady",
        "state": "Hlavní město Praha",
        "city_en": "Vinohrady",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Vinohrady",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Vinohrady",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Nové Město",
        "state": "Hlavní město Praha",
        "city_en": "Nové Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Staré Město",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Staré Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      }
    ]
  }
}
"""