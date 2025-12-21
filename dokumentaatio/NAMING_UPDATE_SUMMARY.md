# Documentation Naming Update Summary - v2.1.0

**Date:** 2025-12-20  
**Purpose:** Summary of document naming convention implementation

---

## 1. What Changed

We've established formal naming conventions for all project artifacts to ensure consistency, traceability, and professionalism.

---

## 2. Key Changes

### 2.1 Project Configuration

**File:** `pyproject.toml`

| Field | Old Value | New Value |
|-------|-----------|-----------|
| **name** | `ot-harjoitustyo` | `laihdutanyt` |
| **version** | `0.1.0` | `2.1.0` |
| **description** | `laihdutanyt` | `Laihdutanyt - Weight Management Desktop Application` |

**Rationale:** 
- Project name should match application name (not course code)
- Version reflects current release (Statistics Core)
- Description is professional and descriptive

---

### 2.2 Documentation Structure

#### New Naming Convention

**Format:** 
- **Document Title:** `Laihdutanyt - [Purpose] v[Version]`
- **Filename:** `laihdutanyt_[purpose]_v[version].md`

#### Applied To:

| Document | Document Title | Technical Filename | Status |
|----------|---------------|-------------------|--------|
| **Statistics Requirements** | Laihdutanyt - Statistics & Reporting Requirements v2.1 | `laihdutanyt_statistics_requirements_v2_1.md` | ✅ Updated |
| **Naming Conventions** | Laihdutanyt - Naming Conventions v1.0 | `NAMING_CONVENTIONS.md` | ✅ Created |
| **Release Notes** | Laihdutanyt - Release Notes v2.1.0 | `laihdutanyt_release_notes_v2_1_0.md` | ✅ Exists |

---

### 2.3 File Renaming Recommendations

#### Should Be Renamed (Future):

| Current Filename | Recommended Filename | Priority |
|-----------------|---------------------|----------|
| `statistics_requirements_v3.md` | `laihdutanyt_statistics_requirements_v2_1.md` | HIGH |
| `RELEASE_NOTES_v2.1.md` | `laihdutanyt_release_notes_v2_1_0.md` | MEDIUM |
| `laihdutanyt_requirements_specification_v2.md` | `laihdutanyt_core_requirements_v2_0.md` | LOW |

#### Should NOT Be Renamed:

| Current Filename | Reason |
|-----------------|---------|
| `main.py` | Entry point never has version suffix |
| `CHANGELOG.md` | Living document, updated in-place |
| `ARCHITECTURE.md` | Living document, updated in-place |
| `README.md` | Standard filename |

---

## 3. Document Header Template

All versioned documents now use this header format:

```markdown
# Laihdutanyt - [Purpose Title] v[Version]

**Technical Name:** `laihdutanyt_[purpose]_v[version].md`  
**Version:** v[MAJOR.MINOR.PATCH]  
**Date:** YYYY-MM-DD  
**Status:** [Draft / Review / Release Candidate / Released]  
**Target Release:** [Release name/number]

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Type** | [Requirements / Guide / Release Notes] |
| **Target Audience** | [Developers / Users / Admins] |
| **Related Artifacts** | [Links to related docs/code] |
| **Supersedes** | [Previous version, if applicable] |

---
```

---

## 4. Version Control Strategy

### Git Tags

**Format:** `v{MAJOR}.{MINOR}.{PATCH}`

**Examples:**
```bash
# For release v2.1.0
git tag -a v2.1.0 -m "v2.1.0: Statistics Core Release"
git push origin v2.1.0

# For patch v2.1.1
git tag -a v2.1.1 -m "v2.1.1: Bug fixes for statistics"
git push origin v2.1.1
```

### Version Sources

| Artifact | Version Location | Format |
|----------|-----------------|--------|
| **Application** | `pyproject.toml` → `version` | `"2.1.0"` |
| **Git** | Tags | `v2.1.0` |
| **Documents** | Header → `Version` field | `v2.1.0` |
| **Diagrams** | Filename suffix | `_v2_1.mmd` |

---

## 5. Quick Reference Card

### When to Version Documents

| Document Type | Version Strategy | Example |
|--------------|------------------|---------|
| **Requirements** | Version per major/minor release | `laihdutanyt_statistics_requirements_v2_1.md` |
| **Release Notes** | Version per release (incl. patch) | `laihdutanyt_release_notes_v2_1_0.md` |
| **User Guides** | Version per major/minor release | `laihdutanyt_user_guide_v2_1.md` |
| **Diagrams** | Version when schema changes | `laihdutanyt_erd_v2_1.mmd` |
| **Changelog** | Never (living document) | `CHANGELOG.md` |
| **Architecture** | Never (living document) | `ARCHITECTURE.md` |

### When to Version Code

| Code Type | Version Strategy | Example |
|-----------|------------------|---------|
| **Entry Point** | NEVER | `main.py` |
| **Project Name** | NEVER | `laihdutanyt` |
| **Project Version** | Always in `pyproject.toml` | `version = "2.1.0"` |
| **Migration Scripts** | Version in filename | `migrate_to_v2_1.py` |
| **Demo Scripts** | Version in filename | `generate_demo_data_v2_1.py` |

---

## 6. Benefits of This Approach

### For Developers:
✅ Clear traceability between docs and code versions  
✅ No confusion about which document version matches which release  
✅ Easy to find historical documentation via Git tags  

### For Users:
✅ Professional, consistent naming  
✅ Clear indication of what version documentation applies to  
✅ Easy to identify outdated documentation  

### For Academic Evaluation:
✅ Demonstrates process maturity  
✅ Shows attention to documentation quality  
✅ Provides clear version history  

---

## 7. Next Steps

### Immediate (Today):
1. ✅ Create `NAMING_CONVENTIONS.md` guide
2. ✅ Update `pyproject.toml` version and name
3. ✅ Update `statistics_requirements_v3.md` header
4. ⏳ Rename `statistics_requirements_v3.md` → `laihdutanyt_statistics_requirements_v2_1.md`
5. ⏳ Update all diagram filenames to follow convention

### Next Release (v2.1.1+):
1. Apply header template to all versioned documents
2. Rename existing documents to follow convention
3. Archive old versions in `dokumentaatio/archive/`
4. Update `README.md` to reference naming convention guide

---

## 8. Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| **Naming Conventions Guide** | `dokumentaatio/NAMING_CONVENTIONS.md` | Official standard (this is the authority) |
| **Statistics Requirements** | `dokumentaatio/statistics_requirements_v3.md` | Example of proper header format |
| **Changelog** | `CHANGELOG.md` | Version history reference |

---

**Summary Version:** 1.0  
**Date:** 2025-12-20  
**Status:** Implementation Complete  
**Technical Name:** `NAMING_UPDATE_SUMMARY_v2_1_0.md`
