"""Dependency resolver for batch operations.

Detects cross-object references and performs topological sorting
to prevent "not a valid reference" errors during parallel creation.

Example:
    address_group references address objects -> addresses must be created first
    service_group references services -> services must be created first
"""

import logging
from collections import defaultdict, deque
from typing import Any

logger = logging.getLogger(__name__)

# Mapping of object types to their reference fields
# Format: {object_type: [(field_name, referenced_object_type), ...]}
REFERENCE_FIELDS = {
    "address": [
        ("tag", "tag"),  # Address objects can reference tags
    ],
    "address_group": [
        ("static_value", "address"),  # Static members reference addresses
        ("static_members", "address"),  # Alternate field name
        ("tag", "tag"),
    ],
    "service": [
        ("tag", "tag"),
    ],
    "service_group": [
        ("value", "service"),  # Members reference services
        ("members", "service"),  # Alternate field name
        ("tag", "tag"),
    ],
    "security_policy": [
        ("source", "address"),  # Source zones/addresses
        ("destination", "address"),  # Destination zones/addresses
        ("service", "service"),  # Services
        ("tag", "tag"),
    ],
    "nat_policy": [
        ("source", "address"),
        ("destination", "address"),
        ("service", "service"),
        ("tag", "tag"),
    ],
}


def extract_references(item: dict, object_type: str) -> set[str]:
    """Extract all object references from an item.

    Args:
        item: Object data dictionary
        object_type: Type of object (address, service, etc.)

    Returns:
        Set of referenced object names
    """
    references = set()

    if object_type not in REFERENCE_FIELDS:
        return references

    for field_name, ref_type in REFERENCE_FIELDS[object_type]:
        if field_name in item:
            value = item[field_name]

            # Handle both single values and lists
            if isinstance(value, list):
                references.update(value)
            elif isinstance(value, str):
                references.add(value)

    return references


def build_dependency_graph(
    items: list[dict], object_type: str
) -> tuple[dict[str, set[str]], dict[str, dict]]:
    """Build dependency graph from items.

    Args:
        items: List of objects to create
        object_type: Type of objects

    Returns:
        Tuple of (dependency_graph, item_lookup)
        - dependency_graph: {item_name: set(dependencies)}
        - item_lookup: {item_name: item_dict}
    """
    dependency_graph = defaultdict(set)
    item_lookup = {}

    # Build lookup and initialize graph
    for item in items:
        name = item.get("name")
        if not name:
            logger.warning(f"Item missing 'name' field: {item}")
            continue

        item_lookup[name] = item
        dependency_graph[name] = set()

    # Find dependencies
    for item in items:
        name = item.get("name")
        if not name:
            continue

        references = extract_references(item, object_type)

        # Check if references are in the batch (internal dependencies)
        for ref in references:
            if ref in item_lookup:
                # This item depends on 'ref'
                dependency_graph[name].add(ref)
                logger.debug(f"{name} depends on {ref}")

    return dict(dependency_graph), item_lookup


def topological_sort(dependency_graph: dict[str, set[str]]) -> list[list[str]]:
    """Perform topological sort to determine dependency levels.

    Args:
        dependency_graph: {item_name: set(dependencies)}

    Returns:
        List of levels, each level is a list of items that can be created in parallel
        [[level0_items], [level1_items], ...]

    Raises:
        ValueError: If circular dependency detected
    """
    # Calculate in-degree for each node
    in_degree = {node: 0 for node in dependency_graph}
    for node in dependency_graph:
        for dep in dependency_graph[node]:
            in_degree[dep] = in_degree.get(dep, 0)

    for node in dependency_graph:
        for dep in dependency_graph[node]:
            in_degree[node] += 1

    # Find nodes with no dependencies (level 0)
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    levels = []
    visited = set()

    while queue:
        # All items in queue have same depth - can be processed in parallel
        current_level = list(queue)
        levels.append(current_level)

        # Process current level
        next_queue = deque()
        for node in current_level:
            visited.add(node)

            # Find nodes that depend on current node
            for other_node in dependency_graph:
                if node in dependency_graph[other_node]:
                    in_degree[other_node] -= 1
                    if in_degree[other_node] == 0:
                        next_queue.append(other_node)

        queue = next_queue

    # Check for circular dependencies
    if len(visited) != len(dependency_graph):
        unvisited = set(dependency_graph.keys()) - visited
        raise ValueError(f"Circular dependency detected for items: {unvisited}")

    return levels


def sort_items_by_dependencies(items: list[dict], object_type: str) -> list[list[dict]]:
    """Sort items into dependency levels for batch processing.

    Args:
        items: List of objects to create
        object_type: Type of objects

    Returns:
        List of levels, where each level contains items that can be created in parallel
        Items in level N depend on items in levels 0..N-1

    Example:
        items = [
            {"name": "addr-1", "tag": ["tag-1"]},  # Depends on tag-1
            {"name": "tag-1", "color": "Red"},     # No dependencies
        ]
        result = [
            [{"name": "tag-1", ...}],              # Level 0
            [{"name": "addr-1", ...}],             # Level 1
        ]
    """
    if not items:
        return []

    # Build dependency graph
    dep_graph, item_lookup = build_dependency_graph(items, object_type)

    logger.info(f"Built dependency graph with {len(dep_graph)} nodes")
    for name, deps in dep_graph.items():
        if deps:
            logger.debug(f"  {name} -> {deps}")

    # Perform topological sort
    try:
        sorted_levels = topological_sort(dep_graph)
    except ValueError as e:
        logger.error(f"Dependency resolution failed: {e}")
        raise

    # Convert from names to item dicts
    result = []
    for level_names in sorted_levels:
        level_items = [item_lookup[name] for name in level_names]
        result.append(level_items)

    logger.info(f"Dependency levels: {[len(level) for level in result]}")
    return result


def has_dependencies(items: list[dict], object_type: str) -> bool:
    """Check if items have internal dependencies.

    Args:
        items: List of objects
        object_type: Type of objects

    Returns:
        True if dependencies exist, False otherwise
    """
    dep_graph, _ = build_dependency_graph(items, object_type)

    for deps in dep_graph.values():
        if deps:
            return True

    return False


def get_dependency_summary(items: list[dict], object_type: str) -> dict[str, Any]:
    """Get summary of dependencies for reporting.

    Args:
        items: List of objects
        object_type: Type of objects

    Returns:
        Summary dict with dependency info
    """
    dep_graph, _ = build_dependency_graph(items, object_type)
    levels = sort_items_by_dependencies(items, object_type)

    return {
        "total_items": len(items),
        "has_dependencies": has_dependencies(items, object_type),
        "num_levels": len(levels),
        "items_per_level": [len(level) for level in levels],
        "dependency_count": sum(len(deps) for deps in dep_graph.values()),
    }
