# This is a configuration class for generating the JS context for Google Maps 3D Platform

class TacticalMapsRenderer:
    """Generates the HTML/JS configuration for rendering Google Maps Platform 3D views."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def generate_dashboard_view(self, lat, lng, zoom=12, heatmaps_mode=False):
        """Returns the necessary component logic for the tactical dashboard map."""
        
        heatmap_js = ""
        if heatmaps_mode:
            heatmap_js = "libraries=visualization&"
            
        return f"""
        <script src="https://maps.googleapis.com/maps/api/js?key={self.api_key}&{heatmap_js}callback=initMap" async defer></script>
        <div id="map" style="width: 100%; height: 100%;"></div>
        <script>
            let map;
            function initMap() {{
                map = new google.maps.Map(document.getElementById("map"), {{
                    center: {{ lat: {lat}, lng: {lng} }},
                    zoom: {zoom},
                    mapTypeId: 'satellite',
                    tilt: 45 // Enforce 3D mode
                }});
                
                // Overlay SIRIUS Polygons
                const siriusCoords = [
                    {{ lat: -23.5505, lng: -46.6333 }},
                    {{ lat: -23.5605, lng: -46.6433 }},
                    {{ lat: -23.5705, lng: -46.6533 }}
                ];
                
                const siriusPolygon = new google.maps.Polygon({{
                    paths: siriusCoords,
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#FF0000",
                    fillOpacity: 0.35,
                }});
                siriusPolygon.setMap(map);
            }}
        </script>
        """
