
function GetHtmlGeneratorHelper () {

    var restaurantToCompare = [];
    var chartConfig = undefined;
    var featuresChart = undefined;

    var _marked_features = [];

    function setMarkFeatures( features) {
        _marked_features = [];
        selectedFeatures =  features.split(",")
        for (index in selectedFeatures) {
            try {
                _marked_features.push(parseInt(selectedFeatures[index]));
            } catch (err) {
            }
        }
    }

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
        } else if (polarity < 0) {
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

    function createBarChartData(featuresInfo, id){
        var featurelabelsOrder = [];
        var datasets = [];
        var positive = [];
        var negative = []
        var neutral = [];
        var colorForPositive = [];
        var colorForNegative = [];
        var colorForNeutral = [];
        for (index in featuresInfo.featureOrder) {
            featurelabelsOrder.push(featuresInfo.featureInfo[featuresInfo.featureOrder[index]].name);
            positive.push(featuresInfo.featureInfo[featuresInfo.featureOrder[index]].positive);
            negative.push(featuresInfo.featureInfo[featuresInfo.featureOrder[index]].negative);
            neutral.push(featuresInfo.featureInfo[featuresInfo.featureOrder[index]].neutral);
            alpha = '0.2';
            if(  $.inArray(featuresInfo.featureOrder[index],_marked_features)> -1){
                alpha = '1'
            }

            colorForPositive.push('rgba(0, 225, 0, '+alpha+')');
            colorForNegative.push('rgba(255,0, 0, '+alpha+')');
            colorForNeutral.push('rgba(255, 206, 86, '+alpha+')');
        }
        var datasets = [] ;
        datasets.push({
            label: 'Negative',
            fillColor: '#7BC225',
            data: negative ,
            backgroundColor:colorForNegative
        });
        datasets.push({
            label: 'Neutral',
            fillColor: '#7BC225',
            data: neutral ,
            backgroundColor:colorForNeutral
        });
        datasets.push({
            label: 'Positive',
            fillColor: '#7BC225',
            data: positive ,
            backgroundColor:colorForPositive
        });
        return {datasets:datasets,labels:featurelabelsOrder};
    }

    function createFeaturesInfo(featuresInfo,id) {
        var chartBarData = createBarChartData(featuresInfo,id);
        var chartBarCofgin = chart_config = {
            type: "bar",
            data: chartBarData,
            options: {
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                },
                responsive: false,
                maintainAspectRatio: false,
                onClick: handlefeatureChartClick,
            }
        };
        chartConfig = chartBarCofgin

        return '<div><canvas id="featuresChart"></canvas>'+
            featuresSentences(featuresInfo,id)+'</div>'
    }

    function featuresSentences(featuresInfo,id) {
        var html = '<div id="featuresSentences">'
        for (index in featuresInfo.featureOrder) {
            name = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].name;
            featureHtml = '<div id="'+name+'" style="display:none" class="featuresInfo"><table class="table">';
            var numberOfAllSentences = featuresInfo.frequencyOfMentions[featuresInfo.featureOrder[index]].positive +
                featuresInfo.frequencyOfMentions[featuresInfo.featureOrder[index]].negative +
                featuresInfo.frequencyOfMentions[featuresInfo.featureOrder[index]].neutral
            var numberOfAllSentencesInRestaurent = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].positive +
                featuresInfo.featureInfo[featuresInfo.featureOrder[index]].negative +
                featuresInfo.featureInfo[featuresInfo.featureOrder[index]].neutral
            var numberOfPositiveInPhoenix = featuresInfo.frequencyOfMentions[featuresInfo.featureOrder[index]].positive;
            var numberOfNegativeInPhoenix = featuresInfo.frequencyOfMentions[featuresInfo.featureOrder[index]].negative;
            var numberOfPositiveInRestaurent = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].positive
            var numberOfNegativeInRestaurent = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].negative
            var percentPositiveInPhoenix =  numberOfPositiveInPhoenix * 100 / numberOfAllSentences;
            var percentNegativeInPhoenix =  numberOfNegativeInPhoenix * 100 / numberOfAllSentences;
            var percentPositive =  numberOfPositiveInRestaurent * 100 / numberOfAllSentencesInRestaurent;
            var percentNegative =  numberOfNegativeInRestaurent * 100 / numberOfAllSentencesInRestaurent;
            var polarity = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].polarity;

            var headLine =  '<tr class="'+getColorClassByPolarity(polarity)+'">' +
                '<td><span class="featureName">'+name+'</span></td>' +
                '<td class="featureProperty">Feature polarity</span></td>' + '<td class="featureProperty">' + getClassByPolarity(polarity)+'</span></td>' +
                '<td><button type="button"class="btn" onclick="$(\'#featuresSentences.featuresInfo\').hide();">hide</button></td>' +
                '<td><button type="button"class="btn" onclick="FeatureHelper.featureManager.getFeatureInfo('+featuresInfo.featureOrder[index]+');">Feature Global</button></td>' +
                '</tr>'

            var pmsg  = '<tr> <td colspan="4"><div class="bg-info">Positive sentences of "'+ name +'" '+percentPositive.toFixed(2) +'% '+numberOfPositiveInRestaurent+'' +
                ' ; In Phoenix '+percentPositiveInPhoenix.toFixed(2) +'%  '+ numberOfPositiveInPhoenix+'.</td> </tr></div>';
            var nmsg = '<tr> <td colspan="4"><div class="bg-info">Negative sentences of "'+ name +'" '+percentNegative.toFixed(2)+'% '+numberOfNegativeInRestaurent+'' +
                ' ; In Phoenix '+percentNegativeInPhoenix.toFixed(2) +'%  '+ numberOfNegativeInPhoenix+'.</td> </tr></div>';
            featureHtml += headLine + pmsg + nmsg;

            for (sentenceIndex in featuresInfo.featureInfo[featuresInfo.featureOrder[index]].positivePreview) {
                var sentence = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].positivePreview[sentenceIndex];
                var sentenceHtml = '<tr> <td colspan="4"><div reviewId="'+sentence.reviewId+'" class="'+getColorClassByPolarity(sentence.polarity)+'">'+sentence.text+'</td> </tr></div>';
                featureHtml += sentenceHtml
            }

            for (sentenceIndex in featuresInfo.featureInfo[featuresInfo.featureOrder[index]].negativePreview) {
                var sentence = featuresInfo.featureInfo[featuresInfo.featureOrder[index]].negativePreview[sentenceIndex];
                var sentenceHtml = '<tr> <td colspan="4"><div reviewId="'+sentence.reviewId+'" class="'+getColorClassByPolarity(sentence.polarity)+'">'+sentence.text+'</td> </tr></div>';
                featureHtml += sentenceHtml
            }

            featureHtml += '</table></div>';
            html += featureHtml;
        }
        html+= '</div>'
        return html
    }

    function handlefeatureChartClick(evt){
        var activeElement = featuresChart.getElementAtEvent(evt);
        var a = chartConfig;
        if (activeElement.length > 0){

            $('#featuresSentences .featuresInfo').hide();

            var name = chart_config.data.labels[activeElement[0]._index]
            if (name != undefined){
                $('#featuresSentences #'+name).show();
            }
        }
    }

    function initFeatureChartBar() {
        initChar(chartConfig, 'featuresChart', '#generalInfo')
    }

    function initChar(chartBarCofgin, chartBarPlaceHtmlholder, divId){

        var ctx = document.getElementById(chartBarPlaceHtmlholder).getContext("2d");
        var dw = $(divId).width();
        var dh = $(divId).height()*0.8;
        ctx.canvas.width=dw;
        ctx.canvas.height= dh;
        featuresChart = new Chart(ctx,chartBarCofgin);
        return featuresChart
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
            + '<li>'
            + '    <a data-toggle="tab" href="#itemFeatures" onclick="htmlcontroller.initFeatureChartBar()">Features</a>'
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
           /* + '<li>'
            + '    <a data-toggle="tab" href="#sentences">Sentences</a>'
            + '</li>'*/
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
        $('#infoDataMain').modal('toggle');
        $('#messageBox').modal('toggle');
        $('#messageBox').modal('show');
    }

    function createRestaurantInfo(restaurantInfo) {
        var infoHtml = '';
        infoHtml = '<h2>'+restaurantInfo.name+' ('+ restaurantInfo.stars +')</h2>'

        infoHtml += carouselHtml('photos',restaurantInfo.photos)
        infoHtml += restaurantProperties(restaurantInfo);
        //restaurantInfo.hours
        //full_address
        return infoHtml;
    }

    function getRestaurantfullAddress(restaurentInfo) {
        var html = ''
        if (restaurentInfo["full_address"] != undefined){
            html =   '	<div class="panel panel-default">'+
                '		<div class="panel-heading">'+
                '			<h4 class="panel-title">'+
                '				<a data-toggle="collapse" data-parent="#accordion" href="#address">Address</a>'+
                '			</h4>'+
                '		</div>'+
                '		<div id="address" class="panel-collapse collapse in">'+
                '			<div class="panel-body">'+restaurentInfo["full_address"]+'</div>'+
                '		</div>'+
                '	    </div>';
        }
        return html;
    }

    function getRestaurantOpenHours(restaurantInfo){
        var html = '';
        if (restaurantInfo["hours"] != undefined){
            var weekDaysOrder = ["Monday", "Tuesday","Wednesday","Thursday","Friday",  "Saturday","Sunday"];
            var openhoursHtml = '<div>'
            hours = restaurantInfo["hours"];
            for (index in weekDaysOrder){

                if(hours[weekDaysOrder[index]] != undefined){
                    openhoursHtml += '<div>' + weekDaysOrder[index]+':' +
                        hours[weekDaysOrder[index]]['open']+'-'+ hours[weekDaysOrder[index]]['close']+'</div>'
                }
            }
            openhoursHtml += '</div>'

            html =   '	<div class="panel panel-default">'+
                '		<div class="panel-heading">'+
                '			<h4 class="panel-title">'+
                '				<a data-toggle="collapse" data-parent="#accordion" href="#openHours">Open hours</a>'+
                '			</h4>'+
                '		</div>'+
                '		<div id="openHours" class="panel-collapse collapse">'+
                '			<div class="panel-body">'+openhoursHtml+'</div>'+
                '		</div>'+
                '	    </div>';
        }
        return html;
    }

    function getRestaurantCategories(categories){
        var html = '';
        if (categories != undefined){

            var categoriesHtml = '<div>'
            for (index in categories){

                if(categories[index] != undefined){
                    categoriesHtml += '#'+categories[index] + ' ';
                }
            }
            categoriesHtml += '</div>'

            html =   '	<div class="panel panel-default">'+
                '		<div class="panel-heading">'+
                '			<h4 class="panel-title">'+
                '				<a data-toggle="collapse" data-parent="#accordion" href="#categories">Categories</a>'+
                '			</h4>'+
                '		</div>'+
                '		<div id="categories" class="panel-collapse collapse">'+
                '			<div class="panel-body">'+categoriesHtml+'</div>'+
                '		</div>'+
                '	    </div>';
        }
        return html;
    }

    function getRestaurantAttributes(attributes){
        var html = '';
        if (attributes != undefined){
            var attributesHtml = '<div>'
            for (index in attributes){
                if(attributes[index] != undefined){
                    var html = '';
                    var propertyName = attributes[index];
                    if ( typeof(attributes[index]) == 'string'){
                        html='<div>'+index+': '+propertyName.replace(/_/g, ' ')+'</div>';
                    }
                    if ( typeof(attributes[index]) == 'boolean' && attributes[index] == true){
                        html='<div>'+index+'</div>';
                    }
                    var typeName = typeof(attributes[index])

                    if ( typeof(attributes[index]) == 'object') {
                        var trueList = '';
                        html = '<div>' + index +':';
                        for (subIndex in propertyName) {
                            if (propertyName[subIndex] == true){
                                trueList += ' ' +  subIndex;
                            }
                        }
                        html = '<div>' + index +':' + trueList+'</div>' ;
                    }
                    if ( 'Price Range' == index){
                        var priceRange = ' under $10'
                        if (attributes[index]==2){
                            priceRange = '$11-$30'
                        }
                        if (attributes[index]==3){
                            priceRange = '$31-$60'
                        }
                        if (attributes[index]>=2){
                            priceRange = 'bove $61'
                        }
                        html='<div>'+index+': '+priceRange+'</div>';
                    }
                }
                attributesHtml += html;
            }

            attributesHtml += '</div>'

            html =   '	<div class="panel panel-default">'+
                '		<div class="panel-heading">'+
                '			<h4 class="panel-title">'+
                '				<a data-toggle="collapse" data-parent="#accordion" href="#attributes">Attributes</a>'+
                '			</h4>'+
                '		</div>'+
                '		<div id="attributes" class="panel-collapse collapse">'+
                '			<div class="panel-body">'+attributesHtml+'</div>'+
                '		</div>'+
                '	    </div>';
        }
        return html;
    }

    function restaurantProperties(restaurantInfo)
    {
        var html = '<div class="panel-group" id="accordion">'+
            getRestaurantfullAddress(restaurantInfo)+
            getRestaurantOpenHours(restaurantInfo) +
            getRestaurantCategories(restaurantInfo["categories"])+
            getRestaurantAttributes(restaurantInfo["attributes"])+
            '</div>'
        return html;
    }

    function carouselHtml(name,itemsArr) {
        var html = '<div id="' + name + '" class="carousel slide" data-ride="carousel">'
        html += '<ol class="carousel-indicators">'
        for (index in itemsArr) {
            var liClass = '';
            if (index == 0) {
                liClass = 'class="active"';
            }
            html += '<li data-target="#' + name + '" data-slide-to="' + index + '"' + liClass + ' ></li>';
        }
        html += '</ol>';
        html += '<div class="carousel-inner" role="listbox">'

        for (index in itemsArr) {
            var liClass = '';
            if (index == 0) {
                liClass = ' active';
            }
            html += '<div class="item' + liClass + '" ><img src="http://dilixo.net/UniqueHiddenCharacteristics/static/images/' + itemsArr[index] + '">    </div>';
        }
        html += ' </div>' +
            '<!-- Left and right controls -->'+
            '<a class="left carousel-control" href="#' + name + '" role="button" data-slide="prev">' +
            '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>' +
            '<span class="sr-only">Previous</span>' +
            '</a>' +
            '<a class="right carousel-control" href="#' + name + '" role="button" data-slide="next">' +
            '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>' +
            '<span class="sr-only">Next</span>' +
            '</a>' +
            '</div>'
        return html;
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
            var rowData = '<div class="col-md-4">'+restaurantsInfoArr[restaurantId][2]+'</div>';
            rowData += '<div class="col-md-4">'+getClassByPolarity(itemSentementArr[restaurantId])+'</div>';
            rowData += '<div class="col-md-4">' +
                '<button type="button" class="btn btn-default navbar-btn" ' +
                'onclick="MainControl.GoogleMapHelper.showItemDetails('+restaurantId+');">Show Restaurant</button>' +
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
        var sentences = '';

        generalInfo = generalInfo +createFeatureInfo(details.info)+'</div>';
        restaurants += createFeatureRestaurantsInfo(details.items,details.info.itemSentement)+'</div>';

        /*
        sentences = '<div id="sentences" class="tab-pane fade">';
        for (restaurant in details.reviews) {
            sentences += getFeatureSentences(featureId, details.reviews[restaurant].reviews)
        }
        sentences += '</div>';
        */
        reviewsHtml = generalInfo + restaurants + sentences
        LoadFeatureDialogNav();
        $('#featureDialogContent').html(reviewsHtml);

        $('#infoFeature').modal('show');
        $('#infoFeature').css('z-index','1101');
    }

    function showRestaurantDetails(id, details) {

        var reviewsHtml = '';
        var generalInfo = '<div id="generalInfo" class="tab-pane fade in active">';
        //var itemReviews = '<div id="itemReviews" class="tab-pane fade" style="height:80%;">';
        var features = '<div id="itemFeatures" class="tab-pane fade">';
        /*   if (details.reviews.constructor === Array) {
         var i = 0;
         for (i = 0; i < details.reviews.length; i++) {
         itemReviews += createReview(details.reviews[i])
         }
         }
         itemReviews =  itemReviews + '</div>';
         features = features + createFeatures(id, details.features, details.reviews) + '</div>';
         */
        generalInfo = generalInfo +createRestaurantInfo(details.restaurantInfo)+'</div>';
        features += createFeaturesInfo(details.featuresInfo,id ) + '</div>';

        reviewsHtml = generalInfo + features;
        LoadRestaurantDialogNav(id, details.restaurantInfo.name);
        $('#dialogContent').html(reviewsHtml);
        $('#infoDataMain').modal('hide');
        $('#messageBox').modal('hide');
        $('#infoDataMain').modal('show');
        $('#infoDataMain').css('z-index','1100');

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
        initFeatureChartBar:initFeatureChartBar,
        setMarkFeatures:setMarkFeatures,

    };

}
var htmlManager = htmlManager || {}
htmlManager.htmlGenerator = GetHtmlGeneratorHelper();
