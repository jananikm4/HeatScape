import streamlit as st
import folium
from streamlit_folium import st_folium

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeatScape | Chennai Climate Intelligence",
    page_icon="🌿",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0d1016;
    color: #f5f7fa;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

h2 {
    font-size: 26px !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 20px !important;
}

.metric-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 25px;
    min-height: 165px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
}

.metric-label {
    color: #58708c;
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 15px;
}

.metric-value {
    color: #171a21;
    font-size: 31px;
    font-weight: 700;
    line-height: 1.15;
}

.metric-small {
    color: #64748b;
    font-size: 13px;
    margin-top: 10px;
}

.recommendation-card {
    background: linear-gradient(135deg, #effff5, #e5faed);
    border-radius: 22px;
    padding: 32px;
    margin-top: 10px;
    color: #17251c;
    border: 1px solid #ccebd8;
}

.recommendation-title {
    color: #557261;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.recommendation-main {
    color: #163a25;
    font-size: 31px;
    font-weight: 700;
    margin-top: 7px;
}

.recommendation-location {
    color: #486454;
    font-size: 16px;
    margin-top: 10px;
}

.recommendation-reason {
    color: #405548;
    font-size: 14px;
    margin-top: 17px;
    line-height: 1.6;
}

.info-card {
    background: #171a21;
    border: 1px solid #292e38;
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
}

.info-label {
    color: #8fa0b4;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.info-value {
    color: #ffffff;
    font-size: 21px;
    font-weight: 700;
    margin-top: 8px;
}

.info-detail {
    color: #9da8b7;
    font-size: 13px;
    margin-top: 10px;
    line-height: 1.5;
}

.fingerprint-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    color: #171a21;
    box-shadow: 0 3px 12px rgba(0,0,0,0.10);
}

.fingerprint-name {
    color: #526b82;
    font-size: 14px;
}

.fingerprint-score {
    color: #171a21;
    font-size: 25px;
    font-weight: 700;
    margin-top: 5px;
}

.cost-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 23px;
    min-height: 135px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.10);
}

.cost-label {
    color: #58708c;
    font-size: 14px;
}

.cost-value {
    color: #17231d;
    font-size: 27px;
    font-weight: 700;
    margin-top: 10px;
}

.option-card {
    background: #171a21;
    border: 1px solid #292e38;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 10px;
}

.option-title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
}

.option-detail {
    color: #9da8b7;
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.5;
}

