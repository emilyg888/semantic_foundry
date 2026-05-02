from __future__ import annotations

import ast
from pathlib import Path

from semantic_foundry.config import FunctionLogic


class LogicCollector(ast.NodeVisitor):
    def __init__(self, module_path: str) -> None:
        self.module_path = module_path
        self.functions: list[FunctionLogic] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        assigned = sorted(collect_assigned_names(node))
        compared = sorted(collect_compared_names(node))
        called = sorted(collect_called_names(node))
        returned = sorted(collect_return_names(node))
        self.functions.append(
            FunctionLogic(
                module_path=self.module_path,
                function_name=node.name,
                assigned_names=assigned,
                compared_names=compared,
                called_names=called,
                return_names=returned,
            )
        )
        self.generic_visit(node)


def mine_python_logic(root: Path) -> list[FunctionLogic]:
    results: list[FunctionLogic] = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        collector = LogicCollector(str(path.relative_to(root)))
        collector.visit(tree)
        results.extend(collector.functions)
    return results


def collect_assigned_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                names.update(extract_target_names(target))
        elif isinstance(child, ast.AnnAssign):
            names.update(extract_target_names(child.target))
    return names


def extract_target_names(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.Tuple, ast.List)):
        names: set[str] = set()
        for element in node.elts:
            names.update(extract_target_names(element))
        return names
    return set()


def collect_compared_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Compare):
            names.update(extract_name_nodes(child.left))
            for comparator in child.comparators:
                names.update(extract_name_nodes(comparator))
    return names


def collect_called_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                names.add(child.func.id)
            elif isinstance(child.func, ast.Attribute):
                names.add(child.func.attr)
    return names


def collect_return_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Return) and child.value is not None:
            names.update(extract_name_nodes(child.value))
    return names


def extract_name_nodes(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
    return names
