function CreateFeatureHelper(mapHalper,htmlGenerator){
    var _mapHalper = mapHalper;
    var _htmlGenerator = htmlGenerator;
    function getAllFeatures (onSucess) {
        $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        $.ajax({
            type: "GET",
            url: 'allfeatures',
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
    
    function getItemsByFeatures (featuresArr) {
        $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        $.ajax({
            type: "GET",
            url: 'searchitemsbyfeatures?features='+featuresArr,
            data: {},
            success: function (results) {
                _mapHalper.AddFeatures(results, true);
                markers = {};
                markers.items = {}
                markers.items.items = results.items;
                _mapHalper.AddMarkersYello(markers)
            }
        });
    }

    function getFeatureInfo (featureId) {
      $('#infoDataMain').modal('hide');
        $('#infoFeature').modal('hide');
        $.ajax({
            type: "GET",
            url: 'getfeatureinfo',
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
