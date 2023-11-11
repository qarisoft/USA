function reqAjax() {
    let myarray = [];
    let cross = $('#crosss').find(":selected").val();


    $("input:checkbox[name=filtr_list]:checked").each(function() {
        myarray.push($(this).val());
    });
    $.ajax({
        url: '/filter_ajax/',
        data: {
            filtr_with_sec: myarray,
            crostype: cross,
        },
        dataType: 'json',
        success: function(res) {
            if (res.data.length != 0) {

                $('#stks-count').html(`companies ` + res.data.length + `<i class="fa-solid fa-check" style="color: #16e324;"></i>`);

                if ($('#stks-count').hasClass('text-danger')) {
                    $('#stks-count').removeClass('text-danger');

                };
                if ($('#stks-count').hasClass('text-success')) {
                    console.log("yesssssssssssssssssss")
                } else {
                    $('#stks-count').addClass('text-success');
                };
                let myA = "";
                for (let xx in res.data) {
                    myA += '<li>' + res.data[xx] + '</li>';
                }
                $('.tooltiptext').html(`<ul>` + myA + `</ul>`);
                $('.tooltiptext').css({
                    'display': 'inline-block',
                });
                $('#stks-count').on('mouseenter', function() {
                    $('.tooltiptext').css({
                        'visibility': 'visible',
                        'z-index': 1000,
                    });
                });
                $('.tooltiptext').on('mouseleave', function() {
                    $('.tooltiptext').css({
                        'visibility': 'hidden',
                    });
                });
            } else {
                if ($('#stks-count').hasClass('text-success')) {
                    $('#stks-count').removeClass('text-success');
                };
                $('#stks-count').html(`companies ` + res.data.length);
                if ($('#stks-count').hasClass('text-danger')) {
                    console.log("noooooooooooooo")
                } else {
                    $('#stks-count').addClass('text-danger')
                }
            }
        }
    })

}
$('#create-f-btn').click(function(e) {
    $('.container-myC').toggle();
    $('.container-myC').css({ 'display': 'flex' });

});
$('#dropdown').click(function() {
    $('.filtr-sec').toggle();
});

$('#crosss').change(function() {
    console.log($(this).val());
    reqAjax();
});


let va = $('.filter-chkbox');
$('.filter-chkbox').change(function() {
    reqAjax();

});