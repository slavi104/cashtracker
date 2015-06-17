App = {

};

App.settingsScript = function() {
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

App.categoryAddEdit = function() {
    var step_category_counter = 0;
    $('#add_subcategory').on('click', function(e){
        e.preventDefault();  
        step_category_counter++;
        $(".subcategory-input-holder").first().clone().appendTo(".subcategory-holder");
        $(".subcategory-input-holder").last().removeClass('hidden');
        $('.delete_button').last().on('click', function(){
            $(this).parent().parent().parent().remove();
        });
        $('.subcategory-name-input').last().attr('name', 'new_' + step_category_counter);
    });

    $('.delete_button').on('click', function(){
        $(this).parent().parent().parent().remove();
    });
}

App.homeScript = function(subcategories_json) {
    $('#categories_select').on('change', function(){
        var subcategories = subcategories_json[$(this).val()];
        $('#subcategories_select').empty();
        $.each(subcategories, function(subcategory_id, name) {
            $('#subcategories_select').append('<option value="' + subcategory_id + '" >' + name + '</option>');
        });
    });

    $('#categories_select').trigger('change');
}

App.paymentsScript = function() {
    
}