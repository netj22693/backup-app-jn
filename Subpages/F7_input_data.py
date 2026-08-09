# Rounding in the function 
ROUND_TO = 2

# Unit distance
UNIT_DISTANCE = 30

# Transport type speed - km/h
TRANSPORT_SPEED = {
    "truck": 70,
    "train": 80,
    "airplane": 700,
}


# type of transport
tranport_types_list = ['Truck','Train','Airplane']


# List of cities with coordinates and types of transport availability
dataset_cities = ({
"cz" : {
    "Prague" : {"big" : ["4","10"], "small" : ["10","29"], "train":"y", "air":"y"},
    "Brno" : {"big" : ["5","12"], "small" : ["14","35"], "train":"y", "air":"y"},
    "Olomouc" : {"big" : ["4","13"], "small" : ["12","37"], "train":"n", "air":"n"},
    "Plzen" : {"big" : ["4","9"], "small" : ["12","26"], "train":"n", "air":"n"},
    "Tabor" : {"big" : ["5","10"], "small" : ["13","30"], "train":"n", "air":"n"},
    "Ostrava" : {"big" : ["4","13"], "small" : ["11","39"], "train":"y", "air":"n"},
    "Liberec" : {"big" : ["3","11"], "small" : ["7","31"], "train":"n", "air":"n"},
    "Hradec Kralove" : {"big" : ["4","11"], "small" : ["10","33"], "train":"n", "air":"n"},
    "Pardubice" : {"big" : ["4","11"], "small" : ["10","33"], "train":"y", "air":"y"},
    "Zlin" : {"big" : ["5","13"], "small" : ["14","38"], "train":"n", "air":"n"},
    "Chomutov" : {"big" : ["3","9"], "small" : ["9","26"], "train":"n", "air":"n"},
    "Ceske Budejovice" : {"big" : ["5","10"], "small" : ["15","29"], "train":"n", "air":"n"},
    "Teplice" : {"big" : ["3","9"], "small" : ["8","27"], "train":"n", "air":"n"},
    "Most" : {"big" : ["3","9"], "small" : ["8","27"], "train":"y", "air":"n"},
    "Karlovy Vary" : {"big" : ["3","9"], "small" : ["9","25"], "train":"n", "air":"n"},
    "Kolin" : {"big" : ["4","11"], "small" : ["10","31"], "train":"y", "air":"n"},
    "Ceska Trebova" : {"big" : ["4","12"], "small" : ["11","34"], "train":"y", "air":"n"},
    "Jihlava" : {"big" : ["5","11"], "small" : ["13","31"], "train":"n", "air":"n"},
    "Pisek" : {"big" : ["5","10"], "small" : ["13","28"], "train":"y", "air":"n"},
    # "TEST1" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
    # "TEST2" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
    # "TEST3" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"y"},
    # "TEST4" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
},
"sk" : {
	"Bratislava" : {"big" : ["6","12"], "small" : ["18","36"], "train":"y", "air":"y"},
    "Kosice" : {"big" : ["6","16"], "small" : ["16","47"], "train":"y", "air":"y"},
    "Banska Bystrica" : {"big" : ["6","14"], "small" : ["16","40"], "train":"n", "air":"n"}, # tady jsem skoncil
    "Zilina" : {"big" : ["3","7"], "small" : ["14","40"], "train":"y", "air":"n"},	
    "Presov" : {"big" : ["5","16"], "small" : ["15","47"], "train":"n", "air":"n"},	
    "Trnava" : {"big" : ["6","13"], "small" : ["17","39"], "train":"y", "air":"n"},	
    "Trencin" : {"big" : ["5","13"], "small" : ["15","39"], "train":"n", "air":"n"},	
    "Poprad" : {"big" : ["5","15"], "small" : ["14","44"], "train":"y", "air":"n"},	
    "Banska Stiavnica" : {"big" : ["6","14"], "small" : ["17","41"], "train":"n", "air":"n"},
    # "TEST_S1" : {"big" : ["5","7"], "small" : ["13","20"], "train":"n", "air":"n"},	
    # "TEST_S2" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"n"},	
    # "TEST_S3" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"n"},	
    # "TEST_S4" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"y"},	
    # "TEST_S5" : {"big" : ["5","7"], "small" : ["13","20"], "train":"n", "air":"y"},		
},
"at" : {
    "Vienna" : {"big" : ["6","12"], "small" : ["18","34"], "train":"y", "air":"y"},	
    "Innsbruck" : {"big" : ["8","7"], "small" : ["22","21"], "train":"y", "air":"n"},	
    "Linz" : {"big" : ["5","10"], "small" : ["18","28"], "train":"y", "air":"y"},	
    "Salzburg" : {"big" : ["7","9"], "small" : ["20","25"], "train":"y", "air":"y"},	
    "Graz" : {"big" : ["8","11"], "small" : ["23","32"], "train":"y", "air":"y"},	# in the map "22","32" - but it is on the edge and with the '23' it gets much better results
    "Klagenfurt" : {"big" : ["8","10"], "small" : ["24","29"], "train":"y", "air":"n"},	
    "Villach" : {"big" : ["8","9"], "small" : ["24","27"], "train":"y", "air":"n"},		
},
"de" : {
    "Munich" : {"big" : ["5","7"], "small" : ["18","21"], "train":"y", "air":"y"},	
    "Sonthofen" : {"big" : ["7","6"], "small" : ["17","19"], "train":"y", "air":"n"},	
    "Nuremberg" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"y"},	
    "Dresden" : {"big" : ["2","9"], "small" : ["6","27"], "train":"y", "air":"y"},	
    "Chemnitz" : {"big" : ["3","9"], "small" : ["7","25"], "train":"n", "air":"n"},	
    "Bamberg" : {"big" : ["4","7"], "small" : ["11","19"], "train":"y", "air":"n"},	
    "Augsburg" : {"big" : ["6","7"], "small" : ["17","19"], "train":"y", "air":"n"},
    "Würzburg" : {"big" : ["4","5"], "small" : ["11","17"], "train":"y", "air":"n"},		
},
"pl" : {
    "Krakow" : {"big" : ["4","15"], "small" : ["10","43"], "train":"y", "air":"y"},	
    "Novy Sacz" : {"big" : ["4","15"], "small" : ["12","45"], "train":"n", "air":"n"},	
    "Czestochowa" : {"big" : ["3","14"], "small" : ["7","41"], "train":"y", "air":"n"},	
    "Bielsko-Biala" : {"big" : ["4","14"], "small" : ["11","41"], "train":"n", "air":"n"},	
    "Wroclav" : {"big" : ["2","12"], "small" : ["6","36"], "train":"y", "air":"y"},	
    "Katowice" : {"big" : ["3","14"], "small" : ["9","41"], "train":"y", "air":"y"},	
    "Walbrzych" : {"big" : ["3","12"], "small" : ["7","34"], "train":"n", "air":"n"},	
    "Opole" : {"big" : ["3","13"], "small" : ["8","38"], "train":"y", "air":"n"},	
    "Rzeszow" : {"big" : ["4","17"], "small" : ["10","49"], "train":"y", "air":"y"},		
}
})


