import uuid
from django.db import models
from apps.storyline.models import Quest
from services.openai_service import client
from django.db import transaction



class GeneralInstructions(models.Model):
    name = models.CharField(max_length=255)
    instructions = models.TextField()

    def __str__(self):
        return self.name


class QuestInstructions(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.quest})"


class Assistant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    quest_instructions = models.ForeignKey(QuestInstructions, on_delete=models.CASCADE)
    general_instructions = models.ForeignKey(GeneralInstructions, on_delete=models.CASCADE)
    openai_assistant_id = models.CharField(max_length=255, blank=True, null=True)  # Stores the assistant ID from OpenAI
    name = models.CharField(max_length=255)  # The name of the assistant in the playground
    model = models.CharField(max_length=255, default="gpt-4o")  # The model used by the assistant

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic(): 
            instructions = self.build_instructions()
            if not self.openai_assistant_id:
                # Creating a new assistant
                try:
                    assistant = client.beta.assistants.create(
                        instructions=instructions,
                        name=self.name,
                        tools=[],
                        model=self.model,
                    )
                    self.openai_assistant_id = assistant.id
                    super().save(*args, **kwargs)
                    QuestAssistant.objects.create(quest=self.quest, assistant=self)
                except Exception as e:
                    print(f"Error creating assistant: {e}")
                    raise
            else:
                # Updating the assistant instructions
                try:
                    assistant = client.beta.assistants.update(
                        self.openai_assistant_id,
                        instructions=instructions,
                    )
                    super().save(*args, **kwargs)
                except Exception as e:
                    print(f"Error updating assistant: {e}")
                    raise
                
    def delete(self, *args, **kwargs):
        if self.openai_assistant_id:
            try:
                response = client.beta.assistants.delete(self.openai_assistant_id)
                if not response.get('deleted', False):
                    raise Exception(f"Assistant deletion failed: {response}")
            except Exception as e:
                print(f"Error deleting assistant: {e}")
                raise
        super().delete(*args, **kwargs)


    def build_instructions(self):
        """
        Combine instructions from general instructions, quest instructions,
        and include data from Character, Quest, and Objectives.
        """
        instructions = ""
        if self.general_instructions and self.general_instructions.instructions:
            instructions += self.general_instructions.instructions.strip() + "\n\n"
        if self.quest_instructions and self.quest_instructions.instructions:
            instructions += self.quest_instructions.instructions.strip() + "\n\n"
        # Include Character information
        if self.quest.character:
            instructions += "Adopt the personality described in the character section below:\n" + self.quest.character.as_text() + "\n\n"
        # Include Quest information
        instructions += "This is the quest instructions the individual you are talking to is following, you should follow and push them to complete the objectives:\n" + self.quest.as_text() + "\n\n"
        return instructions.strip()


class QuestAssistant(models.Model):
    quest = models.OneToOneField(Quest, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assistant} for {self.quest}"