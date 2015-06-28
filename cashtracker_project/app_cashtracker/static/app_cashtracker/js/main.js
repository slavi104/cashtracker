App = {

};

App.delete_item_id = 0;

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
        if (typeof subcategories != 'undefined') {
            $('#subcategories_select').empty();
            $.each(subcategories, function(subcategory_id, name) {
                $('#subcategories_select').append('<option value="' + subcategory_id + '" >' + name + '</option>');
            });
        };
    });

    $('#categories_select').trigger('change');
}

App.paymentsScript = function(payments_for, payments_cat, payments_curr) {
    $('#payments_for').val(payments_for);
    $('#categories_select').val(payments_cat);
    $('#currency').val(payments_curr);

    $('#payments_for').on('change', function(){
        $('#payments_select_form').submit();
    });

    $('#categories_select').on('change', function(){
        $('#payments_select_form').submit();
    });

    $('#currency').on('change', function(){
        $('#payments_select_form').submit();
    });

    $('#generate_pdf_button').on('click', function(e){
        e.preventDefault();
        $('#payments_select_form').attr('action', '/app_cashtracker/generate_report/')
        $('#payments_select_form').submit();
    });
}

App.reportsScript = function() {
    $('.delete').on('click', function(){
        App.delete_item_id = $(this).data('id');
    });
    $('.modal_delete_modal').on('click', function(){
        if (App.delete_item_id) {
            $.ajax({
                type: 'post',
                url: "/app_cashtracker/delete_report/",
                data: {
                    report_id: App.delete_item_id,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                },
                dataType: 'json'
            }).done(function(data){
                if (data.success) {
                    $('#report_' + App.delete_item_id).parent().parent().parent().remove();
                } else {
                    alert(data.message);
                };
            });
        };
    });
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}