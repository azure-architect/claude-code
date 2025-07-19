#!/usr/bin/env python3
import json
import os
import re
import sys
from io import StringIO
from typing import List, Tuple

import yaml  # type: ignore


def validate_and_fix_yaml(file_path: str, content: str) -> Tuple[List[str], str]:
    """Validate YAML content and automatically fix common issues."""
    issues = []
    fixed_content = content

    # Check max file length
    if len(content.splitlines()) > 500:
        issues.append("File exceeds 500 lines maximum length")

    try:
        # Try to parse YAML
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        # Try to auto-fix common issues
        fixed_content = auto_fix_yaml_issues(content)

        # Try parsing again
        try:
            yaml.safe_load(fixed_content)
            issues.append(f"Auto-fixed YAML syntax issues: {str(e)}")
        except yaml.YAMLError as e2:
            issues.append(f"YAML syntax error that couldn't be auto-fixed: {str(e2)}")
            return issues, content  # Return original content if can't fix

    # Check for common YAML best practices
    lines = fixed_content.splitlines()

    for i, line in enumerate(lines, 1):
        # Check for trailing spaces
        if line.endswith(" ") or line.endswith("\t"):
            issues.append(f"Line {i}: Remove trailing whitespace")
            lines[i - 1] = line.rstrip()
            fixed_content = "\n".join(lines)

        # Check for tabs (should use spaces)
        if "\t" in line:
            issues.append(f"Line {i}: Use spaces instead of tabs for indentation")
            lines[i - 1] = line.expandtabs(2)
            fixed_content = "\n".join(lines)

        # Check for inconsistent indentation (basic check)
        if line.strip() and line.startswith(" "):
            indent = len(line) - len(line.lstrip())
            if indent % 2 != 0:
                issues.append(f"Line {i}: Use consistent 2-space indentation")

    # Check for security issues in YAML
    if "password:" in content.lower() and not content.lower().count("example"):
        issues.append("Avoid hardcoding passwords in YAML files")

    if "api_key:" in content.lower() and not content.lower().count("example"):
        issues.append("Avoid hardcoding API keys in YAML files")

    # Check for common Docker Compose issues
    if "version:" in content and "services:" in content:
        if not re.search(r'version:\s*["\']?3\.\d+["\']?', content):
            issues.append("Consider using Docker Compose version 3.x format")

    return issues, fixed_content


def auto_fix_yaml_issues(content: str) -> str:
    """Attempt to automatically fix common YAML issues."""
    lines = content.splitlines()
    fixed_lines = []

    for line in lines:
        # Fix trailing spaces
        line = line.rstrip()

        # Fix tabs to spaces
        line = line.expandtabs(2)

        # Fix common quote issues
        if ":" in line and not line.strip().startswith("#"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                key, value = parts
                value = value.strip()

                # Add quotes around values that need them
                if (
                    value
                    and not value.startswith(("'", '"', "[", "{", "|", ">"))
                    and not value.replace(".", "").replace("-", "").isdigit()
                ):
                    if " " in value or value in (
                        "true",
                        "false",
                        "null",
                        "yes",
                        "no",
                        "on",
                        "off",
                    ):
                        if not (
                            value.lower()
                            in ("true", "false", "null", "yes", "no", "on", "off")
                        ):
                            line = f'{key}: "{value}"'

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def validate_file(file_path: str, content: str) -> Tuple[List[str], str]:
    """Validate file content based on file type."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".yml", ".yaml"]:
        return validate_and_fix_yaml(file_path, content)

    return [], content


def write_fixed_content(
    file_path: str, original_content: str, fixed_content: str
) -> bool:
    """Write the fixed content back to the file if changes were made."""
    if original_content != fixed_content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            return True
        except IOError as e:
            print(
                f"Warning: Could not write fixed content to {file_path}: {e}",
                file=sys.stderr,
            )
            return False
    return False


try:
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # For Write tool
    if tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        issues, fixed_content = validate_file(file_path, content)

        # If we have fixes, update the content that will be written
        if content != fixed_content:
            # Update the tool input with fixed content
            tool_input["content"] = fixed_content
            # Update the input data
            input_data["tool_input"] = tool_input
            # Write the updated input back
            print(json.dumps(input_data))

        if issues:
            print("YAML validation issues (some may be auto-fixed):", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            # Don't block if we auto-fixed issues, just warn
            if any("couldn't be auto-fixed" in issue for issue in issues):
                sys.exit(2)  # Block only for unfixable issues

    # For Edit tool
    elif tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        new_content = tool_input.get("new_content", "")

        issues, fixed_content = validate_file(file_path, new_content)

        # If we have fixes, update the content
        if new_content != fixed_content:
            tool_input["new_content"] = fixed_content
            input_data["tool_input"] = tool_input
            print(json.dumps(input_data))

        if issues:
            print("YAML validation issues (some may be auto-fixed):", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            if any("couldn't be auto-fixed" in issue for issue in issues):
                sys.exit(2)  # Block only for unfixable issues

    # Exit normally if no blocking issues found
    sys.exit(0)

except Exception as e:
    print(f"YAML validator error: {str(e)}", file=sys.stderr)
    sys.exit(1)  # Non-blocking error
