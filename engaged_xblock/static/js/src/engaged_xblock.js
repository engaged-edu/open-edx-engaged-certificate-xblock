/* Javascript for EngagEDXBlock. */
function EngagEDXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'request_certificate');

    function updateData(result) {
        $('#request-content', element).html(result.request_content_html);
    }

    function onSuccessInit(result) {
        $('#request-content', element).html(result.request_content_html);
        document.getElementById("request-content").onsubmit = request_certificate;
    }

    function request_certificate(e) {
        e.preventDefault();
        const lead_full_name = $('#student-name').val();
        console.log(lead_full_name)
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"custom_fields": {
                "lead_full_name": lead_full_name
            }}),
            success: updateData
        });
        return false;
    }

    $(function ($) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'get_component_data'),
            data: JSON.stringify({}),
            success: onSuccessInit
        });
    });
}
