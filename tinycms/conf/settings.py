from django.conf import settings

PUBLISH_DEFAULT     = getattr(settings, "PUBLISH_DEFAULT", True)
DRAFT_DEFAULT       = getattr(settings, "DRAFT_DEFAULT", False)
TEMPLATE_DEFAULT    = getattr(settings, "TEMPLATE_DEFAULT", "default")
