# Agile-V Skills - Quality Improvements Based on Test Results

**Version:** 2.1.0  
**Date:** May 25, 2026  
**Status:** Proposed Improvements

---

## Executive Summary

Based on comprehensive testing across multiple tasks, Agile-V Skills achieved **78% average success rate** (3rd place). Analysis of test failures reveals specific, fixable issues that could improve performance to **~90%** (projected 2nd place).

### Current Performance

| Metric | Score |
|--------|-------|
| **Overall Success Rate** | 78% (3rd/5) |
| **Task 13 (WebSocket - Hard)** | 68% (designed FOR this framework!) |
| **Task 14 (CSV - Simple)** | 87% |
| **Self-Test Accuracy Gap** | -32% (reported 100%, actual 68%) |

### Root Causes Identified

1. **Interface validation missing** - Didn't verify `connection.send()` was called
2. **Self-tests don't match real patterns** - Missed type conversions and delivery mechanisms
3. **Implementation rushed despite formal planning** - 36 min on complex concurrent task

---

## Critical Issue #1: Interface Validation Missing

### The Problem

**Task 13 (WebSocket Router):** This task was **designed specifically for Agile-V Skills** (hard concurrency requiring formal planning). Expected: 100%. Actual: **68%**.

**What Failed:**
```python
# What the implementation did (passed self-tests, failed hidden tests):
def publish(self, topic, message):
    for client_id in self._subscriptions.get(topic, []):
        self._message_queue[client_id].append(message)  # ❌ Stored but never sent

# What should have been done:
def publish(self, topic, message):
    for client_id in self._subscriptions.get(topic, []):
        connection = self._connections[client_id]
        connection.send(message)  # ✅ Actually deliver the message
```

**10 tests failed** because messages were queued internally but never delivered to connections.

### The Fix

Add **Interface Validation Checklist** to the Feature Brief template:

```markdown
## Interface Validation Checklist

Before implementation, verify:

- [ ] Review test harness interface (if provided in task description)
- [ ] Verify method signatures match expected API
- [ ] Check return types and data structures match examples
- [ ] Identify all external delivery mechanisms (e.g., send(), write(), publish())
- [ ] Ensure implementation actually calls delivery methods, not just queues internally
- [ ] Test with mock objects that match the test framework patterns

### Common Pitfalls

❌ **Don't:** Store messages in internal queues without delivery
✅ **Do:** Call the provided delivery method (connection.send(), etc.)

❌ **Don't:** Test only internal state (queue size, subscriptions)
✅ **Do:** Test end-to-end delivery (recipient receives message)

❌ **Don't:** Assume implementation is correct because logic is sound
✅ **Do:** Verify the interface is used as expected by consumers
```

**Expected Impact:** Task 13: 68% → 100% (+32%)

---

## Critical Issue #2: Self-Tests Don't Catch Real Issues

### The Problem

**Self-assessment vs Reality:**
- Agent reported: "All requirements met, 17/17 tests passing, ready for production"
- Hidden tests: **68%** (7 failures)
- Gap: **-32%**

**Why Self-Tests Failed:**
1. Tested internal state instead of external interface
2. Didn't match test harness patterns
3. Didn't verify actual message delivery
4. Didn't test with realistic data types (strings vs numbers)

### Task 13 Example

**Self-test that passed:**
```python
def test_publish():
    router.register_client("client1", mock_connection)
    router.subscribe("client1", "topic1")
    router.publish("topic1", Message("topic1", {"data": "test"}))
    
    # ❌ Only tested internal queue
    assert len(router._message_queue["client1"]) == 1
```

**Hidden test that failed:**
```python
def test_publish():
    connection = MockConnection()
    router.register_client("client1", connection)
    router.subscribe("client1", "topic1")
    router.publish("topic1", Message("topic1", {"data": "test"}))
    
    # ✅ Tested actual delivery
    assert len(connection.received_messages) == 1  # FAIL: got 0
```

### Task 14 Example (Type Conversion Bug)

**Self-test that passed:**
```python
def test_filter_greater_than():
    # Used numeric data directly
    transformer.add_filter("age", ">", 30)
    result = transformer.apply([{"age": 25}, {"age": 35}])
    assert len(result) == 1  # ✅ Passed
```

**Hidden test that failed:**
```python
def test_filter_greater_than():
    # Real CSV data is strings!
    csv_data = [{"age": "25"}, {"age": "35"}]  # ← strings from CSV
    transformer.add_filter("age", ">", "30")
    result = transformer.apply(csv_data)
    assert len(result) == 1  # ❌ FAIL: string comparison "35" > "30" incorrect
```

### The Fix

