App = {

};

App.settingsScript = function(argument) {
    $('#menu_button').on('click', function(){
        if ($(this).data('showed_menu') == '0') {
            $('#settings_menu').show('slide',{direction:'left'}, 200);
            $(this).data('showed_menu', '1');
        } else {
            $('#settings_menu').hide('slide',{direction:'left'}, 200);
            $(this).data('showed_menu', '0');
        };
    });
}