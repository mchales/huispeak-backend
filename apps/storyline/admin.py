from django.contrib import admin
from .models import Story, Adventure, Quest

# Note objects must be deleted from their page, not with a select delete
class QuestInline(admin.TabularInline):
    model = Quest
    extra = 0
    fields = ('quest_num', 'title', 'description', 'objectives')
    ordering = ('quest_num',)
    show_change_link = True

class AdventureInline(admin.TabularInline):
    model = Adventure
    extra = 0
    fields = ('adventure_num', 'title', 'description')
    ordering = ('adventure_num',)
    show_change_link = True

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','story_num', 'include', 'description', 'created_at', 'updated_at')
    ordering = ('story_num',)
    search_fields = ('title',)
    inlines = [AdventureInline]

class AdventureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','adventure_num', 'include', 'story',  'description', 'created_at', 'updated_at')
    ordering = ('story', 'adventure_num')
    search_fields = ('title', 'story__title')
    inlines = [QuestInline]
    list_filter = ('story',)

class QuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quest_num', 'include', 'adventure', 'description', 'created_at', 'updated_at')
    ordering = ('adventure', 'quest_num')
    search_fields = ('title', 'adventure__title')
    list_filter = ('adventure__story', 'adventure')

admin.site.register(Story, StoryAdmin)
admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Quest, QuestAdmin)