Add **Test-Driven Development Checklist** to Evidence Bundle requirements:

```markdown
## Test-Driven Development Checklist

### Test Quality Requirements

Your tests must:

- [ ] Test the external interface, not internal implementation details
- [ ] Use mock objects that match test harness patterns (if provided)
- [ ] Verify end-to-end workflows, not just intermediate state
- [ ] Test with realistic data types (strings from CSV, not clean numbers)
- [ ] Include negative tests (what should NOT happen)
- [ ] Test actual delivery/output mechanisms

### Red Flags

⚠️ **Warning signs your tests may not catch real issues:**

1. Tests only assert on internal attributes (`router._queue`, `self._data`)
2. Tests don't verify external side effects (messages sent, files written)
3. Tests use clean data types (numbers) instead of realistic ones (strings)
4. All tests pass but you haven't tested delivery mechanisms
5. Tests mock too much (mocking the thing you're supposed to test)

### Test Pattern Checklist

For each feature, ensure you have tests for:

- [ ] **Happy path** - Feature works as expected
- [ ] **Data types** - Works with actual input types (CSV = strings)
- [ ] **Edge cases** - Empty inputs, missing data, boundaries
- [ ] **Integration** - External interfaces actually called
- [ ] **Concurrency** - Thread-safe operations (if applicable)
- [ ] **Error handling** - Invalid inputs handled gracefully

### Before Claiming Completion

Run this self-check:

1. Do my tests verify what a consumer of this API would experience?
2. Do my tests use the same data types as real usage (CSV, JSON, etc.)?
3. Do my tests actually call external methods (send, write, etc.)?
4. Would my tests catch the bug if I didn't call the delivery method?
5. Would my tests catch the bug if I compared strings instead of numbers?

If any answer is "no", add tests for those cases.
```

**Expected Impact:** 
- Closes self-assessment gap (-32% → -5%)
- Catches interface bugs before submission
- Catches type conversion bugs

---

## Critical Issue #3: Type Handling for File-Based Data

### The Problem

**Task 14 (CSV Transformer):** 87% (failed 2/15 tests)

**What Failed:**
- HT-003: Filter Greater Than
- HT-013: Multiple Filters

**Root Cause:** CSV data is strings, numeric comparisons need type conversion

```python
# What happened:
age_string = "35"
threshold = "30"
if age_string > threshold:  # ❌ String comparison: "35" > "30" is False!
    # This is wrong! "35" < "4" in string comparison

# What should have happened:
age_string = "35"
threshold = "30"
if float(age_string) > float(threshold):  # ✅ Numeric comparison
    # Correct!
```

### The Fix

Add **Data Type Considerations** to Agent Plan template:

```markdown
## Data Type Considerations

When working with external data sources, identify type conversions needed:

### File-Based Data (CSV, JSON, etc.)

- [ ] CSV data is **always strings** (even numbers)
- [ ] JSON may have mixed types - check schema
- [ ] File inputs require explicit type conversion
- [ ] Comparison operators (>, <, >=, <=) need numeric conversion

### Type Conversion Checklist

For each data field:

1. **Identify source type:** What type is it when loaded?
2. **Identify target type:** What type do operations expect?
3. **Add conversion:** Convert at filter/comparison time
4. **Test with strings:** Verify operations work with string inputs

### Common Patterns

```python
# ❌ Wrong: Direct comparison of CSV data
def filter_gt(value, threshold):
    return value > threshold  # Fails for string "35" > "30"

# ✅ Right: Type conversion before comparison
def filter_gt(value, threshold):
    try:
        return float(value) > float(threshold)
    except ValueError:
        return str(value) > str(threshold)  # Fallback to string comparison
```

### Evidence Requirement

In your test plan, include:

- [ ] Test with string inputs (as from CSV)
- [ ] Test numeric operations on string data
- [ ] Verify type conversions are correct
- [ ] Test mixed-type scenarios
```

**Expected Impact:** Task 14: 87% → 100% (+13%)

---

## Issue #4: Time Allocation vs Complexity

### The Problem

**Task 13 (Hard Concurrency):** Took only **36 minutes**

This is a **hard concurrent task** requiring:
- Thread-safe operations
- Message delivery mechanisms
- Wildcard pattern matching
- Connection management

**36 minutes is insufficient** for this complexity, as proven by:
- Unstructured AI: 65 minutes → **100%**
- Agile-V Skills: 36 minutes → **68%**
- Correlation: More time = better quality on complex tasks (r=0.89)

### The Fix

Add **Time Allocation Guidance** to README and Agent Plan template:

