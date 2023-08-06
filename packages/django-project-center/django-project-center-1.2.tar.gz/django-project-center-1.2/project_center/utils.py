from django.template.loader import render_to_string

def generate_email_body(html_template_path, **kwargs):
    html = render_to_string((html_template_path), context=kwargs)
    return html