.budget-card {
    background: linear-gradient(135deg, #f0fff5, #e4faec);
    border: 1px solid #ccebd8;
    border-radius: 22px;
    padding: 28px;
    color: #17251c;
}

.budget-title {
    color: #53705e;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.4px;
}

.budget-main {
    color: #163a25;
    font-size: 28px;
    font-weight: 700;
    margin-top: 7px;
}

.budget-detail {
    color: #496052;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 12px;
}

.section-note {
    color: #8995a6;
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 18px;
}

.technique-card {
    background: #171a21;
    border: 1px solid #292e38;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

.technique-name {
    color: #ffffff;
    font-weight: 600;
    font-size: 15px;
}

.technique-category {
    color: #8c9aaa;
    font-size: 12px;
    margin-top: 4px;
}

.footer {
    text-align: center;
    color: #657181;
    font-size: 12px;
    padding-top: 40px;
    padding-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# Prototype / representative values
# ============================================================

LOCATIONS = {

    "Washermanpet": {
        "lat": 13.1158,
        "lon": 80.2875,
        "lst": 41.2,
        "ndvi": 0.18,
        "built": 84,
        "population": 82,

        "roads": [
            {
                "name": "Mint Street Corridor",
                "area": 1550,
                "tree_capacity": 125,
                "lat": 13.1165,
                "lon": 80.2878
            },
            {
                "name": "Moolakadai Road",
                "area": 1100,
                "tree_capacity": 90,
                "lat": 13.1190,
                "lon": 80.2860
            }
        ],

        "open_spaces": [
            {
                "name": "Local Community Open Space",
                "area": 1200,
                "lat": 13.1150,
                "lon": 80.2890
            }
        ],

        "roofs": [
            {
                "name": "Washermanpet Commercial Roof Cluster",
                "area": 30000,
                "lat": 13.1160,
                "lon": 80.2880
            }
        ]
    },

    "Royapuram": {
        "lat": 13.1155,
        "lon": 80.2940,
        "lst": 40.8,
        "ndvi": 0.21,
        "built": 81,
        "population": 78,

        "roads": [
            {
                "name": "Royapuram High Road",
                "area": 1700,
                "tree_capacity": 135,
                "lat": 13.1148,
                "lon": 80.2925
            }
        ],

        "open_spaces": [
            {
                "name": "Royapuram Community Space",
                "area": 2400,
                "lat": 13.1170,
                "lon": 80.2950
            }
        ],

        "roofs": [
            {
                "name": "Royapuram Building Cluster",
                "area": 28000,
                "lat": 13.1155,
                "lon": 80.2940
            }
        ]
    },

    "Perambur": {
        "lat": 13.1198,
        "lon": 80.2336,
        "lst": 41.0,
        "ndvi": 0.24,
        "built": 78,
        "population": 76,

        "roads": [
            {
                "name": "Perambur High Road",
                "area": 2100,
                "tree_capacity": 170,
                "lat": 13.1210,
                "lon": 80.2340
            }
        ],

        "open_spaces": [
            {
                "name": "Perambur Green Space",
                "area": 3000,
                "lat": 13.1180,
                "lon": 80.2320
            }
        ],

        "roofs": [
            {
                "name": "Perambur Roof Cluster",
                "area": 26000,
                "lat": 13.1198,
                "lon": 80.2336
            }
        ]
    },

    "Ambattur": {
        "lat": 13.1143,
        "lon": 80.1548,
        "lst": 40.2,
        "ndvi": 0.28,
        "built": 73,
        "population": 69,

        "roads": [
            {
                "name": "Ambattur Industrial Road",
                "area": 2600,
                "tree_capacity": 210,
                "lat": 13.1150,
                "lon": 80.1555
            }
        ],

        "open_spaces": [
            {
                "name": "Ambattur Open Area",
                "area": 5200,
                "lat": 13.1130,
                "lon": 80.1530
            }
        ],

        "roofs": [
            {
                "name": "Ambattur Industrial Roof Cluster",
                "area": 42000,
                "lat": 13.1143,
                "lon": 80.1548
            }
        ]
    },

    "Avadi": {
        "lat": 13.1147,
        "lon": 80.1018,
        "lst": 39.1,
        "ndvi": 0.38,
        "built": 62,
        "population": 63,

        "roads": [
            {
                "name": "Avadi Main Road",
                "area": 3000,
                "tree_capacity": 240,
                "lat": 13.1150,
                "lon": 80.1025
            }
        ],

        "open_spaces": [
            {
                "name": "Avadi Green Area",
                "area": 6500,
                "lat": 13.1130,
                "lon": 80.1000
            }
        ],

        "roofs": [
            {
                "name": "Avadi Building Cluster",
                "area": 22000,
                "lat": 13.1147,
                "lon": 80.1018
            }
        ]
    },

    "Anna Nagar": {
        "lat": 13.0850,
        "lon": 80.2101,
        "lst": 38.4,
        "ndvi": 0.42,
        "built": 70,
        "population": 64,

        "roads": [
            {
                "name": "2nd Avenue",
                "area": 2200,
                "tree_capacity": 175,
                "lat": 13.0845,
                "lon": 80.2110
            }
        ],

        "open_spaces": [
            {
                "name": "Anna Nagar Open Space",
                "area": 3500,
                "lat": 13.0860,
                "lon": 80.2090
            }
        ],

        "roofs": [
            {
                "name": "Anna Nagar Roof Cluster",
                "area": 24000,
                "lat": 13.0850,
                "lon": 80.2101
            }
        ]
    },

    "Nungambakkam": {
        "lat": 13.0569,
        "lon": 80.2425,
        "lst": 39.2,
        "ndvi": 0.34,
        "built": 76,
        "population": 68,

        "roads": [
            {
                "name": "College Road",
                "area": 1800,
                "tree_capacity": 145,
                "lat": 13.0575,
                "lon": 80.2430
            }
        ],

        "open_spaces": [
            {
                "name": "Nungambakkam Green Space",
                "area": 2800,
                "lat": 13.0560,
                "lon": 80.2410
            }
        ],

        "roofs": [
            {
                "name": "Nungambakkam Roof Cluster",
                "area": 25000,
                "lat": 13.0569,
                "lon": 80.2425
            }
        ]
    },

    "T Nagar": {
        "lat": 13.0418,
        "lon": 80.2341,
        "lst": 40.0,
        "ndvi": 0.22,
        "built": 87,
        "population": 74,

        "roads": [
            {
                "name": "Usman Road Corridor",
                "area": 1900,
                "tree_capacity": 150,
                "lat": 13.0420,
                "lon": 80.2350
            }
        ],

        "open_spaces": [
            {
                "name": "T Nagar Community Space",
                "area": 1800,
                "lat": 13.0405,
                "lon": 80.2330
            }
        ],

        "roofs": [
            {
                "name": "T Nagar Commercial Roof Cluster",
                "area": 35000,
                "lat": 13.0418,
                "lon": 80.2341
            }
        ]
    },

    "Mylapore": {
        "lat": 13.0339,
        "lon": 80.2676,
        "lst": 38.8,
        "ndvi": 0.35,
        "built": 72,
        "population": 66,

        "roads": [
            {
                "name": "R K Mutt Road",
                "area": 2000,
                "tree_capacity": 160,
                "lat": 13.0345,
                "lon": 80.2680
            }
        ],

        "open_spaces": [
            {
                "name": "Mylapore Open Space",
                "area": 4200,
                "lat": 13.0325,
                "lon": 80.2660
            }
        ],

        "roofs": [
            {
                "name": "Mylapore Roof Cluster",
                "area": 23000,
                "lat": 13.0339,
                "lon": 80.2676
            }
        ]
    },

    "Guindy": {
        "lat": 13.0067,
        "lon": 80.2206,
        "lst": 39.5,
        "ndvi": 0.39,
        "built": 68,
        "population": 58,

        "roads": [
            {
                "name": "Guindy Industrial Corridor",
                "area": 3200,
                "tree_capacity": 255,
                "lat": 13.0070,
                "lon": 80.2210
            }
        ],

        "open_spaces": [
            {
                "name": "Guindy Green Area",
                "area": 7000,
                "lat": 13.0050,
                "lon": 80.2190
            }
        ],

        "roofs": [
            {
                "name": "Guindy Industrial Roof Cluster",
                "area": 40000,
                "lat": 13.0067,
                "lon": 80.2206
            }
        ]
    },

    "Adyar": {
        "lat": 13.0063,
        "lon": 80.2574,
        "lst": 37.9,
        "ndvi": 0.51,
        "built": 61,
        "population": 55,

        "roads": [
            {
                "name": "LB Road",
                "area": 2400,
                "tree_capacity": 190,
                "lat": 13.0070,
                "lon": 80.2580
            }
        ],

        "open_spaces": [
            {
                "name": "Adyar Green Corridor",
                "area": 6500,
                "lat": 13.0050,
                "lon": 80.2560
            }
        ],

        "roofs": [
            {
                "name": "Adyar Roof Cluster",
                "area": 21000,
                "lat": 13.0063,
                "lon": 80.2574
            }
        ]
    },

    "Velachery": {
        "lat": 12.9815,
        "lon": 80.2180,
        "lst": 40.1,
        "ndvi": 0.25,
        "built": 79,
        "population": 73,

        "roads": [
            {
                "name": "Velachery Main Road",
                "area": 2500,
                "tree_capacity": 200,
                "lat": 12.9820,
                "lon": 80.2190
            }
        ],

        "open_spaces": [
            {
                "name": "Velachery Open Space",
                "area": 4000,
                "lat": 12.9800,
                "lon": 80.2170
            }
        ],

        "roofs": [
            {
                "name": "Velachery Roof Cluster",
                "area": 30000,
                "lat": 12.9815,
                "lon": 80.2180
            }
        ]
    },

    "Perungudi": {
        "lat": 12.9591,
        "lon": 80.2400,
        "lst": 39.8,
        "ndvi": 0.30,
        "built": 75,
        "population": 61,

        "roads": [
            {
                "name": "OMR Service Road",
                "area": 3500,
                "tree_capacity": 280,
                "lat": 12.9600,
                "lon": 80.2410
            }
        ],

        "open_spaces": [
            {
                "name": "Perungudi Green Space",
                "area": 5500,
                "lat": 12.9580,
                "lon": 80.2390
            }
        ],

        "roofs": [
            {
                "name": "Perungudi Roof Cluster",
                "area": 38000,
                "lat": 12.9591,
                "lon": 80.2400
            }
        ]
    },

    "Sholinganallur": {
        "lat": 12.9010,
        "lon": 80.2279,
        "lst": 40.4,
        "ndvi": 0.27,
        "built": 77,
        "population": 70,

        "roads": [
            {
                "name": "Sholinganallur OMR Corridor",
                "area": 4200,
                "tree_capacity": 335,
                "lat": 12.9020,
                "lon": 80.2290
            }
        ],

        "open_spaces": [
            {
                "name": "Sholinganallur Open Area",
                "area": 6000,
                "lat": 12.9000,
                "lon": 80.2260
            }
        ],

        "roofs": [
            {
                "name": "Sholinganallur Roof Cluster",
                "area": 45000,
                "lat": 12.9010,
                "lon": 80.2279
            }
        ]
    },

    "Tambaram": {
        "lat": 12.9249,
        "lon": 80.1000,
        "lst": 39.4,
        "ndvi": 0.40,
        "built": 64,
        "population": 65,

        "roads": [
            {
                "name": "Tambaram Main Road",
                "area": 2800,
                "tree_capacity": 225,
                "lat": 12.9255,
                "lon": 80.1010
            }
        ],

        "open_spaces": [
            {
                "name": "Tambaram Green Area",
                "area": 5000,
                "lat": 12.9230,
                "lon": 80.0990
            }
        ],

        "roofs": [
            {
                "name": "Tambaram Roof Cluster",
                "area": 25000,
                "lat": 12.9249,
                "lon": 80.1000
            }
        ]
    }
}


# ============================================================
# CONSTANTS
# ============================================================

TECHNIQUES = [
    "Urban Forests & Trees",
    "Green Corridors",
    "Pocket Parks",
    "Blue Infrastructure",
    "Reflective Cool Roofs",
    "Reflective Pavements",
    "Shaded Pedestrian Corridors",
    "Green + Shade Corridors"
]

COSTS = {

    "Urban Forests & Trees": {
        "unit": "tree",
        "install": 650,
        "establishment": 300,
        "maintenance": 250
    },

    "Green Corridors": {
        "unit": "m²",
        "install": 650,
        "establishment": 250,
        "maintenance": 150
    },

    "Pocket Parks": {
        "unit": "m²",
        "install": 1600,
        "establishment": 0,
        "maintenance": 100
    },

    "Blue Infrastructure": {
        "unit": "m²",
        "install": 1200,
        "establishment": 0,
        "maintenance": 80
    },

    "Reflective Cool Roofs": {
        "unit": "m²",
        "install": 300,
        "establishment": 0,
        "maintenance": 30
    },

    "Reflective Pavements": {
        "unit": "m²",
        "install": 400,
        "establishment": 0,
        "maintenance": 25
    },

    "Shaded Pedestrian Corridors": {
        "unit": "m²",
        "install": 650,
        "establishment": 250,
        "maintenance": 150
    },

    "Green + Shade Corridors": {
        "unit": "m²",
        "install": 650,
        "establishment": 250,
        "maintenance": 150
    }
}


# ============================================================
# HEAT RISK FUNCTIONS
# ============================================================

def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0

    result = (
        (value - minimum) /
        (maximum - minimum)
    ) * 100

    return max(0, min(100, result))


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(
        lst,
        30,
        45
    )

    vegetation_deficit = max(
        0,
        min(
            100,
            100 - ndvi * 100
        )
    )

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )

    return max(
        0,
        min(100, risk)
    )


def get_contributions(data):

    heat = normalize(
        data["lst"],
        30,
        45
    )

    vegetation_deficit = max(
        0,
        min(
            100,
            100 - data["ndvi"] * 100
        )
    )

    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Intensity": 0.25 * data["built"],
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * data["population"]
    }


def risk_category(risk):

    if risk >= 75:
        return "Critical", "🔴"

    if risk >= 50:
        return "High", "🟠"

    if risk >= 25:
        return "Moderate", "🟡"

    return "Low", "🟢"


# ============================================================
# SITE HELPERS
# ============================================================

def best_road(data):

    if not data.get("roads"):
        return None

    return max(
        data["roads"],
        key=lambda x: x["area"]
    )


def best_open_space(data):

    if not data.get("open_spaces"):
        return None

    return max(
        data["open_spaces"],
        key=lambda x: x["area"]
    )


def best_roof(data):

    if not data.get("roofs"):
        return None

    return max(
        data["roofs"],
        key=lambda x: x["area"]
    )


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def get_recommendation(data):

    contributions = get_contributions(data)

    dominant = max(
        contributions,
        key=contributions.get
    )

    road = best_road(data)
    space = best_open_space(data)
    roof = best_roof(data)

    # Vegetation problem
    if dominant == "Vegetation Deficit":

        if space and space["area"] >= 2500:

            trees = min(
                int(space["area"] / 20),
                500
            )

            return {
                "technique": "Urban Forests & Trees",
                "location": space["name"],
                "quantity": trees,
                "unit": "trees",
                "available": space["area"],
                "lat": space["lat"],
                "lon": space["lon"],
                "reason": (
                    "Vegetation deficit is the strongest "
                    "contributor and a suitable open space "
                    "is available for a large-scale tree intervention."
                )
            }

        if road:

            return {
                "technique": "Urban Forests & Trees",
                "location": road["name"],
                "quantity": road["tree_capacity"],
                "unit": "trees",
                "available": road["area"],
                "lat": road["lat"],
                "lon": road["lon"],
                "reason": (
                    "Vegetation deficit is a major contributor. "
                    "The selected roadside corridor has capacity "
                    "for additional tree canopy."
                )
            }

    # Built-up problem
    if dominant == "Built-up Intensity":

        if roof:

            recommended_area = int(
                roof["area"] * 0.50
            )

            return {
                "technique": "Reflective Cool Roofs",
                "location": roof["name"],
                "quantity": recommended_area,
                "unit": "m²",
                "available": roof["area"],
                "lat": roof["lat"],
                "lon": roof["lon"],
                "reason": (
                    "High built-up intensity is the strongest "
                    "contributor. Treating a portion of suitable "
                    "roof area directly targets this source."
                )
            }

    # Surface heat
    if dominant == "Surface Heat":

        if road:

            return {
                "technique": "Green + Shade Corridors",
                "location": road["name"],
                "quantity": int(road["area"] * 0.60),
                "unit": "m²",
                "available": road["area"],
                "lat": road["lat"],
                "lon": road["lon"],
                "reason": (
                    "Surface heat is the strongest contributor. "
                    "A combined green and shade corridor can "
                    "target exposed roadside space."
                )
            }

    # Population
    if dominant == "Population Exposure":

        if space and space["area"] >= 2000:

            return {
                "technique": "Pocket Parks",
                "location": space["name"],
                "quantity": int(space["area"] * 0.60),
                "unit": "m²",
                "available": space["area"],
                "lat": space["lat"],
                "lon": space["lon"],
                "reason": (
                    "High population exposure makes accessible "
                    "cooling space a priority."
                )
            }

    # General fallback
    if road:

        return {
            "technique": "Shaded Pedestrian Corridors",
            "location": road["name"],
            "quantity": int(road["area"] * 0.50),
            "unit": "m²",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"],
            "reason": (
                "Roadside space is available for a targeted "
                "pedestrian cooling intervention."
            )
        }

    return {
        "technique": "Blue Infrastructure",
        "location": space["name"] if space else "Selected hotspot",
        "quantity": int(space["area"] * 0.50) if space else 1000,
        "unit": "m²",
        "available": space["area"] if space else 1000,
        "lat": space["lat"] if space else data["lat"],
        "lon": space["lon"] if space else data["lon"],
        "reason": (
            "A blue-green intervention can provide additional "
            "cooling where suitable space is available."
        )
    }


# ============================================================
# AVAILABLE OPTIONS FOR A LOCATION
# ============================================================

def build_options(data):

    options = []

    road = best_road(data)
    space = best_open_space(data)
    roof = best_roof(data)

    if road:

        options.append({
            "technique": "Urban Forests & Trees",
            "location": road["name"],
            "max_quantity": road["tree_capacity"],
            "unit": "trees",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"]
        })

        options.append({
            "technique": "Green Corridors",
            "location": road["name"],
            "max_quantity": road["area"],
            "unit": "m²",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"]
        })

        options.append({
            "technique": "Reflective Pavements",
            "location": road["name"],
            "max_quantity": road["area"],
            "unit": "m²",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"]
        })

        options.append({
            "technique": "Shaded Pedestrian Corridors",
            "location": road["name"],
            "max_quantity": road["area"],
            "unit": "m²",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"]
        })

        options.append({
            "technique": "Green + Shade Corridors",
            "location": road["name"],
            "max_quantity": road["area"],
            "unit": "m²",
            "available": road["area"],
            "lat": road["lat"],
            "lon": road["lon"]
        })

    if space:

        options.append({
            "technique": "Pocket Parks",
            "location": space["name"],
            "max_quantity": space["area"],
            "unit": "m²",
            "available": space["area"],
            "lat": space["lat"],
            "lon": space["lon"]
        })

        options.append({
            "technique": "Blue Infrastructure",
            "location": space["name"],
            "max_quantity": space["area"],
            "unit": "m²",
            "available": space["area"],
            "lat": space["lat"],
            "lon": space["lon"]
        })

    if roof:

        options.append({
            "technique": "Reflective Cool Roofs",
            "location": roof["name"],
            "max_quantity": roof["area"],
            "unit": "m²",
            "available": roof["area"],
            "lat": roof["lat"],
            "lon": roof["lon"]
        })

    return options


# ============================================================
# SIMULATION MODEL
# ============================================================

def simulate_intervention(
    original_risk,
    technique,
    quantity,
    data,
    available_area=0
):

    reduction = 0

    if quantity <= 0:
        return original_risk, 0

    if technique == "Urban Forests & Trees":

        reduction = (
            quantity / 2000
        ) * 18

    elif technique == "Green Corridors":

        reduction = (
            quantity / 2000
        ) * 17

    elif technique == "Pocket Parks":

        reduction = (
            quantity / 5000
        ) * 22

    elif technique == "Blue Infrastructure":

        reduction = (
            quantity / 5000
        ) * 18

    elif technique == "Reflective Cool Roofs":

        coverage = 0

        if available_area > 0:
            coverage = min(
                quantity / available_area,
                1
            )

        heat_score = normalize(
            data["lst"],
            30,
            45
        )

        heat_component = (
            heat_score * 0.45
        )

        reduction = (
            heat_component *
            0.20 *
            coverage
        )

    elif technique == "Reflective Pavements":

        reduction = (
            quantity / 10000
        ) * 8

    elif technique == "Shaded Pedestrian Corridors":

        reduction = (
            quantity / 2000
        ) * 12

    elif technique == "Green + Shade Corridors":

        reduction = (
            quantity / 2000
        ) * 20

    reduction = min(
        reduction,
        original_risk * 0.75
    )

    new_risk = max(
        0,
        original_risk - reduction
    )

    return new_risk, reduction


# ============================================================
# COST CALCULATOR
# ============================================================

def calculate_cost(
    technique,
    quantity
):

    price = COSTS[technique]

    initial = quantity * (
        price["install"] +
        price["establishment"]
    )

    annual = quantity * price["maintenance"]

    five_year = (
        initial +
        annual * 5
    )

    return initial, annual, five_year


# ============================================================
# FORMAT
# ============================================================

def money(value):

    return f"₹{value:,.0f}"


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<h1 style="margin-bottom:0;">
HeatScape
</h1>

<p style="
color:#91a0b2;
font-size:16px;
margin-top:4px;
margin-bottom:28px;
">
Climate Intelligence · Chennai
</p>
""", unsafe_allow_html=True)


# ============================================================
# LOCATION
# ============================================================

selected_location = st.selectbox(
    "Select Location",
    list(LOCATIONS.keys())
)

data = LOCATIONS[selected_location]

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

category, icon = risk_category(risk)

contributions = get_contributions(data)

recommendation = get_recommendation(data)

recommended_technique = recommendation["technique"]

recommended_quantity = recommendation["quantity"]

recommended_unit = recommendation["unit"]

recommended_location = recommendation["location"]

recommended_available = recommendation["available"]


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.markdown("## Current Conditions")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Heat Risk
        </div>

        <div class="metric-value">
        {risk:.0f}/100
        </div>

        <div class="metric-small">
        {icon} {category}
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Surface Temperature
        </div>

        <div class="metric-value">
        {data["lst"]:.1f}°C
        </div>

        <div class="metric-small">
        Surface heat variable
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Vegetation
        </div>

        <div class="metric-value">
        {data["ndvi"]:.2f}
        </div>

        <div class="metric-small">
        NDVI
        </div>

    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Built-up Area
        </div>

        <div class="metric-value">
        {data["built"]}%
        </div>

        <div class="metric-small">
        Built-up intensity
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HEAT MAP
# ============================================================

st.markdown("## Chennai Heat Map")

st.markdown("""
<p class="section-note">
Select a locality to understand its heat conditions and identify where cooling action can be implemented.
</p>
""", unsafe_allow_html=True)

heat_map = folium.Map(
    location=[13.05, 80.22],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)

for name, location_data in LOCATIONS.items():

    location_risk = calculate_risk(
        location_data["lst"],
        location_data["ndvi"],
        location_data["built"],
        location_data["population"]
    )

    if location_risk >= 75:
        color = "red"
    elif location_risk >= 50:
        color = "orange"
    elif location_risk >= 25:
        color = "beige"
    else:
        color = "green"

    folium.CircleMarker(
        [
            location_data["lat"],
            location_data["lon"]
        ],
        radius=11,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.65,
        popup=folium.Popup(
            f"""
            <b>{name}</b><br><br>
            Heat Risk: {location_risk:.0f}/100<br>
            Surface Temperature: {location_data["lst"]:.1f}°C<br>
            NDVI: {location_data["ndvi"]:.2f}<br>
            Built-up: {location_data["built"]}%
            """,
            max_width=300
        )
    ).add_to(heat_map)

folium.Marker(
    [
        data["lat"],
        data["lon"]
    ],
    popup=f"""
    <b>{selected_location}</b><br>
    Heat Risk: {risk:.0f}/100
    """,
    tooltip=f"{selected_location} · {risk:.0f}/100"
).add_to(heat_map)

st_folium(
    heat_map,
    width=None,
    height=500,
    returned_objects=[],
    key=f"main_map_{selected_location}"
)


# ============================================================
# HEAT FINGERPRINT
# ============================================================

st.markdown("## Heat Fingerprint")

st.markdown("""
<p class="section-note">
This explains what is actually contributing to the Heat Risk Index.
</p>
""", unsafe_allow_html=True)

sorted_contributions = sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
)

finger_cols = st.columns(4)

for i, (name, value) in enumerate(sorted_contributions):

    with finger_cols[i]:

        st.markdown(f"""
        <div class="fingerprint-card">

            <div class="fingerprint-name">
            {name}
            </div>

            <div class="fingerprint-score">
            {value:.1f}
            </div>

            <div style="
            color:#7b8796;
            font-size:12px;
            margin-top:4px;
            ">
            Risk contribution
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.progress(
            min(value / 100, 1)
        )


# ============================================================
# RECOMMENDED ACTION
# ============================================================

st.markdown("## Recommended First Action")

st.markdown(f"""
<div class="recommendation-card">

    <div class="recommendation-title">
    Recommended Technique
    </div>

    <div class="recommendation-main">
    {recommended_technique}
    </div>

    <div class="recommendation-location">
    📍 {recommended_location}
    </div>

    <div class="recommendation-reason">

    <b>Recommended implementation:</b>
    {recommended_quantity:,} {recommended_unit}

    <br><br>

    <b>Available site capacity:</b>
    {recommended_available:,} {recommended_unit if recommended_unit == "m²" else "trees"}

    <br><br>

    {recommendation["reason"]}

    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# RECOMMENDED COST
# ============================================================

rec_initial, rec_annual, rec_five = calculate_cost(
    recommended_technique,
    recommended_quantity
)

st.markdown("### Recommended Implementation Cost")

cost1, cost2, cost3 = st.columns(3)

with cost1:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        Initial implementation
        </div>

        <div class="cost-value">
        {money(rec_initial)}
        </div>

    </div>
    """, unsafe_allow_html=True)

with cost2:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        Annual maintenance
        </div>

        <div class="cost-value">
        {money(rec_annual)}
        </div>

    </div>
    """, unsafe_allow_html=True)

with cost3:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        5-year lifecycle
        </div>

        <div class="cost-value">
        {money(rec_five)}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# IMPLEMENTATION LOCATION
# ============================================================

st.markdown("## Where Should It Be Implemented?")

st.markdown("""
<p class="section-note">
HeatScape identifies a candidate implementation site instead of giving only a generic city-level recommendation.
</p>
""", unsafe_allow_html=True)

site1, site2, site3 = st.columns(3)

with site1:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
        Technique
        </div>

        <div class="info-value">
        {recommended_technique}
        </div>

        <div class="info-detail">
        The intervention selected from the heat fingerprint.
        </div>

    </div>
    """, unsafe_allow_html=True)


