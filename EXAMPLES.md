# Agile V Examples

Real-world examples demonstrating Agile V framework in action. Each example shows what typically goes wrong with unguided AI agents and how Agile V prevents these failures.

---

## Example 1: Missing Traceability

**User Request:** "Add a login feature"

### ❌ What Typical AI Agents Do (No Traceability)

```python
# app/auth.py
def login(username, password):
    """User login handler."""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')
```

**Problems:**
- Code appears without any requirements document
- No linkage to user stories or acceptance criteria
- Impossible to trace back to business need
- Cannot verify if it meets actual requirements
- No evidence for compliance audits

### ✅ What Agile V Agents Do (Proper Traceability)

**Agent Output:**
```
⚠️ HALT CONDITION: No requirement specification found for "login feature"

Before implementing, I need to invoke the Requirement Architect to:
1. Decompose "login feature" into formal requirements
2. Define acceptance criteria
3. Identify security and compliance constraints
4. Establish traceability baseline

Invoking: requirement-architect
```

**Requirement Architect Output:**
```yaml
# .agile-v/REQUIREMENTS.md

REQ-0001:
  description: System shall authenticate users via username/password
  rationale: Enable secure access to protected resources
  acceptance_criteria:
    - Valid credentials grant access
    - Invalid credentials return error message
    - Failed attempts are logged
  priority: MUST
  compliance: ISO 27001 (Access Control), GxP (Audit Trail)
  linked_to: USER-STORY-001

REQ-0002:
  description: System shall enforce password complexity rules
  rationale: Prevent weak password attacks
  acceptance_criteria:
    - Minimum 8 characters
    - Contains uppercase, lowercase, number, special char
    - Rejects common passwords
  priority: MUST
  compliance: ISO 27001 (A.9.4.3)
```

**Build Agent Output (with traceability):**
```python
# app/auth.py
# ART-0001: User authentication handler
# Implements: REQ-0001 (username/password authentication)
# Related: REQ-0002 (password complexity enforced at registration)

def login(username, password):
    """
    Authenticate user via username/password.
    
    Traceability: REQ-0001
    Security: ISO 27001 A.9.4.1 (Access Control)
    """
    # REQ-0001: Validate credentials
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # REQ-0001: Grant access on valid credentials
        session['user_id'] = user.id
        audit_log.info(f"LOGIN_SUCCESS: user={username}")
        return redirect('/dashboard')
    
    # REQ-0001: Log failed attempts
    audit_log.warning(f"LOGIN_FAILED: user={username}")
    return render_template('login.html', error='Invalid credentials')
```

**Evidence Summary:**
```
Scope: Implemented user authentication feature
Traceability: REQ-0001 ✓, REQ-0002 (referenced)
Artifacts: ART-0001 (auth.py:login) → REQ-0001
Compliance: ISO 27001 A.9.4.1 mapped
Next: Red Team Verifier to test security edge cases
```

---

## Example 2: Silent Assumptions (Hardware Constraints)

**User Request:** "Optimize the image processing pipeline"

### ❌ What Typical AI Agents Do (Assume Unlimited Resources)

```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def process_images(image_paths):
    """Process images in parallel."""
    # Assumes unlimited CPU cores and RAM
    with ProcessPoolExecutor(max_workers=mp.cpu_count() * 2) as executor:
        results = executor.map(process_single_image, image_paths)
    return list(results)

def process_single_image(path):
    # Loads entire 4K image into memory
    img = Image.open(path)  # Could be 50+ MB per image
    # Assumes GPU acceleration available
    img_tensor = torch.from_numpy(np.array(img)).cuda()
    return ml_model(img_tensor)
```

**Problems:**
- Assumes target system has multiple CPU cores
- Assumes sufficient RAM to load all images
- Assumes CUDA-capable GPU exists
- May crash on Raspberry Pi, embedded devices, or low-memory systems
- No validation of physical constraints

### ✅ What Agile V Agents Do (Hardware-Aware)

