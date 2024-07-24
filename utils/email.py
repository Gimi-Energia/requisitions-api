from setup.settings import BASE_DIR

class EmailUtils:
    def get_template(self, template_name):
       base_template = f"{BASE_DIR}/templates/email/{template_name}.html"
       with open(base_template, "r") as file:
           return file.read()

    def get_base_email(self, template_name: str = 'base_email', content: dict = None):
        template = self.get_template(template_name)
        template = template.replace('EMAIL_BODY_INTRO', content.get('email_body_intro', ''))
        template = template.replace('COMMON_BODY', content.get('common_body', ''))
        template = template.replace('IMPORTANT_NOTE', content.get('important_note', ''))
        return template