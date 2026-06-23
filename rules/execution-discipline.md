# Execution Discipline Rules

> Injected on every tool execution by rules-injector hook.
> Applied globally to ALL projects.

## Current Phase Check

Before ANY tool execution, verify current phase from `.sisyphus/plans/PLAN-STATE.json`:

```
If phase == "plan_pending":
  - STOP execution
  - Present plan card for approval
  - Wait for explicit approval keyword

If phase == "executing":
  - Check if current task is approved
  - Update progress after completion

If phase == "completed":
  - Wait for user acceptance
  - Do NOT start new tasks
```

## Approval Keywords (REQUIRED)

**Valid approval:**
- "确认执行"
- "approved"
- "execute"
- "go"
- "开始执行"

**NOT valid:**
- "ok", "好的", "sure"
- "looks good", "不错"
- "继续", "下一步"
- Any vague response

## Visual Templates

### Plan Card Template

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 IMPLEMENTATION PLAN: [Feature Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Source: `.sisyphus/plans/YYYY-MM-DD-feature.md`
Status: 🟡 PENDING APPROVAL

┌────────────────────────────────────────────────────┐
│ 🎯 OBJECTIVE                                        │
├────────────────────────────────────────────────────┤
│ [One sentence goal]                                │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ 📊 OVERVIEW                                         │
├────────────────────────────────────────────────────┤
│ Metric     │ Value                                  │
├────────────┼────────────────────────────────────────┤
│ Tasks      │ N                                      │
│ New files  │ N                                      │
│ Modified   │ N                                      │
│ Stack      │ [Stack]                                │
│ Est. time  │ [Time]                                 │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ 📝 TASK BREAKDOWN                                   │
├────────────────────────────────────────────────────┤
│                                                    │
│ Task 1: [Name]                                     │
│   📄 `file/path.py`                                │
│   📝 [Brief description]                           │
│                                                    │
│ [Repeat for each task]                             │
│                                                    │
└────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────┐
│ ✅ CONFIRM  →  Type "确认执行" or "approved"        │
│ ✏️ MODIFY   →  Tell me what to change              │
│ ❌ CANCEL   →  Type "取消"                         │
└────────────────────────────────────────────────────┘
```

### Task Completion Template

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ TASK COMPLETED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task N: [Name]

📁 CHANGES:
  ✏️  `file/path.py` (modified)
  ➕  `file/new.py` (created)

🧪 VERIFICATION:
  ✅ Tests: X/Y passed
  ✅ Lint: Clean

📊 UPDATED PROGRESS: [████████████░░░░░░░░] 60% (3/5)
```

### Completion Dashboard Template

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ IMPLEMENTATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 DELIVERABLES:
┌────────────────────────────────────────────────────┐
│ File              │ Status │ Notes                 │
├───────────────────┼────────┼───────────────────────┤
│ `src/core.py`     │ ✅ New │ Core logic            │
│ `tests/...`       │ ✅ New │ Unit tests            │
└────────────────────────────────────────────────────┘

📊 EXECUTION STATS:
┌────────────────────────────────────────────────────┐
│ Total tasks │ 5                                    │
│ Success     │ 5      ✅ 100%                      │
│ Failed      │ 0      ✅ 0%                        │
└────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ACCEPTANCE REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────┐
│ ✅ ACCEPT   →  Type "接受" or "完成"               │
│ ✏️ MODIFY   →  Tell me what needs adjustment       │
│ 🔄 REDO     →  Type "重做 Task N"                  │
└────────────────────────────────────────────────────┘
```

## Hard Rules

1. NEVER write code before plan approval
2. NEVER skip approach selection
3. NEVER execute without explicit approval keyword
4. NEVER skip completion acceptance
5. Vague responses ("ok", "好的") are NOT approval
