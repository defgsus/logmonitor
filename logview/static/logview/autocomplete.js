$(function() {

    $(".table-filter").each(function (i, e) {
        var $e = $(e);
        $e.autocomplete({
            delay: 200,
            minLength: 1,
            source: function(request, response) {
                $.ajax({
                    url: $e.data("ac-url"),
                    dataType: "json",
                    data: {
                        'n': $e.data("ac-field"),
                        'q': request.term
                    },
                    success: function(data) {
                        response(data.items);
                    }
                });
            }
        });
    });

});