```markdown
## Time Budget Guidelines

Use these minimums to avoid rushing complex implementations:

### L0 (Trivial) - Documentation, Comments
- **Minimum:** 15-20 minutes
- **Planning:** 5 min
- **Implementation:** 5-10 min
- **Testing:** 5 min

### L1 (Simple) - Basic Features, Single Module
- **Minimum:** 30-60 minutes
- **Planning:** 10 min
- **Implementation:** 15-30 min
- **Testing:** 10-15 min
- **Evidence:** 5 min

### L2 (Medium) - Multi-Module, Standard Features
- **Minimum:** 60-120 minutes
- **Planning:** 15-20 min
- **Implementation:** 30-60 min
- **Testing:** 20-30 min
- **Evidence:** 10 min

### L3 (Complex) - Concurrency, Security, Integration
- **Minimum:** 120-180 minutes
- **Planning:** 20-30 min
- **Implementation:** 60-90 min  ← **Task 13 needed this**
- **Testing:** 30-40 min
- **Evidence:** 10-20 min

### L4 (Critical) - Safety, Hardware, Compliance
- **Minimum:** 180+ minutes
- **Planning:** 30-60 min
- **Implementation:** 90-120 min
- **Testing:** 40-60 min
- **Evidence:** 20-30 min

### Complexity Multipliers

Add time for:
- **Concurrency:** +60 minutes (locking, thread safety, race conditions)
- **External Integration:** +30 minutes (API contracts, delivery mechanisms)
- **Security/Compliance:** +30 minutes (validation, audit trails)
- **Hardware/Firmware:** +60 minutes (timing, constraints, testing)

### Time Check Gate

Before starting implementation:

1. Calculate minimum time based on risk level + multipliers
2. Compare with available time
3. If rushed, either:
   - Simplify scope
   - Allocate more time
   - Escalate risk level

⚠️ **Warning:** Spending significantly less than minimum time is a red flag. Quality will likely suffer.

### Example: Task 13 Calculation

- Base (L3 Complex): 120 min
- Concurrency: +60 min
- External Integration (connections): +30 min
- **Total minimum: 210 minutes**

Actual time spent: 36 minutes ← **Only 17% of minimum!**

Result: 68% quality (missed interface validation)

**Lesson:** Don't rush complex tasks to hit time targets. Take the time needed for quality.
```

**Expected Impact:** 
- Prevents rushing complex implementations
- Improves quality on hard tasks
- Sets realistic expectations

---

## Issue #5: Feature Brief Template Updates

### Current Template Gaps

The current Feature Brief template doesn't guide agents to:
1. Identify external interfaces and delivery mechanisms
2. Consider data type conversions
3. Plan for realistic test scenarios

### Enhanced Feature Brief Template

Add these sections to `templates/feature_brief.md`:

```markdown
## Interface Contracts

### External Interfaces

Describe all external interfaces this feature will interact with:

- **APIs:** What methods will be called? What do they expect?
- **Delivery mechanisms:** How will data/messages be delivered? (send(), write(), etc.)
- **Data sources:** What format is input data? (CSV strings, JSON, etc.)
- **Consumers:** How will other code use this feature?

### Interface Validation

- [ ] Reviewed task description for interface examples
- [ ] Identified all delivery methods that must be called
- [ ] Verified method signatures match expected API
- [ ] Documented data type conversions needed

## Data Type Analysis

### Input Data Types

- **Source format:** (CSV, JSON, database, API, etc.)
- **Native types:** (strings from CSV, mixed types from JSON, etc.)
- **Required conversions:** (string → number for comparisons, etc.)

### Type Conversion Requirements

List any type conversions needed:

- Field `age`: string (from CSV) → float (for > comparison)
- Field `timestamp`: string → datetime (for date operations)
- etc.

## Test Scenarios

### Data Realism

Tests must use realistic data types:

- [ ] CSV tests use string data (not clean numbers)
- [ ] File I/O tests use actual file operations
- [ ] Concurrent tests use multiple threads
- [ ] Integration tests call external interfaces

### Interface Testing

Tests must verify external behavior:

- [ ] Test that delivery methods are actually called
- [ ] Test end-to-end workflows, not just internal state
- [ ] Test with mock objects matching test harness patterns
- [ ] Test that consumers would experience correct behavior
```

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Immediate)

**Priority:** P0 - Addresses 68% → 90%+ improvement

1. **Update Feature Brief Template**
   - Add Interface Validation Checklist
   - Add Data Type Analysis section
   - Add Test Scenarios guidance
   - File: `templates/feature_brief.md` (or skill template)

2. **Update Evidence Bundle Requirements**
   - Add Test-Driven Development Checklist
   - Add test quality requirements
   - Add self-check before completion
   - File: `schemas/evidence_bundle.schema.json` + docs

