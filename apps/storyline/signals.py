from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Character, Quest, Objectives
from apps.assistants.models import Assistant

@receiver(post_save, sender=Character)
def update_assistants_on_character_change(sender, instance, **kwargs):
    # Find all Quests associated with this Character
    quests = instance.quests.all()
    # Find all Assistants associated with these Quests
    assistants = Assistant.objects.filter(quest__in=quests)
    for assistant in assistants:
        assistant.save()

@receiver(post_save, sender=Quest)
def update_assistants_on_quest_change(sender, instance, **kwargs):
    try:
        assistant = Assistant.objects.get(quest=instance)
        assistant.save()  # Update the assistant
    except Assistant.DoesNotExist:
        pass 

@receiver(post_save, sender=Objectives)
def update_assistants_on_objectives_change(sender, instance, **kwargs):
    try:
        assistant = Assistant.objects.get(quest=instance.quest)
        assistant.save()  # Update the assistant
    except Assistant.DoesNotExist:
        pass 

# Deleting objectives can also affect the assistant
@receiver(post_delete, sender=Objectives)
def update_assistants_on_objectives_delete(sender, instance, **kwargs):
    try:
        assistant = Assistant.objects.get(quest=instance.quest)
        assistant.save()
    except Assistant.DoesNotExist:
        pass