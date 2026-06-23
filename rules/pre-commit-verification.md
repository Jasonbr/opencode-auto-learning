# Pre-Commit Verification Rule

> Injected before any git commit operation.
> Applied globally to ALL projects.

## Iron Law

```
NO COMMIT WITHOUT VERIFICATION
```

## Verification Steps (MUST PASS ALL)

### Step 1: Self-Review Checklist

Quick scan before committing:

- [ ] **No hardcoded secrets** (API keys, passwords, tokens)
- [ ] **No debug print/console.log** left behind
- [ ] **No commented-out code** (delete or keep, don't comment)
- [ ] **Input validation** on user-provided data
- [ ] **Error handling** for external calls
- [ ] **Test exists** for the changed code
- [ ] **Test passes** locally

### Step 2: Static Security Scan

Run on staged changes:

```bash
# Hardcoded secrets
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]" && echo "ERROR: Found potential secret"

# Shell injection
git diff --cached | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True" && echo "WARNING: Potential shell injection"

# Dangerous eval/exec
git diff --cached | grep "^+" | grep -E "\beval\(|\bexec\(" && echo "WARNING: eval/exec found"
```

**Any match = MUST FIX before commit**

### Step 3: Regression Test

Compare failures before and after changes:

```bash
# Python
python -m pytest --tb=no -q 2>&1 | tail -5

# Node
npm test -- --passWithNoTests 2>&1 | tail -5

# Rust
cargo test 2>&1 | tail -5

# Go
go test ./... 2>&1 | tail -5
```

**Rule: 0 new failures vs baseline**

### Step 4: Lint Check (if tools installed)

```bash
# Python
which ruff && ruff check . 2>&1 | grep "^+" | head -5

# Node
which npx && npx eslint . 2>&1 | grep "error" | head -5

# Rust
cargo clippy -- -D warnings 2>&1 | grep "error" | head -5
```

**Fix lint errors before commit**

### Step 5: Commit with Verification

If all checks pass:

```bash
git add -A && git commit -m "[verified] <description>"
```

The `[verified]` prefix indicates code passed self-review and tests.

## Failure Handling

**If any check fails:**

1. STOP commit
2. Fix the issue
3. Re-run all checks
4. Only then commit

**Never commit with "fix later" or "TODO"**

## Quick Reference

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Secrets | `git diff --cached \| grep -i secret` | No matches |
| Tests | `pytest tests/ -q` | 0 failures |
| Lint | `ruff check .` | Clean |
| Regression | Compare baseline | No new failures |

## Common Patterns to Reject

### Python
```python
# REJECT: SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ACCEPT: Parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# REJECT: Shell injection
os.system(f"ls {user_input}")

# ACCEPT: Safe subprocess
subprocess.run(["ls", user_input], check=True)
```

### JavaScript
```javascript
// REJECT: XSS
element.innerHTML = userInput;

// ACCEPT: Safe
element.textContent = userInput;
```

## Hard Rules

1. **NEVER commit without running tests**
2. **NEVER commit with hardcoded secrets**
3. **NEVER commit with debug code**
4. **NEVER commit if any check fails**
5. **ALWAYS use `[verified]` prefix**

## Red Flags - STOP Commit

- Tests failing
- Secrets detected
- Lint errors
- "Quick fix" without test
- "Will add tests later"
- Commented-out code
- Debug print statements