**Build Agent Output:**
```
⚠️ HALT CONDITION: Hardware constraints unknown

Before optimizing, I need clarification:
1. **Target Platform**: Where will this run?
   - Development workstation (16 cores, 64GB RAM, GPU)?
   - Production server (specs?)?
   - Embedded device (Raspberry Pi, Jetson Nano)?
   - Cloud (auto-scaling available)?

2. **Resource Constraints**:
   - Available RAM?
   - CPU cores?
   - GPU availability?
   - Storage I/O limits?

3. **Image Characteristics**:
   - Typical resolution (720p, 1080p, 4K)?
   - Batch size (10, 100, 1000+ images)?
   - Real-time processing required?

Without this information, I cannot design a valid optimization.
Invoking: discovery-analyst to gather hardware requirements
```

**After Hardware Discovery:**
```yaml
# .agile-v/REQUIREMENTS.md

REQ-0010:
  description: Image processing shall run on Raspberry Pi 4 (4GB RAM)
  rationale: Target deployment is edge device
  constraints:
    cpu_cores: 4
    ram_mb: 4096
    gpu: false
    storage_io: SD card (limited)
  acceptance_criteria:
    - Processes images without OOM errors
    - Uses ≤2GB RAM during peak load
    - Completes batch of 100 images in <5 minutes
```

**Build Agent Output (Hardware-Aware Implementation):**
```python
# image_processor.py
# ART-0010: Hardware-constrained image processing pipeline
# Implements: REQ-0010 (Raspberry Pi 4 deployment)

import os
from PIL import Image

# REQ-0010: Limit workers to available cores (4 on RPi4)
MAX_WORKERS = min(4, os.cpu_count() or 1)
# REQ-0010: Limit RAM usage - process one image at a time
CHUNK_SIZE = 1

def process_images(image_paths):
    """
    Process images with hardware constraints.
    
    Traceability: REQ-0010 (RPi4: 4 cores, 4GB RAM, no GPU)
    Memory: Streams images to avoid OOM on 4GB system
    """
    results = []
    
    # REQ-0010: Sequential processing to stay within 2GB RAM limit
    for path in image_paths:
        try:
            result = process_single_image(path)
            results.append(result)
        except MemoryError:
            # REQ-0010: Graceful degradation on low memory
            result = process_single_image_low_memory(path)
            results.append(result)
    
    return results

def process_single_image(path):
    """Process single image with memory constraints."""
    # REQ-0010: Resize large images to fit in RAM
    img = Image.open(path)
    if img.width * img.height > 1920 * 1080:
        img.thumbnail((1920, 1080))
    
    # REQ-0010: CPU-only processing (no GPU on RPi4)
    return cpu_based_processing(img)
```

**Decision Log:**
```
TIMESTAMP: 2026-05-26T10:30:00Z
AGENT_ID: build-agent-python
DECISION: Use sequential processing instead of parallel
RATIONALE: Target hardware (RPi4) has only 4GB RAM. Parallel processing 
           of 4K images would cause OOM. Sequential processing with 
           thumbnail resizing stays within 2GB limit.
LINKED_REQ: REQ-0010
ALTERNATIVE_CONSIDERED: ProcessPoolExecutor with 2 workers
ALTERNATIVE_REJECTED: Still risks OOM with high-res images
```

---

## Example 3: Build Agent Verifying Own Work (Violation of Red Team Protocol)

**User Request:** "Implement password validation and make sure it works"

### ❌ What Typical AI Agents Do (Self-Verification Bias)

```python
# auth/validators.py
def validate_password(password):
    """Validate password meets security requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a number"
    return True, "Password valid"

# Test written by the same agent
def test_validate_password():
    """Test password validation."""
    # Only tests what the implementation checks
    assert validate_password("Pass123")[0] == True  # Passes
    assert validate_password("short")[0] == False
    assert validate_password("nouppercase1")[0] == False
```

**Problems:**
- Agent tests only what it implemented (confirmation bias)
- Misses edge cases: special characters, length limits, common passwords
- Security vulnerabilities undetected (e.g., "Password123" passes but is weak)
- No independent verification

### ✅ What Agile V Agents Do (Red Team Protocol)

**Build Agent Output:**
```python
# auth/validators.py
# ART-0005: Password validation
# Implements: REQ-0002 (password complexity rules)

def validate_password(password):
    """
    Validate password meets security requirements.
    
    Traceability: REQ-0002
    Compliance: ISO 27001 A.9.4.3 (Password Management)
    """
    # REQ-0002: Minimum 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # REQ-0002: Contains uppercase
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    
    # REQ-0002: Contains lowercase
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    
    # REQ-0002: Contains number
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a number"
    
    # REQ-0002: Contains special character
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain special character"
    
    # REQ-0002: Reject common passwords
    common_passwords = ["Password123!", "Welcome123!", "Admin123!"]
    if password in common_passwords:
        return False, "Password is too common"
    
    return True, "Password valid"
```

