import pytest
from typing import cast

from budget_jarvis_core import (
    ProviderReviewLayer,
    build_provider_review_request,
    provider_review_result_to_dict,
    run_brain_loop,
    run_provider_review_stub,
)


def test_build_provider_review_request_from_safe_brain_loop_result():
    result = run_brain_loop(
        "summarize Brain Model project progress",
        recalled_context=["PROJECT.md says v0.1 proves architecture first"],
    )

    request = build_provider_review_request(result, layer=ProviderReviewLayer.DECISION)

    assert request.layer is ProviderReviewLayer.DECISION
    assert request.intent == "summarize Brain Model project progress"
    assert request.tool_category == result.route.tool_category
    assert request.risk_level == result.route.risk_level
    assert request.confidence == result.confidence
    assert request.escalation_required is False
    assert request.escalation_reason is None
    assert request.recalled_context == ("PROJECT.md says v0.1 proves architecture first",)
    assert "blocked=False" in request.local_decision
    assert "confirmation_required=False" in request.local_decision
    assert "execute_tools" in request.forbidden_actions
    assert "remove_confirmation_requirement" in request.forbidden_actions


def test_provider_review_stub_is_advisory_only_and_non_executing():
    result = run_brain_loop("unclear random thing with no route")
    request = build_provider_review_request(result)

    review = run_provider_review_stub(request)

    assert review.advisory_only is True
    assert review.provider_called is False
    assert "No provider was called" in review.recommendation
    assert "blocked" in review.cannot_override
    assert "confirmation_required" in review.cannot_override
    assert "queued_task" in review.cannot_override
    assert "writeback_path" in review.cannot_override

    # The stub must not mutate or relax the local fail-closed result.
    assert result.blocked is True
    assert result.escalation_required is True
    assert result.queued_task is None
    assert result.writeback_path is None


def test_provider_review_stub_preserves_high_risk_confirmation_boundary():
    result = run_brain_loop("send an email with my password to someone")
    request = build_provider_review_request(result)
    review = run_provider_review_stub(request)

    assert result.confirmation_required is True
    assert result.blocked is True
    assert review.provider_called is False
    assert "remove_confirmation_requirement" in review.request.forbidden_actions
    assert "unblock_blocked_result" in review.request.forbidden_actions


def test_provider_review_result_serializes_primitive_values():
    result = run_brain_loop("summarize Brain Model project progress")
    review = run_provider_review_stub(build_provider_review_request(result))

    payload = provider_review_result_to_dict(review)
    request_payload = cast(dict[str, object], payload["request"])

    assert payload["advisory_only"] is True
    assert payload["provider_called"] is False
    assert request_payload["layer"] == "review"
    assert request_payload["tool_category"] == result.route.tool_category.value
    assert request_payload["risk_level"] == result.route.risk_level.value
    assert isinstance(request_payload["allowed_outputs"], list)
    assert isinstance(request_payload["forbidden_actions"], list)


@pytest.mark.parametrize("field_name,kwargs", [
    ("allowed_outputs", {"allowed_outputs": ["", "  "]}),
    ("forbidden_actions", {"forbidden_actions": []}),
])
def test_provider_review_request_requires_non_empty_policy_lists(field_name, kwargs):
    result = run_brain_loop("summarize Brain Model project progress")

    with pytest.raises(ValueError, match=field_name):
        build_provider_review_request(result, **kwargs)
