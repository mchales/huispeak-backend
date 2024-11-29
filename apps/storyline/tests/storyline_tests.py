import pytest
from apps.storyline.models import Story, Adventure, Quest, Character, Objectives

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
        character = Character.objects.create(name="Hero", description="Brave hero")
        quest1 = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest", adventure=adventure, character=character)

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

        # Adventure should have no adventure_num
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
        character = Character.objects.create(name="Hero", description="Brave hero")
        quest1 = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest", adventure=adventure, character=character)
        quest3 = Quest.objects.create(title="Quest Three", description="Third Quest", adventure=adventure, character=character)

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
        character = Character.objects.create(name="Hero", description="Brave hero")
        quest1 = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)
        quest2 = Quest.objects.create(title="Quest Two", description="Second Quest", adventure=adventure, character=character)
        quest3 = Quest.objects.create(title="Quest Three", description="Third Quest", adventure=adventure, character=character)

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

    def test_character_creation(self):
        character = Character.objects.create(name="Hero", description="Brave hero", voice="alloy")
        assert character.name == "Hero"
        assert character.description == "Brave hero"
        assert character.voice == "alloy"

    def test_character_as_text(self):
        character = Character.objects.create(name="Hero", description="Brave hero", voice="alloy")
        expected_text = "Name: Hero\nDescription: Brave hero\n"
        assert character.as_text() == expected_text

    def test_quest_as_text(self):
        # Create necessary objects
        character = Character.objects.create(name="Hero", description="Brave hero", voice="alloy")
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)
        quest = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)

        # Create objectives
        Objectives.objects.create(quest=quest, objective="Find the treasure")
        Objectives.objects.create(quest=quest, objective="Defeat the dragon")

        expected_text = (
            "Title: Quest One\n"
            "Description: First Quest\n"
            "Objectives: - Find the treasure\n- Defeat the dragon\n"
        )
        assert quest.as_text() == expected_text

    def test_quest_as_text_no_objectives(self):
        # Create necessary objects
        character = Character.objects.create(name="Hero", description="Brave hero", voice="alloy")
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)
        quest = Quest.objects.create(title="Quest Two", description="Second Quest", adventure=adventure, character=character)

        expected_text = (
            "Title: Quest Two\n"
            "Description: Second Quest\n"
            "Objectives: \n"
        )
        assert quest.as_text() == expected_text

    def test_objectives_creation(self):
        character = Character.objects.create(name="Hero", description="Brave hero", voice="alloy")
        story = Story.objects.create(title="Main Story", description="Main Story Description")
        adventure = Adventure.objects.create(title="Main Adventure", description="Main Adventure Description", story=story)
        quest = Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)
        objective = Objectives.objects.create(quest=quest, objective="Find the treasure")

        assert objective.quest == quest
        assert objective.objective == "Find the treasure"

    def test_including_excluded_story(self):
        # Insert stories
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story", include=False)
        story3 = Story.objects.create(title="Story Three", description="Third Story")

        # Include story2
        story2.include = True
        story2.save()

        # Refresh instances
        story1.refresh_from_db()
        story2.refresh_from_db()
        story3.refresh_from_db()

        assert story1.story_num == 1
        assert story2.story_num == 3  # Should be added to the end
        assert story3.story_num == 2

    def test_reordering_after_insertion(self):
        # Insert stories with specific positions
        story1 = Story.objects.create(title="Story One", description="First Story")
        story2 = Story.objects.create(title="Story Two", description="Second Story", story_num=1)

        # Refresh instances
        story1.refresh_from_db()
        story2.refresh_from_db()

        assert story1.story_num == 2  # Shifted down due to insertion at position 1
        assert story2.story_num == 1

    def test_delete_story_with_adventures_and_quests(self):
        # Create story
        story = Story.objects.create(title="Epic Story", description="An epic tale")

        # Create adventure and quests
        adventure = Adventure.objects.create(title="Adventure One", description="First Adventure", story=story)
        character = Character.objects.create(name="Hero", description="Brave hero")
        Quest.objects.create(title="Quest One", description="First Quest", adventure=adventure, character=character)

        # Delete story
        story.delete()

        # Check that adventure and quests are deleted
        assert not Adventure.objects.filter(pk=adventure.pk).exists()
        assert not Quest.objects.filter(adventure=adventure).exists()
