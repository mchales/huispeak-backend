from django.db import models
from django.db import transaction

class OrderingManager:
    def __init__(self, model):
        self.model = model

    def insert(self, instance):
        if not instance.include:
            setattr(instance, instance.num_field_name, None)
            return

        num_field = instance.num_field_name
        parent_field = instance.parent_field_name

        # Get parent instance if applicable
        parent = getattr(instance, parent_field, None) if parent_field else None

        if getattr(instance, num_field) is None:
            # Assign next available order number if not specified
            max_order = self.get_siblings(instance).aggregate(models.Max(num_field)).get(f'{num_field}__max') or 0
            setattr(instance, num_field, max_order + 1)
        else:
            # Shift order numbers to make room for the new instance
            order = getattr(instance, num_field)
            self.get_siblings(instance).filter(**{f"{num_field}__gte": order}).update(**{num_field: models.F(num_field) + 1})

    def update(self, instance, old_order, old_include):
        num_field = instance.num_field_name
        new_order = getattr(instance, num_field)
        new_include = instance.include

        if not old_include and new_include:
            # Include changed from False to True, need to insert into ordering
            self.insert(instance)
        elif old_include and not new_include:
            # Include changed from True to False, need to remove from ordering
            self.delete(instance)
            setattr(instance, num_field, None)
        elif new_include:
            # Regular update
            if old_order == new_order:
                return  # No change in order

            siblings = self.get_siblings(instance).exclude(pk=instance.pk)
            if old_order < new_order:
                # Decrement order numbers of intervening instances
                siblings.filter(**{
                    f"{num_field}__gt": old_order,
                    f"{num_field}__lte": new_order
                }).update(**{num_field: models.F(num_field) - 1})
            else:
                # Increment order numbers of intervening instances
                siblings.filter(**{
                    f"{num_field}__lt": old_order,
                    f"{num_field}__gte": new_order
                }).update(**{num_field: models.F(num_field) + 1})
        else:
            # New include is False; set order number to None
            setattr(instance, num_field, None)

    def delete(self, instance):
        num_field = instance.num_field_name
        order = getattr(instance, num_field)
        if order is None:
            return
        # Decrement order numbers of instances that come after the deleted one
        self.get_siblings(instance).filter(**{f"{num_field}__gt": order}).update(**{num_field: models.F(num_field) - 1})

    def get_siblings(self, instance):
        parent_field = instance.parent_field_name
        if parent_field:
            parent = getattr(instance, parent_field)
            return self.model.objects.filter(**{parent_field: parent, 'include': True})
        else:
            return self.model.objects.filter(include=True)

class OrderedModel(models.Model):
    include = models.BooleanField(default=True)
    num_field_name = None
    parent_field_name = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self._state.adding
            ordering_manager = OrderingManager(self.__class__)

            if is_new:
                # Handle insertion
                ordering_manager.insert(self)
            else:
                # Handle update
                old_instance = self.__class__.objects.get(pk=self.pk)
                old_order = getattr(old_instance, self.num_field_name)
                old_include = old_instance.include
                ordering_manager.update(self, old_order, old_include)

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            ordering_manager = OrderingManager(self.__class__)
            ordering_manager.delete(self)
            super().delete(*args, **kwargs)

class Story(OrderedModel):
    num_field_name = 'story_num'
    parent_field_name = None

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    story_num = models.IntegerField(null=True, blank=True)
    include = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    class Meta:
        ordering = ['story_num']

    def __str__(self):
        return f"Story {self.story_num}: {self.title}"

class Adventure(OrderedModel):
    num_field_name = 'adventure_num'
    parent_field_name = 'story'

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='adventures')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    adventure_num = models.IntegerField(null=True, blank=True)
    include = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['adventure_num']

    def __str__(self):
        return f"Adventure {self.adventure_num} in Story {self.story.story_num}: {self.title}"

class Quest(OrderedModel):
    num_field_name = 'quest_num'
    parent_field_name = 'adventure'

    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='quests')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    quest_num = models.IntegerField(null=True, blank=True)
    image_name = models.CharField(max_length=255, blank=True)
    include = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['quest_num']

    def __str__(self):
        return f"Quest {self.quest_num} in Adventure {self.adventure.adventure_num}: {self.title}"
    
class Objectives(models.Model):
    quest = models.ForeignKey(Quest, related_name='objectives', on_delete=models.CASCADE)
    objective = models.TextField()
    
    def __str__(self):
        return self.objective