with site2:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
        Exact Candidate Site
        </div>

        <div class="info-value">
        {recommended_location}
        </div>

        <div class="info-detail">
        Identified from the available roadside, open-space or roof-site data.
        </div>

    </div>
    """, unsafe_allow_html=True)


with site3:

    st.markdown(f"""
    <div class="info-card">

        <div class="info-label">
        Recommended Scale
        </div>

        <div class="info-value">
        {recommended_quantity:,} {recommended_unit}
        </div>

        <div class="info-detail">
        Based on estimated site capacity and intervention rules.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CUSTOM SIMULATOR
# ============================================================

st.markdown("## Customize & Simulate")

st.markdown("""
<p class="section-note">
Change the intervention or its scale. HeatScape recalculates the projected Heat Risk, implementation cost and maintenance cost automatically.
</p>
""", unsafe_allow_html=True)

technique_choice = st.selectbox(
    "Choose cooling technique",
    TECHNIQUES,
    index=TECHNIQUES.index(recommended_technique),
    key="custom_technique"
)

options = build_options(data)

matching_options = [
    x for x in options
    if x["technique"] == technique_choice
]

if matching_options:

    selected_option = matching_options[0]

else:

    selected_option = {
        "technique": technique_choice,
        "location": selected_location,
        "max_quantity": 10000,
        "unit": COSTS[technique_choice]["unit"],
        "available": 10000,
        "lat": data["lat"],
        "lon": data["lon"]
    }


