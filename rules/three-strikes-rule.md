# Three Strikes Rule (Anti-Whack-a-Mole)

> Injected when fixes fail repeatedly.
> Applied globally to ALL projects.

## Core Principle

```
3 FAILURES = ARCHITECTURE PROBLEM, NOT A BUG
```

## The Rule

| Attempt | Result | Action |
|---------|--------|--------|
| 1st | Fix fails | Return to Phase 1, re-investigate with new info |
| 2nd | Fix fails | Deep analysis, question assumptions |
| 3rd | Fix fails | **STOP** - Question the architecture |

## Pattern Recognition

**Signs of architectural problem:**
- ✅ Each fix reveals new shared state/coupling elsewhere
- ✅ Fixes require "massive refactoring"
- ✅ Each fix creates new symptoms in different places
- ✅ "Just one more fix" feeling

**These indicate wrong architecture, not wrong fixes.**

## Phase 1: First Failure

**After first fix attempt fails:**

1. **STOP attempting new fixes**
2. **Return to systematic debugging:**
   - Re-read error messages carefully
   - Re-reproduce the issue
   - Check recent changes
   - Trace data flow more deeply
3. **Form new hypothesis**
4. **Try different approach**

**Do NOT apply Fix #2 without new investigation**

## Phase 2: Second Failure

**After second fix attempt fails:**

1. **STOP and question assumptions:**
   - Is the diagnosis correct?
   - Is the fix addressing root cause or symptom?
   - Are there hidden dependencies?
   - Is the pattern fundamentally sound?

2. **Deep analysis required:**
   - Read reference implementation completely
   - Compare with working examples
   - List all differences

3. **Try fundamentally different approach**

**Do NOT apply Fix #3 without architectural discussion**

## Phase 3: Third Failure - THE STOP POINT

**After third fix attempt fails:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 ARCHITECTURAL PROBLEM DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pattern indicates fundamental architecture issue:
- Each fix reveals new coupling elsewhere
- Fixes require massive refactoring
- Symptoms keep moving to new places

OPTIONS:
┌────────────────────────────────────────────────────┐
│ 1. REFACTOR ARCHITECTURE                          │
│    → Redesign the problematic pattern             │
│                                                    │
│ 2. CHANGE APPROACH                                │
│    → Try completely different solution            │
│                                                    │
│ 3. ESCALATE TO HUMAN                              │
│    → Present findings, await direction            │
│                                                    │
│ 4. ABANDON CURRENT DIRECTION                        │
│    → Document lessons, try alternatives           │
└────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is NOT a failed hypothesis — this is a wrong architecture.
Stop fixing symptoms. Address the root pattern.
```

## The Psychology of Whack-a-Mole

**Why we keep trying "just one more fix":**
- Sunk cost fallacy ("already spent X hours")
- Optimism bias ("this one will work")
- Tunnel vision (fixating on symptoms)

**Recognize the pattern:**
- Fix A → Breaks B
- Fix B → Breaks C
- Fix C → Breaks A again

**This is not bad luck. This is bad architecture.**

## Hard Rules

1. **Count failures explicitly**
2. **Never attempt Fix #4 without questioning architecture**
3. **3 failures = STOP, not "try harder"**
4. **Document failures and patterns**
5. **Escalate architectural problems to user**

## Success Metrics

| Metric | Good | Bad |
|--------|------|-----|
| Fixes per issue | 1-2 | 3+ |
| Fix success rate | >80% | <50% |
| Regression rate | <10% | >30% |
| Time to fix | Hours | Days |

## Red Flags - STOP and Question Architecture

- ✅ "Just one more fix"
- ✅ "This should work..."
- ✅ "Why is this breaking NOW?"
- ✅ Each fix creates 2 new problems
- ✅ Symptoms keep moving around
- ✅ Feeling of chasing shadows

**All of these mean: STOP. Question the architecture.**

## Integration with Other Rules

**With Systematic Debugging:**
- Each failure triggers re-investigation
- New evidence gathered before next attempt

**With TDD:**
- Tests prove fix works
- If test passes but something else breaks → architectural issue

**With Pre-Commit Verification:**
- Regressions caught before commit
- If regressions keep appearing → architectural issue
