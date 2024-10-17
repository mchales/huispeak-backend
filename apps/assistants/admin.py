from django.contrib import admin
from django.contrib import messages
from .models import GeneralInstructions, QuestInstructions, Assistant, QuestAssistant

@admin.register(GeneralInstructions)
class GeneralInstructionsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(QuestInstructions)
class QuestInstructionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'quest')

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'quest', 'openai_assistant_id')

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
            if not change:
                messages.success(request, 'Assistant created successfully and OpenAI assistant ID retrieved.')
            else:
                messages.success(request, 'Assistant updated successfully.')
        except Exception as e:
            messages.error(request, f'Error saving assistant: {e}')

@admin.register(QuestAssistant)
class QuestAssistantAdmin(admin.ModelAdmin):
    list_display = ('quest', 'assistant')