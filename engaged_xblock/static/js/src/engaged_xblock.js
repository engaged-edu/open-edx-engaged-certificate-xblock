/* Javascript for EngagEDXBlock. */
function EngagEDXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'request_certificate');

    function updateData(result) {
        document.getElementById('request-loader').remove()
        $('#request-content', element).html(result.request_content_html);
    }

    function onSuccessInit(result) {
        $('#request-content', element).html(result.request_content_html);
        document.getElementById("request-content").onsubmit = request_certificate;
    }

    function request_certificate(e) {
        e.preventDefault();
        const lead_full_name = $('#student-name').val();
        const requestContent = document.getElementById('request-content');
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"custom_fields": {
                "lead_full_name": lead_full_name
            }}),
            beforeSend: () => {
                const loader = document.createElement('div');
                loader.id = 'request-loader'
                loader.classList.add('loader')
                requestContent.appendChild(loader);
            },
            success: updateData,
            error: (result) => {
                const msg = result.responseJSON && result.responseJSON.error ? result.responseJSON.error : "Não foi possivel gerar seu certificado"
                const p = document.createElement('p');
                p.innerHTML = msg;
                p.id = 'error-message-return'
                p.classList.add('error')
                document.getElementById('request-loader').remove()
                requestContent.appendChild(p);
                setTimeout(function remove() {
                    document.getElementById('error-message-return').remove()
                }, 2500);
            }
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
