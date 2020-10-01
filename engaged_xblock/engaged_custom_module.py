import requests


class EngagedCustomModule():

    def request_certificate(course_id, ead_user_email_address, certificate_id, certificate_template_id, certificate_custom_fields, ead_server_identifier):
        if(
                bool(course_id) and
                bool(ead_user_email_address) and
                bool(certificate_id) and
                bool(certificate_template_id) and
                bool(certificate_custom_fields) and
                bool(ead_server_identifier)
        ):
            payload = {
                'course_id': course_id,
                'ead_user_email_address': ead_user_email_address,
                'certificate_id': certificate_id,
                'certificate_template_id': certificate_template_id,
                'certificate_custom_fields': certificate_custom_fields,
                'ead_server_identifier': ead_server_identifier
            }
            print('****payload****')
            print(payload)
            headers = {'internal-api-key': '123123'}
            # url = 'https://core.engaged.com.br/internal/ead/certificate/emit'
            url = 'https://webhook.site/86923dcb-ead2-4c08-bbbf-7f17eee1cb52'
            response = requests.post(url, data=payload, headers=headers)
            return response
        else:
            print('Valores invalidos!')
            return False
