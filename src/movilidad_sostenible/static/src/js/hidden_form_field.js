$(document).ready(function (){
            $("#transporteselect").change(function() {
                // vacantes is the id of the input field 
                if ($(this).val() != "bici") {
                    $("#vacantes").show();
                }else{
                    $("#vacantes").hide();
                } 
            });
});