function CreateFeatureHelper(mapHalper,htmlGenerator){
    var _mapHalper = mapHalper;
    var _htmlGenerator = htmlGenerator;
    var urlprefix = '';
    function getAllFeatures (onSucess) {
        $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        $.ajax({
            type: "GET",
            url: urlprefix+'allfeatures',
            data: {},
            success: function (results) {
                var features = [];
                if (results.features.constructor === Array) {
                    var i = 0;
                    for (i = 0; i < results.features.length; i++) {
                        features.push({id:results.features[i][1],text:results.features[i][0]});
                    }
                    if (onSucess !== undefined)
                    {
                        onSucess(features);
                    }
                }
            }
        });
    }

    function getItemsByFeatures (featuresArr,lat,lng,radius) {
        $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        var searchParams = 'features='+featuresArr+'&lat='+lat+'&lng='+lng+'&radius='+radius;
        $.ajax({
            type: "GET",
            url: urlprefix+'searchitemsbyfeatures?'+searchParams,
            data: {},
            success: function (results) {
                markers = {};
                markers.items = {}
                markers.items.items = results.items;
                _mapHalper.AddMarkersYello(markers);
                var selectedFeaturesArr = Array.from(results.features, function(f){return f[1]});
                var restaurants =  Array.from(results.items, function(f){return f.id});
                _mapHalper.updateFeaturePanel('getfeaturesbyitemsid',{'items':restaurants.toString()},selectedFeaturesArr)
                _htmlGenerator.showSearchSummary(results.items,results.restauransFeaturesStatistic );
            }
        });
    }

    function getFeatureInfo (featureId) {
        $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        $.ajax({
            type: "GET",
            url: urlprefix+'getfeatureinfo',
            data: {featureId:featureId},
            success: function (results) {
                _htmlGenerator.showFeatureDetails(featureId,results);
            }
        });
    }

    return {
        getAllFeatures: getAllFeatures,
        getItemsByFeatures:getItemsByFeatures,
        getFeatureInfo:getFeatureInfo,
    };
}
