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
	way_points = {"start":{"lat":26.1048858,"lng":-80.39231649999999},
                      "end":{"lat":25.9416076,"lng":-80.16158410000003},
                      "waypoints":[[26.0487104,-80.22360939999999]]};
        var str = JSON.stringify(way_points)
	document.getElementById('str').innerHTML = str;
// 	alert(str);
	setroute(way_points);
}

function setroute(os)
{
        
	var wp = [];
	alert(os['waypoints']);
	for(var i=0;i<os.waypoints.length;i++)
		wp[i] = {'location': new google.maps.LatLng(os.waypoints[i][0], os.waypoints[i][1]),'stopover':false }
		
	ser.route({
	'origin':new google.maps.LatLng(os.start.lat,os.start.lng),
	'destination':new google.maps.LatLng(os.end.lat,os.end.lng),
	'waypoints': wp,
	'travelMode': google.maps.DirectionsTravelMode.DRIVING
                },
	
	function(res,sts) {
		if(sts=='OK')ren.setDirections(res);
	})
	google.maps.event.addListener(ren, 'directions_changed', function() {
        save_waypoints(ren.getDirections());
       });
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
        
        var test = JSON.stringify(data)

        document.getElementById('test').innerHTML = test;
}