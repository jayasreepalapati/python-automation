import json
import pytest
from unittest.mock import MagicMock, patch

from services.ai_service import AIService, HabitPlan

MOCK_RESPONSE = {
    "identity_statement": "I am someone who exercises every day",
    "habits": [
        {
            "title": "Morning run",
            "two_min_version": "Put on running shoes and step outside",
            "cue": "After I wake up, I will go for a run"
        },
        {
            "title": "Evening stretch",
            "two_min_version": "Do one stretch",
            "cue": "After dinner, I will stretch for 2 minutes"
        },
        {
            "title": "Track workouts",
            "two_min_version": "Write one line in workout log",
            "cue": "After each workout, I will log it"
        }
    ]
}


def make_mock_client(response_json: dict):
    """Build a mock Anthropic client that returns a canned JSON response."""
    mock_content = MagicMock()
    mock_content.text = json.dumps(response_json)

    mock_message = MagicMock()
    mock_message.content = [mock_content]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


class TestAIServiceBreakdownGoal:

    def test_returns_habit_plan(self):
        service = AIService()
        service.client = make_mock_client(MOCK_RESPONSE)

        plan = service.breakdown_goal("I want to get fit")

        assert isinstance(plan, HabitPlan)
        assert plan.identity_statement == "I am someone who exercises every day"
        assert len(plan.habits) == 3

    def test_habits_have_required_fields(self):
        service = AIService()
        service.client = make_mock_client(MOCK_RESPONSE)

        plan = service.breakdown_goal("I want to get fit")

        for habit in plan.habits:
            assert "title" in habit
            assert "two_min_version" in habit
            assert "cue" in habit

    def test_identity_statement_format(self):
        service = AIService()
        service.client = make_mock_client(MOCK_RESPONSE)

        plan = service.breakdown_goal("I want to read more")

        assert plan.identity_statement.startswith("I am someone who")

    def test_api_called_with_goal(self):
        service = AIService()
        mock_client = make_mock_client(MOCK_RESPONSE)
        service.client = mock_client

        service.breakdown_goal("I want to meditate daily")

        call_kwargs = mock_client.messages.create.call_args
        messages = call_kwargs.kwargs.get("messages") or call_kwargs.args[0]
        assert any("meditate" in str(m) for m in
                   (call_kwargs.kwargs.get("messages", []) or []))

    def test_raises_on_invalid_json(self):
        mock_content = MagicMock()
        mock_content.text = "This is not JSON"
        mock_message = MagicMock()
        mock_message.content = [mock_content]
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message

        service = AIService()
        service.client = mock_client

        with pytest.raises(json.JSONDecodeError):
            service.breakdown_goal("Some goal")

    def test_raises_on_missing_key(self):
        bad_response = {"habits": []}
        service = AIService()
        service.client = make_mock_client(bad_response)

        with pytest.raises(KeyError):
            service.breakdown_goal("Some goal")

    def test_uses_correct_model(self):
        service = AIService()
        mock_client = make_mock_client(MOCK_RESPONSE)
        service.client = mock_client

        service.breakdown_goal("Goal")

        call_kwargs = mock_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-sonnet-4-20250514"

    def test_ai_not_called_more_than_once(self):
        service = AIService()
        mock_client = make_mock_client(MOCK_RESPONSE)
        service.client = mock_client

        service.breakdown_goal("Goal")

        assert mock_client.messages.create.call_count == 1
