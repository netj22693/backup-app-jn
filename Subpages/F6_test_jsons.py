

# API 1
def TEST_get_request_1(city,country):

    json_data_api_1 ={
            "query": {
                "city": city,
                "state": "null",
                "country": country
            },
            "results": [
                "251 63",
                "110 00",
                "140 21",
                "140 78",
                "144 00",
            ]
        }
    
    return json_data_api_1

# API 2
def TEST_get_request(codes,country):

    data_json = {
	"query": {
		"codes": [
			codes
		],
		"country": country
	},
	"results": {
		"110007": [
			{
				"postal_code": "110 008888",
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
				"postal_code": "110 007777",
				"country_code": "CZ",
				"latitude": 50.3333,
				"longitude": 15.9167,
				"city": "Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			}
		],
        "9999": [
			{
				"postal_code": "123",
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
				"postal_code": "456",
				"country_code": "CZ",
				"latitude": 50.3333,
				"longitude": 15.9167,
				"city": "Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			}
		]
	}
}
  

    return data_json

test_JSON_GLOBAL =  TEST_get_request(1,2)