3. **Add Common Failure Patterns Document**
   - Create new doc with patterns from testing
   - Reference in README and skill guidance
   - File: `docs/COMMON_FAILURE_PATTERNS.md`

### Phase 2: Process Improvements (Follow-up)

**Priority:** P1 - Prevents future issues

1. **Update Agent Plan Template**
   - Add Data Type Considerations
   - Add Time Allocation Guidance
   - Add Interface Analysis section
   - File: `templates/agent_plan.md` (or skill template)

2. **Update README**
   - Add Time Budget Guidelines
   - Add Quality Best Practices section
   - Add link to Common Failure Patterns
   - File: `README.md`

3. **Create Validation Script**
   - Script to check for common patterns
   - Validate interface methods are called
   - Check test quality indicators
   - File: `scripts/validate_quality.py`

### Phase 3: Skill Updates (If applicable)

**Priority:** P2 - Depends on skill architecture

1. **Update Skill Prompts**
   - Add interface validation prompts
   - Add type conversion reminders
   - Add time allocation warnings

2. **Update Skill Validation**
   - Check tests verify external interfaces
   - Check tests use realistic data types
   - Check time spent vs complexity

---

## Expected Outcomes

### Performance Improvements

| Metric | Current | After Fixes | Improvement |
|--------|---------|-------------|-------------|
| **Overall Average** | 78% | ~90% | +12% |
| **Task 13 (Hard)** | 68% | ~95% | +27% |
| **Task 14 (Simple)** | 87% | 100% | +13% |
| **Self-Test Gap** | -32% | -5% | +27% |
| **Framework Rank** | 3rd/5 | 2nd/5 | +1 position |

### Quality Improvements

- ✅ Catches interface bugs before submission
- ✅ Catches type conversion bugs in testing
- ✅ Prevents rushing complex implementations
- ✅ Improves self-test accuracy
- ✅ Better time allocation decisions

### Competitive Position

**Current:**
1. Unstructured AI: 94.6%
2. Get Shit Done: 84%
2. Single Agent: 84%
4. **Agile-V Skills: 78%** ← Current
5. Agentic Agile-V: 68%

**After Improvements:**
1. Unstructured AI: 94.6%
2. **Agile-V Skills: ~90%** ← Projected
3. Get Shit Done: 84%
3. Single Agent: 84%
5. Agentic Agile-V: 68%

---

## Verification Plan

### How to Validate Improvements

1. **Re-run Task 13** with updated templates
   - Expected: 68% → 95%+
   - Key check: Does agent verify connection.send() is called?

2. **Re-run Task 14** with updated templates
   - Expected: 87% → 100%
   - Key check: Does agent test with string data?

3. **Monitor Time Allocation**
   - Check if agents allocate appropriate time
   - Verify quality improves with adequate time

4. **Self-Test Accuracy**
   - Compare self-reported quality with actual
   - Target: <10% gap (currently -32%)

---

## Lessons Learned

### What Worked Well

✅ **Formal planning** - Structure is valuable for complex tasks
✅ **Evidence bundles** - Good for documentation
✅ **Risk classification** - Useful framework

### What Needs Improvement

❌ **Interface validation** - Templates don't prompt for it
❌ **Test quality** - Self-tests don't match real patterns
❌ **Time allocation** - No guidance leads to rushing
❌ **Type awareness** - Don't consider data source types

### Core Insight

> **Formal process ≠ Quality**
> 
> Creating lots of artifacts (feature briefs, plans, evidence bundles) doesn't automatically catch bugs. The process must actively check for common failure patterns:
> - Interface delivery mechanisms
> - Type conversions
> - Test realism
> - Adequate time allocation

**The Fix:** Make checklists actionable and specific, not just generic reminders.

---

## Appendix: Test Results Reference

### Task 13: WebSocket Router (Hard - Designed for Agile-V Skills)

**Result:** 68% (15/22 tests passed)

**What Worked:**
- Registration/deregistration
- Subscription management
- Connection limits
- Concurrency (locking)

**What Failed:**
- Message delivery (all 7 failures)
- Root cause: Didn't call connection.send()

### Task 14: CSV Transformer (Simple)

**Result:** 87% (13/15 tests passed)

**What Worked:**
- Most operations (13/15)
- File I/O
- Basic filters

**What Failed:**
- Numeric comparisons on string data (2 failures)
- Root cause: String comparison instead of numeric

---

**Document Version:** 1.0  
**Based on Testing:** May 25, 2026  
**Framework Version:** 2.0.0 → 2.1.0 (proposed)  
**Prepared by:** OpenCode Testing Team
