var map, ren, ser;
var data = {};
function load(wp)
{
    alert(wp);
    way_points = "";
//     way_points = {"start":{"lat":26.1048858,"lng":-80.39231649999999},
//                       "end":{"lat":25.9416076,"lng":-80.16158410000003},
//                       "waypoints":[[26.0487104,-80.22360939999999]]};
    if (way_points) {
    wp = way_points;
    }
    map = new google.maps.Map( document.getElementById('mappy'), {
    'zoom':12,
    'mapTypeId': google.maps.MapTypeId.ROADMAP,
    'center': new google.maps.LatLng(4.7553847, -74.08053889999996)
    })

    ren = new google.maps.DirectionsRenderer( {'draggable':true} );
    ren.setMap(map);
    ser = new google.maps.DirectionsService();
    google.maps.event.addListener(ren, 'directions_changed', function() {
    save_waypoints(ren.getDirections()); 
    });
//    if (wp){
//        setroute_wp(wp)
//    }
//    else {
        setroute()
//    }
    
    }

function setroute()
{
    ser.route({ 'origin': new google.maps.LatLng(4.6075486, -74.0712431),
                 'destination':  new google.maps.LatLng(4.7553847, -74.08053889999996),
                 'travelMode': google.maps.DirectionsTravelMode.DRIVING
               },
    function(res,sts) {
             if(sts=='OK')ren.setDirections(res);
             });
}

function setroute_wp(os)
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

    var str = JSON.stringify(data)
    document.getElementById('str').innerHTML = str;
}