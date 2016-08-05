from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel


class Item(TitleSlugDescriptionModel, TimeStampedModel):
    pass
