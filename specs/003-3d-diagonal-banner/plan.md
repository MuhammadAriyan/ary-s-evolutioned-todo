# Implementation Plan: 3D Diagonal ASCII Banner

**Branch**: `003-3d-diagonal-banner` | **Date**: 2025-12-31 | **Spec**: `specs/003-3d-diagonal-banner/spec.md`
**Input**: Feature specification from spec.md + research findings

## Summary

Replace the current static ASCII banner with a dynamic 3D diagonal ASCII banner using the `art` Python library. The banner will display "Ary's Evolved Todo" using the `3d_diagonal` font, providing a visually appealing 3D diagonal effect.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `art>=5.0.0` (pure Python, no external dependencies)
**Storage**: N/A (no persistent data required)
**Testing**: Manual verification, can add unit tests if needed
**Target Platform**: Linux/macOS/Windows terminals
**Project Type**: Single CLI project
**Performance Goals**: Banner generation < 100ms
**Constraints**: Must handle unsupported characters gracefully
**Scale/Scope**: Single feature change, minimal impact

## Constitution Check

*PASSED* - This feature:
- Uses only Python standard library + one new pure-Python dependency
- Makes a smallest viable change (one function modification)
- No security, persistence, or concurrency concerns
- Reversible by reverting dependency and code changes

## Project Structure

### Documentation (this feature)

```text
specs/003-3d-diagonal-banner/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # To be created by /sp.tasks
```

### Source Code (repository root)

```text
src/
├── main.py              # Contains greet() function - only file to modify
└── todo.py              # Unchanged

tests/
└── (no new tests required for this simple change)
```

**Structure Decision**: Single file modification in `src/main.py`. No new files needed.

## Research Findings

### Library: ART (Python)

- **Library ID**: `/sepandhaghighi/art`
- **Installation**: `pip install art`
- **Font**: `3d_diagonal` - provides the 3D diagonal ASCII effect
- **Alternative fonts**: `3d`, `3-d` for standard 3D effect
- **Functions**: `text2art(text, font="3d_diagonal")` - returns ASCII art string
- **Key features**:
  - 677 ASCII fonts available
  - Pure Python, no external dependencies
  - Handles unsupported characters with `chr_ignore=True`
  - High source reputation (92.1/100 benchmark score)

### Usage Example

```python
from art import text2art

# Generate 3D diagonal banner
banner = text2art("Ary's Evolved Todo", font="3d_diagonal")
print(banner)
```

## Implementation Approach

### Phase 1: Dependency Setup

1. Add `art>=5.0.0` to `pyproject.toml` dependencies

### Phase 2: Code Changes

1. Import `text2art` from `art` library in `main.py`
2. Modify `greet()` function to use `text2art()` instead of static banner
3. Set `chr_ignore=True` to handle unsupported characters gracefully

### Phase 3: Verification

1. Run the application and verify banner displays correctly
2. Ensure all existing functionality still works

## Complexity Tracking

*No constitution violations - feature is simple and follows all guidelines.*

## Files to Modify

| File | Change |
|------|--------|
| `pyproject.toml` | Add `art>=5.0.0` to dependencies |
| `src/main.py` | Import `text2art`, modify `greet()` function |

## Dependencies

- **New**: `art>=5.0.0` - for 3D diagonal ASCII banner generation
- **Existing**: None (removes need for inline banner strings)
