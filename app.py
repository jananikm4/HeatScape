import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import math

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }
.stApp { background: #f5f7f5; color: #17231d; }
.block-container { max-width: 1400px; padding-top: 35px; padding-bottom: 60px; }
#MainMenu, footer, header { visibility: hidden; }
h1 { font-size: 44px !important; font-weight: 700 !important; letter-spacing: -2px; color: #17231d !important; }
h2, h3 { color: #17231d !important; }
hr { border: none !important; border-top: 1px solid #dfe5e1 !important; margin: 32px 0 !important; }
.eyebrow { color: #2f8059; font-size: 11px; font-weight: 700; letter-spacing: 1.3px; text-transform: uppercase; margin-bottom: 7px; }
.metric-card { background:#fff; border:1px solid #e1e6e2; border-radius:15px; padding:21px 22px; min-height:112px; box-shadow:0 2px 8px rgba(20,35,28,.035); }
.metric-label { color:#758179; font-size:10px; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
.metric-value { color:#18241e; font-size:29px; line-height:1.1; font-weight:700; }
.metric-sub { color:#7c8780; font-size:12px; margin-top:6px; }
.risk-card { background:#17241d; border-radius:15px; padding:22px 24px; min-height:112px; box-shadow:0 6px 20px rgba(20,35,28,.10); }
.risk-label { color:#aebbb3; font-size:10px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
.risk-number { color:#fff; font-size:38px; font-weight:700; letter-spacing:-1.5px; margin-top:6px; }
.risk-status { color:#c8d4cd; font-size:12px; }
.recommendation-card { background:#fff; border:1px solid #d6e4da; border-radius:18px; padding:30px 32px; min-height:260px; box-shadow:0 8px 28px rgba(30,70,48,.08); }
.recommendation-tag { color:#2e8158; font-size:10px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; }
.recommendation-title { color:#17231d; font-size:29px; line-height:1.15; font-weight:700; margin-top:12px; margin-bottom:12px; }
.recommendation-text { color:#5f6c64; font-size:14px; line-height:1.7; }
.recommendation-highlight { background:#edf7f0; border-radius:10px; padding:11px 13px; margin-top:16px; color:#397052; font-size:12px; }
.decision-box { background:#f0f4f1; border:1px solid #dce5df; border-radius:13px; padding:18px 20px; color:#5c6961; font-size:12px; line-height:1.6; }
.simulator-card { background:#fff; border:1px solid #dfe5e1; border-radius:15px; padding:23px; box-shadow:0 2px 10px rgba(20,35,28,.035); }
.before-number { color:#d94b45; font-size:40px; font-weight:700; letter-spacing:-1px; }
.after-number { color:#25835a; font-size:40px; font-weight:700; letter-spacing:-1px; }
.simulator-label { color:#758179; font-size:10px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
.arrow { color:#a3aea7; font-size:25px; text-align:center; padding-top:12px; }
.reduction-card { background:#edf7f0; border:1px solid #d3e9da; border-radius:11px; padding:13px 16px; margin-top:14px; }
.reduction-number { color:#237a50; font-size:18px; font-weight:700; }
.reduction-label { color:#5b7164; font-size:11px; margin-top:2px; }
.cost-card { background:#fff; border:1px solid #e1e6e2; border-radius:14px; padding:19px 20px; min-height:105px; }
.cost-label { color:#78847d; font-size:11px; margin-bottom:7px; }
.cost-value { color:#1a2820; font-size:23px; font-weight:700; }
.info-box { background:#f0f4f1; border:1px solid #dce5df; border-radius:11px; padding:15px 17px; color:#5c6961; font-size:12px; line-height:1.6; }
.plan-card { background:#fff; border:1px solid #d9e5dc; border-radius:14px; padding:18px 20px; margin-bottom:12px; }
.plan-title { color:#17231d; font-size:18px; font-weight:700; }
.plan-detail { color:#65726a; font-size:12px; margin-top:5px; line-height:1.6; }
.budget-card { background:#17241d; color:#fff; border-radius:16px; padding:24px; }
.budget-label { color:#aebbb3; font-size:10px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
.budget-value { font-size:32px; font-weight:700; margin-top:6px; }
.footer { text-align:center; color:#89938d; font-size:11px; padding-top:35px; }
div[data-baseweb="select"] > div { background:white !important; border:1px solid #d7ded9 !important; border-radius:9px !important; }
div[data-testid="stSlider"] label, div[data-testid="stSlider"] label p { color:#28342d !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOCALITY DATA
# ============================================================

LOCALITIES = {
    "Washermanpet": {"lat":13.116,"lon":80.279,"lst":41.6,"ndvi":0.14,"built":84,"population":91},
    "Royapuram": {"lat":13.115,"lon":80.294,"lst":41.4,"ndvi":0.15,"built":82,"population":89},
    "Perambur": {"lat":13.116,"lon":80.233,"lst":40.8,"ndvi":0.19,"built":78,"population":86},
    "Ambattur": {"lat":13.114,"lon":80.154,"lst":40.7,"ndvi":0.20,"built":79,"population":78},
    "Avadi": {"lat":13.106,"lon":80.096,"lst":39.5,"ndvi":0.28,"built":68,"population":72},
    "Anna Nagar": {"lat":13.085,"lon":80.210,"lst":40.0,"ndvi":0.25,"built":76,"population":80},
    "Nungambakkam": {"lat":13.056,"lon":80.242,"lst":40.1,"ndvi":0.24,"built":77,"population":79},
    "T Nagar": {"lat":13.041,"lon":80.234,"lst":40.3,"ndvi":0.21,"built":83,"population":87},
    "Mylapore": {"lat":13.033,"lon":80.269,"lst":39.4,"ndvi":0.29,"built":73,"population":76},
    "Guindy": {"lat":13.006,"lon":80.220,"lst":39.0,"ndvi":0.34,"built":66,"population":70},
    "Adyar": {"lat":13.006,"lon":80.257,"lst":38.6,"ndvi":0.39,"built":61,"population":68},
    "Velachery": {"lat":12.981,"lon":80.218,"lst":39.1,"ndvi":0.31,"built":69,"population":77},
    "Perungudi": {"lat":12.960,"lon":80.245,"lst":38.9,"ndvi":0.33,"built":67,"population":71},
    "Sholinganallur": {"lat":12.901,"lon":80.227,"lst":38.0,"ndvi":0.40,"built":62,"population":69},
    "Tambaram": {"lat":12.925,"lon":80.127,"lst":37.4,"ndvi":0.46,"built":58,"population":62}
}

# Prototype implementation-space data.
# Replace these values with GIS/cadastral measurements when available.
SITE_DATA = {
    "Washermanpet": {
        "roads":[("M.C. Road",1550),("Mint Street",1250),("Royapuram High Road",1100)],
        "open":[("Washermanpet Community Open Space",1200),("Local Pocket Green",900)],
        "roof":42000},
    "Royapuram": {
        "roads":[("Royapuram High Road",1700),("Mannady Road",1200),("Kalmandapam Road",950)],
        "open":[("Royapuram Community Ground",1800),("Local Park Site",1100)],
        "roof":40000},
    "Perambur": {
        "roads":[("Perambur High Road",1900),("Paper Mills Road",1500),("Madhavaram High Road",1300)],
        "open":[("Perambur Open Ground",3200),("Local Park Parcel",1800)],
        "roof":39000},
    "Ambattur": {
        "roads":[("Ambattur OT Road",2100),("MTH Road",1800),("Red Hills Road",1300)],
        "open":[("Ambattur Community Ground",3600),("Local Green Space",2200)],
        "roof":39500},
    "Avadi": {
        "roads":[("Avadi Main Road",2200),("CTH Road",1800),("Poonamallee Road",1400)],
        "open":[("Avadi Community Ground",4200),("Local Open Space",2500)],
        "roof":34000},
    "Anna Nagar": {
        "roads":[("2nd Avenue",2200),("100 Feet Road",1800),("Shanti Colony Road",1400)],
        "open":[("Anna Nagar Park Edge",3000),("Local Play Ground",2200)],
        "roof":38000},
    "Nungambakkam": {
        "roads":[("College Road",1600),("Nelson Manickam Road",1450),("Sterling Road",1200)],
        "open":[("Nungambakkam Open Ground",2500),("Local Park Site",1600)],
        "roof":38500},
    "T Nagar": {
        "roads":[("Usman Road",1900),("South Usman Road",1450),("North Usman Road",1250)],
        "open":[("Local Community Open Space",2100),("Neighbourhood Park Edge",1400)],
        "roof":43000},
    "Mylapore": {
        "roads":[("R.K. Mutt Road",1800),("Royapettah High Road",1500),("Kutchery Road",1100)],
        "open":[("Mylapore Community Ground",2800),("Local Green Space",1900)],
        "roof":36000},
    "Guindy": {
        "roads":[("Guindy Industrial Estate Road",2300),("Race Course Road",1800),("GST Road Edge",1500)],
        "open":[("Guindy Open Ground",5000),("Local Green Parcel",3000)],
        "roof":33000},
    "Adyar": {
        "roads":[("LB Road",2100),("Sardar Patel Road",1800),("Adyar Bridge Approach",1300)],
        "open":[("Adyar Community Ground",4200),("Neighbourhood Green",2800)],
        "roof":31000},
    "Velachery": {
        "roads":[("Velachery Main Road",2400),("100 Feet Road Edge",1900),("Taramani Link Road",1500)],
        "open":[("Velachery Open Ground",3800),("Local Park Parcel",2300)],
        "roof":35000},
    "Perungudi": {
        "roads":[("OMR Service Road",2600),("Perungudi Link Road",1900),("Industrial Estate Road",1500)],
        "open":[("Perungudi Community Ground",4500),("Local Open Parcel",2600)],
        "roof":34000},
    "Sholinganallur": {
        "roads":[("Sholinganallur Main Road",2800),("OMR Service Road",2300),("ECR Link Road",1700)],
        "open":[("Sholinganallur Open Ground",5000),("Local Green Space",3000)],
        "roof":32000},
    "Tambaram": {
        "roads":[("GST Road Service Lane",2500),("Tambaram Main Road",2100),("Velachery-Tambaram Road",1700)],
        "open":[("Tambaram Community Ground",5200),("Local Park Parcel",3200)],
        "roof":30000}
}

# ============================================================
# COST + MODEL ASSUMPTIONS
# ============================================================

COSTS = {
    "Urban Forests & Trees": {"unit":"tree", "install":650, "establishment":300, "annual":250},
    "Green Corridors": {"unit":"m²", "install":650, "establishment":250, "annual":150},
    "Pocket Parks": {"unit":"m²", "install":1600, "establishment":0, "annual":100},
    "Blue Infrastructure": {"unit":"m²", "install":1200, "establishment":0, "annual":80},
    "Reflective Cool Roofs": {"unit":"m²", "install":300, "establishment":0, "annual":30},
    "Reflective Pavements": {"unit":"m²", "install":400, "establishment":0, "annual":25},
    "Shaded Pedestrian Corridors": {"unit":"m²", "install":650, "establishment":250, "annual":150},
    "Green + Shade Corridor": {"unit":"m²", "install":900, "establishment":250, "annual":180}
}

TECHNIQUES = list(COSTS.keys())

# ============================================================
# RISK ENGINE
# ============================================================

def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 0
    return max(0, min(100, ((value - minimum) / (maximum - minimum)) * 100))


def calculate_risk(lst, ndvi, built, population):
    heat = normalize(lst, 30, 45)
    vegetation_deficit = max(0, min(100, 100 - ndvi * 100))
    return max(0, min(100, (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )))


def get_contributions(data):
    heat = normalize(data["lst"], 30, 45)
    vegetation_deficit = max(0, min(100, 100 - data["ndvi"] * 100))
    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Intensity": 0.25 * data["built"],
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * data["population"]
    }

# ============================================================
# SPACE ANALYSIS
# ============================================================

def site_info(locality):
    return SITE_DATA[locality]


def best_road(locality):
    return max(site_info(locality)["roads"], key=lambda x: x[1])


def best_open_space(locality):
    return max(site_info(locality)["open"], key=lambda x: x[1])


def tree_capacity(road_space):
    # Approx. one tree per 12.5 m² of usable roadside space.
    return max(0, int(road_space / 12.5))


def technique_plan(locality, technique, data, risk):
    roads = site_info(locality)["roads"]
    opens = site_info(locality)["open"]
    road_name, road_space = max(roads, key=lambda x: x[1])
    open_name, open_area = max(opens, key=lambda x: x[1])
    roof_area = site_info(locality)["roof"]

    if technique == "Urban Forests & Trees":
        location, available, unit = road_name, road_space, "trees"
    elif technique in ("Green Corridors", "Pocket Parks", "Blue Infrastructure"):
        location, available, unit = open_name, open_area, "m²"
    elif technique == "Reflective Cool Roofs":
        location, available, unit = f"Suitable roofs in {locality}", roof_area, "m²"
    else:
        location, available, unit = road_name, road_space, "m²"

    quantity, projected, reachable = quantity_to_average(risk, technique, data, available)

    if reachable:
        description = f"Implement exactly {quantity:,} {unit} at {location} to bring the modelled Heat Risk Index from {risk:.1f} to {projected:.1f}, which is in the Moderate range."
    else:
        description = f"The target index of {TARGET_RISK:.0f} cannot be reached with this technique within the available site capacity. Maximum feasible implementation is {quantity:,} {unit} at {location}, giving a modelled index of {projected:.1f}."

    return {"technique":technique,"location":location,"quantity":quantity,"unit":unit,"available":available,"description":description,"target":TARGET_RISK,"target_reached":reachable}

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def recommended_technique(data, locality):
    contributions = get_contributions(data)
    dominant = max(contributions, key=contributions.get)
    spaces = site_info(locality)

    if dominant == "Vegetation Deficit":
        if max(x[1] for x in spaces["open"]) >= 2500:
            technique = "Urban Forests & Trees"
        else:
            technique = "Urban Forests & Trees"
    elif dominant == "Built-up Intensity":
        technique = "Reflective Cool Roofs"
    elif dominant == "Surface Heat":
        technique = "Green + Shade Corridor"
    else:
        technique = "Shaded Pedestrian Corridors"

    plan = technique_plan(locality, technique, data, calculate_risk(data["lst"], data["ndvi"], data["built"], data["population"]))
    return technique, dominant, plan

# ============================================================
# INTERVENTION IMPACT MODEL
# ============================================================

def simulate_intervention(original_risk, technique, quantity, data, available=0):
    # Transparent prototype assumptions: these reduce the HeatScape risk index,
    # not air temperature directly.
    heat_component = 0.45 * normalize(data["lst"], 30, 45)
    veg_component = 0.20 * max(0, min(100, 100 - data["ndvi"] * 100))
    built_component = 0.25 * data["built"]

    if technique == "Urban Forests & Trees":
        reduction = min(18.0, (quantity / 2000.0) * 18.0)
    elif technique == "Green Corridors":
        reduction = min(18.0, (quantity / 5000.0) * 18.0)
    elif technique == "Pocket Parks":
        reduction = min(18.0, (quantity / 5000.0) * 18.0)
    elif technique == "Blue Infrastructure":
        reduction = min(15.0, (quantity / 5000.0) * 15.0)
    elif technique == "Reflective Cool Roofs":
        coverage = quantity / available if available > 0 else 0
        reduction = heat_component * 0.20 * max(0, min(1, coverage))
    elif technique == "Reflective Pavements":
        reduction = min(8.0, (quantity / 10000.0) * 8.0)
    elif technique == "Shaded Pedestrian Corridors":
        reduction = min(12.0, (quantity / 2000.0) * 12.0)
    else:
        green_effect = min(10.0, (quantity / 2500.0) * 10.0)
        shade_effect = min(8.0, (quantity / 2500.0) * 8.0)
        reduction = green_effect + shade_effect

    reduction = min(reduction, original_risk * 0.75)
    return max(0, original_risk - reduction), reduction

# ============================================================
# TARGET QUANTITY
# ============================================================

TARGET_RISK = 50.0

def quantity_to_average(risk, technique, data, available):
    if risk <= TARGET_RISK:
        return 0, risk, True

    max_quantity = tree_capacity(available) if technique == "Urban Forests & Trees" else int(available)

    def projected(q):
        return simulate_intervention(risk, technique, q, data, available)[0]

    if max_quantity <= 0 or projected(max_quantity) > TARGET_RISK:
        return max_quantity, projected(max_quantity), False

    low, high = 0, max_quantity
    while low < high:
        mid = (low + high) // 2
        if projected(mid) <= TARGET_RISK:
            high = mid
        else:
            low = mid + 1

    return low, projected(low), True

# ============================================================
# COST MODEL
# ============================================================

def calculate_cost(technique, quantity):
    c = COSTS[technique]
    initial = quantity * (c["install"] + c["establishment"])
    annual = quantity * c["annual"]
    five_year = initial + annual * 5
    return initial, annual, five_year


def budget_plan(locality, data, risk, budget):
    candidates = []
    for technique in TECHNIQUES:
        plan = technique_plan(locality, technique, data, risk)
        if plan["quantity"] <= 0:
            continue
        max_qty = plan["quantity"]
        unit_initial = COSTS[technique]["install"] + COSTS[technique]["establishment"]
        unit_annual = COSTS[technique]["annual"]
        unit_five = unit_initial + unit_annual * 5
        if unit_five <= 0:
            continue
        affordable_qty = min(max_qty, int(budget // unit_five))
        if affordable_qty <= 0:
            continue
        after, reduction = simulate_intervention(risk, technique, affordable_qty, data, plan["available"])
        initial, annual, five = calculate_cost(technique, affordable_qty)
        efficiency = reduction / five if five else 0
        candidates.append({**plan,"quantity":affordable_qty,"after":after,"reduction":reduction,"initial":initial,"annual":annual,"five_year":five,"efficiency":efficiency})

    if not candidates:
        return None, []
    candidates.sort(key=lambda x: (x["reduction"], x["efficiency"]), reverse=True)
    return candidates[0], candidates

# ============================================================
# MAPS
# ============================================================

def risk_color(risk):
    if risk >= 75: return "#e54848"
    if risk >= 50: return "#f39a35"
    if risk >= 25: return "#e7ca4d"
    return "#38b879"


def generate_thermal_points(lat, lon, risk):
    points = []
    radius = 0.025
    for y in range(-10, 11):
        for x in range(-10, 11):
            distance = math.sqrt(x*x + y*y)
            intensity = math.exp(-(distance**2)/35) * (risk/100)
            if intensity > 0.04:
                points.append([lat + (y/10)*radius, lon + (x/10)*radius, intensity])
    return points


def create_main_map(selected):
    m = folium.Map(location=[13.05,80.22], zoom_start=11, tiles="OpenStreetMap", control_scale=True)
    heat_points = []
    for name, location in LOCALITIES.items():
        r = calculate_risk(location["lst"], location["ndvi"], location["built"], location["population"])
        heat_points.extend(generate_thermal_points(location["lat"], location["lon"], r))
    HeatMap(heat_points, radius=25, blur=30, min_opacity=0.22, max_zoom=13).add_to(m)

    for name, location in LOCALITIES.items():
        r = calculate_risk(location["lst"], location["ndvi"], location["built"], location["population"])
        selected_style = name == selected
        folium.CircleMarker(
            [location["lat"], location["lon"]],
            radius=11 if selected_style else 6,
            color="#ffffff", weight=2, fill=True,
            fill_color=risk_color(r), fill_opacity=.95,
            popup=folium.Popup(
                f"<b>{name}</b><br><br>Heat Risk: <b>{r:.1f}/100</b><br>Surface Temperature: {location['lst']:.1f}°C<br>Built-up: {location['built']}%<br>NDVI: {location['ndvi']:.2f}",
                max_width=280
            )
        ).add_to(m)
    return m


def create_intervention_map(lat, lon, before, after):
    html = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
html,body{margin:0;padding:0;width:100%;height:100%;}#map{width:100%;height:620px;}
.legend{position:absolute;bottom:18px;left:18px;z-index:9999;background:rgba(255,255,255,.96);border:1px solid #d9dfdb;border-radius:10px;padding:12px 15px;font-family:Arial,sans-serif;font-size:12px;color:#26332c;box-shadow:0 2px 10px rgba(0,0,0,.12)}
.legend-title{font-weight:bold;margin-bottom:8px}.legend-row{margin:5px 0}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
</style></head><body>
<div id="map"></div>
<div class="legend"><div class="legend-title">Heat Risk</div>
<div class="legend-row"><span class="dot" style="background:#e54848"></span>Critical</div>
<div class="legend-row"><span class="dot" style="background:#f39a35"></span>High</div>
<div class="legend-row"><span class="dot" style="background:#e7ca4d"></span>Moderate</div>
<div class="legend-row"><span class="dot" style="background:#38b879"></span>Low</div></div>
<script>
var lat=__LAT__,lon=__LON__,beforeRisk=__BEFORE__,afterRisk=__AFTER__;
var map=L.map('map').setView([lat,lon],14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
L.circleMarker([lat,lon],{radius:8,color:'#fff',weight:3,fillColor:'#e54848',fillOpacity:1}).addTo(map).bindPopup('Selected hotspot').openPopup();
var cells=[];
for(var y=-12;y<=12;y++){for(var x=-12;x<=12;x++){
var d=Math.sqrt(x*x+y*y),s=Math.exp(-(d*d)/55);
if(s>.08){var c=L.circle([lat+(y/10)*.022,lon+(x/10)*.022],{radius:95,stroke:false,fillOpacity:.35}).addTo(map);cells.push({circle:c,strength:s});}}}
function getColor(r){if(r>=75)return '#e54848';if(r>=50)return '#f39a35';if(r>=25)return '#e7ca4d';return '#38b879';}
function animate(){var start=null,duration=1200;function frame(t){if(!start)start=t;var p=Math.min(1,(t-start)/duration),e=p*p*(3-2*p),current=beforeRisk+(afterRisk-beforeRisk)*e;
cells.forEach(function(item){var local=current*(.55+item.strength*.45);item.circle.setStyle({fillColor:getColor(local),fillOpacity:.18+item.strength*.35});});
if(p<1)requestAnimationFrame(frame);}requestAnimationFrame(frame);}animate();
</script></body></html>
"""
    return (html.replace("__LAT__",str(lat)).replace("__LON__",str(lon)).replace("__BEFORE__",str(before)).replace("__AFTER__",str(after)))

# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([4,1])
with header_left:
    st.markdown('<div class="eyebrow">CLIMATE INTELLIGENCE · CHENNAI</div>', unsafe_allow_html=True)
    st.markdown('<h1>HeatScape</h1>', unsafe_allow_html=True)
    st.markdown("Urban heat reduction planning, made simple.")
with header_right:
    st.markdown('<div style="text-align:right;padding-top:12px"><div style="font-size:10px;color:#7b8780;letter-spacing:1px;font-weight:700">GREATER CHENNAI</div><div style="font-size:13px;color:#26342c;font-weight:600;margin-top:4px">Planning View</div></div>', unsafe_allow_html=True)

st.divider()

# ============================================================
# SELECT LOCATION
# ============================================================

st.markdown('<div class="eyebrow">01 · SELECT LOCATION</div>', unsafe_allow_html=True)
location_col, status_col = st.columns([2.5,1])
with location_col:
    selected = st.selectbox("Locality", list(LOCALITIES.keys()), label_visibility="collapsed")
with status_col:
    st.markdown('<div style="text-align:right;padding-top:11px;color:#6e7b73;font-size:12px">● Planning dataset active</div>', unsafe_allow_html=True)

data = LOCALITIES[selected]
risk = calculate_risk(data["lst"], data["ndvi"], data["built"], data["population"])
contributions = get_contributions(data)
best_intervention, dominant, recommended_plan = recommended_technique(data, selected)

# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.markdown(f'<div style="margin-top:25px;margin-bottom:13px"><div class="eyebrow">CURRENT CONDITIONS</div><div style="font-size:25px;font-weight:700;color:#17231d">{selected}</div></div>', unsafe_allow_html=True)
m1,m2,m3,m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="risk-card"><div class="risk-label">Heat Risk Index</div><div class="risk-number">{risk:.1f}</div><div class="risk-status">out of 100</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Surface Temperature</div><div class="metric-value">{data["lst"]:.1f}°C</div><div class="metric-sub">Observed surface heat</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Built-up Intensity</div><div class="metric-value">{data["built"]}%</div><div class="metric-sub">Developed surface</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Vegetation</div><div class="metric-value">{data["ndvi"]:.2f}</div><div class="metric-sub">NDVI indicator</div></div>', unsafe_allow_html=True)

# ============================================================
# MAIN MAP
# ============================================================

st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
st.markdown('<div class="eyebrow">02 · EXPLORE THE HOTSPOT</div>', unsafe_allow_html=True)
map_title_col,map_info_col=st.columns([3,1])
with map_title_col:
    st.markdown('<div style="font-size:23px;font-weight:700;color:#17231d">Chennai heat map</div><div style="font-size:13px;color:#718078;margin-top:3px">Thermal intensity across selected localities</div>', unsafe_allow_html=True)
with map_info_col:
    st.markdown('<div style="text-align:right;color:#718078;font-size:11px;padding-top:7px">LEAFLET · OPENSTREETMAP</div>', unsafe_allow_html=True)
st_folium(create_main_map(selected), width=None, height=570, returned_objects=[], key="main_heat_map")

# ============================================================
# DIAGNOSIS
# ============================================================

st.divider()
st.markdown('<div class="eyebrow">03 · UNDERSTAND THE HOTSPOT</div>', unsafe_allow_html=True)
diag_left,diag_right=st.columns([1,1.15],gap="large")
with diag_left:
    st.markdown('<div style="font-size:23px;font-weight:700;color:#17231d">What\'s driving the heat?</div><div style="color:#718078;font-size:13px;margin-top:3px;margin-bottom:18px">Contribution to the current Heat Risk Index</div>', unsafe_allow_html=True)
    for name,value in sorted(contributions.items(),key=lambda x:x[1],reverse=True):
        pct=(value/risk*100) if risk>0 else 0
        c1,c2=st.columns([4,1])
        with c1: st.markdown(f'<div style="font-size:13px;font-weight:600;color:#28342d;padding-top:4px">{name}</div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="text-align:right;font-size:12px;font-weight:700;color:#718078;padding-top:4px">{pct:.0f}%</div>',unsafe_allow_html=True)
        st.progress(min(1.0,value/45))
with diag_right:
    st.markdown(f'<div class="recommendation-card"><div class="recommendation-tag">RECOMMENDED FIRST ACTION</div><div class="recommendation-title">{best_intervention}</div><div class="recommendation-text">{recommended_plan["description"]}</div><div class="recommendation-highlight">Primary driver: {dominant}. The recommendation is matched to the available implementation space in {selected}.</div></div>',unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div>',unsafe_allow_html=True)
    st.markdown('<div class="decision-box"><b>Decision logic</b><br><br>HeatScape identifies the largest contributor, checks candidate implementation space, then produces a technique, location and implementable quantity.</div>',unsafe_allow_html=True)

# ============================================================
# SPECIFIC IMPLEMENTATION PLAN
# ============================================================

st.divider()
st.markdown('<div class="eyebrow">04 · IMPLEMENTATION PLAN</div>',unsafe_allow_html=True)
st.markdown('<div style="font-size:25px;font-weight:700;color:#17231d">Where and how much?</div><div style="color:#718078;font-size:13px;margin-top:4px;margin-bottom:18px">The recommendation is converted into a specific location and starting quantity.</div>',unsafe_allow_html=True)

p1,p2,p3=st.columns(3)
with p1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Technique</div><div class="metric-value" style="font-size:21px">{recommended_plan["technique"]}</div><div class="metric-sub">Recommended first action</div></div>',unsafe_allow_html=True)
with p2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Location</div><div class="metric-value" style="font-size:18px">{recommended_plan["location"]}</div><div class="metric-sub">Candidate implementation site</div></div>',unsafe_allow_html=True)
with p3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Starting quantity</div><div class="metric-value">{recommended_plan["quantity"]:,} {recommended_plan["unit"]}</div><div class="metric-sub">Estimated available capacity</div></div>',unsafe_allow_html=True)

if recommended_plan["target_reached"]:
    st.success(f"Exact target: implement {recommended_plan['quantity']:,} {recommended_plan['unit']} at {recommended_plan['location']} to reduce the Heat Risk Index from {risk:.1f} to {TARGET_RISK:.0f} or below.")
else:
    st.warning(f"Even the full available capacity ({recommended_plan['quantity']:,} {recommended_plan['unit']}) only reduces the modelled index to {simulate_intervention(risk, recommended_plan['technique'], recommended_plan['quantity'], data, recommended_plan['available'])[0]:.1f}. A combined intervention is needed to reach {TARGET_RISK:.0f}.")

rec_initial,rec_annual,rec_five=calculate_cost(recommended_plan["technique"],recommended_plan["quantity"])
rc1,rc2,rc3=st.columns(3)
with rc1: st.markdown(f'<div class="cost-card"><div class="cost-label">Initial implementation</div><div class="cost-value">₹{rec_initial:,.0f}</div></div>',unsafe_allow_html=True)
with rc2: st.markdown(f'<div class="cost-card"><div class="cost-label">Annual maintenance</div><div class="cost-value">₹{rec_annual:,.0f}</div></div>',unsafe_allow_html=True)
with rc3: st.markdown(f'<div class="cost-card"><div class="cost-label">5-year lifecycle</div><div class="cost-value">₹{rec_five:,.0f}</div></div>',unsafe_allow_html=True)

# ============================================================
# SIMULATOR
# ============================================================

st.divider()
st.markdown('<div class="eyebrow">05 · TEST AN INTERVENTION</div>',unsafe_allow_html=True)
st.markdown(f'<div style="font-size:26px;font-weight:700;color:#17231d">What happens if we change the plan?</div><div style="color:#718078;font-size:13px;margin-top:4px;margin-bottom:20px">Change the recommended technique, quantity and location. The Heat Risk and lifecycle cost update immediately.</div>',unsafe_allow_html=True)

sim_left,sim_right=st.columns([1,1.25],gap="large")
with sim_left:
    st.markdown('<div class="simulator-card"><div style="font-size:17px;font-weight:700;color:#17231d">Implementation controls</div><div style="color:#718078;font-size:12px;margin-top:3px;margin-bottom:16px">The recommended option is pre-filled, but the planner can test alternatives.</div></div>',unsafe_allow_html=True)
    technique_options=[best_intervention]+[x for x in TECHNIQUES if x!=best_intervention]
    selected_technique=st.selectbox("Cooling technique",technique_options,key="sim_technique")
    plan=technique_plan(selected,selected_technique,data,risk)
    if selected_technique=="Urban Forests & Trees":
        max_q=max(1,int(plan["available"] / 12.5))
        quantity=st.slider("Trees planted",0,max_q,min(plan["quantity"],max_q),1,key="sim_quantity")
    else:
        max_q=max(1,int(plan["available"]))
        step=100 if max_q>=1000 else 50
        default=min(max_q,plan["quantity"])
        quantity=st.slider(f"Implementation quantity ({plan['unit']})",0,max_q,default,step,key="sim_quantity")
    st.caption(f"Candidate location: {plan['location']} · Available capacity: {plan['available']:,} {plan['unit'] if selected_technique != 'Urban Forests & Trees' else 'm²'}")
    sim_location=st.selectbox("Implementation location",[x[0] for x in site_info(selected)["roads"]]+[x[0] for x in site_info(selected)["open"]]+[f"Suitable roofs in {selected}"],index=0,key="sim_location")

sim_after,sim_reduction=simulate_intervention(risk,selected_technique,quantity,data,plan["available"])
sim_initial,sim_annual,sim_five=calculate_cost(selected_technique,quantity)
reduction_pct=(sim_reduction/risk*100) if risk else 0

with sim_right:
    st.markdown('<div class="simulator-card"><div style="font-size:17px;font-weight:700;color:#17231d;margin-bottom:15px">Projected impact</div></div>',unsafe_allow_html=True)
    b,a=st.columns([1,1])
    with b: st.markdown(f'<div class="simulator-label">CURRENT RISK</div><div class="before-number">{risk:.1f}</div>',unsafe_allow_html=True)
    with a: st.markdown(f'<div class="simulator-label">PROJECTED RISK</div><div class="after-number">{sim_after:.1f}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="reduction-card"><div class="reduction-number">↓ {sim_reduction:.1f} risk points</div><div class="reduction-label">{reduction_pct:.1f}% projected reduction</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div style="height:12px"></div><div class="info-box"><b>{selected_technique}</b><br>{quantity:,} {plan["unit"]} at <b>{sim_location}</b><br>Initial: ₹{sim_initial:,.0f} · Annual maintenance: ₹{sim_annual:,.0f} · 5-year lifecycle: ₹{sim_five:,.0f}</div>',unsafe_allow_html=True)

# ============================================================
# INTERVENTION MAP
# ============================================================

st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
st.markdown('<div class="eyebrow">06 · WATCH THE CHANGE</div>',unsafe_allow_html=True)
st.markdown('<div style="font-size:25px;font-weight:700;color:#17231d">Intervention impact simulation</div><div style="color:#718078;font-size:13px;margin-top:4px;margin-bottom:13px">Watch the modelled heat-risk field change as the selected quantity changes.</div>',unsafe_allow_html=True)
components.html(create_intervention_map(data["lat"],data["lon"],risk,sim_after),height=640,scrolling=False)
st.markdown('<div style="color:#7c8781;font-size:10px;margin-top:5px">Thermal field represents the modelled Heat Risk Index, not physical heat dispersion or exact temperature reduction.</div>',unsafe_allow_html=True)

# ============================================================
# BUDGET PLANNER
# ============================================================

st.divider()
st.markdown('<div class="eyebrow">07 · PLAN TO A BUDGET</div>',unsafe_allow_html=True)
st.markdown('<div style="font-size:25px;font-weight:700;color:#17231d">What can we do with the available budget?</div><div style="color:#718078;font-size:13px;margin-top:4px;margin-bottom:18px">Enter a 5-year budget and HeatScape finds the strongest affordable single intervention for this locality.</div>',unsafe_allow_html=True)

budget_col, budget_result = st.columns([1,1.35],gap="large")
with budget_col:
    budget=st.number_input("Budget for 5-year lifecycle (₹)",min_value=0,step=100000,value=1000000,format="%d",key="budget_input")
    st.markdown(f'<div class="budget-card"><div class="budget-label">Available budget</div><div class="budget-value">₹{budget:,.0f}</div><div style="color:#c8d4cd;font-size:12px;margin-top:5px">Includes implementation + 5 years of maintenance in the planning model.</div></div>',unsafe_allow_html=True)
with budget_result:
    affordable, alternatives=budget_plan(selected,data,risk,budget)
    if affordable:
        st.markdown(f'<div class="plan-card"><div class="plan-title">Best affordable option: {affordable["technique"]}</div><div class="plan-detail"><b>Where:</b> {affordable["location"]}<br><b>How much:</b> {affordable["quantity"]:,} {affordable["unit"]}<br><b>5-year cost:</b> ₹{affordable["five_year"]:,.0f}<br><b>Projected Heat Risk:</b> {risk:.1f} → {affordable["after"]:.1f} (↓ {affordable["reduction"]:.1f} points)</div></div>',unsafe_allow_html=True)
        st.markdown("**Other affordable alternatives**")
        for alt in alternatives[1:4]:
            st.markdown(f'<div class="plan-card"><div class="plan-title">{alt["technique"]}</div><div class="plan-detail">{alt["location"]} · {alt["quantity"]:,} {alt["unit"]} · ₹{alt["five_year"]:,.0f} over 5 years · ↓ {alt["reduction"]:.1f} risk points</div></div>',unsafe_allow_html=True)
    else:
        st.warning("The entered budget is too small to fund the minimum modelled intervention. Increase the budget to see an affordable plan.")

# ============================================================
# COST DETAILS
# ============================================================

st.divider()
st.markdown('<div class="eyebrow">08 · COST OF IMPLEMENTATION</div>',unsafe_allow_html=True)
st.markdown('<div style="font-size:25px;font-weight:700;color:#17231d">Current simulation cost</div><div style="color:#718078;font-size:13px;margin-top:4px;margin-bottom:18px">The numbers below update whenever the technique or quantity changes.</div>',unsafe_allow_html=True)
c1,c2,c3=st.columns(3)
with c1: st.markdown(f'<div class="cost-card"><div class="cost-label">Initial implementation</div><div class="cost-value">₹{sim_initial:,.0f}</div></div>',unsafe_allow_html=True)
with c2: st.markdown(f'<div class="cost-card"><div class="cost-label">Annual maintenance</div><div class="cost-value">₹{sim_annual:,.0f}</div></div>',unsafe_allow_html=True)
with c3: st.markdown(f'<div class="cost-card"><div class="cost-label">5-year lifecycle</div><div class="cost-value">₹{sim_five:,.0f}</div></div>',unsafe_allow_html=True)
st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
st.markdown('<div class="info-box"><b>Cost formula</b><br>Initial cost = quantity × (installation + establishment)<br>Annual maintenance = quantity × annual maintenance rate<br>5-year lifecycle = initial cost + (annual maintenance × 5)<br><br>Planning assumptions only. Actual costs vary by site, material, labour and procurement.</div>',unsafe_allow_html=True)

# ============================================================
# METHODOLOGY
# ============================================================

st.divider()
with st.expander("Methodology & data sources"):
    st.markdown("""
### Heat Risk Index
HeatScape combines four transparent indicators:

| Factor | Weight |
|---|---:|
| Surface Heat | 45% |
| Built-up Intensity | 25% |
| Vegetation Deficit | 20% |
| Population Exposure | 10% |

The resulting **Heat Risk Index ranges from 0–100**.

### Data inputs
**Landsat** — Surface temperature  
**Sentinel-2** — Vegetation / NDVI  
**Land cover** — Built-up intensity  
**WorldPop** — Population exposure  
**OpenStreetMap** — Road network and geographic context

### Implementation logic
The prototype checks candidate roadside space, candidate open/green space and estimated suitable roof area to turn a general recommendation into a location and quantity.

### Simulation
The simulator estimates how intervention quantity changes the **HeatScape risk index**. It is a scenario model, not a validated physical climate model, and does not claim an exact future air-temperature reduction.

### Budget mode
The budget planner tests the available budget against the 5-year lifecycle cost of each intervention, respects the estimated site capacity, and selects the strongest affordable option based on modelled risk reduction.

**Important:** current locality, space and cost values are prototype planning values. They should be replaced or validated with processed satellite, municipal GIS/cadastral and procurement data before real-world deployment.
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown('<div class="footer">HeatScape · Urban Heat Reduction Planner<br>Decision support for targeted, explainable cooling interventions</div>',unsafe_allow_html=True)
