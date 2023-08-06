import logging
import os
from email.mime.image import MIMEImage

import html2text
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail.message import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from jinja2 import Template as JinjaTemplate

logger = logging.getLogger("emails")


def send_custom_email(
    recipient: list[str] | str,
    path: str = None,
    template: any = None,
    template_prefix: str = None,
    context=None,
    subject: str = None,
    body: str = None,
    attachments: list[ContentFile] = None,
    attachment_path: str = None,
    enable_logo: bool = False,
) -> str:
    """This function is responsible to send emails and create emails in database model.

    Parameters:
    recipient (list[str]): List of Receivers emails
    path (str): path to html file for email content and subject (path should be upto parent folder of html file inside template folder)
    template (any): Object of Template Model if exists (Optional)
    template_prefix (str): html file name
    context (dict): context to replace variable name in template
    subject (str): subject of email as string
    body (str): content of email as string
    attachment (list[ContentFile]): attach file to send email as attachement
    attachment_path (str): send string path of attachment,
    enable_logo (bool): set true to enable logo in email

    Returns:
    str : email success or error message
    """
    from email_service.models import Attachment, Email

    if not recipient or len(recipient) == 0:
        logger.error("Please provide at least one recipient.")
        return "Please provide at least one recipient."
    if (path or template_prefix) and (subject or body):
        return (
            "You can either send templated email or simple email at a time, not both."
        )

    from_email = settings.EMAIL_FROM
    to = recipient if isinstance(recipient, list) else [recipient]
    bcc_email = settings.EMAIL_BCC

    if template:
        email_subject = JinjaTemplate(template.subject).render(context)
        html_content = JinjaTemplate(template.body).render(context)

    else:
        if not ((path and template_prefix) or subject):
            logger.error(
                "Please provide either path to html template or text subject of email."
            )
            return (
                "Please provide either path to html template or text subject of email."
            )

        if not ((path and template_prefix) or body):
            logger.error(
                "Please provide either path to html template or text body of email."
            )
            return "Please provide either path to html template or text body of email."

        subject_file = (
            f"{path}/{template_prefix}_subject.txt"
            if path
            else f"{template_prefix}_subject.txt"
        )
        html_file = (
            f"{path}/{template_prefix}.html" if path else f"{template_prefix}.html"
        )
        try:
            email_subject = (
                render_to_string(subject_file, context).strip()
                if template_prefix and path
                else subject
            )
            html_content = (
                render_to_string(html_file, context)
                if template_prefix and path
                else body
            )
        except TemplateDoesNotExist:
            return f"Email template file or subject file not exists for prefix {template_prefix}"

    email = Email.objects.create(
        subject=email_subject,
        body=html_content,
        recipients=recipient,
        from_user=from_email,
        template=template,
    )
    text_content = html2text.HTML2Text().handle(html_content)
    msg = EmailMultiAlternatives(
        subject or email_subject, text_content, from_email, to, bcc=[bcc_email]
    )
    msg.attach_alternative(html_content, "text/html")

    if attachment_path:
        full_file_path = f"{settings.BASE_DIR}/{attachment_path}"
        with open(full_file_path, mode="rb") as file:
            content_file = ContentFile(
                file.read(), name=os.path.basename(attachment_path)
            )
            attachement = Attachment.objects.create(file=content_file)
            email.attachments.add(attachement)
        msg.attach_file(full_file_path)

    if attachments:
        for attachement_file in attachments:
            attachement = Attachment.objects.create(file=attachement_file)
            email.attachments.add(attachement)
            msg.attach_file(f"{settings.BASE_DIR}/{attachement.file.url}")

    if enable_logo:
        msg.content_subtype = "html"
        msg.mixed_subtype = "related"
        image_path = os.path.join(
            settings.BASE_DIR, f"static/{settings.LOGO_IMAGE_NAME}"
        )
        with open(image_path, "rb") as banner_image:
            banner_image = MIMEImage(banner_image.read())
            banner_image.add_header("Content-ID", f"<{settings.LOGO_IMAGE_NAME}>")
            msg.attach(banner_image)
    try:
        msg.send()
        email.status = Email.EmailStatus.sent
        email.save()
        return "Email Sent Successfully."
    except Exception as ex:  # pragma: no cover
        logger.exception(
            f"""Caught exception {ex} while sending email with params:
            path-{path} template-{template_prefix}, recipient-{recipient},
            context-{context}, subject-{subject}, body-{body}"""
        )
        email.remarks = f"""Caught exception {ex} while sending email with params:
            path-{path} template-{template_prefix}, recipient-{recipient},
            context-{context}, subject-{subject}, body-{body}"""
        email.status = Email.EmailStatus.error
        email.save()
        return "Facing some problem while sending email."
