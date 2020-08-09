"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.template import Context, Template

# from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, Boolean, String, Dict
from xblock.fragment import Fragment

import uuid


class EngagEDXBlock(XBlock):
    """
    Esse xblock tem como principal função gerar o certificado para o aluno.
    """

    # Campos compartilhados entre os escopos.
    certificate_page_url = String(
        help="Url da api geradora de certificado",
        default="ensimais.engaged.com.br",
        scope=Scope.settings,
    )
    certificate_template_id = String(
        help="Id do template do certificado que será utilizado para os alunos",
        default="Não especificado",
        scope=Scope.settings,
    )
    # Campos especificos do aluno
    certificate_status = String(
        help="Estado do certificado do aluno, variando entre não solicitado/solicitado",
        default="not-requested",
        scope=Scope.user_state,
    )
    certificate_request_id = String(
        help="Id gerado para o certificado que o aluno ficará fazendo a busca",
        default=None,
        scope=Scope.user_state,
    )
    certificate_custom_fields = Dict(
        help="Campos variaveis que poderão sobrescrever o certificado",
        default={},
        scope=Scope.user_state,
    )
    certificate_request_template_id = String(
        help="Copia do id do template para ficar salvo no state do usuario",
        default=None,
        scope=Scope.user_state,
    )
    request_content_html = String(
        help="HTML apresentado antes de ter solicitado o certificado, utilizado em uma variavel para poder atualizar",
        default="""
            <div class="flex-center">
                <input class="input-width input-margin" type="text" id="student-name" placeholder="Seu nome para o certificado" maxlength="32" required />
            </div>
            <button type="submit" class="request-certificate">Solicitar Certificado</button>
        """,
        scope=Scope.user_state,
    )

    def load_resource(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    """
    Util functions
    """

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    def student_view(self, context=None):
        """
        View principal do XBlock, como aparece para os alunos.
        """
        context = {
            "certificate_status": self.certificate_status,
            "request_content_html": self.request_content_html,
            "certificate_page_url": self.certificate_page_url,
            "certificate_request_id": self.certificate_request_id,
        }
        html = self.render_template("static/html/engaged_xblock.html", context)

        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/engaged_xblock.css"))
        frag.add_javascript(self.load_resource("static/js/src/engaged_xblock.js"))
        frag.initialize_js("EngagEDXBlock")
        return frag

    def studio_view(self, context=None):
        """
        The primary view of the EngagEDXBlock, shown to administrators on edit mode
        when viewing courses.
        """
        context = {
            "certificate_page_url": self.certificate_page_url,
            "certificate_template_id": self.certificate_template_id,
        }
        html = self.render_template("static/html/certificate_studio_view.html", context)

        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/engaged_xblock.css"))
        frag.add_javascript(
            self.load_resource("static/js/src/engaged_xblock_studio.js")
        )
        frag.initialize_js("EngagEDXBlock")
        return frag

    def author_view(self, context=None):
        """
        The primary view of the EngagEDXBlock, shown to administrators on preview mode
        when viewing courses.
        """
        context = {
            "certificate_page_url": self.certificate_page_url,
            "certificate_template_id": self.certificate_template_id,
        }
        html = self.render_template("static/html/certificate_author_view.html", context)
        frag = Fragment(html.format(self=self))
        frag.add_css(self.load_resource("static/css/engaged_xblock.css"))
        frag.add_javascript(self.load_resource("static/js/src/engaged_xblock.js"))
        frag.initialize_js("EngagEDXBlock")
        return frag

    @XBlock.json_handler
    def get_component_data(self, data, suffix=""):
        """
        Retorna informações do componente.
        """
        return {
            "request_content_html": self.request_content_html,
        }

    @XBlock.json_handler
    def confirm_config(self, data, suffix=""):
        """
        Realiza as configurações
        """
        self.certificate_page_url = data["certificate_page_url"]
        self.certificate_template_id = data["certificate_template_id"]
        return {
            "certificate_page_url": self.certificate_page_url,
            "certificate_template_id": self.certificate_template_id,
        }

    @XBlock.json_handler
    def request_certificate(self, data, suffix=""):
        """
        Executa a solicitação para emissão do certificado.
        """

        if self.certificate_status != "not-requested":
            log.error("Certificate already requested!")
            return {}

        self.certificate_status = "requested"
        self.certificate_request_id = str(uuid.uuid4())
        self.certificate_custom_fields = data["custom_fields"]
        self.certificate_request_template_id = self.certificate_template_id
        self.request_content_html = (
            """<p>Certificado solicitado, aguarde e será notificado por e-mail.</p>"""
        )

        # iframe url: {{ certificate_page_url }}/id/{{certificate_request_id }}?error_type=requested
        return {
            "certificate_status": self.certificate_status,
            "certificate_request_id": self.certificate_request_id,
            "certificate_custom_fields": self.certificate_custom_fields,
            "certificate_request_template_id": self.certificate_template_id,
            "request_content_html": self.request_content_html,
        }

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            (
                "EngagEDXBlock",
                """<engaged_xblock/>
             """,
            ),
            (
                "Multiple EngagEDXBlock",
                """<vertical_demo>
                <engaged_xblock/>
                <engaged_xblock/>
                <engaged_xblock/>
                </vertical_demo>
             """,
            ),
        ]
