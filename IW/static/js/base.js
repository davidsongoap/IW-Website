$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    $('.special.cards .image').dimmer({
        on: 'hover',
        duration: {
            show: 400,
            hide: 400
        }
    });

    $('.button').click(function () {
        // this.addClass('loading')
         $(this).addClass("loading");
    });
});