**Evidence Summary:**
```
Scope: Implemented password validation (ART-0005)
Traceability: REQ-0002 ✓
Status: IMPLEMENTATION_COMPLETE
Next: Handing off to Red Team Verifier for independent security testing

⚠️ Build Agent does NOT verify own work per Directive #4
```

**Red Team Verifier Output (Independent Agent, Fresh Context):**
```python
# tests/security/test_password_security.py
# TC-0005: Password validation security tests
# Verifies: REQ-0002
# Agent: red-team-verifier (INDEPENDENT)

import pytest
from auth.validators import validate_password

class TestPasswordSecurity:
    """Red Team security tests for password validation."""
    
    def test_req_0002_basic_requirements(self):
        """TC-0005-01: Verify basic requirements (REQ-0002)."""
        valid, msg = validate_password("SecureP@ss123")
        assert valid, "Valid password should pass"
    
    def test_edge_case_max_length(self):
        """TC-0005-02: Edge case - extremely long password."""
        # ❌ FAILURE: Implementation doesn't enforce max length
        long_pwd = "A1b!" + "x" * 10000
        valid, msg = validate_password(long_pwd)
        assert not valid, "Should reject excessively long passwords (DoS risk)"
    
    def test_security_unicode_bypass(self):
        """TC-0005-03: Security - Unicode character bypass attempt."""
        # ❌ FAILURE: Unicode uppercase not detected
        valid, msg = validate_password("pαssw0rd!")  # α is Greek lowercase
        assert not valid, "Should reject passwords with Unicode tricks"
    
    def test_security_common_patterns(self):
        """TC-0005-04: Security - Common password patterns."""
        # ❌ FAILURE: Only checks 3 common passwords
        common = ["Password1!", "Qwerty123!", "Letmein1!"]
        for pwd in common:
            valid, msg = validate_password(pwd)
            assert not valid, f"Should reject common password: {pwd}"
    
    def test_security_empty_string(self):
        """TC-0005-05: Security - Empty string handling."""
        valid, msg = validate_password("")
        assert not valid, "Should reject empty password"
    
    def test_security_whitespace(self):
        """TC-0005-06: Security - Whitespace-only password."""
        valid, msg = validate_password("        ")
        assert not valid, "Should reject whitespace-only password"
```

**Red Team Validation Summary:**
```
Scope: Security testing of password validation (ART-0005)
Traceability: REQ-0002
Test Results: 6 test cases
  ✓ PASS: 2 tests (basic requirements)
  ❌ FAIL: 4 tests (max length, Unicode bypass, common patterns, whitespace)

FINDINGS:
- SECURITY-001: No maximum length validation (DoS risk)
- SECURITY-002: Unicode character bypass detected
- SECURITY-003: Common password list too short (only 3 entries)
- SECURITY-004: Whitespace-only passwords not rejected

RECOMMENDATION: Return to Build Agent for fixes
STATUS: FAILED_VERIFICATION

Evidence: Independent Red Team found issues Build Agent didn't self-detect
```

**Build Agent Response (after Red Team findings):**
```python
# auth/validators.py (v2)
# ART-0005: Password validation (updated after Red Team findings)
# Implements: REQ-0002 + SECURITY-001/002/003/004 fixes

import unicodedata

def validate_password(password):
    """
    Validate password with security hardening.
    
    Traceability: REQ-0002 + Red Team findings
    Fixes: SECURITY-001 (max length), SECURITY-002 (Unicode), 
           SECURITY-003 (common passwords), SECURITY-004 (whitespace)
    """
    # SECURITY-001: Enforce maximum length (prevent DoS)
    if len(password) > 128:
        return False, "Password must be 128 characters or less"
    
    # SECURITY-004: Reject empty or whitespace-only
    if not password or password.isspace():
        return False, "Password cannot be empty or whitespace"
    
    # SECURITY-002: Normalize Unicode to prevent bypass
    password = unicodedata.normalize('NFKC', password)
    
    # REQ-0002: Minimum 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # REQ-0002: Complexity checks (ASCII only after normalization)
    if not any(c.isupper() and c.isascii() for c in password):
        return False, "Password must contain ASCII uppercase letter"
    if not any(c.islower() and c.isascii() for c in password):
        return False, "Password must contain ASCII lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a number"
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain special character"
    
    # SECURITY-003: Expanded common password list
    # (In production: use external dictionary like pwned-passwords)
    common_passwords = load_common_passwords()  # 10,000+ entries
    if password.lower() in common_passwords:
        return False, "Password is too common"
    
    return True, "Password valid"
```

