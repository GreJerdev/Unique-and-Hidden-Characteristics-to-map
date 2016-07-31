var MainControl = MainControl || {}
MainControl.GoogleMapHelper = (function () {

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
            marker.setIcon('http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png')
            showItemDetails(id);
            //$('#itemInfo').html(text);
            //$('#itemInfo').show();
        });
        markers.push(marker);
        infowindows.push(infowindow);
    }

    function getClassByPolarity(polarity) {
        var polarityClass ='neutral';
        if (polarity > 0){
            polarityClass = 'positive'
        }else{
            polarityClass = 'negative'
        }
        return polarityClass
    }

    function getColorClassByPolarity(polarity) {
        var colorClass ='nautral ';
        if (polarity == 0) {
            colorClass = 'bg-warning';
        }else if (polarity > 0){
            colorClass = 'bg-success'
        }else{
            colorClass = 'bg-danger'
        }

        return colorClass
    }

    function getSizeByTfIdf(tfIdf) {
        var floatTfIdf = parseFloat(tfIdf);
        var size = 6;
        if (floatTfIdf > 0 && floatTfIdf <= 0.2){
            size = 5;
        }else if (floatTfIdf > 0.2 && floatTfIdf <= 0.4){
            size = 4;
        }else if (floatTfIdf > 0.4 && floatTfIdf <= 0.6){
            size = 3;
        }else if (floatTfIdf > 0.6 && floatTfIdf <= 0.8){
            size = 2;
        }else if (floatTfIdf > 0.8 && floatTfIdf <= 1){
            size = 1;
        }
        return size;
    }

    function createSenteces(sentence){
        var sentenceHtml = '<div class="sentence ' + getColorClassByPolarity(sentence.polarity) + ' '+getClassByPolarity(sentence.polarity)+'">';
        for (j = 0; j < sentence.members.length; j++) {
            var member = sentence.members[j]
            var memberHtml = ''
            if (member.hasOwnProperty('featureId')) {
                memberHtml = '<a href="#" onclick="return ' + member.featureId + ';">' + member.text + '</a>'
            }
            else {
                memberHtml = member.text;
            }
            sentenceHtml += memberHtml
        }
        sentenceHtml += '</div>'
        return sentenceHtml;
    }

    function createReview(review) {
        var reviewHtml = '<div class="row well '+getClassByPolarity(review.polarity)+'" reviewid="' + review.id + '">';
        for (r = 0; r < review.sentences.length; r++) {
            reviewSentences = review.sentences[r];
            reviewHtml += createSenteces(reviewSentences);
        }
        reviewHtml += '</div>'
        return reviewHtml;
    }

    function getFeatureReivews(fId, reviews){
        var reviewsHtml =  '';
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true){
                if (reviews[reviews_index]['features'].hasOwnProperty(fId) == true){
                    reviewsHtml += createReview(reviews[reviews_index]);
                }
            }
         }

        return reviewsHtml;
    }

    function  getFeatureSentences(featureId, reviews) {
        var sentencesHtml ='';
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true){
                if (reviews[reviews_index]['features'].hasOwnProperty(featureId) == true){
                    var sentences = reviews[reviews_index].sentences;
                    for(sentencesIndex = 0; sentencesIndex < sentences.length;sentencesIndex++){
                        if (sentences[sentencesIndex].features.hasOwnProperty(reviews[reviews_index]['features'][featureId]) == true){
                            sentencesHtml+=createSenteces(sentences[sentencesIndex]);
                        }
                    }
                }
            }
         }
        return sentencesHtml;
    }

    function countSentences(featureId, reviews, polarity){
        var count = 0;
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true){
                if (reviews[reviews_index]['features'].hasOwnProperty(featureId) == true){
                    var sentences = reviews[reviews_index].sentences;
                    for(sentencesIndex = 0; sentencesIndex < sentences.length;sentencesIndex++){
                        if (sentences[sentencesIndex].features.hasOwnProperty(reviews[reviews_index]['features'][featureId]) == true){
                            if(polarity=='all'){
                                 count++
                            }
                            else if (sentences[sentencesIndex].polarity > 0 && polarity=='pos'){
                                count++
                            }else if  (sentences[sentencesIndex].polarity < 0 && polarity=='neg') {
                                count++
                            }
                        }
                    }
                }
            }
         }
        return count;
    }

    function createFeatures(itemId,features,reviews){
        var featuresHtml = '<table class="table"><thead><tr><th>Feature</th><th>Tf-Idf</th><th>Polarety</th><th>All Sentemens</th><th>Pos Sentemens</th><th>Neg Sentemens</th></tr></thead><tbody>';
        for (i = 0; i < features.length; i++) {
            var coloreClass = getColorClassByPolarity(features[i].polarity);
            var size = getSizeByTfIdf(features[i].tf_idf);
            //var listOfSentences = getFeatureSentences(features[i].id, reviews)
            var listOfReviews = getFeatureReivews(features[i].id, reviews)
            var listOfSentences = getFeatureSentences(features[i].id, reviews)
            //x.hasOwnProperty('key')
            featuresHtml += '<tr class="'+coloreClass+'">'
            featuresHtml += '<td>'+features[i].text+'</td>'
            featuresHtml += '<td>'+features[i].tf_idf+'</td>'
            featuresHtml += '<td>'+features[i].polarity+'</td>'
            featuresHtml += '<td>'+countSentences(features[i].id, reviews,"all")+'</td>'
            featuresHtml += '<td>'+countSentences(features[i].id, reviews,"pos")+'</td>'
            featuresHtml += '<td>'+countSentences(features[i].id, reviews,"neg")+'</td>'
            featuresHtml += '</tr>'
            featuresHtml += '<tr class="tableButtons">'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showReviews('+features[i].id+',\'all\')"><button type="button" class="btn btn-default">All Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showReviews('+features[i].id+',\'pos\')"><button type="button" class="btn btn-default">Pos Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showReviews('+features[i].id+',\'neg\')"><button type="button" class="btn btn-default">Neg Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showSentences('+features[i].id+',\'all\')"><button type="button" class="btn btn-default">All Sentences</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showSentences('+features[i].id+',\'pos\')"><button type="button" class="btn btn-default">Pos Sentences</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="'+features[i].id+'" role="group" onclick="MainControl.GoogleMapHelper.showSentences('+features[i].id+',\'neg\')"><button type="button" class="btn btn-default">Neg Sentences</button></div></td>'
            featuresHtml += '</tr>'

            featuresHtml += '<tr id="reviews'+features[i].id+'" class="reviews"><td colspan="6">'+listOfReviews+'</td></tr>'
            featuresHtml += '<tr id="sentences'+features[i].id+'" class="sentences"><td colspan="6">'+listOfSentences+'</td></tr>'
     }
        featuresHtml+= '</tbody></table>'
        return featuresHtml;
    }

    function showReviews(featureId,polarity){
        hideAll();
        var selector = '#reviews'+featureId
        $(selector).show();
         var hideselector = selector + '> td > div'
        $(hideselector).hide();
        if (polarity == 'all'){
            $(hideselector).show();
        }else if(polarity == 'pos'){
            var polarityselector = selector + '> td > div.positive'
            $(polarityselector).show();
        }else if(polarity == 'neg'){
            var polarityselector = selector + '> td > div.negative'
            $(polarityselector).show();
        }

    }

    function showSentences(featureId,polarity){
        hideAll();
        var selector = '#sentences'+featureId
        $(selector).show();

        var hideselector = selector + '> td > div'
        $(hideselector).hide();
        if (polarity == 'all'){
            $(hideselector).show();
        }else if(polarity == 'pos'){
            var polarityselector = selector + '> td > div.positive'
            $(polarityselector).show();
        }else if(polarity == 'neg'){
            var polarityselector = selector + '> td > div.negative'
            $(polarityselector).show();
        }
    }

    function hideAll(){
        $('tr.sentences').hide();
        $('tr.reviews').hide();
    }

    function createSimilarItems(itemId,similarItems){

        var similarHtml = '';
        featureIds = Object.keys(similarItems[itemId].features);
         for (i = 0; i < featureIds.length; i++){
             var index = featureIds[i]
             similarHtml +=  similarItems[itemId].features[index]["text"] + ' ';
         }
        return similarHtml
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
                        reviewsHtml += createReview(results.reviews[i])
                    }
                    $('#itemReviews').html('<div class="container-fluid">' + reviewsHtml + '</div>');
                    $('#generalInfo').html('<div class="container-fluid">' + reviewsHtml + '</div>');
                    $('#features').html('<div class="container-fluid">' + createFeatures(id,results.features,results.reviews) + '</div>');
                    //$('#similar').html('<div class="container-fluid">' + createSimilarItems(id,results.similarItems) + '</div>');
                    hideAll();
                    $('#infoDataMain').modal('toggle');
                    $('#infoDataMain').modal('show');

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
                    var loc = {lat: parseFloat(point.lat), lng: parseFloat(point.lng)};
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
        showReviews:showReviews,
        showSentences:showSentences,
    };
})();
