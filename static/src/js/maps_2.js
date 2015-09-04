var map, ren, ser;
var data = {};
function goma()
{
	map = new google.maps.Map( document.getElementById('mappy'), {
	'zoom':12,
	'mapTypeId': google.maps.MapTypeId.ROADMAP,
	'center': new google.maps.LatLng(26.05678288577881, -80.30236816615798)
	})

	ren = new google.maps.DirectionsRenderer( {'draggable':true} );
	ren.setMap(map);
	ser = new google.maps.DirectionsService();
	
	ser.route({ 'origin': new google.maps.LatLng(26.104887637199948, -80.39231872768141),
                    'destination':  new google.maps.LatLng(25.941991877144947, -80.16160583705641),
                    'travelMode': google.maps.DirectionsTravelMode.DRIVING
                  },
        function(res,sts) {
		if(sts=='OK')ren.setDirections(res);
                          })		
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