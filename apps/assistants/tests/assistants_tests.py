import pytest
from unittest.mock import patch, MagicMock
from django.db.utils import IntegrityError
from apps.storyline.models import Story, Adventure, Quest
from apps.assistants.models import (
    GeneralInstructions,
    QuestInstructions,
    Assistant,
    QuestAssistant,
)

@pytest.mark.django_db
class TestAssistantModels:
    @patch("apps.assistants.models.client")
    def test_assistant_creation(self, mock_client):
        # Mock the assistant creation response
        mock_assistant = MagicMock()
        mock_assistant.id = "asst_mock_id"

        mock_client.beta.assistants.create.return_value = mock_assistant

        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story and Adventure as required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )

        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,  # Provide the required Adventure
        )

        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        assistant = Assistant(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant",
            model="gpt-4",
        )

        assistant.save()

        # Ensure assistant has openai_assistant_id set
        assert assistant.openai_assistant_id == "asst_mock_id"

        # Ensure assistant was created via the API with correct parameters
        instructions_combined = "General Instructions\n\nQuest Instructions"

        mock_client.beta.assistants.create.assert_called_once_with(
            instructions=instructions_combined,
            name=assistant.name,
            tools=[],
            model=assistant.model,
        )

        # Ensure QuestAssistant was created
        quest_assistant = QuestAssistant.objects.get(quest=quest)
        assert quest_assistant.assistant == assistant

    @patch("apps.assistants.models.client")
    def test_assistant_deletion(self, mock_client):
        # Mock the assistant deletion response for success
        mock_delete_response_success = {
            "id": "asst_mock_id",
            "object": "assistant.deleted",
            "deleted": True,
        }
        mock_client.beta.assistants.delete.return_value = mock_delete_response_success

        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story and Adventure as required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )

        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,
        )
        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        assistant = Assistant.objects.create(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant",
            model="gpt-4",
            openai_assistant_id="asst_mock_id",
        )

        # Delete the assistant
        assistant.delete()

        # Ensure assistant was deleted via the API
        mock_client.beta.assistants.delete.assert_called_once_with("asst_mock_id")

        # Ensure the assistant is deleted from the database
        assert not Assistant.objects.filter(id=assistant.id).exists()

        # Now test the case where deletion fails
        # Reset the mock
        mock_client.reset_mock()

        # Mock the assistant deletion response to indicate failure
        mock_delete_response_failure = {
            "id": "asst_mock_id",
            "object": "assistant.deleted",
            "deleted": False,
        }
        mock_client.beta.assistants.delete.return_value = mock_delete_response_failure

        # Re-create the assistant
        assistant_failure = Assistant.objects.create(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant Failure",
            model="gpt-4",
            openai_assistant_id="asst_mock_id",
        )

        # Attempt to delete the assistant, expecting an exception
        with pytest.raises(Exception) as excinfo:
            assistant_failure.delete()

        # Ensure the exception message is as expected
        assert "Assistant deletion failed" in str(excinfo.value)

        # Ensure assistant was deleted via the API
        mock_client.beta.assistants.delete.assert_called_once_with("asst_mock_id")

        # Ensure the assistant still exists in the database because deletion failed
        assert Assistant.objects.filter(id=assistant_failure.id).exists()

    def test_build_instructions(self):
        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story, Adventure, and Quest if required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )
        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,
        )

        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        assistant = Assistant(
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant",
            model="gpt-4",
        )

        instructions = assistant.build_instructions()
        expected_instructions = "General Instructions\n\nQuest Instructions"

        assert instructions == expected_instructions

    @patch("apps.assistants.models.client")
    def test_save_existing_assistant(self, mock_client):
        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story, Adventure, and Quest as required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )
        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,
        )

        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        # Mock assistant
        assistant = Assistant.objects.create(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant",
            model="gpt-4",
            openai_assistant_id="asst_existing_id",
        )

        # Save assistant again
        assistant.save()

        # Ensure that API create is not called since openai_assistant_id is already set
        mock_client.beta.assistants.create.assert_not_called()


    @pytest.mark.django_db(transaction=True)
    @patch("apps.assistants.models.client")
    def test_assistant_save_failure(self, mock_client):
        # Mock the assistant creation to raise an exception
        mock_client.beta.assistants.create.side_effect = Exception("API Error")

        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story and Adventure as required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )

        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,
        )
        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        assistant = Assistant(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Test Assistant",
            model="gpt-4",
        )

        with pytest.raises(Exception) as excinfo:
            assistant.save()

        assert "API Error" in str(excinfo.value)

        # Ensure that the assistant was not saved to the database
        assert not Assistant.objects.filter(name="Test Assistant").exists()

    @patch("apps.assistants.models.client")
    def test_quest_assistant_uniqueness(self, mock_client):
        # Mock the assistant creation response
        mock_assistant = MagicMock()
        mock_assistant.id = "asst_mock_id"

        mock_client.beta.assistants.create.return_value = mock_assistant

        # Create necessary instances
        general_instructions = GeneralInstructions.objects.create(
            name="General", instructions="General Instructions"
        )

        # Create Story and Adventure as required
        story = Story.objects.create(
            title="Story One", description="First Story"
        )
        adventure = Adventure.objects.create(
            title="Adventure One", description="First Adventure", story=story
        )

        quest = Quest.objects.create(
            title="Quest One",
            description="First Quest",
            objectives="Objectives",
            adventure=adventure,
        )
        quest_instructions = QuestInstructions.objects.create(
            quest=quest, name="Quest Specific", instructions="Quest Instructions"
        )

        assistant1 = Assistant(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Assistant One",
            model="gpt-4",
        )
        assistant1.save()

        assistant2 = Assistant(
            quest=quest,
            quest_instructions=quest_instructions,
            general_instructions=general_instructions,
            name="Assistant Two",
            model="gpt-4",
        )

        with pytest.raises(IntegrityError):
            assistant2.save()