max_quantity = int(
    max(
        selected_option["max_quantity"],
        1
    )
)

unit = selected_option["unit"]

default_quantity = min(
    recommended_quantity
    if technique_choice == recommended_technique
    else int(max_quantity * 0.50),
    max_quantity
)

if unit == "trees":

    minimum_quantity = 1
    step = 1

else:

    minimum_quantity = 100
    step = 100

    if max_quantity < minimum_quantity:
        max_quantity = minimum_quantity

quantity = st.slider(
    f"Implementation quantity ({unit})",
    min_value=minimum_quantity,
    max_value=max_quantity,
    value=max(
        minimum_quantity,
        min(default_quantity, max_quantity)
    ),
    step=step,
    key="simulation_quantity"
)


# ============================================================
# CUSTOM LOCATION
# ============================================================

st.markdown("### Implementation Site")

st.info(
    f"📍 {selected_option['location']} · "
    f"Available capacity: {selected_option['available']:,} {unit}"
)


# ============================================================
# CUSTOM SIMULATION
# ============================================================

custom_available = selected_option["available"]

custom_risk, custom_reduction = simulate_intervention(
    risk,
    technique_choice,
    quantity,
    data,
    custom_available
)

custom_initial, custom_annual, custom_five = calculate_cost(
    technique_choice,
    quantity
)


