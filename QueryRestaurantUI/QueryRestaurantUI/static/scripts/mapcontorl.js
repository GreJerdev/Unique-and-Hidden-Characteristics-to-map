
var MainControl = MainControl || {}
MainControl.GoogleMapHelper = (function () {

    var map;
    var infowindows = [];
    var isMapInit = false;
    var markers = [];
    var selectedFeatures = [];
    var searchCircle = null;
    
    function mapOnClick(event) {
        ShowItems({ lat: event.latLng.lat, lon: event.latLng.lng }, 'getitemsnearme', 'getfeaturesnearme');
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
            center: { lat: 33.4664494, lng: -112.0655065 },
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
            marker.setIcon('http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png')
            showItemDetails(id);
            //$('#itemInfo').html(text);
            //$('#itemInfo').show();
        });
        markers.push(marker);
        infowindows.push(infowindow);
    }

    function createReview(review){
        var reviewHtml = '<div class="row"> <div polarity="'+review.polarity+'" reviewid="'+review.id+'">';
        for(r = 0; r <review.sentences.length; r++){
            var colorClass = 'bg-warning'
            if(colorClass != 0){
                colorClass = review.sentences[r].polarity > 0 ? 'bg-success' : 'bg-danger';
            }
            var sentenceHtml = '<div class="'+colorClass+'">';
            for(j=0; j <review.sentences[r].members.length; j++){
                var member = review.sentences[r].members[j]
                var memberHtml = ''
                if ( member.hasOwnProperty('featureId') ) {
                    memberHtml = '<a href="#" onclick="return '+member.featureId+';">'+member.text+'</a>'
                }
                else{
                    memberHtml = member.text;
                }
                sentenceHtml += memberHtml
            }
            sentenceHtml += '</div>'
            reviewHtml += sentenceHtml
        }
        reviewHtml+= '</div></div><div class="row">__</div>'
        return reviewHtml;
    }

    function showItemDetails(id) {
        $.ajax({
            type: "GET",
            url: 'getreviewsentencesbyitemid',
            data: {id:id},
            success: function (results) {
                var reviewsHtml = '';
                debugger;
                if(results.reviews.constructor === Array){
                var i = 0;
                for(i = 0; i < results.reviews.length; i++){
                    reviewsHtml += createReview(results.reviews[i])
               }

               $('#itemInfo').html( '<div class="container-fluid">'+reviewsHtml+'</div>')
               }


            }
        });

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
                data: { items: items, features: features },
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

    function ShowItems(data, itemUrl, featureUrl) {
        $.ajax({
            type: "GET",
            url: itemUrl,
            data: data,
            success: function (results) {

                console.log(results.items)
                deleteMarkers();
                selectedFeatures = [];
                results.items.items.forEach(function (point) {
                    var loc = { lat: parseFloat(point.lat), lng: parseFloat(point.lng) };
                    console.log(loc);

                    MainControl.GoogleMapHelper.addMarker(loc, point.Name, point.id);
                })

            }
        });
        $.ajax({
            type: "GET",
            url: featureUrl,
            data: data,
            success: function (results) {
                var text = '';
                for (i = 0; i < results.features.length; i++) {
                    text += '<button type="button" class="btn btn-default" feature="' + results.features[i][1] + '" onclick="MainControl.GoogleMapHelper.featureClick(' + results.features[i][1] + ')">' + results.features[i][0] + '(' + results.features[i][2] + ')' + '</button>'
                }
                $('#homeInfo').html(text);


            }
        });
    }

    function showAll() {
        ShowItems({}, "allpoints", "allfeatures")
        if (searchCircle != null) {
            searchCircle.setMap(null);
        }
        searchCircle = null;
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
    };
})();
