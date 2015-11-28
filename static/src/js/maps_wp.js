var map, ren, ser, otra;
var data = {};
var x = document.getElementById("otraprueba");
var arreglo ={};
wp = "";

function ofertar()
{
    console.log("Entro a load");
    console.log("Verifico prueba");
    if (prueba){
        console.log("Entro a prueba");
        var otra = prueba;
        var find = '&quot;';
        var re = new RegExp(find, 'g');
        otra = otra.replace(re,'"');
        wp = JSON.parse(otra);
    }
    console.log("Salta Prueb");
    way_points = "";
//    way_points = {"start":{"lat":4.6085621,"lng":-74.0716666},
//                       "end":{"lat":4.6074777,"lng":-74.0702044},
//                       "waypoints":[[4.694334899999999,-74.06263419999999]]};
    if (way_points) {
        wp = way_points;
        console.log("Asigna WPS");
    }
    map = new google.maps.Map( document.getElementById('mappy'), {
    'zoom':12,
    'mapTypeId': google.maps.MapTypeId.ROADMAP,
    'center': new google.maps.LatLng(4.7553847, -74.08053889999996)
    })

    ren = new google.maps.DirectionsRenderer( {'draggable':false} );
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

function load()
{
    console.log("Entro a load");
    console.log("Verifico prueba");
    if (prueba){
        console.log("Entro a prueba");
        var otra = prueba;
        var find = '&quot;';
        var re = new RegExp(find, 'g');
        otra = otra.replace(re,'"');
        wp = JSON.parse(otra);
    }
    console.log("Salta Prueb");
    way_points = "";
//    way_points = {"start":{"lat":4.607561599999999,"lng":-74.0712666},
//                       "end":{"lat":4.7553847,"lng":-74.08053889999996},
//                       "waypoints":[[4.694334899999999,-74.06263419999999]]};
    if (way_points) {
        wp = way_points;
        console.log("Asigna WPS");
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

    ser.route({ 'origin': new google.maps.LatLng(4.6074777, -74.0702044),
                 'destination':  new google.maps.LatLng(4.6085621, -74.0716666),
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
        for(var i=0;i<os.waypoints.length;i++)
        {
            wp[i] = {'location': new google.maps.LatLng(os.waypoints[i][0], os.waypoints[i][1]),'stopover':false }
        }
        console.log("Paso chequeo wp");
        if (steps)
        {
            var steps = [];
            for(var i=0; i < os.steps.length; i++) 
            {
                steps[i] = {
                    'location': new google.maps.LatLng(os.steps[i][0], os.steps[i][1])
                           }
            }
            ser.route({
              'origin':new google.maps.LatLng(os.start.lat,os.start.lng),
              'destination':new google.maps.LatLng(os.end.lat,os.end.lng),
              'waypoints': wp,
              'steps': steps,
              'travelMode': google.maps.DirectionsTravelMode.DRIVING
            },
    
            function(res,sts) {
                if(sts=='OK') {
                    ren.setDirections(res);
                }
            })
        }   
        else
        {
        console.log("Paso chequeo steps");
        ser.route({
          'origin':new google.maps.LatLng(os.start.lat,os.start.lng),
          'destination':new google.maps.LatLng(os.end.lat,os.end.lng),
          'waypoints': wp,
          //'steps': steps,
          'travelMode': google.maps.DirectionsTravelMode.DRIVING
        },

        function(res,sts) {
            if(sts=='OK') {
                ren.setDirections(res);
            }
        })
        }
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
    for(var i=0;i<wp.length;i++) {
        w[i] = [wp[i].lat(),wp[i].lng()]
    }
    data.waypoints = w;
    var steps = [[rleg.start_location.lng(), rleg.start_location.lat()]];
    for(var i=0; i < rleg.steps.length; i++) {
        steps[i+1] = [ rleg.steps[i].end_point.lng(), rleg.steps[i].end_point.lat()]
    }
    data.steps = steps;

    var str = document.getElementById('str');
    var str = JSON.stringify(data);
    arreglo.str = str;
//    document.getElementById('str').innerHTML = str;
    x.setAttribute("value", str);
}