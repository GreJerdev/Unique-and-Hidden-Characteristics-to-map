
function GetHtmlGeneratorHelper () {

    var restaurantToCompare = [];

    function arrayToString(array) {
        var result = '';
        result = array.join(',');
        //   for(index in array){
        //	result += array.toString()+',';
        //}
        return result;
    }

    function getClassByPolarity(polarity) {
        var polarityClass = 'neutral';
        if (polarity > 0) {
            polarityClass = 'positive'
        } else {
            polarityClass = 'negative'
        }
        return polarityClass
    }

    function getColorClassByPolarity(polarity) {
        var colorClass = 'nautral ';
        if (polarity == 0) {
            colorClass = 'bg-warning';
        } else if (polarity > 0) {
            colorClass = 'bg-success'
        } else {
            colorClass = 'bg-danger'
        }

        return colorClass
    }

    function getSizeByTfIdf(tfIdf) {
        var floatTfIdf = parseFloat(tfIdf);
        var size = 6;
        if (floatTfIdf > 0 && floatTfIdf <= 0.2) {
            size = 5;
        } else if (floatTfIdf > 0.2 && floatTfIdf <= 0.4) {
            size = 4;
        } else if (floatTfIdf > 0.4 && floatTfIdf <= 0.6) {
            size = 3;
        } else if (floatTfIdf > 0.6 && floatTfIdf <= 0.8) {
            size = 2;
        } else if (floatTfIdf > 0.8 && floatTfIdf <= 1) {
            size = 1;
        }
        return size;
    }

    function createSenteces(sentence) {
        var sentenceHtml = '<div class="sentence ' + getColorClassByPolarity(sentence.polarity) + ' ' + getClassByPolarity(sentence.polarity) + '">';
        for (j = 0; j < sentence.members.length; j++) {
            var member = sentence.members[j]
            var memberHtml = ''
            if (member.hasOwnProperty('featureId')) {

                memberHtml = '<a href="#" onclick="return FeatureHelper.featureManager.getFeatureInfo(' + member.featureId + ');">' + member.text + '</a>'

            }
            else {
                memberHtml = member.text;
            }
            sentenceHtml += memberHtml
        }
        sentenceHtml += '</div>'
        return sentenceHtml;
    }

    function createSimilarItems(itemId, similarItems) {

        var similarHtml = '';
        featureIds = Object.keys(similarItems[itemId].features);
        for (i = 0; i < featureIds.length; i++) {
            var index = featureIds[i]
            similarHtml += similarItems[itemId].features[index]["text"] + ' ';
        }
        return similarHtml
    }

    function createReview(review) {
        var reviewHtml = '<div class="row well ' + getClassByPolarity(review.polarity) + '" reviewid="' + review.id + '">';
        for (s in review.sentences) {
            reviewSentences = review.sentences[s];
            reviewHtml += createSenteces(reviewSentences);
        }
        reviewHtml += '</div>'
        return reviewHtml;
    }

    function getFeatureReivews(fId, reviews) {
        var reviewsHtml = '';
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true) {
                if (reviews[reviews_index]['features'].hasOwnProperty(fId) == true) {
                    reviewsHtml += createReview(reviews[reviews_index]);
                }
            }
        }

        return reviewsHtml;
    }

    function getFeatureSentences(featureId, reviews) {
        var sentencesHtml = '';
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true) {
                if (reviews[reviews_index]['features'].hasOwnProperty(featureId) == true) {
                    var sentences = reviews[reviews_index].sentences;
                    for (sentencesIndex = 0; sentencesIndex < sentences.length; sentencesIndex++) {
                        if (sentences[sentencesIndex].features.hasOwnProperty(reviews[reviews_index]['features'][featureId]) == true) {
                            sentencesHtml += createSenteces(sentences[sentencesIndex]);
                        }
                    }
                }
            }
        }
        return sentencesHtml;
    }

    function countSentences(featureId, reviews, polarity) {
        var count = 0;
        for (reviews_index = 0; reviews_index < reviews.length; reviews_index++) {
            if (reviews[reviews_index].hasOwnProperty('features') == true) {
                if (reviews[reviews_index]['features'].hasOwnProperty(featureId) == true) {
                    var sentences = reviews[reviews_index].sentences;
                    for (sentencesIndex = 0; sentencesIndex < sentences.length; sentencesIndex++) {
                        if (sentences[sentencesIndex].features.hasOwnProperty(reviews[reviews_index]['features'][featureId]) == true) {
                            if (polarity == 'all') {
                                count++
                            }
                            else if (sentences[sentencesIndex].polarity > 0 && polarity == 'pos') {
                                count++
                            } else if (sentences[sentencesIndex].polarity < 0 && polarity == 'neg') {
                                count++
                            }
                        }
                    }
                }
            }
        }
        return count;
    }

    function createFeatures(itemId, features, reviews) {
        var featuresHtml = '<table class="table"><thead><tr><th>Feature</th><th>Tf-Idf</th><th>Polarety</th><th>All Sentemens</th><th>Pos Sentemens</th><th>Neg Sentemens</th></tr></thead><tbody>';
        for (i = 0; i < features.length; i++) {
            var coloreClass = getColorClassByPolarity(features[i].polarity);
            var size = getSizeByTfIdf(features[i].tf_idf);
            //var listOfSentences = getFeatureSentences(features[i].id, reviews)
            var listOfReviews = getFeatureReivews(features[i].id, reviews)
            var listOfSentences = getFeatureSentences(features[i].id, reviews)
            //x.hasOwnProperty('key')
            featuresHtml += '<tr class="' + coloreClass + '">'
            featuresHtml += '<td>' + features[i].text + '</td>'
            featuresHtml += '<td>' + features[i].tf_idf + '</td>'
            featuresHtml += '<td>' + features[i].polarity + '</td>'
            featuresHtml += '<td>' + countSentences(features[i].id, reviews, "all") + '</td>'
            featuresHtml += '<td>' + countSentences(features[i].id, reviews, "pos") + '</td>'
            featuresHtml += '<td>' + countSentences(features[i].id, reviews, "neg") + '</td>'
            featuresHtml += '</tr>'
            featuresHtml += '<tr class="tableButtons">'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showReviews(' + features[i].id + ',\'all\')"><button type="button" class="btn btn-default">All Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showReviews(' + features[i].id + ',\'pos\')"><button type="button" class="btn btn-default">Pos Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showReviews(' + features[i].id + ',\'neg\')"><button type="button" class="btn btn-default">Neg Reviews</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showSentences(' + features[i].id + ',\'all\')"><button type="button" class="btn btn-default">All Sentences</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showSentences(' + features[i].id + ',\'pos\')"><button type="button" class="btn btn-default">Pos Sentences</button></div></td>'
            featuresHtml += '<td><div class="btn-group btn-group-xs featureInText" id="' + features[i].id + '" role="group" onclick="MainControl.GoogleMapHelper.showSentences(' + features[i].id + ',\'neg\')"><button type="button" class="btn btn-default">Neg Sentences</button></div></td>'
            featuresHtml += '</tr>'

            featuresHtml += '<tr id="reviews' + features[i].id + '" class="reviews"><td colspan="6">' + listOfReviews + '</td></tr>'
            featuresHtml += '<tr id="sentences' + features[i].id + '" class="sentences"><td colspan="6">' + listOfSentences + '</td></tr>'
        }
        featuresHtml += '</tbody></table>'
        return featuresHtml;
    }

    function showReviews(featureId, polarity) {
        var selector = '#reviews' + featureId
        $(selector).show();
        var hideselector = selector + '> td > div'
        $(hideselector).hide();
        if (polarity == 'all') {
            $(hideselector).show();
        } else if (polarity == 'pos') {
            var polarityselector = selector + '> td > div.positive'
            $(polarityselector).show();
        } else if (polarity == 'neg') {
            var polarityselector = selector + '> td > div.negative'
            $(polarityselector).show();
        }

    }

    function showSentences(featureId, polarity) {
        var selector = '#sentences' + featureId
        $(selector).show();

        var hideselector = selector + '> td > div'
        $(hideselector).hide();
        if (polarity == 'all') {
            $(hideselector).show();
        } else if (polarity == 'pos') {
            var polarityselector = selector + '> td > div.positive'
            $(polarityselector).show();
        } else if (polarity == 'neg') {
            var polarityselector = selector + '> td > div.negative'
            $(polarityselector).show();
        }
    }

    function LoadRestaurantDialogNav(itemId,name) {
        var parameters = itemId+", '"+name+"'";
        var dialogNav = '  <ul class="nav nav-tabs" ><li class="active">'
            + '<a data-toggle="tab" href="#generalInfo">Information</a>'
            + '</li>'
            + '<li >'
            + '    <a data-toggle="tab" href="#itemReviews">Reviews</a>'
            + '</li>'
            + '<li>'
            + '    <a data-toggle="tab" href="#itemFeatures">Features</a>'
            + '</li>'
            /*  + '<li>'
             + '    <a data-toggle="tab" href="#similar">Similar </a>'
             + '</li>'*/
            + '<li>'
            + '    <button type="button" class="btn btn-default navbar-btn" onclick="htmlManager.htmlGenerator.addRestaurantToCompareList('+parameters+');">Add to Comper List</button>'
            + '</li>'
            + '</ul>';
        $('#dialogNav').html(dialogNav);
    }

    function LoadFeatureDialogNav() {
        var dialogNav = '  <ul class="nav nav-tabs" ><li class="active">'
            + '<a data-toggle="tab" href="#featuresGeneralInfo">Information</a>'
            + '</li>'
            + '<li >'
            + '    <a data-toggle="tab" href="#restaurants">Restaurants</a>'
            + '</li>'
            + '<li>'
            + '    <a data-toggle="tab" href="#reviews">Reviews</a>'
            + '</li>'
            + '<li>'
            + '    <a data-toggle="tab" href="#sentences">Sentences</a>'
            + '</li>'
            + '</ul>';
        $('#featureDialogNav').html(dialogNav);
    }

    function updateComperList(){
        var restaurantToCompareHtml = ''
        for(restaurant in restaurantToCompare){
         restaurantToCompareHtml += '<button type="button" class="btn btn-default navbar-btn" onclick="#">'+restaurantToCompare[restaurant].name+'</button>';
        }
         $('#restaurantsToCompare').html(restaurantToCompareHtml);
    }

    function addRestaurantToCompareList(itemId, name) {
        if (restaurantToCompare.findIndex(function (restaurantid) {
                return restaurantid == itemId;
            }) == -1) {
            restaurantToCompare.push({id:itemId,name:name})
            showMessage('Restaurant To Compare List', '', 'success')
        }
        else {
            showMessage('Restaurant already in  Compare List', '', 'danger')
        }
        updateComperList();
    }

    function getReataurantsToCompare() {
        return restaurantToCompare;
    }

    function cleanRestaurantToCompareList() {
        restaurantToCompare = [];
        updateComperList();
    }

    function showMessage(messgeText, headLine, type) {
        var selector = '.alert .alert-' + type + ' #text';
        $('#messgeHeader').val(headLine);
        $('#messageBody').val(headLine);
        $('#messageBox').modal('toggle');
        $('#messageBox').modal('show');
    }

    function createRestaurantInfo(restaurantInfo) {
        var infoHtml = '';
        infoHtml = '<h2>'+restaurantInfo[1]+'</h2>'
        infoHtml +='<img src="/static/__9lry0Yu5ExNpy0WtZ1bQ.jpg" alt="Smiley face" width="300" height="200">'
        infoHtml +='<img src="/static/_1t3f89fFrAsFHmDkku9zg.jpg" alt="Smiley face" width="300" height="200">'
        infoHtml +='<img src="/static/__8oTHle-LCw-oeA6Ui1mw.jpg" alt="Smiley face" width="300" height="200">'
        infoHtml +='<img src="/static/_2lLdkazezco-tDvhDKDLQ.jpg" alt="Smiley face" width="300" height="200">'
        return infoHtml;
    }

    function createFeatureInfo(info) {
        var infoHtml = ''
        infoHtml += '<div> <strong>Features in reviwes</strong> ' + info.nounsForms+'</div><br\>';
        infoHtml += '<div > <strong>Number of positive sentences</strong> ' + info.posSetences+'</div><br\>' ;
        infoHtml += '<div > <strong>Number of negative sentences</strong> ' + info.negSetences+'</div><br\>';
        infoHtml += '<div > <strong>Number of neutral sentences</strong> '+info.netSetences+'</div><br\>' ;
        infoHtml += '<div > <strong>Number of restaurants with feature</strong> '+ info.items+'</div><br\>';
        infoHtml += '<div > <strong>Number of reviews with feature</strong> '+info.reviews+'</div><br\>';
        return infoHtml;

    }

    function createFeatureRestaurantsInfo(restaurantsInfoArr,itemSentementArr ) {
        var infoHtml = '<div>';
        var headline = '<div class="row">' +
              '<div class="col-md-4"><h3>Restaurant Name</h3></div>' +
              '<div class="col-md-4"><h3>Feature Polarite</h3></div>' +
              '<div class="col-md-4"></div>' +
              '</div>';
        infoHtml += headline;
         for (restaurantId in restaurantsInfoArr) {
            var row = '<div class="row '+ getColorClassByPolarity(itemSentementArr[restaurantId])+'">';
            var rowData = '<div class="col-md-4">'+restaurantsInfoArr[restaurantId][1]+'</div>';
            rowData += '<div class="col-md-4">'+getClassByPolarity(itemSentementArr[restaurantId])+'</div>';
            rowData += '<div class="col-md-4">' +
                '<button type="button" class="btn btn-default navbar-btn" onclick="htmlManager.htmlGenerator.addRestaurantToCompareList('+restaurantId+',\''+restaurantsInfoArr[restaurantId][1]+'\');">Add to Comper List</button>' +
                '</div>';
            row += rowData;
            row += '</div>';
            infoHtml += row;
        }
        infoHtml += '</div>';
        return infoHtml;
    }

    function showFeatureDetails(featureId, details) {

        var reviewsHtml = '';
        var generalInfo = '<div id="featuresGeneralInfo" class="tab-pane fade in active">';
        var restaurants = '<div id="restaurants" class="tab-pane fade">';
        var reviews = '<div id="reviews" class="tab-pane fade">';
        var sentences = '<div id="sentences" class="tab-pane fade">';

        for (restaurant in details.reviews) {
            reviews += '<div>'+details.items[restaurant][1]+'</div>';
            for (review in details.reviews[restaurant].reviews){
                reviews += createReview(details.reviews[restaurant].reviews[review])
            }
        }
        generalInfo = generalInfo +createFeatureInfo(details.info)+'</div>';
        restaurants += createFeatureRestaurantsInfo(details.items,details.info.itemSentement)+'</div>';
        reviews += '</div>';

        for (restaurant in details.reviews) {
            sentences += getFeatureSentences(featureId, details.reviews[restaurant].reviews)
        }
        sentences += '</div>';

        reviewsHtml = generalInfo + restaurants + reviews + sentences
        LoadFeatureDialogNav();
        $('#featureDialogContent').html(reviewsHtml);
        $('#infoFeature').modal('toggle');
        $('#infoFeature').modal('show');
        $('#infoFeature').css('z-index','1101');
    }

    function showRestaurantDetails(id, details) {

        var reviewsHtml = '';
        var generalInfo = '<div id="generalInfo" class="tab-pane fade in active">';
        var itemReviews = '<div id="itemReviews" class="tab-pane fade" style="height:80%;">';
        var features = '<div id="itemFeatures" class="tab-pane fade">';
        var similar = '<div id="similar" class="tab-pane fade">';

        if (details.reviews.constructor === Array) {
            var i = 0;
            for (i = 0; i < details.reviews.length; i++) {
                itemReviews += createReview(details.reviews[i])
            }
            generalInfo = generalInfo +createRestaurantInfo(details.restaurantInfo[id])+'</div>';
            itemReviews =  itemReviews + '</div>';
            features = features + createFeatures(id, details.features, details.reviews) + '</div>';
            similar = similar + '</div>';//$('#similar').html('<div class="container-fluid">' + createSimilarItems(id,details.similarItems) + '</div>');

            reviewsHtml = generalInfo + itemReviews + features + similar
            LoadRestaurantDialogNav(id, details.restaurantInfo[id][1]);
            $('#dialogContent').html(reviewsHtml);
            $('#infoDataMain').modal('toggle');
            $('#infoDataMain').modal('show');
            $('#infoDataMain').css('z-index','1100');
        }
    }

    return {
        showReviews: showReviews,
        createFeatures: createFeatures,
        createReview: createReview,
        createSimilarItems: createSimilarItems,
        showSentences:showSentences,
        addRestaurantToCompareList:addRestaurantToCompareList,
        getReataurantsToCompare:getReataurantsToCompare,
        cleanRestaurantToCompareList:cleanRestaurantToCompareList,
        showRestaurantDetails:showRestaurantDetails,
        showFeatureDetails:showFeatureDetails,
    };

}
var htmlManager = htmlManager || {}
htmlManager.htmlGenerator = GetHtmlGeneratorHelper();