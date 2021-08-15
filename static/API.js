function toSave() {
    titleChannel = $('#field-titleChannel').val();
    subscriberCount = $('#field-subscriberCount').val();
    viewCount = $('#field-viewCount').val();
    videoCount = $('#field-videoCount').val();
    publishedAt = $('#field-publishedAt').val();
    var lang = $('#field-lang').val();

    $.ajax({
        type: 'POST',
        url: "https:/test/User_update",
        data: {
            "titleChannel": titleChannel,
            "subscriberCount": subscriberCount,
            "viewCount": viewCount,
            "videoCount": videoCount,
            "publishedAt": publishedAt,
            "lang": lang
        },
        dataType: "json"
    }).done(function () {
        $('#modal-1').modal('hide');
        table.row.data([titleChannel, subscriberCount, viewCount, videoCount, publishedAt, lang, UserIndex_CreateEditButton(titleChannel, subscriberCount, viewCount, videoCount, publishedAt, lang), UserIndex_CreateDeleteButton(val_no)], $('#' + tempUpdate));
    });
}