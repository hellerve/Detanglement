//Don't pollute the global namespace, kids!
var tangle = {};
tangle.city = false;
tangle.country = false; 
tangle.map = null;
tangle.googleLocationMarker = null;
tangle.osmLocationMarker = null;
tangle.kartographLocationMarker = null;
tangle.googleMarkers = [];
tangle.osmMarkers = [];
tangle.kartographMarkers = [];
tangle.googleMarkerNames = [];
tangle.osmMarkerNames = [];
tangle.kartographMarkerNames = [];
tangle.mapchoice = 0;
tangle.loc = [];
load();

toastr.options.closeButton = true;
checkButtonDisplay();
window.onresize = load;

(function() {
  $(document).ready(function() {
    $('.menu').click(function() {
      $('nav.right').addClass('open');
      $('body').addClass('menu-open');
      return false;
    });
    return $(document).click(function() {
      $('body').removeClass('menu-open');
      return $('nav').removeClass('open');
    });
  });

}).call(this);

//Startup function; checks whether the button should be disabled
//and initializes the map.
function load(){
    if(tangle.mapchoice === 0){
        initializeGoogleMap();
    }else if(tangle.mapchoice === 1){
        initializeKartograph();
    }else if(tangle.mapchoice === 2){
        initializeOSM();
    }
};

//Gets the currently used map.
function getMap(){
    return tangle.google;
}

//Sets the currently used map.
function setMap(value){
    tangle.mapchoice = value;
}

//Checks whether the form is filled.
function fillForm(){
    tangle.country = (document.getElementById("country").value != "");
    tangle.city = (document.getElementById("city").value != "");
    checkButtonDisplay();
};

//Checks whether the form submit button should be enabled.
function checkButtonDisplay(){
    document.getElementById("submitBtn").disabled = !(tangle.country && tangle.city);
};

//Initializes the Google Map with center at berlin.
//Yeah, I know, I ama a europocentric asshole.
function initializeGoogleMap(){
    document.getElementById('kartograph-canvas').style.height = "0px";
    document.getElementById('kartograph-canvas').style.width = "0px";
    document.getElementById('osm-canvas').style.height = "0px";
    document.getElementById('osm-canvas').style.width = "0px";
    document.getElementById('google-canvas').style.height = window.innerHeight + "px";
    document.getElementById('google-canvas').style.width = window.innerWidth + "px";
    if(tangle.googleLocationMarker === null){
        var berlin = new google.maps.LatLng(52.524, 13.401);
        var mapOptions = {
            center: berlin,
            zoom: 3
        };
        tangle.map = new google.maps.Map(document.getElementById("google-canvas"), 
                                  mapOptions);
        var image = "../images/pinico.png";
        tangle.googleLocationMarker = new google.maps.Marker({position: berlin, 
                                map: null,
                                title: "Your Location",
                                icon: image});
    }else
        googleLocationMarker.setMap(tangle.map);
};

//Initializes the Kartograph Map.
function initializeKartograph(){
    document.getElementById("kartograph-canvas").style.height = window.innerHeight + "px";
    document.getElementById("kartograph-canvas").style.width = window.innerWidth + "px";
    document.getElementById('osm-canvas').style.height = "0px";
    document.getElementById('osm-canvas').style.width = "0px";
    document.getElementById("google-canvas").style.height = "0px";
    document.getElementById("google-canvas").style.width = "0px";
    tangle.map = kartograph.map('#kartograph-canvas');
    tangle.map.loadMap('../images/worldView.svg', addBasicLayers);
};

//initializes the OSM map
function initializeOSM(){
    document.getElementById('osm-canvas').style.height = window.innerHeight + "px";
    document.getElementById('osm-canvas').style.width = window.innerWidth + "px";
    document.getElementById('kartograph-canvas').style.height = "0px";
    document.getElementById('kartograph-canvas').style.width = "0px";
    document.getElementById('google-canvas').style.height = "0px";
    document.getElementById('google-canvas').style.width = "0px";
    tangle.map = new OpenLayers.Map("osm-canvas");
    var fromProjection = new OpenLayers.Projection("EPSG:4326");
    var toProjection = new OpenLayers.Projection("EPSG:900913");
    var position = new OpenLayers.LonLat(13.401, 52.524).transform(fromProjection, toProjection);
    var zoom = 3; 
    tangle.osmMarkers = new OpenLayers.Layer.Markers("Markers"); 
    tangle.map.addLayer(new OpenLayers.Layer.OSM());
    tangle.map.addLayer(tangle.osmMarkers);
    tangle.map.setCenter(position, zoom);
    if(tangle.osmLocationMarker === null){
        tangle.osmLocationMarker = new OpenLayers.Marker(position);
        tangle.osmLocationMarker.icon.imageDiv.title = "Your Location";
        var image = "../images/osmicon.png";
        tangle.osmLocationMarker.setUrl(image);
    }
};

//Adds layers to the Kartograph SVG. Needed for Kartograph's setup.
function addBasicLayers(){
    tangle.map.addLayer('background');
    tangle.map.addLayer('graticule');
    tangle.map.addLayer('world');
    tangle.map.addLayer('lakes');
    tangle.map.addLayer('trees');
    tangle.map.addLayer('depth');
    tangle.map.addLayer('cities');
};

//Tells Python the location submitted by the user via form.
function getRegion(){
    var countryVal = document.getElementById('country').value;
    var cityVal = document.getElementById('city').value;
    interfaces.submitLocation(countryVal, cityVal);
};

