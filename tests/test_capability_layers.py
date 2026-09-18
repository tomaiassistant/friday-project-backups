"""Tests for Brain Model provider-replacement capability layers."""

from budget_jarvis_core import (
    BrainCapability,
    CapabilityLayer,
    ProviderDependency,
    default_capability_map,
    provider_required_layers,
    replacement_ready_layers,
)


def test_default_capability_map_covers_core_layers() -> None:
    capabilities = default_capability_map()

    assert {capability.layer for capability in capabilities} == set(CapabilityLayer)
    assert all(capability.current_owner for capability in capabilities)
    assert all(capability.replacement_goal for capability in capabilities)
    assert all(capability.next_step for capability in capabilities)


def test_capability_can_run_without_provider_for_optional_or_local() -> None:
    optional = BrainCapability(
        layer=CapabilityLayer.MEMORY,
        dependency=ProviderDependency.OPTIONAL,
        current_owner="local files",
        replacement_goal="local memory",
        next_step="index files",
    )
    required = BrainCapability(
        layer=CapabilityLayer.GENERATION,
        dependency=ProviderDependency.REQUIRED,
        current_owner="external model",
        replacement_goal="local generation",
        next_step="evaluate local models",
    )

    assert optional.can_run_without_provider is True
    assert required.can_run_without_provider is False


def test_replacement_ready_layers_are_not_provider_required() -> None:
    ready = replacement_ready_layers()

    assert ready
    assert all(capability.dependency is not ProviderDependency.REQUIRED for capability in ready)
    assert CapabilityLayer.MEMORY in {capability.layer for capability in ready}
    assert CapabilityLayer.ACTION in {capability.layer for capability in ready}


def test_provider_required_layers_identify_hard_model_work() -> None:
    required = provider_required_layers()

    assert {capability.layer for capability in required} == {
        CapabilityLayer.REASONING,
        CapabilityLayer.GENERATION,
        CapabilityLayer.LEARNING,
    }


def test_layer_filters_accept_custom_capability_sets() -> None:
    capabilities = (
        BrainCapability(
            layer=CapabilityLayer.MEMORY,
            dependency=ProviderDependency.LOCAL,
            current_owner="local memory",
            replacement_goal="no provider needed",
            next_step="keep testing",
        ),
        BrainCapability(
            layer=CapabilityLayer.GENERATION,
            dependency=ProviderDependency.REQUIRED,
            current_owner="provider",
            replacement_goal="replace later",
            next_step="collect examples",
        ),
    )

    assert [capability.layer for capability in replacement_ready_layers(capabilities)] == [CapabilityLayer.MEMORY]
    assert [capability.layer for capability in provider_required_layers(capabilities)] == [CapabilityLayer.GENERATION]
