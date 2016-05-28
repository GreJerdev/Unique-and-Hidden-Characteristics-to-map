
var MainControl = MainControl || {}
MainControl.GoogleMapHelper = (function(){

       var map;
       var infowindows = [];
       var isMapInit = false;
       var markers = [];
       function initMap() {
            isMapInit = true; 
           
            map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 33.4664494, lng: -112.0655065},
            zoom: 8
        });
           
        map.addListener('click', function(e) {
            $.ajax ({
        type: "GET",
        url:"getitemsnearme",
        data:  {lat: e.latLng.lat, lon: e.latLng.lng},
        success: function(results) {
          
            console.log(results.items)
            deleteMarkers();
           
            results.items.items.forEach(function(point){
                var loc =  {lat: parseFloat( point.lat), lng: parseFloat( point.lng)};
                console.log(loc);
               
               MainControl.GoogleMapHelper.addMarker(loc,point.Name);
            })
            
        }
    });
           
        });
      }
       function addMarker(loc, text) {
          var infowindow = new google.maps.InfoWindow({
                content: text
            });
           var marker = new google.maps.Marker({
            position: loc,
            map: map,
            title: text
            });
         
           marker.addListener('click', function() {
               closeInfoWindow(); 
               infowindow.open(map, marker);
            });
            markers.push(marker);
           infowindows.push(infowindow);
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
    
    close()
      function clearMarkers() {
        setMapOnAll(null);
      }

      function deleteMarkers() {
        clearMarkers();
        markers = [];
      }  
    
      function isInit(){
        return isMapInit;
      }
        
      
    
      return {
            initMap:initMap,
            addMarker:addMarker,   
            isInit :isInit,
        };
})();
   

$(function() {
    
   
   
 /*   */
});
