// Когда HTML документ готов (прорисован)
$(document).ready(function () {
    console.log("jQuery загружен, версия:", $.fn.jquery);

    // Берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");
    console.log("Элемент уведомлений найден:", successMessage.length > 0);

    // Элемент счетчика товаров в корзине
    var goodsInCartCount = $("#goods-in-cart-count");

    // --- Логика добавления товара в корзину (AJAX POST) ---

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        console.log("=== Клик по кнопке 'Добавить в корзину' ===");

        // Берем текущее значение счетчика
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");
        console.log("ID товара:", product_id);

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");
        console.log("URL для добавления:", add_to_cart_url);

        // Получаем CSRF токен
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();
        console.log("CSRF токен найден:", csrfToken ? "Да" : "Нет");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (data) {
                console.log("=== Успешный ответ от сервера (Добавление) ===");
                console.log("Данные:", data);

                // Сообщение
                successMessage.html(data.message);
                successMessage.removeClass("alert-danger").addClass("alert-success");
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);
                console.log("Новое количество товаров в корзине:", cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                if (cartItemsContainer.length > 0) {
                    cartItemsContainer.html(data.cart_items_html);
                    console.log("Содержимое корзины обновлено");
                } else {
                    console.warn("Элемент #cart-items-container не найден");
                }
            },

            error: function (xhr, status, error) {
                console.log("=== ОШИБКА при добавлении товара ===");
                console.log("Статус:", status);
                console.log("Ошибка:", error);
                console.log("Ответ сервера:", xhr.responseText);

                // Показываем уведомление об ошибке
                successMessage.removeClass("alert-success").addClass("alert-danger");
                successMessage.html("Ошибка при добавлении товара в корзину");
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400, function () {
                        // Возвращаем класс успеха после скрытия, если нужно
                        successMessage.removeClass("alert-danger").addClass("alert-success");
                    });
                }, 7000);
            },
        });
    });

    // --- Закомментированная логика удаления товара из корзины ---

    /*
    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем текущее значение счетчика
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
                // Добавьте логику отображения ошибки, если нужно
            },
        });
    });
    */

    // --- Закомментированная логика изменения количества товара в корзине ---

    /*
    // Функция для обновления корзины (изменение количества)
    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Изменяем количество товаров в корзине
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при изменении количества товара в корзине");
                // Добавьте логику отображения ошибки, если нужно
            },
        });
    }

    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию
        updateCart(cartID, currentValue + 1, 1, url);
    });
    */

    // --- Обработчик оповещений Django ---

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем (используя alert('close') для Bootstrap-уведомлений)
    if (notification.length > 0) {
        setTimeout(function () {
            // Примечание: .alert('close') работает для Bootstrap-уведомлений
            // Если используется другой UI-фреймворк, может потребоваться другой метод (например, fadeOut)
            notification.alert('close');
        }, 7000);
    }

    // --- Логика модального окна корзины ---

    // При клике по значку корзины открываем всплывающее (модальное) окно
    $('#modalButton').click(function () {
        // Перемещаем модальное окно в body, чтобы избежать проблем с z-index или стилями
        $('#exampleModal').appendTo('body');
        // Показываем модальное окно
        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // --- Логика выбора доставки ---

    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

    console.log("Все обработчики событий установлены");
});