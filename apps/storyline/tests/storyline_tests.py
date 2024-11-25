import pytest
from django.db import IntegrityError
from apps.storyline.models import Story, Adventure, Quest

@pytest.mark.django_db
class TestOrderedModels:
    def test_story_insertion(self):
        # Insert stories without specifying story_num
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story")

        assert story1.story_num == 1
        assert story2.story_num == 2

        # Insert a story with a specific story_num
        story3 = Story.objects.create(title="Story Three", description="Third Story", story_num=1)

        # story3 should take position 1, and others should shift
        story1.refresh_from_db()
        story2.refresh_from_db()
        story3.refresh_from_db()

        assert story3.story_num == 1
        assert story1.story_num == 2  # Previously 1, now shifted to 2
        assert story2.story_num == 3  # Previously 2, now shifted to 3

    def test_story_update_order(self):
        # Insert stories
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story")
        story3 = Story.objects.create(title="Story Three", description="Third Story")

        # Move story3 from position 3 to position 1
        old_order = story3.story_num
        story3.story_num = 1
        story3.save()

        # Refresh instances
        story1.refresh_from_db()
        story2.refresh_from_db()
        story3.refresh_from_db()

        assert story3.story_num == 1
        assert story1.story_num == 2
        assert story2.story_num == 3

    def test_story_exclude_include(self):
        # Insert stories
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story")
        story3 = Story.objects.create(title="Story Three", description="Third Story")

        # Exclude story2
        story2.include = False
        story2.save()

        # Refresh instances
        story1.refresh_from_db()
        story2.refresh_from_db()
        story3.refresh_from_db()

        assert story1.story_num == 1
        assert story2.story_num is None  # Excluded stories have no order
        assert story3.story_num == 2

        # Re-include story2
        story2.include = True
        story2.save()

        # Refresh instances
        story1.refresh_from_db()
        story2.refresh_from_db()
        story3.refresh_from_db()

        assert story2.story_num == 3  # Should be placed at the end

    def test_story_deletion(self):
        # Insert stories
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story")
        story3 = Story.objects.create(title="Story Three", description="Third Story")

        # Delete story2
        story2.delete()

        # Refresh instances
        story1.refresh_from_db()
        story3.refresh_from_db()

        assert story1.story_num == 1
        assert story3.story_num == 2

    def test_adventure_ordering_within_story(self):
        # Create stories
        story = Story.objects.create(title="Main Story", description="Main Story Description")

        # Create adventures
        adv1 = Adventure.objects.create(title="Adventure One", description="First Adventure", story=story)
        adv2 = Adventure.objects.create(title="Adventure Two", description="Second Adventure", story=story)

        assert adv1.adventure_num == 1
        assert adv2.adventure_num == 2

        # Insert adventure at specific position
        adv3 = Adventure.objects.create(title="Adventure Three", description="Third Adventure", story=story, adventure_num=1)

        adv1.refresh_from_db()
        adv2.refresh_from_db()
        adv3.refresh_from_db()

        assert adv3.adventure_num == 1
        assert adv1.adventure_num == 2
        assert adv2.adventure_num == 3

    def test_quest_ordering_within_adventure(self):
        # Create story and adventure
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)

        # Create quests
        quest1 = Quest.objects.create(title="Quest One", description="First Quest",  adventure=adventure)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest", adventure=adventure)

        assert quest1.quest_num == 1
        assert quest2.quest_num == 2

        # Exclude quest1
        quest1.include = False
        quest1.save()

        quest1.refresh_from_db()
        quest2.refresh_from_db()

        assert quest1.quest_num is None
        assert quest2.quest_num == 1

    def test_nested_ordering(self):
        # Create stories
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story")

        # Create adventures for story1
        adv1_s1 = Adventure.objects.create(title="Adventure One", description="First Adventure", story=story1)
        adv2_s1 = Adventure.objects.create(title="Adventure Two", description="Second Adventure", story=story1)

        # Create adventures for story2
        adv1_s2 = Adventure.objects.create(title="Adventure Three", description="Third Adventure", story=story2)
        adv2_s2 = Adventure.objects.create(title="Adventure Four", description="Fourth Adventure", story=story2)

        assert adv1_s1.adventure_num == 1
        assert adv2_s1.adventure_num == 2
        assert adv1_s2.adventure_num == 1
        assert adv2_s2.adventure_num == 2

        # Exclude adv1_s2
        adv1_s2.include = False
        adv1_s2.save()

        adv1_s2.refresh_from_db()
        adv2_s2.refresh_from_db()

        assert adv1_s2.adventure_num is None
        assert adv2_s2.adventure_num == 1

    def test_update_include_false_to_true(self):
        # Create story and adventure
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story, include=False)

        # adventure should have no adventure_num
        assert adventure.adventure_num is None

        # Include adventure
        adventure.include = True
        adventure.save()

        adventure.refresh_from_db()

        assert adventure.adventure_num == 1

    def test_update_include_true_to_false(self):
        # Create story and adventures
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adv1 = Adventure.objects.create(title="Adventure One", description="First Adventure", story=story)
        adv2 = Adventure.objects.create(title="Adventure Two", description="Second Adventure", story=story)

        assert adv1.adventure_num == 1
        assert adv2.adventure_num == 2

        # Exclude adv1
        adv1.include = False
        adv1.save()

        adv1.refresh_from_db()
        adv2.refresh_from_db()

        assert adv1.adventure_num is None
        assert adv2.adventure_num == 1

    def test_quest_deletion(self):
        # Create story, adventure, and quests
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)
        quest1 = Quest.objects.create(title="Quest One", description="First Quest",  adventure=adventure)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest",  adventure=adventure)
        quest3 = Quest.objects.create(title="Quest Three", description="Third Quest",  adventure=adventure)

        # Delete quest2
        quest2.delete()

        # Refresh instances
        quest1.refresh_from_db()
        quest3.refresh_from_db()

        assert quest1.quest_num == 1
        assert quest3.quest_num == 2

    def test_quest_update_order(self):
        # Create story, adventure, and quests
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)
        quest1 = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest",  adventure=adventure)
        quest3 = Quest.objects.create(title="Quest Three", description="Third Quest",  adventure=adventure)

        # Move quest3 from position 3 to position 1
        quest3.quest_num = 1
        quest3.save()

        # Refresh instances
        quest1.refresh_from_db()
        quest2.refresh_from_db()
        quest3.refresh_from_db()

        assert quest3.quest_num == 1
        assert quest1.quest_num == 2
        assert quest2.quest_num == 3