**Final Red Team Verification:**
```
Scope: Re-test password validation after fixes
Test Results: 6 test cases → ALL PASS ✓
Status: VERIFIED
```

---

## Example 4: Missing Human Gate (Unauthorized Deployment)

**User Request:** "Deploy the new API to production"

### ❌ What Typical AI Agents Do (Autonomous Deployment)

```bash
# Agent executes immediately
git push origin main
kubectl apply -f deployment.yaml
echo "✓ Deployed to production"
```

**Problems:**
- No human approval before production deployment
- No evidence summary of what's being deployed
- No verification that all tests passed
- Violates change management protocols
- Compliance failure (no approval trail)

### ✅ What Agile V Agents Do (Human Gate + Evidence Summary)

**Release Manager Output:**
```
⚠️ HUMAN GATE: Production deployment requires approval

=== EVIDENCE SUMMARY ===
Scope: Deploy API v2.1.0 to production

Traceability:
- REQ-0101 through REQ-0115 (15 requirements)
- CR-0010 (Change Request: Add rate limiting)

Artifacts:
- ART-0101 to ART-0118 (18 code artifacts)
- All artifacts linked to parent REQs ✓

Verification Status:
- Build Agent: Implementation complete ✓
- Test Designer: 47 test cases created (TC-0101 to TC-0147)
- Red Team Verifier: All tests PASS ✓
- Compliance Auditor: ISO 9001 design phase docs complete ✓

Test Results:
- Unit tests: 47/47 PASS
- Integration tests: 12/12 PASS
- Security tests: 8/8 PASS
- Performance tests: 3/3 PASS (latency <100ms)

Risk Assessment:
- RISK-003: Rate limiting may block legitimate high-frequency users
  Mitigation: Implement whitelist for known high-volume clients
  Status: MITIGATED ✓

Deployment Plan:
1. Deploy to staging environment
2. Run smoke tests
3. Blue-green deployment to production
4. Monitor for 1 hour
5. Rollback procedure ready

Approvals Required:
- [ ] Technical Lead (deployment authorization)
- [ ] Product Owner (feature acceptance)
- [ ] Compliance Officer (if regulated environment)

Decision Log: See DECISION_LOG.md entries #0089 to #0103

🛑 AWAITING HUMAN APPROVAL
Type 'APPROVE' to proceed or 'REJECT' with reason.
```

**After Human Approval:**
```
APPROVAL RECEIVED
Approver: tech-lead@company.com
Timestamp: 2026-05-26T15:30:00Z
Approval ID: APR-0042

Proceeding with deployment...
[deployment logs]

✓ Deployment complete
Evidence archived to: .agile-v/cycles/C3/phases/07-deployment/APPROVAL_APR-0042.md
```

---

## Example 5: Ambiguous Requirements (Proper Halt Behavior)

**User Request:** "Make the app faster"

### ❌ What Typical AI Agents Do (Silent Interpretation)

```python
# Agent assumes "faster" means "optimize database queries"
# and implements caching without asking

@lru_cache(maxsize=1000)
def get_user_data(user_id):
    return db.query(User).filter_by(id=user_id).first()

# ... 300 lines of optimization code
```

**Problems:**
- Assumes specific interpretation of "faster"
- May optimize the wrong thing (user meant UI responsiveness)
- Wastes time on wrong solution
- No verification of actual bottleneck

### ✅ What Agile V Agents Do (Halt on Ambiguity)

