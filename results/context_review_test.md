# Test context review (AI-assisted; learner confirmation pending)

Grade 0 means the packed retrieval context does not contain the required evidence. Grade 1 means partial evidence or missing conditions/source. Grade 2 means the full evidence and source are present. This review concerns the **single retrieval run** stored in `test_dense_*/traces.json`; agent searches may later change the final context.

| Case | Gold evidence location | Baseline k=3, 800 chars | Selected k=10, 3000 chars | Reason |
|---|---|---:|---:|---|
| d7-t01 | p21, GV-1.7-001 | 0 | 0 | The initial search misses the deactivation sentence; the agent later finds it by searching the action code. |
| d7-t02 | p23, GV-4.1-003 | 2 | 2 | Full lifecycle sentence and source ID are in both packed contexts. |
| d7-t03 | p24, GV-5.1-001 | 0 | 2 | The larger context includes the complete time-and-resources sentence; agent still abstains. |
| d7-t04 | p36, MS-2.6-003 | 2 | 2 | Full safety re-evaluation sentence and source ID are in both contexts; baseline agent still abstains. |
| d7-t05 | p48, MG-3.2-008 | 0 | 0 | Human-moderation sentence is absent from both packed contexts. |

Distribution: baseline grade 0/1/2 = **3/0/2**, selected = **2/0/3**. Evidence Hit@3 is a separate ranking measure. The agent's final answer quality is scored separately in each `agent_test_*/agent_metrics_ai_assisted.json`.