# ============================================================
# LIVE SIMULATION RESULTS
# ============================================================

st.markdown("### Live Simulation")

sim1, sim2, sim3, sim4 = st.columns(4)

with sim1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Current Heat Risk
        </div>

        <div class="metric-value">
        {risk:.0f}/100
        </div>

        <div class="metric-small">
        Before intervention
        </div>

    </div>
    """, unsafe_allow_html=True)


with sim2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Projected Heat Risk
        </div>

        <div class="metric-value">
        {custom_risk:.1f}/100
        </div>

        <div class="metric-small">
        After intervention
        </div>

    </div>
    """, unsafe_allow_html=True)


with sim3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        Risk Reduction
        </div>

        <div class="metric-value">
        {custom_reduction:.1f}
        </div>

        <div class="metric-small">
        Heat Risk Index points
        </div>

    </div>
    """, unsafe_allow_html=True)


with sim4:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
        5-Year Cost
        </div>

        <div class="metric-value">
        {money(custom_five)}
        </div>

        <div class="metric-small">
        Lifecycle estimate
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# COST CHANGES
# ============================================================

st.markdown("### Cost Breakdown")

cc1, cc2, cc3 = st.columns(3)

with cc1:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        Initial implementation
        </div>

        <div class="cost-value">
        {money(custom_initial)}
        </div>

    </div>
    """, unsafe_allow_html=True)

