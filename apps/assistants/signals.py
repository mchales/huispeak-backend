# When the quest instructions and general instructions get updated, we want to automatically update the assistant instructions

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuestInstructions, GeneralInstructions, Assistant

@receiver(post_save, sender=QuestInstructions)
def update_assistants_on_questinstructions_change(sender, instance, **kwargs):

    assistants = Assistant.objects.filter(quest_instructions=instance)
    for assistant in assistants:
        assistant.save()

@receiver(post_save, sender=GeneralInstructions)
def update_assistants_on_generalinstructions_change(sender, instance, **kwargs):
    # Find all Assistants that reference this GeneralInstructions
    assistants = Assistant.objects.filter(general_instructions=instance)
    for assistant in assistants:
        assistant.save()  