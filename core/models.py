from django.db import models

# Create your models here.
class TimeStampModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-created_at", "-updated_at"]


class Gender(TimeStampModel):
    name = models.CharField(max_length=255, unique=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class Country(TimeStampModel):
    name = models.CharField(max_length=255, unique=True, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class State(TimeStampModel):
    name = models.CharField(max_length=255, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "country")
        ordering = ["name"]
        verbose_name_plural = "States"

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class City(TimeStampModel):
    name = models.CharField(max_length=255, default=None)
    state = models.ForeignKey(State, on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "state")
        ordering = ["name"]
        verbose_name_plural = "Cities"

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class RelationType(TimeStampModel):
    name = models.CharField(max_length=255, unique=True, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Relation Types"

    def __str__(self):
        return "%s - %s" % (self.id, self.name)
