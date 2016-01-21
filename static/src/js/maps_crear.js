var map, ren, ser, otra;
var data = {};
var x = document.getElementById("crear_ruta");
var arreglo ={};
wp = "";

function crear()
{
    console.log("Entro a load");
    console.log("Salta Prueb");
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
    if (wp){
        setroute_wp(wp)
    }
    else {
        setroute()
    }
    
    }

function setroute()
{
    console.log("Entro a setroute()");
    if (arreglo.str)
    {
        carga = JSON.parse(arreglo.str);
        ser.route({
              'origin':new google.maps.LatLng(carga.start.lat,carga.start.lng),
              'destination':new google.maps.LatLng(carga.end.lat,carga.end.lng),
              'travelMode': google.maps.DirectionsTravelMode.DRIVING
                },
        function(res,sts) {
             if(sts=='OK')ren.setDirections(res);
             });
    }
    else
    {
    ser.route({ 'origin': new google.maps.LatLng(4.6075486, -74.0712431),
                 'destination':  new google.maps.LatLng(4.7553847, -74.08053889999996),
                 'travelMode': google.maps.DirectionsTravelMode.DRIVING
               },
    function(res,sts) {
             if(sts=='OK')ren.setDirections(res);
             });
    }
}

function setroute_wp(os)
{
        console.log("Entro a setroute(os)");
        var wp = [];
        console.log("Entro a setroute");
//        alert(os['waypoints']);
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
    console.log("Entro a save");
    var w=[],wp;
    var rleg = ren.directions.routes[0].legs[0];
    data.start = {'lat': rleg.start_location.lat(), 'lng':rleg.start_location.lng()}
    data.end = {'lat': rleg.end_location.lat(), 'lng':rleg.end_location.lng()}
    var wp = rleg.via_waypoints 
    for(var i=0;i<wp.length;i++)w[i] = [wp[i].lat(),wp[i].lng()]    
    data.waypoints = w;
    var crear = document.getElementById('crear');
    var crear = JSON.stringify(data);
    arreglo.crear = crear;
//    document.getElementById('crear').innerHTML = crear;
    x.setAttribute("value", crear);
}
