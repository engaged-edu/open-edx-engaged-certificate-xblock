import requests
from django.conf import settings
import json


class EngagedCustomModule():

    def request_certificate(course_id, ead_user_email_address, certificate_id, certificate_template_id, certificate_custom_fields):
        if(
                bool(course_id) and
                bool(ead_user_email_address) and
                bool(certificate_id) and
                bool(certificate_template_id) and
                bool(certificate_custom_fields)
        ):
            payload = {
                'course_id': course_id,
                'ead_user_email_address': ead_user_email_address,
                'certificate_id': certificate_id,
                'certificate_template_id': certificate_template_id,
                'certificate_custom_fields': json.dumps(certificate_custom_fields),
                'ead_server_identifier': settings.ENGAGED_SERVER_IDENTIFIER
            }
            url = settings.ENGAGED_CORE_API_EMIT_CERTIFICATE_URL
            headers = {'internal-api-key': settings.ENGAGED_CORE_API_SECRET_KEY}
            response = requests.post(url, data=payload, headers=headers)
            return response
        else:
            raise Exception("Valores inválidos!")
