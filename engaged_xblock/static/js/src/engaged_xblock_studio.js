/* Javascript for EngagEDXBlock. */
function EngagEDXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'confirm_config');

    function onFinish(result, message, classToAdd) {
        document.getElementById("result-message").innerHTML = message;
        document.getElementById("result-message").classList.add(classToAdd);
    }

    function onSuccessInit() {
        document.getElementById("config-form").onsubmit = confirm_config;
    }

    function confirm_config(e) {
        e.preventDefault();
        const certificate_page_url = $('#certificate_page_url').val();
        const certificate_template_id = $('#certificate_template_id').val();
        runtime.notify('save', {state: 'start'});
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({certificate_page_url, certificate_template_id}),
            success: (result) => {
                runtime.notify('save', {state: 'end'});
                setTimeout(function(){
                    window.location.reload();
                }, 700);
            },
            error: (result) => {
                onFinish(result,"Não foi possivel salvar a configuração.","error");
                runtime.notify('error', {msg: response.message})
            },
        });
        return false;
    }

    $(function ($) {
        // init
        onSuccessInit()
    });
}
