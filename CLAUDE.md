# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code integration template that provides advanced hooks, context engineering, and a structured development pipeline. It's designed to enhance AI-assisted development through systematic context preservation and quality enforcement.

## Development Commands

### Core Commands
- `black <files>` - Code formatting
- `pytest <path>` - Run tests
- `mypy <files>` - Type checking
- `pylint <files>` - Code linting
- `isort <files>` - Import sorting
- `git <commands>` - Version control operations

### Available Slash Commands
- `/implement <task>` - Structured implementation following template patterns
- `/test <component>` - Generate comprehensive tests with fixtures and edge cases
- `/document <component>` - Create documentation with examples and usage
- `/generate-co <requirements>` - Generate Change Order from requirements
- `/execute-co <co-file>` - Implement approved Change Order
- `/restore-context` - Recover context after session interruption

## Architecture

### Hook System
- **PreToolUse**: Validates files before changes (type annotations, security, file length <500 lines)
- **PostToolUse**: Formats code automatically with black/isort after changes
- **Stop**: Captures session state, extracts artifacts, generates summaries

### Pipeline Structure
Development follows a 5-stage pipeline:
1. **1-planned/**: Generated Change Orders awaiting approval
2. **2-in-progress/**: Approved COs being implemented  
3. **3-testing/**: Implemented COs undergoing testing
4. **4-documented/**: Completed COs with documentation
5. **5-archived/**: Fully completed COs

### Change Orders (COs)
Self-contained context capsules that include:
- Complete requirements and implementation plans
- Project context and dependency mapping
- Decision history and rationale
- Validation criteria and test requirements

## Code Quality Standards

### Required Patterns
- All functions must have type annotations
- Docstrings required for public functions
- Security patterns enforced (no os.system, require SSL for SMTP)
- Files limited to 500 lines maximum
- Comprehensive error handling

### Testing Requirements
- Use pytest with fixtures
- Aim for 90%+ test coverage
- Include edge cases and error conditions
- Add integration tests for complex systems
- Test TTL expiration, timeouts, and failure scenarios

### Security Enforcement
- No insecure subprocess calls (use subprocess.run with check=True)
- SSL required for email/network operations
- Input validation for all user data
- Proper secret handling (no hardcoded credentials)

## Context Engineering Approach

This project treats context as deliberately engineered infrastructure:

### Context Preservation
- Session transcripts automatically saved to `.claude/logs/transcripts/`
- Code artifacts extracted to `.claude/logs/artifacts/`
- Session summaries generated on stop
- Pipeline state maintains task information

### Context Resilience
- Change Orders designed as context capsules
- `/restore-context` command for recovery after interruption
- Comprehensive project state tracking
- Decision history preservation

## Development Workflow

### 1. Planning Phase
Use `/implement` or `/generate-co` to create structured plans with:
- Requirements analysis
- Architecture design
- Implementation roadmap
- Validation criteria

### 2. Implementation Phase  
Follow template patterns:
- Type-annotated interfaces
- Comprehensive error handling
- Security-first design
- Modular architecture (separate concerns)

### 3. Testing Phase
Use `/test` to generate:
- Unit tests for all methods
- Integration tests for systems
- Edge case coverage
- Performance/load tests where applicable

### 4. Documentation Phase
Use `/document` to create:
- API documentation with examples
- Configuration guides
- Troubleshooting information
- Usage patterns

## File Organization

### Key Directories
- `.claude/hooks/` - Python validation and formatting scripts
- `.claude/commands/` - Reusable command templates  
- `.claude/logs/` - Session artifacts (gitignored)
- `pipeline/` - 5-stage development workflow
- `templates/` - Template files for COs and artifacts

### Environment
- `PYTHONPATH` includes `src/` directory
- Python hooks have access to project structure
- Additional directory permissions for `./docs/tasks/`

## Best Practices

### Code Implementation
- Start with interface design using abstract base classes
- Implement async-first patterns for I/O operations
- Use dependency injection for testability
- Follow existing codebase patterns and conventions

### Quality Assurance
- Let hooks guide code quality automatically
- Run type checking and linting before commits
- Maintain test coverage above 90%
- Document complex business logic

### Context Management
- Provide relevant context in requests
- Break large features into smaller, manageable tasks
- Reference existing patterns when implementing similar functionality
- Use the pipeline to track progress and maintain state

## Integration Notes

This template works with projects in any language - it's not Python-specific. The hooks and validation can be adapted for different technology stacks while maintaining the same context engineering principles.