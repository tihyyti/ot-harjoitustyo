# Laihdutanyt - Document and Code Naming Conventions v2.1

## 1. Purpose

This document establishes consistent naming conventions for all project artifacts to ensure clarity, traceability, and professionalism.

---

## 2. Version Numbering Scheme

**Semantic Versioning:** `MAJOR.MINOR.PATCH`

- **MAJOR** (e.g., v2): Breaking changes, major rewrites
- **MINOR** (e.g., v2.1): New features, backward-compatible
- **PATCH** (e.g., v2.1.1): Bug fixes, minor updates

**Current Version:** `v2.1.0` (Statistics Core Release)

---

## 3. Naming Conventions by Artifact Type

### 3.1 Application Code

| Artifact Type | Naming Format | Example |
|--------------|---------------|---------|
| **Main Entry Point** | `main.py` (never versioned) | `src/main.py` |
| **Project Name** | `laihdutanyt` (lowercase, no version) | In `pyproject.toml` |
| **Version Field** | Semantic version string | `version = "2.1.0"` |
| **Git Tags** | `v{MAJOR}.{MINOR}.{PATCH}` | `v2.1.0` |

**Rationale:** Main application files remain stable. Versioning handled via Git tags and `pyproject.toml`.

---

### 3.2 Migration Scripts

| Artifact Type | Naming Format | Example |
|--------------|---------------|---------|
| **Database Migration** | `migrate_to_v{MAJOR}_{MINOR}.py` | `migrate_to_v2_1.py` |
| **Data Import Script** | `import_{entity}_{purpose}.py` | `import_foods_from_csv.py` |
| **Demo Data Generator** | `generate_demo_data_v{MAJOR}_{MINOR}.py` | `generate_demo_data_v2_1.py` |

**Rationale:** Scripts are version-specific and should indicate which version they target.

---

### 3.3 Documentation Files

#### 3.3.1 User-Facing Documents (Formal Names)

**Format:** `Laihdutanyt - [Purpose] v[Version]`

| Document Type | Document Name | Technical Filename |
|--------------|---------------|-------------------|
| **Requirements** | Laihdutanyt - Statistics Requirements v2.1 | `laihdutanyt_statistics_requirements_v2_1.md` |
| **Release Notes** | Laihdutanyt - Release Notes v2.1.0 | `laihdutanyt_release_notes_v2_1_0.md` |
| **User Instructions** | Laihdutanyt - User Guide v2.1 | `laihdutanyt_user_guide_v2_1.md` |
| **Installation Guide** | Laihdutanyt - Ubuntu Installation v2.1 | `laihdutanyt_ubuntu_installation_v2_1.md` |

**Header Format in Document:**
```markdown
# Laihdutanyt - [Purpose] v[Version]

**Technical Name:** `laihdutanyt_[purpose]_v[version]`  
**Version:** v2.1.0  
**Date:** 2025-12-20  
**Status:** Release Candidate
```

---

#### 3.3.2 Technical Documents (No Formal Name Needed)

**Format:** `[PURPOSE]_[SCOPE].md` (UPPERCASE, no version)

| Document Type | Filename | Version Strategy |
|--------------|----------|------------------|
| **Architecture** | `ARCHITECTURE.md` | Updated in-place, changelog at bottom |
| **Changelog** | `CHANGELOG.md` | Keep a Changelog format, all versions |
| **Quick Start** | `QUICK_START.md` | Updated for current version |
| **Implementation Status** | `IMPLEMENTATION_STATUS.md` | Reflects current work |
| **Poetry/Invoke Guide** | `POETRY_INVOKE_GUIDE.md` | Updated in-place |

**Rationale:** Living documents that evolve with the project. Historical versions tracked via Git.

---

#### 3.3.3 Diagrams

**Format:** `laihdutanyt_[diagram_type]_v[version].[extension]`

| Diagram Type | Example Filename |
|-------------|------------------|
| **ERD (Entity-Relationship)** | `laihdutanyt_erd_v2_1.mmd` |
| **Class Diagram** | `laihdutanyt_classes_v2_1.drawio` |
| **Sequence Diagram** | `laihdutanyt_sequence_uc1_v2_1.mmd` |
| **Architecture Diagram** | `laihdutanyt_architecture_v2_1.drawio` |

**Rationale:** Diagrams are version-specific and should be archived for historical reference.

---

### 3.4 Test Files

| Artifact Type | Naming Format | Example |
|--------------|---------------|---------|
| **Unit Tests** | `test_{module}.py` | `test_user_service.py` |
| **Integration Tests** | `test_integration_{feature}.py` | `test_integration_statistics.py` |
| **Test Configuration** | `conftest.py` | `tests/conftest.py` |

**Rationale:** Follow pytest conventions. No versioning needed (tests evolve with code).

---

## 4. Practical Examples

### Example 1: New Feature Release (v2.1.0)