with cc2:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        Annual maintenance
        </div>

        <div class="cost-value">
        {money(custom_annual)}
        </div>

    </div>
    """, unsafe_allow_html=True)

with cc3:

    st.markdown(f"""
    <div class="cost-card">

        <div class="cost-label">
        5-year lifecycle
        </div>

        <div class="cost-value">
        {money(custom_five)}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# BEFORE / AFTER
# ============================================================

st.markdown("### Before → After")

st.progress(
    min(risk / 100, 1),
    text=f"Current · {risk:.0f}/100"
)

st.progress(
    min(custom_risk / 100, 1),
    text=f"Projected · {custom_risk:.1f}/100"
)


# ============================================================
# INTERVENTION MAP
# ============================================================

st.markdown("### Intervention Impact Map")

intervention_map = folium.Map(
    location=[
        data["lat"],
        data["lon"]
    ],
    zoom_start=14,
    tiles="OpenStreetMap",
    control_scale=True
)

# Hotspot
folium.CircleMarker(
    [
        data["lat"],
        data["lon"]
    ],
    radius=22,
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.20,
    popup=f"Current Heat Risk: {risk:.0f}/100"
).add_to(intervention_map)

# Selected implementation location
folium.Marker(
    [
        selected_option["lat"],
        selected_option["lon"]
    ],
    tooltip=technique_choice,
    popup=f"""
    <b>{technique_choice}</b><br><br>

    Location:<br>
    {selected_option["location"]}<br><br>

    Quantity:<br>
    {quantity:,} {unit}<br><br>

    Current Risk:<br>
    {risk:.0f}/100<br><br>

    Projected Risk:<br>
    {custom_risk:.1f}/100
    """,
    icon=folium.Icon(
        color="green",
        icon="leaf"
    )
).add_to(intervention_map)

