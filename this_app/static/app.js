$('#add-bucketlist-modal').on('hidden.bs.modal', function (e) {
    $(this).find("input, textarea").val('').end()
    })

$('#add-activity-modal').on('hidden.bs.modal', function (e) {
    $(this).find("input, textarea").val('').end()
           .find("input[type=checkbox]").prop("checked", "").end();
    })