**Documents Created:**
1. `dokumentaatio/laihdutanyt_statistics_requirements_v2_1.md`
   - Header: "Laihdutanyt - Statistics Requirements v2.1"
2. `dokumentaatio/laihdutanyt_release_notes_v2_1_0.md`
   - Header: "Laihdutanyt - Release Notes v2.1.0"
3. `dokumentaatio/laihdutanyt_erd_v2_1.mmd`
   - Title: "Laihdutanyt ERD v2.1"

**Code Changes:**
1. `pyproject.toml`: `version = "2.1.0"`
2. `src/main.py`: Unchanged (no version in filename)
3. `src/migrations/migrate_to_v2_1.py`: Version in filename

**Git Actions:**
```bash
git add .
git commit -m "Release v2.1.0: Statistics Core Features"
git tag -a v2.1.0 -m "v2.1.0: Statistics Core Release"
git push origin v2.1.0
```

---

### Example 2: Bug Fix Release (v2.1.1)

**Documents Updated:**
1. `CHANGELOG.md`: Add new section `## [2.1.1] - 2025-12-21`
2. `dokumentaatio/laihdutanyt_release_notes_v2_1_1.md`: New file for patch notes

**Code Changes:**
1. `pyproject.toml`: `version = "2.1.1"`
2. Fix bug in `src/services/statistics_service.py`

**Git Actions:**
```bash
git tag -a v2.1.1 -m "v2.1.1: Bug fix for statistics calculation"
git push origin v2.1.1
```

---

### Example 3: Documentation Update (No Version Change)

**Documents Updated:**
1. `QUICK_START.md`: Add troubleshooting section
2. `ARCHITECTURE.md`: Update service layer diagram

**Code Changes:**
- None

**Git Actions:**
```bash
git commit -m "docs: Update quick start and architecture"
# No tag needed (documentation-only change)
```

---

## 5. File Naming Quick Reference

### DO ✅

| Scenario | Correct Naming |
|----------|----------------|
| Main app entry point | `main.py` |
| Project name | `laihdutanyt` (in pyproject.toml) |
| Release tag | `v2.1.0` |
| Requirements doc | `laihdutanyt_statistics_requirements_v2_1.md` |
| Migration script | `migrate_to_v2_1.py` |
| Diagram | `laihdutanyt_erd_v2_1.mmd` |

### DON'T ❌

| Scenario | Incorrect Naming | Why Wrong |
|----------|-----------------|-----------|
| Main app file | `laihdutanyt_v2_1.py` | Entry points should never have version suffixes |
| Project name | `laihdutanyt-v2.1` | Versions go in `version` field, not project name |
| Release tag | `release_2.1.0` | Use `v` prefix for version tags |
| Requirements doc | `statistics_requirements.md` | Missing version identifier |
| Test file | `test_user_service_v2.py` | Tests evolve with code, no version |

---

## 6. Header Template for Versioned Documents

```markdown
# Laihdutanyt - [Purpose Title] v[Version]

**Technical Name:** `laihdutanyt_[purpose]_v[version].[ext]`  
**Version:** v[MAJOR.MINOR.PATCH]  
**Date:** YYYY-MM-DD  
**Status:** [Draft / Review / Release Candidate / Released]  
**Supersedes:** [Previous version, if applicable]

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Type** | [Requirements / Guide / Release Notes] |
| **Target Audience** | [Developers / Users / Admins] |
| **Related Artifacts** | [Links to related docs/code] |
| **Change History** | See section [Change Log] |

---

[Main content...]
```

---

## 7. Version Transition Checklist

When releasing a new version:

- [ ] Update `pyproject.toml` version field
- [ ] Create release notes: `laihdutanyt_release_notes_v{version}.md`
- [ ] Update `CHANGELOG.md` with new version section
- [ ] Update diagrams with new version suffix (if schema changed)
- [ ] Create migration scripts with version suffix (if DB changed)
- [ ] Update `README.md` with new version number
- [ ] Create Git tag: `git tag -a v{version} -m "Release message"`
- [ ] Archive old versioned docs in `dokumentaatio/archive/` (optional)

---

## 8. Summary

**Key Principles:**
1. **Main application files**: No version suffixes (use Git tags)
2. **Documentation**: Clear version identifiers in both title and filename
3. **Scripts**: Version suffixes for migration/generation scripts
4. **Diagrams**: Version suffixes for architectural artifacts
5. **Living docs**: Updated in-place (architecture, guides, changelog)

**Version Authority:**
- **Single source of truth**: `pyproject.toml` `version` field
- **Human-readable**: Git tags (`v2.1.0`)
- **Traceability**: CHANGELOG.md records all changes

---

**Document Version:** 1.0  
**Date:** 2025-12-20  
**Status:** Official Standard  
**Technical Name:** `laihdutanyt_naming_conventions_v1_0.md`
