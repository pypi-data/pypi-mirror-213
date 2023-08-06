from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The creation time, always in UTC timezone."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The last update time, always in UTC timezone."),
    )


class Attachment(CreatedUpdatedMixin):  # pragma: no cover
    """Stores the attachements of emails sent by application."""

    file = models.FileField(upload_to="email_attachements")

    def __str__(self) -> str:
        return str(self.id)


class Template(models.Model):
    """Stores user's defined templates to be used in emails."""

    class TemplateType(models.IntegerChoices):
        email_verification = 0, _("User Email Verification")
        password_reset_email = 1, _("Password Reset")
        welcome_email = 2, _("User Welcome")
        announcement = 3, _("Announcement")
        promotional = 4, _("Promotional")
        general = 5, _("General")
        reminder = 6, _("Reminders")

    name = models.CharField(unique=True, max_length=50)
    subject = models.CharField(max_length=200)
    body = RichTextField(null=True, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    template_type = models.PositiveSmallIntegerField(
        choices=TemplateType.choices, default=TemplateType.general
    )

    def __str__(self) -> str:
        return self.name


class Email(CreatedUpdatedMixin):
    """Stores the emails sent by application."""

    class EmailStatus(models.IntegerChoices):
        pending = 0, _("Pending")
        error = 1, _("Error")
        sent = 2, _("Sent")

    class EmailPriority(models.IntegerChoices):
        low = 0, _("Low")
        hogh = 1, _("High")

    subject = models.CharField(max_length=200)
    body = models.TextField()
    recipients = models.TextField(null=True, help_text="emails separated by newline")
    cc_emails = models.TextField(
        null=True, blank=True, help_text="emails separated by newline"
    )
    from_user = models.EmailField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=EmailStatus.choices, default=EmailStatus.pending
    )
    remarks = models.TextField(
        blank=True,
        help_text="It will be used to store any error message while sending, or any additional remarks",
    )
    priority = models.PositiveSmallIntegerField(
        choices=EmailPriority.choices, default=EmailPriority.low
    )
    scheduled_at = models.DateTimeField(null=True, blank=True)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.subject
