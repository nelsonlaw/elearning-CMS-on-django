$(document).ready(function () {
    $("a.subnav_click").click(function (event) {
        event.preventDefault();
        var subnav = $(".subnav");
        if (subnav.is(':visible')) {
            subnav.hide();
        } else {
            subnav.show();
        }
        return false;
    })
});

$(document).ready(function () {
    $("a.answer_click").click(function (event) {
        event.preventDefault();
        var answer = $(".answer");
        if (answer.is(':visible')) {
        } else {
            answer.show();
        }
        var answer_click = $("a.answer_click");
        if (answer_click.is(':visible')) {
            answer_click.hide();
        } else {
        }
        var next = $("a.next");
        if (next.is(':visible')) {
        } else {
            next.show();
        }
        return false;
    })
});