# Correction list
correction_list_data = [
    {"city1" : "Krakow" , "city2" : "Prague", "distance": 509},
    {"city1" : "Liberec" , "city2" : "Linz", "distance": 342},
    {"city1" : "Dresden" , "city2" : "Bratislava", "distance": 479},
    {"city1" : "Dresden" , "city2" : "Nuremberg", "distance": 316},
    {"city1" : "Krakow" , "city2" : "Pardubice", "distance": 395},
    {"city1" : "Karlovy Vary" , "city2" : "Zlin", "distance": 427},
    {"city1" : "Opole" , "city2" : "Klagenfurt", "distance": 765},
    {"city1" : "Opole" , "city2" : "Salzburg", "distance": 748},
    {"city1" : "Opole" , "city2" : "Linz", "distance": 623},
    {"city1" : "Opole" , "city2" : "Innsbruck", "distance": 857},
    {"city1" : "Chemnitz" , "city2" : "Sonthofen", "distance": 526},
    {"city1" : "Rzeszow" , "city2" : "Dresden", "distance": 689},
    {"city1" : "Banska Bystrica" , "city2" : "Bratislava", "distance": 211},
    {"city1" : "Prague" , "city2" : "Zlin", "distance": 298},
    {"city1" : "Prague" , "city2" : "Brno", "distance": 205},
    {"city1" : "Prague" , "city2" : "Salzburg", "distance": 341},
    {"city1" : "Zilina" , "city2" : "Brno", "distance": 207},
    {"city1" : "Klagenfurt" , "city2" : "Plzen", "distance": 481},
    {"city1" : "Krakow" , "city2" : "Vienna", "distance": 451},
    {"city1" : "Graz" , "city2" : "Bamberg", "distance": 550},
    {"city1" : "Graz" , "city2" : "Banska Bystrica", "distance": 440},
    {"city1" : "Graz" , "city2" : "Zilina", "distance": 463},
    {"city1" : "Klagenfurt" , "city2" : "Sonthofen", "distance": 476},
    {"city1" : "Klagenfurt" , "city2" : "Hradec Kralove", "distance": 593},
    {"city1" : "Klagenfurt" , "city2" : "Bratislava", "distance": 367},
    {"city1" : "Munich" , "city2" : "Jihlava", "distance": 458},
]

