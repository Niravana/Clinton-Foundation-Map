import IPython.core.display as di

# This line will hide code by default when the notebook is exported as HTML
di.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)
import pandas as pd 
import json
import branca
import folium
import os
from folium.plugins import MarkerCluster

m = folium.Map(location = [30.0150, -105.2705],zoom_start=2.7)
df = pd.read_csv("info.csv")
df.columns = [c.lower().replace(' ', '_') for c in df.columns]
y=[-74.005974,-66.1057,33.759819,30.104429,35.686073,-72.000,-75.479424,123.3833318,-89.1871800,55.45,-78.1332,-60.987469,-61.383333,-77.355415,-81.716650,-88.073889,-61.390049,-61.840130,-80.191788,-76.612190,-95.369804,-82.324829,-91.40317,-117.161087,-122.419418,-122.271111,-119.787125,-118.243683,-95.682510,-95.992775,-80.19,-92.289597,-76.147423,-93.265015,-83.045753,-74.005,-134.418498326,-86.299969,-92.289595,-112.074037,-121.494400,-104.990251,-72.685093,-75.524368,-84.280733,-84.387982,-157.858333,-93.624959,-116.202314,-89.650148,-86.158068,-95.675158,-84.873283,-91.140320,-71.058880,-76.492183,-82.010515,-84.555535,-93.089958,-92.173516,-90.184810,-112.024505,-78.638179,-100.783739,-96.685198,-122.031073,-74.742938,-105.937799,-119.767403,-73.756232,-82.998794,-97.516428,-70.896715,-76.886701,-71.412834,-81.034814,-100.350966,-86.781602,-97.743061,-111.891047,-77.436048,-72.575387,-122.900695,-89.401230,-79.931051,-104.820246,-92.289596,-92.289594]
x=[40.712776,18.466299,-13.995720,-1.970579,-7.768059,19.167,10.391049,-10.4666648,13.6893500,-4.61667,18.21895,14.010109,12.65,25.047983,12.547930,17.553056,15.302880,17.118480,25.761681,39.290386,29.760427,29.651634,31.56044,32.715736,37.774929,37.804363,36.737797,34.052235,37.417824,36.153980,25.76,34.746483,43.048122,44.977753,42.331429,40.713,58.301165462,32.366805,34.746481,33.448377,38.581572,39.739236,41.763711,39.158168,30.438256,33.748995,21.306944,41.586835,43.615019,39.781721,39.768403,39.047345,38.200905,30.458283,42.360082,38.978445,33.473498,42.732535,44.953703,38.576702,32.298757,46.588371,35.779590,46.808327,40.825763,37.977978,40.217053,35.686975,39.163798,42.652579,39.961176,35.467560,42.519540,40.273191,41.823989,34.000710,44.368316,36.162664,30.267153,40.760779,37.540725,44.260059,47.037874,43.073052,32.776475,41.139981,34.74648,34.746483]
df["lat"] = x
df["long"] = y
for row in df.itertuples():
    html = ""
    html += """<h1>""" + row.thematic_area + """</h1><br>""" + """<p><strong>""" + row.initiative + """</strong></p>""" + """<p><b>""" + row.name +"""</b></p>""" + """<p> """+ row.copy + """</p>""" 
    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(location=[row.lat, row.long], popup=popup, icon=folium.Icon(color='green' if row.thematic_area == 'Inspiring Civic Engagement & Service' else 'red' if row.thematic_area == "Improving Public Health" else 'blue', prefix='fa', icon='circle')).add_to(m)


with open('countries.json') as geo_json_data:
    geo_json_data = json.load(geo_json_data)

country_dict = df.set_index('state')['number']
country_dict = country_dict[~country_dict.index.duplicated(keep="first")]


import branca.colormap as cm
step = cm.StepColormap(
    ['blue', 'red', 'green', 'purple', 'white'],
    vmin=1, vmax=6,
    index=[1, 1.9, 2.9, 3.9, 4.9, 5.9],
    caption='step'
)


colormap = cm.StepColormap(
    ['blue', 'red', 'green', 'purple', 'white'],
    vmin=1, vmax=6,
    index=[1, 1.9, 2.9, 3.9, 4.9, 5.9],
    caption='step'
)

def style_function(feature):
    countried = country_dict.get(feature['id'], None)
    return {
        'fillOpacity': 0.5,
        'weight': 0.5,
        'fillColor': '#C0C0C0' if countried is None else step(countried)
    }
folium.GeoJson(
    geo_json_data,
    style_function=style_function
).add_to(m)


from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Thematic Area</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Improving Public Health</li>
    <li><span style='background:blue;opacity:0.7;'></span>Creating Economic Opportunity</li>
    <li><span style='background:green;opacity:0.7;'></span>Inspiring Civic Engagement & Service</li>
    <li><span style='background:purple;opacity:0.7;'></span>More Than One Thematic Area</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)
m.save('qlikmap.html')
m