# Road sites
for road in data.get("roads", []):

    folium.CircleMarker(
        [
            road["lat"],
            road["lon"]
        ],
        radius=7,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.65,
        popup=f"""
        <b>{road["name"]}</b><br>
        Available roadside area:
        {road["area"]:,} m²<br>
        Tree capacity:
        {road["tree_capacity"]}
        """
    ).add_to(intervention_map)

# Open spaces
for space in data.get("open_spaces", []):

    folium.CircleMarker(
        [
            space["lat"],
            space["lon"]
        ],
        radius=8,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.65,
        popup=f"""
        <b>{space["name"]}</b><br>
        Estimated area:
        {space["area"]:,} m²
        """
    ).add_to(intervention_map)

# Roof sites
for roof in data.get("roofs", []):

    folium.CircleMarker(
        [
            roof["lat"],
            roof["lon"]
        ],
        radius=8,
        color="purple",
        fill=True,
        fill_color="purple",
        fill_opacity=0.55,
        popup=f"""
        <b>{roof["name"]}</b><br>
        Suitable roof area:
        {roof["area"]:,} m²
        """
    ).add_to(intervention_map)

st_folium(
    intervention_map,
    width=None,
    height=520,
    returned_objects=[],
    key=f"intervention_map_{selected_location}_{technique_choice}"
)

st.caption(
    "The map shows the selected candidate implementation location. "
    "The projected change represents a modelled Heat Risk Index scenario, "
    "not exact physical temperature reduction."
)


# ============================================================
# BUDGET PLANNER
# ============================================================

st.divider()

st.markdown("## Plan Within Your Budget")

st.markdown("""
<p class="section-note">
Enter the amount available for cooling. HeatScape searches the available interventions and identifies the option that provides the strongest modelled risk reduction within that budget.
</p>
""", unsafe_allow_html=True)

budget = st.number_input(
    "Available cooling budget (₹)",
    min_value=10000,
    max_value=1000000000,
    value=5000000,
    step=100000,
    format="%d",
    key="budget_input"
)


# ============================================================
# BUDGET OPTIMIZER
# ============================================================

budget_results = []

for option in options:

    technique = option["technique"]

    maximum = int(
        option["max_quantity"]
    )

    if maximum <= 0:
        continue

    unit_cost = (
        COSTS[technique]["install"] +
        COSTS[technique]["establishment"]
    )

    if unit_cost <= 0:
        continue

    # Maximum quantity affordable from initial budget
    affordable_quantity = int(
        budget / unit_cost
    )

    quantity_budget = min(
        maximum,
        affordable_quantity
    )

    if option["unit"] == "m²":

        quantity_budget = (
            quantity_budget // 100
        ) * 100

    if option["unit"] == "trees":

        quantity_budget = int(
            quantity_budget
        )

    if quantity_budget <= 0:
        continue

    initial, annual, five_year = calculate_cost(
        technique,
        quantity_budget
    )

    projected_risk, reduction = simulate_intervention(
        risk,
        technique,
        quantity_budget,
        data,
        option["available"]
    )

    if five_year <= 0:
        efficiency = 0
    else:
        efficiency = (
            reduction / five_year
        ) * 1000000

    budget_results.append({

        "technique": technique,
        "location": option["location"],
        "quantity": quantity_budget,
        "unit": option["unit"],
        "initial": initial,
        "annual": annual,
        "five_year": five_year,
        "risk": projected_risk,
        "reduction": reduction,
        "efficiency": efficiency,
        "lat": option["lat"],
        "lon": option["lon"]

    })


# ============================================================
# BUDGET RESULT
# ============================================================

if budget_results:

    # Rank primarily by risk reduction per rupee
    budget_results.sort(
        key=lambda x: x["efficiency"],
        reverse=True
    )

    best_budget = budget_results[0]

    remaining = max(
        0,
        budget - best_budget["five_year"]
    )

    st.markdown(f"""
    <div class="budget-card">

        <div class="budget-title">
        Best solution within your budget
        </div>

        <div class="budget-main">
        {best_budget["technique"]}
        </div>

        <div class="budget-detail">

        📍 <b>{best_budget["location"]}</b>

        <br>

        📐 <b>{best_budget["quantity"]:,} {best_budget["unit"]}</b>

        <br>

        💰 5-year lifecycle cost:
        <b>{money(best_budget["five_year"])}</b>

        <br>

        🔧 Annual maintenance:
        <b>{money(best_budget["annual"])}</b>

        <br>

        📊 Projected Heat Risk:
        <b>{risk:.0f} → {best_budget["risk"]:.1f}</b>

        <br>

        📉 Modelled reduction:
        <b>{best_budget["reduction"]:.1f} points</b>

        <br>

        💵 Budget remaining:
        <b>{money(remaining)}</b>

        </div>

    </div>
    """, unsafe_allow_html=True)