**Discovery Analyst Output:**
```
⚠️ HALT CONDITION: Ambiguous requirement "make the app faster"

Before proceeding, I need to decompose this request:

"Faster" could mean:

1. **Faster Response Time** (Backend Performance)
   - Current: API responses take 500ms average
   - Target: <200ms?
   - Approach: Database indexing, query optimization, caching
   - Estimated effort: Medium (2-3 days)

2. **Faster Perceived Speed** (Frontend UX)
   - Current: Users wait for full page load
   - Target: Progressive loading, skeleton screens?
   - Approach: UI optimization, lazy loading, optimistic updates
   - Estimated effort: High (5-7 days)

3. **Faster Time-to-First-Byte** (Infrastructure)
   - Current: Server response starts after 300ms
   - Target: <100ms?
   - Approach: CDN, edge caching, load balancing
   - Estimated effort: Medium-High (3-5 days)

4. **Faster Build/Deploy** (Developer Experience)
   - Current: CI/CD pipeline takes 15 minutes
   - Target: <5 minutes?
   - Approach: Optimize Docker builds, parallel testing
   - Estimated effort: Low-Medium (1-2 days)

QUESTIONS FOR CLARIFICATION:
1. What specific user experience are you trying to improve?
2. What does "faster" mean to the end user?
3. Have you identified a specific bottleneck?
4. Is there a target performance metric (e.g., "page load <2 seconds")?

🛑 HALTED: Awaiting clarification before creating requirements
```

**After Clarification:**
```
User Response: "Users complain the dashboard takes 5 seconds to load. 
                Need it under 2 seconds."

Discovery Analyst: Understood. Clarified requirement:
- Scope: Dashboard page load time
- Current: 5 seconds
- Target: <2 seconds
- User-facing metric: Time to interactive

Performing performance audit...
[analysis reveals: database N+1 query problem + large bundle size]

Invoking: requirement-architect to formalize performance requirements
```

**Requirement Architect Output:**
```yaml
REQ-0201:
  description: Dashboard page shall load in <2 seconds (90th percentile)
  rationale: User feedback indicates 5s load time causes frustration
  acceptance_criteria:
    - Time to Interactive <2s for 90% of page loads
    - First Contentful Paint <500ms
    - No blocking JavaScript >100KB
  current_state: 5s average load time
  root_causes:
    - N+1 database queries (15 queries per page load)
    - Bundle size 800KB (unminified)
  priority: HIGH
  linked_to: USER-COMPLAINT-089
```

**Now Build Agent can proceed with clear, traceable requirements.**

---

## How to Know Agile V Is Working

After using Agile V, you should see:

✅ **Traceability Everywhere**
- Every code file has `// REQ-XXXX` or `# Implements: REQ-XXXX` comments
- `.agile-v/REQUIREMENTS.md` exists with formal requirements
- `.agile-v/BUILD_MANIFEST.md` maps artifacts to requirements

✅ **Agents Halt on Ambiguity**
- Instead of assuming, agents ask clarifying questions
- "HALT CONDITION" messages appear when requirements are unclear
- Decision Log captures "Why" for every choice

✅ **Independent Verification**
- Build Agent implements, Red Team Verifier tests (separate agents)
- Red Team finds issues Build Agent didn't self-detect
- Evidence Summaries show both perspectives

✅ **Human Gates Present Evidence**
- Before deployments, you see comprehensive Evidence Summaries
- Approvals are logged with timestamp and approver ID
- No autonomous production deployments

✅ **Hardware Constraints Validated**
- Agents ask about target hardware before optimizing
- Implementations stay within physical resource limits
- No "works on my machine" problems

✅ **Compliance-Ready Artifacts**
- Decision Log is append-only audit trail
- Requirements map to compliance standards (ISO 9001, ISO 27001, GxP)
- Change Requests tracked in multi-cycle lifecycle

---

## Getting Started

**Quick Start:**
1. Install Agile V skills (see [Installation Guide](./README.md#installation))
2. Start a new project: Agent loads `agile-v-core` skill
3. Give a vague request (e.g., "add login") and watch agent halt for requirements
4. Work with Requirement Architect to formalize REQ-XXXX entries
5. Build Agent implements with traceability comments
6. Red Team Verifier finds edge cases
7. Review Evidence Summary before deployment

**For More Examples:**
- See [SKILL_ROUTING_GUIDE.md](./SKILL_ROUTING_GUIDE.md) for agent selection
- See individual skill directories for role-specific examples
- See [V1.5_RELEASE_NOTES.md](./V1.5_RELEASE_NOTES.md) for latest features

---

**License:** CC-BY-SA-4.0 | **Author:** Agile V™ | **Homepage:** https://github.com/Agile-V/agile_v_skills
