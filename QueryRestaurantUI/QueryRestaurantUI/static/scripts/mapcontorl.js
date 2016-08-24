

var MainControl = MainControl || {}
function CreateMapHalper (htmlcontroller) {

    var map;
    var infowindows = [];
    var isMapInit = false;
    var markers = [];
    var selectedFeatures = [];
    var searchCircle = null;
    var centerOfSearchLatLong = undefined;
    var searchOnMap = false;
    var centerOfSearchSelected = false;
    var centerOfSearchControlDiv = document.createElement('div');
    var centerOfSearchControl;
    var controlUI = document.createElement('div');
    var controlText = document.createElement('div');

    function SearchOnMapControl(controlDiv, map) {

        // Set CSS for the control border.
        controlUI.style.backgroundColor = 'rgb(225,0,0)';
        controlUI.style.border = '2px solid #fff';
        controlUI.style.borderRadius = '3px';
        controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
        controlUI.style.cursor = 'pointer';
        controlUI.style.marginBottom = '22px';
        controlUI.style.textAlign = 'select search area';
        controlUI.title = 'Click to select search area on the map';
        controlDiv.appendChild(controlUI);

        // Set CSS for the control interior.
        controlText.style.color = 'rgb(25,25,25)';
        controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
        controlText.style.fontSize = '16px';
        controlText.style.lineHeight = '38px';
        controlText.style.paddingLeft = '5px';
        controlText.style.paddingRight = '5px';
        controlText.innerHTML = 'Click Here for Map Search';
        controlUI.appendChild(controlText);

        // Setup the click event listeners: simply set the map to Chicago.
        controlUI.addEventListener('click', StartSelectingSearchArea);

    }

    function mouseMove(event) {
        if (searchOnMap == true) {
            if (centerOfSearchSelected == true) {
                var radius = google.maps.geometry.spherical.computeDistanceBetween(centerOfSearchLatLong, event.latLng);
                if (searchCircle != undefined) {
                    searchCircle.setMap(null);
                }
                searchCircle = new google.maps.Circle({
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: '#FF0000',
                    fillOpacity: 0.15,
                    map: map,
                    center: centerOfSearchLatLong,
                    radius: radius
                });
                google.maps.event.addListener(searchCircle, 'click', mapOnClick);
                google.maps.event.addListener(searchCircle, "mousemove", mouseMove);

            }
        }
    }

    function mapOnClick(event) {
        if (searchOnMap == true) {
            if (centerOfSearchSelected == false) {
                centerOfSearchLatLong = event.latLng;
                centerOfSearchSelected = true;
            }
            else {
                var radius = google.maps.geometry.spherical.computeDistanceBetween(centerOfSearchLatLong, event.latLng);
                radius = radius / 1600
                centerOfSearchSelected = false;
                if (searchCircle != undefined) {
                    searchCircle.setMap(null);
                }
                searchCircle = new google.maps.Circle({
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: '#FF0000',
                    fillOpacity: 0.15,
                    map: map,
                    center: centerOfSearchLatLong,
                    radius: radius * 1600
                });
                google.maps.event.addListener(searchCircle, 'click', mapOnClick);
                google.maps.event.addListener(searchCircle, "mousemove", mouseMove);
                FinishSelectingSearchArea();
                ShowItems({
                    lat: centerOfSearchLatLong.lat,
                    lon: centerOfSearchLatLong.lng,
                    distance: radius
                }, 'getitemsnearme', 'getfeaturesnearme');

            }
        }
    }

    function FinishSelectingSearchArea() {
        controlUI.style.backgroundColor = 'rgb(225,0,0)';
        controlText.innerHTML = 'Click Here for Map Search';
        searchOnMap = false;
        centerOfSearchSelected == false
    }

    function StartSelectingSearchArea() {
        controlUI.style.backgroundColor = 'rgb(0,225,0)';
        controlText.innerHTML = 'Select on Map Search Area';
        centerOfSearchSelected == false;
        searchOnMap = true;
        clearMarkers();
        if (searchCircle != undefined) {
            searchCircle.setMap(null);
        }
    }

    function initMap() {
        isMapInit = true;

        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 33.4664494, lng: -112.0655065},
            zoom: 12
        });

        map.addListener('click', mapOnClick);
        google.maps.event.addListener(map, "mousemove", mouseMove);
        centerOfSearchControl = new SearchOnMapControl(centerOfSearchControlDiv, map);
        centerOfSearchControlDiv.index = 1;
        map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerOfSearchControlDiv);
    }

    function addMarker(loc, text, id) {
        var infowindow = new google.maps.InfoWindow({
            content: text
        });
        var marker = new google.maps.Marker({
            position: loc,
            map: map,
            Icon: 'http://maps.google.com/mapfiles/ms/micons/red-dot.png',
            title: text,
            item: id
        });

        marker.addListener('click', function () {
            closeInfoWindow();
            infowindow.open(map, marker);
            //marker.setIcon('http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png')
            showItemDetails(id);

        });
        markers.push(marker);
        infowindows.push(infowindow);
    }

    function hideAll(){
        $('tr.sentences').hide();
        $('tr.reviews').hide();
    }

    function showItemDetails(id) {
        $.ajax({
            type: "GET",
            url: 'getitem',
            data: {id: id},
            success: function (results) {
                htmlcontroller.showRestaurantDetails(id, results);
                hideAll();
            }
        });

    }

    function showReviews(featureId,polarity){
        hideAll();
        htmlcontroller.showReviews(featureId,polarity)
    }

    function showSentences(featureId,polarity){
        hideAll();
        htmlcontroller.showSentences(featureId,polarity)
    }

    function arrayToString(array) {
        var result = '';
        result = array.join(',');
        //   for(index in array){
        //	result += array.toString()+',';
        //}
        return result;
    }

    function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
            infowindows[i].setMap(map);
        }
    }

    function closeInfoWindow() {
        for (var i = 0; i < infowindows.length; i++) {
            infowindows[i].close();
        }
    }

    function clearMarkers() {
        setMapOnAll(null);
    }

    function cleanMap() {
        clearsearchCircle();
        clearMarkers();
    }

    function clearsearchCircle(){
        if (searchCircle != null) {
            searchCircle.setMap(null);
        }
        searchCircle = null;
    }
    function deleteMarkers() {
        clearMarkers();
        markers = [];
    }

    function isInit() {
        showAll();
        return isMapInit;
    }

    function markRestaurantsBySelectedFeatures() {
        items = '';
        itemsArr = [];
        for (m in markers) {

            itemsArr.push(markers[m].item);
        }

        if (selectedFeatures.length > 0) {
            features = arrayToString(selectedFeatures);
            items = arrayToString(itemsArr);
            $.ajax({
                type: "GET",
                url: "getitemswithfeatures",
                data: {items: items, features: features},
                success: function (results) {
                    for (m in markers) {
                        if (results.items.HaveAllFeatures.indexOf(markers[m].item) > -1) {
                            markers[m].setIcon('http://maps.google.com/mapfiles/ms/micons/green-dot.png')
                        }
                        else if (results.items.HavePartOFFeatures.indexOf(markers[m].item) > -1) {
                            markers[m].setIcon('http://maps.google.com/mapfiles/ms/micons/yellow-dot.png')
                        }
                        else {
                            markers[m].setIcon('http://maps.google.com/mapfiles/ms/micons/red-dot.png')
                        }
                    }
                }
            });
        }
    }

    function updateFeaturePanel(featureUrl, data) {
        $.ajax({
            type: "GET",
            url: featureUrl,
            data: data,
            success: AddFeatures
        });
    }

    function AddMarkers (markers) {
        deleteMarkers();
        selectedFeatures = [];
        markers.items.items.forEach(function (point) {
            var loc = {lat: parseFloat(point.lat), lng: parseFloat(point.lng)};
            MainControl.GoogleMapHelper.addMarker(loc, point.Name, point.id);
        })

    }

    function updateMapsItems(itemUrl, data) {
        $.ajax({
            type: "GET",
            url: itemUrl,
            data: data,
            success:AddMarkers
        });
    }

    function AddFeatures(results) {
        var text = '';
        for (i = 0; i < results.features.length; i++) {
            text += '<button type="button" class="btn btn-default" feature="' + results.features[i][1] + '" onclick="MainControl.GoogleMapHelper.featureClick(' + results.features[i][1] + ')">' + results.features[i][0] + '(' + results.features[i][2] + ')' + '</button>'
        }
        $('#homeInfo').html(text);
        text = '';
        for (i = 0; i < results.features.length; i++) {
            text += '<button type="button" class="btn btn-default" feature="' + results.features[i][1] + '" onclick="FeatureHelper.featureManager.getFeatureInfo(' + results.features[i][1] + ')">' + results.features[i][0] + '(' + results.features[i][2] + ')' + '</button>'
        }
        $('#features').html(text);

    }
    function ShowItems(data, itemUrl, featureUrl) {
        updateMapsItems(itemUrl, data);
        updateFeaturePanel(featureUrl, data);
    }

    function showAll() {
        clearsearchCircle();
        ShowItems({}, "allpoints", "allfeatures");

    }

    function featureClick(id) {
        itemIndex = $.inArray(id, selectedFeatures)
        if (itemIndex >= 0) {
            delete selectedFeatures[itemIndex];
            $('button[feature="' + id + '"]').removeClass('btn-info').addClass('btn-default');

        } else {
            selectedFeatures.push(id);
            $('button[feature="' + id + '"]').removeClass('btn-default').addClass('btn-info');
        }
        markRestaurantsBySelectedFeatures();
    }

    return {
        initMap: initMap,
        addMarker: addMarker,
        isInit: isInit,
        featureClick: featureClick,
        ShowAll: showAll,
        showReviews: showReviews,
        showSentences: showSentences,
        cleanMap:cleanMap,
        ShowItems:ShowItems,
        updateFeaturePanel:updateFeaturePanel,
        updateMapsItems:updateMapsItems,
        AddFeatures:AddFeatures,
        AddMarkers:AddMarkers
    };
};



var htmlcontroller = htmlManager.htmlGenerator
var MainControl = MainControl || {}
MainControl.GoogleMapHelper = CreateMapHalper(htmlManager.htmlGenerator);
var FeatureHelper = FeatureHelper || {}
FeatureHelper.featureManager = CreateFeatureHelper(MainControl.GoogleMapHelper,htmlManager.htmlGenerator);