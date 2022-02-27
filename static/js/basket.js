window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let target = event.target;
        let basket_ID = target.name
        let basketQuantity = target.value
        $.ajax({
            url: '/baskets/basket-edit/' + basket_ID + '/' + basketQuantity + '/',
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        })
    })
}