# Dataset impacting costs based on exchange rate value
criteria_dict = {
    "kc": [
        {
            "min": None,
            "max": 20,
            "rule_text": "x < 20",
            "impact_pct": -9.3,
            "cost_trend": "cost decrease"
        },
        {
            "min": 20,
            "max": 21,
            "rule_text": "20 ≤ x < 21",
            "impact_pct": -4.7,
            "cost_trend": "cost decrease"
        },
        {
            "min": 21,
            "max": 22,
            "rule_text": "21 ≤ x < 22",
            "impact_pct": 0,
            "cost_trend": "default value"
        },
        {
            "min": 22,
            "max": None,
            "rule_text": "22 ≤ x",
            "impact_pct": 4.7,
            "cost_trend": "cost increase"
        }
    ],
    "eur": [
        {
            "min": None,
            "max": 0.82,
            "rule_text": "x < 0.82",
            "impact_pct": -5.9,
            "cost_trend": "cost decrease"
        },
        {
            "min": 0.82,
            "max": 0.87,
            "rule_text": "0.82 ≤ x < 0.87",
            "impact_pct": 0,
            "cost_trend": "default value"
        },
        {
            "min": 0.87,
            "max": 0.90,
            "rule_text": "0.87 ≤ x < 0.90",
            "impact_pct": 3.5,
            "cost_trend": "cost increase"
        },
        {
            "min": 0.90,
            "max": None,
            "rule_text": "0.90 ≤ x",
            "impact_pct": 7.1,
            "cost_trend": "cost increase"
        }
    ]
}

# Dataset SLA
sla_dict = {
	"truck": {
		"slow": {
			"extra_time": 120,
            "coef" : 0.4
		},
		"standard": {
			"extra_time": 32,
            "coef" : None
		},
		"express": {
			"extra_time": 6,
            "coef" : 0.4
		}
	},
	"train": {
		"slow": {
			"extra_time": 120,
            "coef" : 0.5
		},
		"standard": {
			"extra_time": 48,
            "coef" : None
		},
		"express": {
			"extra_time": 10,
            "coef" : 0.5
		}
	},
	"airplane": {
		"slow": {
			"extra_time": 240,
            "coef": 0.1
		},
		"standard": {
			"extra_time": 72,
            "coef" : None
		},
		"express": {
			"extra_time": 2,
            "coef": 0.7
		}
	}
}


