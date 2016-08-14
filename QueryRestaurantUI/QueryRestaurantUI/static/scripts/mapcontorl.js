

var MainControl = MainControl || {}
function CreateMapHalper (htmlcontroller) {

    var map;
    var infowindows = [];
    var isMapInit = false;
    var markers = [];
    var selectedFeatures = [];
    var searchCircle = null;

    function mapOnClick(event) {
        ShowItems({lat: event.latLng.lat, lon: event.latLng.lng}, 'getitemsnearme', 'getfeaturesnearme');
        if (searchCircle != null) {
            searchCircle.setMap(null);
        }
        searchCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: event.latLng,
            radius: 3.21869 * 1000
        });
        searchCircle.addListener('click', mapOnClick)
    }

    function initMap() {
        isMapInit = true;

        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 33.4664494, lng: -112.0655065},
            zoom: 12
        });

        map.addListener('click', mapOnClick);
    }

    function addMarker(loc, text, id) {
        var infowindow = new google.maps.InfoWindow({
            content: text
        });
        var marker = new google.maps.Marker({
            position: loc,
            map: map,
            Icon: 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
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
                var reviewsHtml = '';
                if (results.reviews.constructor === Array) {
                    var i = 0;
                    for (i = 0; i < results.reviews.length; i++) {
                        reviewsHtml += htmlcontroller.createReview(results.reviews[i])
                    }
                    $('#itemReviews').html('<div class="container-fluid">' + reviewsHtml + '</div>');
                    $('#generalInfo').html('<div class="container-fluid">' + reviewsHtml + '</div>');
                    $('#features').html('<div class="container-fluid">' + htmlcontroller.createFeatures(id,results.features,results.reviews) + '</div>');
                    //$('#similar').html('<div class="container-fluid">' + htmlcontroller.createSimilarItems(id,results.similarItems) + '</div>');
                    hideAll();
                    $('#infoDataMain').modal('toggle');
                    $('#infoDataMain').modal('show');

                }
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
                        if (results.items.indexOf(markers[m].item) > -1) {
                            markers[m].setIcon('http://maps.google.com/mapfiles/kml/paddle/grn-circle.png')
                        }
                        else {
                            markers[m].setIcon('http://maps.google.com/mapfiles/kml/paddle/red-circle.png')
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
FeatureHelper.featureManager = CreateFeatureHelper(MainControl.GoogleMapHelper);