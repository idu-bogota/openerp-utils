    var customIcons = {
      restaurant: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
      },
      bar: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
      }
    };
    var data = {};
    var dummy="hello";
    var directionDisplay;
    var directionsService = new google.maps.DirectionsService();
    var rendererOptions = {
        draggable: true
    };

    function load() {
      var map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(4.6075486, -74.0712431),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
      });
       directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
       directionsDisplay.setMap(map);
       var infoWindow = new google.maps.InfoWindow;
       google.maps.event.addListener(directionsDisplay, 'directions_changed', function() {
        computeTotalDistance(directionsDisplay.getDirections());
        WaypointsDistance(directionsDisplay.getDirections());
       });
      calcRoute();
    }

//     function calcRoute(start, end, waypts) {
//         var request = {
//             origin:start, 
//             destination:end,
//             waypoints: waypts,
//             optimizeWaypoints: true,
//             travelMode: google.maps.DirectionsTravelMode.DRIVING
//         };
//         directionsService.route(request, function(response, status) {
//           if (status == google.maps.DirectionsStatus.OK) {
//             directionsDisplay.setDirections(response);
//           }
//         });
//   }

        function calcRoute() {
        var pos_idu = new google.maps.LatLng(4.6075486, -74.0712431);
        var pos_pablo = new google.maps.LatLng(4.669138, -74.014840);
        var request = {
            origin: pos_idu,
            destination: pos_pablo,
        // waypoints:[{location: pos_idu}, {location: pos_pablo}],
        waypoints:[],
        //    waypoints: [{location: new google.maps.LatLng(4.618083299999999,-74.06835269999999)},{location:new google.maps.LatLng(4.628582499999999,-74.0682926)}],
            travelMode: google.maps.TravelMode.DRIVING
        };
        directionsService.route(request, function(response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
            }
        });
        }

    function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
      });
    }

    function downloadUrl(url, callback) {
      var request = window.ActiveXObject ?
          new ActiveXObject('Microsoft.XMLHTTP') :
          new XMLHttpRequest;

      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          request.onreadystatechange = doNothing;
          callback(request, request.status);
        }
      };

      request.open('GET', url, true);
      request.send(null);
    }


//     function doNothing() {}
// 
//                         i = $('.inputs').size();        
//                                         
//                                 $('#add').click(function() {
//                                         var nameName = "dynamic" + i;
//                                                 $('<div><input type="text"data-provide="typeahead"   class="field" placeholder="Hop " +"' +i+'" name="'+ nameName+'"   value="" /></div>').fadeIn('slow').appendTo('.inputs');
//                         
//                         $(".field").typeahead({source : city});
//                         i++;
//                                                 var fields= Number($("#total").val())+Number(1);
//                                                 $("#total").val(fields);
//                         
//                                                 
//                                 });
//                                 
//                                 $('#remove').click(function() {
//                                 if(i > 1) {
//                                                 $('.field:last').remove();
//                                                 var fields= Number($("#total").val())-Number(1);
//                                                 i--;
//                                 }
//                                 });
//                                 
//                                 $('#reset').click(function() {
//                                 while(i >= 1) {
//                                                 $('.field:last').remove();
//                                                 var fields= Number($("#total").val())-Number(1);
//                                                 i--;
//                                 }
//                                 });

//         function RefreshMap(){
//                 waypts =[];
//                 var start = $('#From').val();
//                 var end = $('#To').val();
//                 divs = $('.inputs');
//                 //alert(start);
//                 $('.field').each(function(){
//                     waypts.push({
//                     location:this.value,
//                      stopover:true
//                      });
//               
// 
//                 });
//                     
//                 calcRoute(start, end, waypts);
//  
//         }

function computeTotalDistance(result) {
  

  var total = 0;
  var myroute = result.routes[0];
  var ruta;
  for (var i = 0; i < myroute.legs.length; i++) {
    total += myroute.legs[i].distance.value;
    ruta += myroute;
  }
  total = total / 1000.0;
  document.getElementById('total').innerHTML = total + ' km';
  document.getElementById('ruta').innerHTML = ruta;
}

function WaypointsDistance(result) {
  

  // WAYPOINTS
  
  var w=[],wp;
    var rleg = result.routes[0].legs[0];
//     data.start = {'lat': rleg.start_location.lat(), 'lng':rleg.start_location.lng()}
    data.start = {'lat': rleg.start_location.lat(), 'lng': rleg.start_location.lng()}
//     data.end = {rleg.end_location.lat(), rleg.end_location.lng()}
    data.end = {'lat': rleg.end_location.lat(), 'lng':rleg.end_location.lng()}
    var wp = rleg.via_waypoints
    for(var i=0;i<wp.length;i++)w[i] = [wp[i].lat(),wp[i].lng()]
    data.waypoints = w;
  
   var str = JSON.stringify(data);
   var start = JSON.stringify(data["start"]);
   var startr = start.replace("lat",'');
   startr = startr.replace(":",'');
   startr = startr.replace("lng",'');
   startr = startr.replace(":",'');
   var end = JSON.stringify(data["end"]);
   var waypointst = JSON.stringify(data["waypoints"]);
   

  var prueba = 1;
  var waypoints = result.routes[0];
  var longitud = 0;
//   var longitud = waypoints.length;
  for (var i = 0; i < waypoints.legs.length; i++) {
    longitud += waypoints.legs[i].distance.value;
  }
  
  document.getElementById('waypoints').innerHTML = longitud;
  document.getElementById('prueba').innerHTML = prueba;
  document.getElementById('str').innerHTML = str;
  document.getElementById('starts').innerHTML = startr;
  document.getElementById('end').innerHTML = end;
  document.getElementById('waypointst').innerHTML = waypointst;
  
}

function save_waypoints()
{
	var w=[],wp;
	var rleg = ren.directions.routes[0].legs[0];
	data.start = {'lat': rleg.start_location.lat(), 'lng':rleg.start_location.lng()}
	data.end = {'lat': rleg.end_location.lat(), 'lng':rleg.end_location.lng()}
	var wp = rleg.via_waypoints	
	for(var i=0;i<wp.length;i++)w[i] = [wp[i].lat(),wp[i].lng()]	
	data.waypoints = w;
	
	var str = JSON.stringify(data)


	document.getElementById('str').innerHTML = str;
}