else:

    st.warning(
        "The entered budget is too small for the available implementation options."
    )


# ============================================================
# AFFORDABLE OPTIONS
# ============================================================

if budget_results:

    st.markdown("### Other Affordable Options")

    top_options = budget_results[:6]

    for option in top_options:

        st.markdown(f"""
        <div class="option-card">

            <div class="option-title">
            {option["technique"]}
            </div>

            <div class="option-detail">

            📍 {option["location"]}

            &nbsp;&nbsp;·&nbsp;&nbsp;

            📐 {option["quantity"]:,} {option["unit"]}

            <br>

            5-year cost:
            <b>{money(option["five_year"])}</b>

            &nbsp;&nbsp;·&nbsp;&nbsp;

            Risk reduction:
            <b>{option["reduction"]:.1f}</b> points

            &nbsp;&nbsp;·&nbsp;&nbsp;

            Efficiency:
            <b>{option["efficiency"]:.2f}</b> points / ₹1M

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# BUDGET LOGIC EXPLANATION
# ============================================================

with st.expander("How does the Budget Planner choose?"):

    st.markdown("""
### 1. Check available sites

HeatScape checks candidate:

- roadside corridors
- open spaces
- roof clusters

### 2. Check the budget

For each intervention, it calculates how much can actually be implemented within the entered budget.

### 3. Calculate projected impact

The intervention quantity is passed through the HeatScape simulation model to estimate the new Heat Risk Index.

### 4. Calculate lifecycle cost

The planner considers:

**Initial implementation + 5 years of maintenance**

### 5. Rank the solutions

The current prototype ranks options using:

**Modelled Risk Reduction ÷ 5-Year Lifecycle Cost**

This identifies interventions that provide more Heat Risk reduction for the money available.

The result is a planning recommendation, not a procurement decision.
""")


# ============================================================
# COOLING TECHNIQUES
# ============================================================

st.markdown("## Cooling Techniques")

technique_categories = {

    "Nature-based": [
        "Urban Forests & Trees",
        "Green Corridors",
        "Pocket Parks",
        "Blue Infrastructure"
    ],

    "Reflective Materials": [
        "Reflective Cool Roofs",
        "Reflective Pavements"
    ],

    "Smart Planning": [
        "Shaded Pedestrian Corridors",
        "Green + Shade Corridors"
    ]
}

for category_name, names in technique_categories.items():

    st.markdown(
        f"### {category_name}"
    )

    for name in names:

        st.markdown(f"""
        <div class="technique-card">

            <div class="technique-name">
            {name}
            </div>

            <div class="technique-category">
            {category_name}
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander("Methodology & Data Sources"):

    st.markdown("""
## Heat Risk Index

HeatScape combines four transparent indicators:

| Factor | Weight |
|---|---:|
| Surface Heat | 45% |
| Built-up Intensity | 25% |
| Vegetation Deficit | 20% |
| Population Exposure | 10% |

The resulting **Heat Risk Index ranges from 0–100**.

---

## Data Inputs

**Landsat**  
Surface temperature

**Sentinel-2**  
Vegetation / NDVI

**Land Cover**  
Built-up intensity

**WorldPop**  
Population exposure

**OpenStreetMap**  
Road network and geographic context

---

## Recommendation

The system first identifies the strongest contributor to heat risk.

It then checks the available implementation space:

**Road space → Trees / shade / reflective pavement**

**Open space → Urban forests / pocket parks / blue infrastructure**

**Roof space → Reflective cool roofs**

The recommendation therefore includes:

**WHAT + WHERE + HOW MUCH**

---

## Cost

The system calculates:

**Initial Cost = Quantity × (Installation + Establishment)**

**Annual Maintenance = Quantity × Annual Maintenance Rate**

**5-Year Lifecycle Cost = Initial Cost + 5 × Annual Maintenance**

---

## Intervention Simulation

The simulator estimates the effect of changing intervention quantity on the HeatScape Heat Risk Index.

It is a **modelled scenario tool**.

It does not claim an exact future air-temperature reduction or exact physical heat dispersion.

---

## Budget Planner

The budget planner:

1. Takes the user's available budget.
2. Checks candidate implementation sites.
3. Calculates affordable quantities.
4. Calculates lifecycle cost.
5. Estimates projected risk reduction.
6. Ranks interventions by risk reduction per lifecycle cost.

This allows a planner to ask:

**"I have ₹X. What cooling intervention gives me the best modelled impact?"**
""")


# ============================================================
# DATA DISCLAIMER
# ============================================================

st.markdown("""
<div style="
background:#171a21;
border:1px solid #292e38;
border-radius:14px;
padding:18px;
margin-top:25px;
color:#8e9aaa;
font-size:12px;
line-height:1.6;
">

<b style="color:#ffffff;">Prototype data note</b><br><br>

The current hackathon prototype uses representative locality,
site-capacity and environmental values to demonstrate the complete
decision-support workflow.

The production system would replace these values with processed
satellite-derived, municipal GIS, cadastral and other verified
spatial datasets.

Candidate implementation spaces are estimates and should be verified
with detailed site-level GIS before real-world implementation.

Cost figures are configurable planning assumptions and actual costs
will vary by material, labour, procurement and site conditions.

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

HeatScape · Urban Heat Reduction Planner

<br><br>

From hotspot detection → explanation → location → intervention
→ simulation → cost → budget-aware planning

</div>
""", unsafe_allow_html=True)