//Deletes a data marker at a specific location.
function deleteMarker(lat, lon){
    if(tangle.mapchoice === 0)
        deleteGoogleMarker(lat, lon);
    else if(tangle.mapchoice === 1)
        deleteKartographMarker(lat, lon);
    else if(tangle.mapchoice === 2)
        deleteOsmMarker(lat, lon);
};

//Deletes a google marker at a specific location
function deleteGoogleMarker(lat, lon){
    var latlng = new google.maps.LatLng(lat, lon);
    for(var i = 0; i < tangle.googleMarkers.length; i++){
        if(tangle.googleMarkers[i].getPosition() == latlng){
            tangle.googleMarkers[i].setMap(null);
            tangle.googleMarkers.splice(i, 1);
            tangle.googleMarkerNames.splice(i, 1);
        }
    }
};

//deletes a kartograph marker at a specific location(STUB)
function deleteKartographMarker(lat, lon){
};

//deletes an osm marker at a specific location
function deleteOsmMarker(lat, lon){
    var lonlat = new OpenLayers.LonLat(lon, lat);
    for(var i = 0; i < tangle.osmMarkers.length; i++){
        if(tangle.osmMarkers[i].getPosition() == lonlat){
            tangle.osmMarkers[i].destroy();
            tangle.osmMarkers.splice(i, 1);
            tangle.osmMarkerNames.splice(i, 1);
        };
    }
}

//Deletes the location marker,
function deleteLocationMarker(){
    if(tangle.mapchoice === 0)
        tangle.locationMarker.setMap(null);
    else if(tangle.mapchoice === 1)
        return;
    else if(tangle.mapchoice === 2)
        tangle.locationMarker.destroy();
};

//Adds a data marker at a specific location.
function addMarker(lat, lon, name){
    if(tangle.mapchoice === 0)
        addGoogleMarker(lat, lon, name);
    else if(tangle.mapchoice === 1)
        addKartographMarker(lat, lon, name);
    else if(tangle.mapchoice === 2)
        addOsmMarker(lat, lon, name);
};

//Adds a google marker at a specific location.
function addGoogleMarker(lat, lon, name){
    var latlon = new google.maps.LatLng(lat, lon);
    var marker = new google.maps.Marker({position: latlon, 
                                        map: tangle.map,
                                        title: name});
    tangle.googleMarkers.push(marker);
    tangle.googleMarkerNames.push(name);
    google.maps.event.addListener(marker, 'click', function(){
        interfaces.visualizeTrends(name);
    });
};

//Adds a kartograph marker at a specific location.(STUB)
function addKartographMarker(lat, lon, name){
};

//Adds an osm marker at a specific location
function addOsmMarker(lat, lon, name){
    var lonlat = new OpenLayers.LonLat(lon, lat).transform(
            new OpenLayers.Projection("EPSG:4326"),
            tangle.map.getProjectionObject());
    var marker = new OpenLayers.Marker(lonlat);
    marker.icon.imageDiv.title = name;
    tangle.osmMarkers.addMarker(marker);
    tangle.osmMarkerNames.push(name);
    marker.events.register('click', tangle.osmMarkers, function(){
        interfaces.visualizeTrends(name);
    });
};


//adds a location marker at a specific location.
function addLocationMarker(lat, lon){
    if(tangle.mapchoice === 0)
        addGoogleLocationMarker(lat, lon, name);
    else if(tangle.mapchoice === 1)
        addKartographMarker(lat, lon, name);
    else if(tangle.mapchoice === 2)
        addOsmMarker(lat, lon, name);
    toastr.success("Located you at: " + lat + ", " + lon, "Location success");
};

//adds a google location marker at a specific location
function addGoogleLocationMarker(lat, lon){
    var latlon = new google.maps.LatLng(lat, lon);
    tangle.googleLocationMarker.setPosition(latlon);
    tangle.googleLocationMarker.setMap(tangle.map);
};

//adds a kartograph location marker at a specific location(STUB)
function addKartographLocationMarker(lat, lon){
};

//adds an osm location marker at a specific location
function addOsmLocationMarker(lat, lon){
    var lonlat = new OpenLayer.LonLat(lon, lat).tranfrom(
                    newOpenLayers.Projection("EPSG:4326"),
                    tangle.map.getProjectionObject());
    tangle.osmLocationMarker.setPosition(lonlat);
    tangle.osmLocationMarker.display(true);
};

//Tells Python to visualize the data for a clicked location.
function getLocalizedTrends(){
    if(tangle.locationMarker.getMap == null){
        toastr.error("You have not submitted your location yet.", "Trends error");
    }else{
        interfaces.visualizeLocationTrends(locationMarker.getPosition().lat(), 
                                           locationMarker.getPosition().lon());
    }
};

//geolocates the user
function geolocate(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(locationSuccess(), locationError());
        return true;
    } else {
        toastr.error('Geolocalization is not supported by your device. Trying ip-based localization.', 
                     'Localization error');
        return false;
    }
};

//reacts to the failure of the localization
function locationError(error){
    toastr.error('Geolocalization failed with code ' + error.code + '; the returned message states' +
                 error.message, 'Localization error');
};

//reacts to success of the localization
function locationSuccess(pos){
    tangle.loc = [pos.coords.latitude, pos.coords.longitude];
};

function getLocation(){
    return tangle.loc;
}

