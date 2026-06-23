# TDD Enforcement Rule

> Injected on every code-writing operation.
> Applied globally to ALL projects.

## Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## RED-GREEN-REFACTOR Cycle (MANDATORY)

### RED Phase - Write Failing Test

**Before writing ANY implementation code:**

1. **Check for existing test**
   - Search for test file: `tests/test_*.py` or `*.test.ts`
   - Look for test matching the feature/bug

2. **If no test exists → STOP and write test first**

3. **Write minimal test**
   ```python
   def test_feature_behavior():
       result = function_under_test(input)
       assert result == expected_output
   ```

4. **Run test - MUST FAIL**
   ```bash
   # Python
   pytest tests/test_feature.py::test_name -v
   
   # Node
   npm test -- test_name
   ```

5. **Verify failure reason is expected**
   - Error should be: "function not defined" or "assertion failed"
   - Should NOT be: syntax error, import error

**If test passes immediately → Test is wrong. Fix test.**

### GREEN Phase - Minimal Implementation

**After test fails correctly:**

1. **Write simplest code to pass**
   - No extra features
   - No refactoring
   - No "while I'm here" improvements

2. **Run test - MUST PASS**

3. **Run full test suite - No regressions**
   ```bash
   pytest tests/ -q
   # or
   npm test
   ```

**If other tests fail → Fix regressions NOW**

### REFACTOR Phase - Clean Up (Optional)

**Only after test passes:**

1. **Remove duplication**
2. **Improve names**
3. **Keep tests green throughout**

**If tests fail during refactor → Undo and take smaller steps**

## Hard Rules

1. **NEVER write code before a failing test**
2. **NEVER skip watching the test fail**
3. **NEVER bundle multiple changes**
4. **NEVER commit without running full test suite**

## Red Flags - STOP and Delete Code

- Writing implementation before test
- Test passes on first run
- "I'll add tests later"
- "This is too simple to test"
- Multiple changes in one commit

## Verification Checklist

Before marking task complete:

- [ ] Test exists and failed first
- [ ] Minimal implementation passes test
- [ ] Full test suite passes
- [ ] No debug code left
- [ ] Committed with clear message
