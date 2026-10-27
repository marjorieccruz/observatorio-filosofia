import pandas as pd, json, plotly.express as px, plotly.io as pio
pio.templates.default = "plotly_white"
COR = "#3b5b92"
mun25 = pd.read_csv("dados/es_municipios_2025.csv")
esc25 = pd.read_csv("dados/es_escolas_2025.csv")
serie = pd.read_csv("dados/es_municipios_em_serie.csv")
afd = pd.read_csv("dados/es_afd_municipios_medio.csv")
with open("dados/es_municipios.geojson") as f:
    geo = json.load(f)
for ft in geo["features"]:
    ft["id"] = int(ft["properties"]["CD_MUN"])
