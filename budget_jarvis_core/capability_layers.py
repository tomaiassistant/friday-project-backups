"""Capability layers for reducing external model-provider dependence.

The Brain Model should not be treated as one black-box model. It is a layered
system: memory, reasoning, decision, generation, action, reflection, and
learning can mature separately. This module gives the project a small typed map
for tracking which layers still need an external provider and which layers can
already be handled by local Brain Model code.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CapabilityLayer(StrEnum):
    """Major Brain Model capability layers."""

    INPUT_UNDERSTANDING = "input_understanding"
    MEMORY = "memory"
    REASONING = "reasoning"
    DECISION = "decision"
    GENERATION = "generation"
    ACTION = "action"
    REFLECTION = "reflection"
    LEARNING = "learning"


class ProviderDependency(StrEnum):
    """How much a layer currently depends on an external model provider."""

    REQUIRED = "required"
    ASSISTED = "assisted"
    OPTIONAL = "optional"
    LOCAL = "local"


@dataclass(frozen=True)
class BrainCapability:
    """Replacement status for one capability layer."""

    layer: CapabilityLayer
    dependency: ProviderDependency
    current_owner: str
    replacement_goal: str
    next_step: str

    @property
    def can_run_without_provider(self) -> bool:
        return self.dependency in {ProviderDependency.OPTIONAL, ProviderDependency.LOCAL}


def default_capability_map() -> tuple[BrainCapability, ...]:
    """Return the initial provider-replacement roadmap for Budget Jarvis."""

    return (
        BrainCapability(
            layer=CapabilityLayer.INPUT_UNDERSTANDING,
            dependency=ProviderDependency.ASSISTED,
            current_owner="provider model plus local router",
            replacement_goal="local transcript parsing and intent extraction for routine commands",
            next_step="expand deterministic intent/risk/entity extraction tests",
        ),
        BrainCapability(
            layer=CapabilityLayer.MEMORY,
            dependency=ProviderDependency.OPTIONAL,
            current_owner="local project files and JSON state",
            replacement_goal="local durable memory with retrieval and freshness rules",
            next_step="add project-memory recall over markdown and queue state",
        ),
        BrainCapability(
            layer=CapabilityLayer.REASONING,
            dependency=ProviderDependency.REQUIRED,
            current_owner="external model for complex synthesis",
            replacement_goal="local structured reasoning plans for routine work, provider only for hard cases",
            next_step="encode reusable reasoning patterns and compare them against provider outputs",
        ),
        BrainCapability(
            layer=CapabilityLayer.DECISION,
            dependency=ProviderDependency.ASSISTED,
            current_owner="local risk/router rules plus provider judgment",
            replacement_goal="local policy engine decides safe next actions and escalation gates",
            next_step="add decision scoring and confidence thresholds to brain-loop output",
        ),
        BrainCapability(
            layer=CapabilityLayer.GENERATION,
            dependency=ProviderDependency.REQUIRED,
            current_owner="external model writes natural language and code",
            replacement_goal="template/local-model generation for routine reports, providers for complex creation",
            next_step="separate structured result generation from prose/code generation",
        ),
        BrainCapability(
            layer=CapabilityLayer.ACTION,
            dependency=ProviderDependency.OPTIONAL,
            current_owner="local tools with explicit confirmation gates",
            replacement_goal="local action executor with strict safety and audit logs",
            next_step="connect queued tasks to a non-executing action adapter first",
        ),
        BrainCapability(
            layer=CapabilityLayer.REFLECTION,
            dependency=ProviderDependency.OPTIONAL,
            current_owner="local daily logs and project memory",
            replacement_goal="local self-review that updates durable memory after each run",
            next_step="standardize reflection records and retrieval tags",
        ),
        BrainCapability(
            layer=CapabilityLayer.LEARNING,
            dependency=ProviderDependency.REQUIRED,
            current_owner="manual improvements by Jerry/Tom plus provider assistance",
            replacement_goal="evaluation-driven improvement loop using stored outcomes and tests",
            next_step="create evaluation cases for tasks, decisions, and provider-vs-local outputs",
        ),
    )


def replacement_ready_layers(capabilities: tuple[BrainCapability, ...] | None = None) -> tuple[BrainCapability, ...]:
    """Return layers that can already operate without mandatory providers."""

    selected = capabilities or default_capability_map()
    return tuple(capability for capability in selected if capability.can_run_without_provider)


def provider_required_layers(capabilities: tuple[BrainCapability, ...] | None = None) -> tuple[BrainCapability, ...]:
    """Return layers where external providers remain mandatory for now."""

    selected = capabilities or default_capability_map()
    return tuple(capability for capability in selected if capability.dependency is ProviderDependency.REQUIRED)
