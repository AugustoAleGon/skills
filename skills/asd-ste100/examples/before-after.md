# Before / After Examples

## Part 1 — Official STE Examples

These illustrate real ASD-STE100 rules, drawn from public secondary sources (see [writing rules](../references/writing-rules.md)). They are paraphrased illustrations of the rule, not quotes from the standard itself.

| Rule | Before | After | Why |
|---|---|---|---|
| One meaning per word | "Verify the system." / "Check the connections." / "Confirm receipt." | "Check the system." / "Check the connections." / "Confirm receipt." | Use one term for the same action. Keep different terms when the actions differ, such as inspecting connections and acknowledging receipt; dictionary approval is not verified here. |
| One part of speech per word | "Oil the valve." | "Apply oil to the valve." | If "oil" is approved only as a noun, using it as a verb breaks the one-word-one-role guarantee. |
| Precise verb meaning | "Follow the safety instructions." | "Obey the safety instructions." | "Follow" can mean "come after" or "obey" — STE picks the unambiguous one. |
| Simple tense only | "We have received the technical reports from HQ." | "We received the technical reports from HQ." | Present perfect adds a second parse ("received, and still relevant now?") that simple past avoids. |
| Verb, not noun | "Perform an inspection of the filter." | "Inspect the filter." | The noun form hides the action and adds a filler verb that carries no meaning. |
| No phrasal verbs | "Take off the access panel." | "Remove the access panel." | "Take off" also means "depart" and "deduct" — the two words together do not predict the meaning. |

## Part 2 — Applied to Agent Output

These are original examples built for this skill's actual use case: rewriting AI agent output so another agent, a translation layer, or a non-native reader can parse it without ambiguity. They are illustrations, not quotes from any real system.

Word counts below are whitespace-separated tokens (`text.split()`), punctuation not counted separately. A different tokenizer will produce a different number.

### Example A — Tool description

**Before:**
> This tool will attempt to synchronize state across the various backends that have been configured, and if a conflict is detected it may resolve it automatically depending on the strategy that has been set, or otherwise it will surface the conflict for manual review.

**Violations flagged:**
- Two instructions in one sentence (sync + resolve/surface).
- Present perfect in the relative clauses ("have been configured", "has been set").
- 44 words, far over the 25-word descriptive cap.

Note what is *not* flagged: "will attempt to" and "may resolve". Those are hedges, not violations. The tool is not promised to succeed, and the rewrite must not promise it either.

**After:**
> The tool tries to synchronize state across the configured backends. If it finds a conflict, it may resolve the conflict automatically, depending on the configured strategy. If the tool does not resolve the conflict, it reports the conflict for manual review.

The last sentence branches on whether the conflict was resolved, not on what the strategy allows. That is what "or otherwise" meant in the original: the fallback covers a permitted resolution that still did not happen.

### Example B — Error message

**Before:**
> An error may have occurred while processing your request due to a possible mismatch in the expected data format, which could be caused by an outdated client version.

**Violations flagged:**
- One sentence carrying three separate claims (an error occurred, a format mismatch, a client version).
- 28 words, over the descriptive cap.

Not flagged: "may have occurred" and "could be caused by". The message is written by a system that does not know what went wrong. Both hedges are accurate reporting of that ignorance.

**After:**
> An error may have occurred while the system processed your request. A data format mismatch may be the cause. An outdated client could cause this mismatch.

**This example is the reason the modality rule exists.** An earlier version of this file rewrote the first sentence as "The request failed", and the third as "an outdated client **is the most common cause**". Both read better. Both are wrong: the first asserts a failure the system only suspects, and the second invents a frequency claim that appears nowhere in the input. A rewrite that supplies a cause, a frequency, or a mechanism has stopped being a rewrite.

Note also that "may have occurred" keeps a compound verb form that the simple-tense rule would otherwise remove. **When the tense rule and the modality rule conflict, modality wins** — dropping the auxiliary here would delete the uncertainty along with the tense.

### Example C — Inter-agent instruction

**Before:**
> Once the upstream job has completed and assuming no errors were raised, the downstream agent should proceed to consume the output artifact, though it is worth noting that partial artifacts are sometimes produced under timeout conditions.

**Violations flagged:**
- Present perfect ("has completed") and subordinate-clause stacking ("assuming...", "though it is worth noting...").
- One sentence, three separate facts (completion condition, next action, edge-case warning).
- 36 words, over the 20-word instruction cap.

**After:**
> After the upstream job finishes, the downstream agent should read the output artifact if no errors were reported. Warning: timeouts sometimes produce partial artifacts.

The rewrite keeps the recommendation ("should"), the no-errors condition, and
"sometimes". It does not add an artifact-validation step. Such a step could be
useful advice, but it would need to be labeled separately from the rewrite.

### Example D — README prose (STE-flavored mode)

**Before:**
> Our caching layer is designed to slot seamlessly into your existing stack with minimal friction and no vendor lock-in; it leverages semantic similarity to dramatically reduce the cache misses that traditionally plague LLM workloads.

**Violations flagged:**
- Marketing adjectives and claims without measurement ("seamlessly", "minimal friction", "dramatically").
- Semicolon joining two separate ideas.
- Nominalization and soft phrasing ("is designed to slot into", "leverages").
- 34 words, over the 25-word descriptive cap.

**After:**
> Our caching layer is designed to integrate easily with your existing stack without vendor lock-in. It uses semantic similarity to substantially reduce cache misses in LLM workloads.

The rewrite preserves the original claims without endorsing them. It adds no
claim about where data is stored. If the user wants factual editing, ask for
evidence for "easily", "without vendor lock-in", and "substantially" rather than
silently replacing those claims with invented measurements or architecture.

## How to Read These Examples

Part 1 shows the actual rules this skill is built on. Part 2 shows the transfer: the same discipline — one meaning per word, active voice, simple tense, one instruction per sentence, explicit conditions instead of buried subordinate clauses — makes machine-to-machine and cross-language text safer to parse, not just aircraft manuals.