# Dataset price per transport type & currency 
# "standard" Price per 1t/per approx 30km (one square on map) - STANDARD servide
# "coef" - price coeficients increasing(Express delivery) or decreasign (Slow delivery) price per square

price_dict = {
	"truck": {
		"eur": {
			"standard": 60,
		},
		"kc": {
			"standard": 1_500,
		}
	},
	"train": {
		"eur": {
			"standard": 48,
		},
		"kc": {
			"standard": 1_200,
		}
	},
	"airplane": {
		"eur": {
			"standard": 600,
		},
		"kc": {
			"standard": 15_000,
		}
	}
}


# These to DTD dictionaries need to corespond
# Options per transport type
dtd_options_dict = {
    "truck" : ["Within city", "10 km", "20 km"],
    "train" : ["No", "10 km", "20 km"],
    "airplane" : ["No", "10 km", "20 km"]
}

# Time needed HOURS (Truck) for DTD delivery based on selection + Prices
dtd_calculation_values_dict = {
	"No": {
		"distance": 0, 
		"truck_driving": 0,
		"price": {
			"train": {
				"euro": 0,
				"koruna": 0
			},
			"airplane": {
				"euro": 0,
				"koruna": 0
			},

            # Note: this 'No' option option cannot be selected on UI as part of 'Truck' but it is importtant to have this OBJECT for TAB 2 purposes. Without this function will fail get_door_to_door_cost_and_distance()
            "truck": {
				"euro": 0,
				"koruna": 0
			}
		}
	},
	"Within city": {
		"distance": 0,
		"truck_driving": 0,
		"price": {
			"truck": {
				"euro": 0,
				"koruna": 0
			},

            # Note: this 'Within city' option cannot be selected on UI as part of 'Train' or 'Airplane' but it is importtant to have this OBJECT for TAB 2 purposes. Without this function will fail get_door_to_door_cost_and_distance()
            "train": {
				"euro": 0,
				"koruna": 0
			},
			"airplane": {
				"euro": 0,
				"koruna": 0
			}
		}
	},
	"10 km": {
		"distance": 10,
		"truck_driving": 0.42,
		"price": {
			"truck": {
				"euro": 20,
				"koruna": 500
			},
			"train": {
				"euro": 40,
				"koruna": 1000
			},
			"airplane": {
				"euro": 40,
				"koruna": 1000
			}
		}
	},
	"20 km": {
		"distance": 20,
		"truck_driving": 0.75,
		"price": {
			"truck": {
				"euro": 40,
				"koruna": 1000
			},
			"train": {
				"euro": 60,
				"koruna": 1500
			},
			"airplane": {
				"euro": 60,
				"koruna": 1500
			}
		}
	},
	"transfer": 1
}

# Extra services / % values
extra_service_dict = {
    "insurance" : 10,
    "fragile": 5,
    "danger":  7
}


# =========== F7B UI ==========
states_dict = {
    "CREATED": {
        "name": "Created",
        "symbol" : "⏺",
        "color" : "255, 120, 226"
    },
    "APPROVED": {
        "name": "Approved",
        "symbol" : "✔",
        "color" : "81, 224, 54"
    },
    "REJECTED": {
        "name": "Rejected",
        "symbol" : "✖",
        "color" : "214, 0, 0"
    },
    "EXPIRED": {
        "name": "Expired",
        "symbol" : "⏺",
        "color" : "150, 148, 150"
    },
    "TRANSPORT_PREPARATION": {
        "name": "Transport preparation",
        "symbol" : "⯈",
        "color" : "222, 149, 87"
    },
    "TRANSPORT_ON_THE_WAY": {
        "name": "Transport on the way",
        "symbol" : "🡺",
        "color" : "16, 124, 222"
    },
    "DELIVERED": {
        "name": "Delivered",
        "symbol" : "⏺",
        "color" : "56, 161, 35"
    },
}