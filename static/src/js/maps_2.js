var map, ren, ser;
var data = {};
function load()
{
    
    map = new google.maps.Map( document.getElementById('mappy'), {
    'zoom':12,
    'mapTypeId': google.maps.MapTypeId.ROADMAP,
    'center': new google.maps.LatLng(4.7553847, -74.08053889999996),
    })

    ren = new google.maps.DirectionsRenderer( {'draggable':true} );
    ren.setMap(map);
    ser = new google.maps.DirectionsService();

    ser.route({ 'origin': new google.maps.LatLng(4.6075486, -74.0712431),
                    'destination':  new google.maps.LatLng(4.7553847, -74.08053889999996),
                    'travelMode': google.maps.DirectionsTravelMode.DRIVING
                  },
        function(res,sts) {
        if(sts=='OK')ren.setDirections(res);
	//	save_waypoints(ren.getDirections());
                          })
     save_waypoints();
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