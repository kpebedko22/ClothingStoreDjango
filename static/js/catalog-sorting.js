$(document).ready(function () {

    $('#filter_sort').change(function () { ajaxSorting(); });

    $('#filter_color').change(function () { ajaxSorting(); });

    $('#filter_size').change(function () { ajaxSorting(); });

    function sortClothes(data) {
        var sort_by = $("#filter_sort").val();
        var sort_color = $("#filter_color").val();
        var sort_size = $('#filter_size').val();

        // сортировка по цвету
        if (sort_color.length > 0) {
            data = data.filter(a => sort_color.indexOf(String(a.color)) != -1);
        }

        // сортировка по размеру
        if (sort_size.length > 0) {
            data = data.filter(a => sort_size.indexOf(String(a.size)) != -1);
        }

        // сортировка по цене - возрастание/убывание
        if (sort_by === "ascending_price") {
            data.sort((a, b) => a.price - b.price);
        }
        else if (sort_by === "descending_price") {
            data.sort((a, b) => b.price - a.price);
        }

        return data;
    }

    function ajaxSorting() {

        console.log(window.location.href);

        $.ajax({
            type: "GET",
            url: window.location.href,

            success: function (data) {
                data = sortClothes(data);
                $("#clothes_container").html('');

                if (data.length > 0) {
                    $.each(data, function (index) {
                        console.log(data[index].absolute_url);
                        var imagePath = data[index].imagePath;
                        if (imagePath === "") imagePath = 'empty.png';
                        $("#clothes_container").append(
                            '<div class="col-6 col-sm-6 col-md-6 col-lg-3">' +
                            '<div class="catalog__item">' +
                            '<a href="'+ data[index].absolute_url + '">' +
                            '<img src="' + imagePath + '" class="catalog__item-img" alt="' + data[index].name + '">' +
                            '</a>' +
                            '<a href="/' + data[index].absolute_url + '/">' +
                            '<div class="catalog__item-info">' +
                            '<div class="catalog__item-info-name">' + data[index].name + '</div>' +
                            '<div class="catalog__item-info-price">' + data[index].price + '&#8381;</div>' +
                            '</div>' +
                            '</a>' +
                            '</div>' +
                            '</div>'
                        );
                    });
                }
                else {
                    $("#clothes_container").append(
                        '<div class="msg-filter__container">' +
                        '<div class="msg-filter__label">Ничего не найдено по Вашему запросу &#128549;</div>' +
                        '<div class="msg-filter__text">Попробуйте изменить параметры фильтрации, или посмотрите товары из другой категории</div>' +
                        '</div>'
                    );
                }

            },
            error: function (msg) {
                alert(msg.responseJSON.message)
            },
        });
    }
});