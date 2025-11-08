"""Unit tests for dependency resolver."""

import pytest

from src.core.dependency_resolver import (
    build_dependency_graph,
    extract_references,
    get_dependency_summary,
    has_dependencies,
    sort_items_by_dependencies,
    topological_sort,
)


class TestExtractReferences:
    """Tests for extract_references function."""

    def test_extract_no_references(self):
        """Test extracting references from object with no dependencies."""
        item = {"name": "addr-1", "value": "10.1.1.1"}
        refs = extract_references(item, "address")
        assert refs == set()

    def test_extract_tag_references(self):
        """Test extracting tag references."""
        item = {"name": "addr-1", "value": "10.1.1.1", "tag": ["tag-1", "tag-2"]}
        refs = extract_references(item, "address")
        assert refs == {"tag-1", "tag-2"}

    def test_extract_address_group_references(self):
        """Test extracting address group member references."""
        item = {"name": "group-1", "static_value": ["addr-1", "addr-2"]}
        refs = extract_references(item, "address_group")
        assert refs == {"addr-1", "addr-2"}

    def test_extract_service_group_references(self):
        """Test extracting service group member references."""
        item = {"name": "svc-group", "value": ["svc-1", "svc-2"]}
        refs = extract_references(item, "service_group")
        assert refs == {"svc-1", "svc-2"}


class TestBuildDependencyGraph:
    """Tests for build_dependency_graph function."""

    def test_no_dependencies(self):
        """Test building graph with no dependencies."""
        items = [
            {"name": "addr-1", "value": "10.1.1.1"},
            {"name": "addr-2", "value": "10.1.1.2"},
        ]
        graph, lookup = build_dependency_graph(items, "address")

        assert len(graph) == 2
        assert graph["addr-1"] == set()
        assert graph["addr-2"] == set()
        assert len(lookup) == 2

    def test_with_tag_dependencies(self):
        """Test building graph with tag dependencies."""
        items = [
            {"name": "addr-1", "value": "10.1.1.1", "tag": ["tag-1"]},
            {"name": "tag-1", "color": "Red"},
        ]
        graph, lookup = build_dependency_graph(items, "address")

        assert len(graph) == 2
        assert graph["addr-1"] == {"tag-1"}
        assert graph["tag-1"] == set()

    def test_with_group_dependencies(self):
        """Test building graph with group member dependencies."""
        items = [
            {"name": "addr-1", "value": "10.1.1.1"},
            {"name": "addr-2", "value": "10.1.1.2"},
            {"name": "group-1", "static_value": ["addr-1", "addr-2"]},
        ]
        graph, lookup = build_dependency_graph(items, "address_group")

        assert len(graph) == 3
        assert graph["group-1"] == {"addr-1", "addr-2"}
        assert graph["addr-1"] == set()
        assert graph["addr-2"] == set()


class TestTopologicalSort:
    """Tests for topological_sort function."""

    def test_simple_linear_dependency(self):
        """Test sorting simple linear dependency chain."""
        graph = {
            "a": set(),
            "b": {"a"},
            "c": {"b"},
        }
        levels = topological_sort(graph)

        assert len(levels) == 3
        assert levels[0] == ["a"]
        assert levels[1] == ["b"]
        assert levels[2] == ["c"]

    def test_parallel_dependencies(self):
        """Test sorting with parallel dependencies."""
        graph = {
            "a": set(),
            "b": set(),
            "c": {"a", "b"},
        }
        levels = topological_sort(graph)

        assert len(levels) == 2
        # a and b can be in any order in level 0
        assert set(levels[0]) == {"a", "b"}
        assert levels[1] == ["c"]

    def test_no_dependencies(self):
        """Test sorting with no dependencies."""
        graph = {
            "a": set(),
            "b": set(),
            "c": set(),
        }
        levels = topological_sort(graph)

        assert len(levels) == 1
        assert set(levels[0]) == {"a", "b", "c"}

    def test_circular_dependency(self):
        """Test that circular dependencies raise error."""
        graph = {
            "a": {"b"},
            "b": {"a"},
        }
        with pytest.raises(ValueError, match="Circular dependency"):
            topological_sort(graph)


class TestSortItemsByDependencies:
    """Tests for sort_items_by_dependencies function."""

    def test_no_dependencies(self, sample_addresses):
        """Test sorting items with no dependencies."""
        levels = sort_items_by_dependencies(sample_addresses, "address")

        assert len(levels) == 1
        assert len(levels[0]) == 3

    def test_with_tag_dependencies(self, sample_addresses_with_dependencies):
        """Test sorting items with tag dependencies."""
        levels = sort_items_by_dependencies(sample_addresses_with_dependencies, "address")

        assert len(levels) == 2
        # tag-1 should be in level 0
        assert any(item["name"] == "tag-1" for item in levels[0])
        # addresses should be in level 1
        level1_names = {item["name"] for item in levels[1]}
        assert level1_names == {"addr-1", "addr-2"}

    def test_with_group_dependencies(self, sample_address_groups_with_dependencies):
        """Test sorting items with group dependencies."""
        levels = sort_items_by_dependencies(
            sample_address_groups_with_dependencies, "address_group"
        )

        assert len(levels) == 2
        # Addresses should be in level 0
        level0_names = {item["name"] for item in levels[0]}
        assert level0_names == {"addr-1", "addr-2"}
        # Group should be in level 1
        assert levels[1][0]["name"] == "group-1"

    def test_empty_items(self):
        """Test sorting empty item list."""
        levels = sort_items_by_dependencies([], "address")
        assert levels == []


class TestHasDependencies:
    """Tests for has_dependencies function."""

    def test_no_dependencies(self, sample_addresses):
        """Test detecting no dependencies."""
        result = has_dependencies(sample_addresses, "address")
        assert result is False

    def test_with_dependencies(self, sample_addresses_with_dependencies):
        """Test detecting dependencies."""
        result = has_dependencies(sample_addresses_with_dependencies, "address")
        assert result is True


class TestGetDependencySummary:
    """Tests for get_dependency_summary function."""

    def test_summary_no_dependencies(self, sample_addresses):
        """Test summary for items without dependencies."""
        summary = get_dependency_summary(sample_addresses, "address")

        assert summary["total_items"] == 3
        assert summary["has_dependencies"] is False
        assert summary["num_levels"] == 1
        assert summary["items_per_level"] == [3]
        assert summary["dependency_count"] == 0

    def test_summary_with_dependencies(self, sample_addresses_with_dependencies):
        """Test summary for items with dependencies."""
        summary = get_dependency_summary(sample_addresses_with_dependencies, "address")

        assert summary["total_items"] == 3
        assert summary["has_dependencies"] is True
        assert summary["num_levels"] == 2
        assert summary["items_per_level"] == [1, 2]  # 1 tag, 2 addresses
        assert summary["dependency_count"] == 2  # addr-1 and addr-2 depend on tag-1
