#!/usr/bin/env bash
# Full pipeline: fix/fill → clean/validate → wire unlocks → test
set -euo pipefail
cd /Users/emmy/Documents/KnowledgeGraph

LOG=/tmp/pipeline_log.md
echo "# Full Pipeline Log" > "$LOG"
echo "Started: $(date)" >> "$LOG"

###############################################################################
# STEP 1: Clean and validate after fix/fill agents
###############################################################################
echo "" >> "$LOG"
echo "## Step 1: Clean and validate fix/fill results" >> "$LOG"

bash scripts/codex_worker.sh --out /tmp/step1_clean.log "You are working in /Users/emmy/Documents/KnowledgeGraph.

Fix these files so they pass load_yaml_subset in scripts/kg_core.py — clean YAML lists only:
- data/authored/nodes/amplitude_methods.yaml
- data/authored/dependencies/amplitude_methods.yaml
- data/authored/nodes/math_methods_foundations.yaml
- data/authored/dependencies/math_methods_foundations.yaml
- data/authored/nodes/lattice_dis_cosmo_methods.yaml
- data/authored/dependencies/lattice_dis_cosmo_methods.yaml

Ensure every dep edge has all required fields (from, to, relation_type, necessity, confidence, rationale, failure_mode_if_absent, evidence list, status). Remove edges where from/to IDs don't exist.

After fixing, run: .venv/bin/python scripts/validate_graph.py --all-authored
Then: .venv/bin/python scripts/compile_graph.py --all-authored
Report results."

echo "Step 1 done: $(date)" >> "$LOG"
cat /tmp/step1_clean.log >> "$LOG"

###############################################################################
# STEP 2: Wire "unlocks" edges
###############################################################################
echo "" >> "$LOG"
echo "## Step 2: Wire unlocks edges" >> "$LOG"

# Export all technique nodes with their unlocks fields
.venv/bin/python -c "
import yaml, glob, json

all_techs = []
for path in sorted(glob.glob('data/authored/nodes/*.yaml')):
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, list):
            continue
        for node in data:
            if isinstance(node, dict) and node.get('id','').startswith('technique.'):
                all_techs.append({'id': node['id'], 'label': node.get('label',''), 'summary': node.get('summary','')})
    except:
        pass

with open('/tmp/all_technique_nodes.json', 'w') as f:
    json.dump(all_techs, f, indent=2)
print(f'Exported {len(all_techs)} technique nodes')
"

# Also export all non-technique node IDs (the concept nodes that techniques might unlock)
.venv/bin/python -c "
import json
with open('data/generated/compiled/all_authored.graph.json') as f:
    graph = json.load(f)
concepts = [{'id': n['id'], 'label': n.get('label','')} for n in graph['nodes'] if not n['id'].startswith('technique.')]
with open('/tmp/concept_nodes.json', 'w') as f:
    json.dump(concepts, f, indent=2)
print(f'Exported {len(concepts)} concept nodes')
"

# Wire unlocks in 4 parallel Codex batches
.venv/bin/python -c "
import json, math
with open('/tmp/all_technique_nodes.json') as f:
    techs = json.load(f)
batch_size = math.ceil(len(techs) / 4)
for i in range(4):
    start = i * batch_size
    end = min(start + batch_size, len(techs))
    batch = techs[start:end]
    with open(f'/tmp/unlocks_batch_{i+1}.json', 'w') as f:
        json.dump(batch, f, indent=2)
    print(f'Unlocks batch {i+1}: {len(batch)} techniques')
"

for i in 1 2 3 4; do
    bash scripts/codex_worker.sh --out /tmp/unlocks_wire_${i}.log "You are working in /Users/emmy/Documents/KnowledgeGraph.

Read /tmp/unlocks_batch_${i}.json — a list of technique nodes with their summaries.
Read /tmp/concept_nodes.json — all concept (non-technique) nodes in the graph.
Also read /tmp/all_technique_nodes.json for technique-to-technique unlocks.

For each technique, based on its summary/description, determine what PROBLEMS or CONCEPTS it UNLOCKS (makes tractable). Find matching node IDs from the concept or technique lists.

Write a dependency file: data/authored/dependencies/unlocks_wiring_batch_${i}.yaml

The edge direction is: technique (from) -> concept/problem it unlocks (to)
Use relation_type: requires_for_use (the technique is required for using/computing the downstream concept)

Each edge must have ALL fields:
- from: technique node ID
- to: concept or technique node ID it unlocks
- relation_type: requires_for_use
- necessity: typical
- confidence: 0.75
- rationale: specific explanation of how this technique unlocks the downstream concept
- failure_mode_if_absent: what goes wrong without the technique
- evidence:
    - type: expert_claim
      source_ref: unlocks_wiring_pass
      note: brief note
- status: asserted

ONLY create edges where both from and to are real node IDs. Output clean YAML list only." &
done
wait

echo "Unlocks wiring done: $(date)" >> "$LOG"

# Clean and validate
bash scripts/codex_worker.sh --out /tmp/step2_clean.log "You are working in /Users/emmy/Documents/KnowledgeGraph.

Fix these 4 files for load_yaml_subset compliance:
- data/authored/dependencies/unlocks_wiring_batch_1.yaml through batch_4.yaml

Ensure all required dep fields present. Remove edges with non-existent node IDs.

Run: .venv/bin/python scripts/validate_graph.py --all-authored
Then: .venv/bin/python scripts/compile_graph.py --all-authored
Report results including node/dependency counts."

echo "Step 2 validation done: $(date)" >> "$LOG"
cat /tmp/step2_clean.log >> "$LOG"

###############################################################################
# STEP 3: Method-of-regions test — WITHOUT hint (isolated, no repo access)
###############################################################################
echo "" >> "$LOG"
echo "## Step 3: Cold test (no hint, no repo access)" >> "$LOG"

# Run from /tmp so codex can't see the repo
mkdir -p /tmp/cold_test
cd /tmp/cold_test

bash /Users/emmy/Documents/KnowledgeGraph/scripts/codex_worker.sh --out /tmp/cold_test_result.md "You are a physics PhD student solving a QFT problem. You do NOT have access to any external resources, knowledge graphs, or technique databases. Work from first principles only.

PROBLEM:
Evaluate the one-loop scalar integral

I(p², m²) = ∫ d⁴k / [(2π)⁴] · 1 / [(k² - m²)((k-p)² )]

in dimensional regularization (d = 4 - 2ε), in the regime m² ≪ -p² (i.e., m is much smaller than the external momentum scale).

Compute the result keeping all terms through O(ε⁰), including the full dependence on ln(m²/p²). Show your work step by step.

Do not look up any external files or references. Solve from scratch."

cd /Users/emmy/Documents/KnowledgeGraph
echo "Cold test done: $(date)" >> "$LOG"
echo '```' >> "$LOG"
cat /tmp/cold_test_result.md >> "$LOG"
echo '```' >> "$LOG"

###############################################################################
# STEP 4: Query graph for relevant techniques
###############################################################################
echo "" >> "$LOG"
echo "## Step 4: Graph query for relevant techniques" >> "$LOG"

.venv/bin/python -c "
import json

with open('data/generated/compiled/all_authored.graph.json') as f:
    graph = json.load(f)

# Find techniques relevant to: loop integrals, two-scale problems, expansion in mass ratios
keywords = ['method_of_regions', 'feynman_param', 'dimensional_reg', 'loop_integral',
            'two_scale', 'mass_expansion', 'asymptotic_expansion', 'infrared',
            'mellin_barnes', 'sector_decomp', 'integration_by_parts', 'master_integral',
            'saddle_point', 'passarino_veltman', 'alpha_param']

relevant = []
for node in graph['nodes']:
    nid = node['id'].lower()
    summary = node.get('summary', '').lower()
    label = node.get('label', '').lower()
    for kw in keywords:
        if kw in nid or kw in summary or kw in label:
            relevant.append(node)
            break

# Deduplicate
seen = set()
unique = []
for n in relevant:
    if n['id'] not in seen:
        seen.add(n['id'])
        unique.append(n)

print(f'Found {len(unique)} relevant technique nodes')
with open('/tmp/relevant_techniques.md', 'w') as f:
    f.write('# Relevant Techniques for Two-Scale Loop Integral\n\n')
    for n in unique:
        f.write(f'## {n[\"id\"]}: {n.get(\"label\",\"\")}\n')
        f.write(f'{n.get(\"summary\",\"No summary.\")}\n\n')

print('Wrote /tmp/relevant_techniques.md')
" >> "$LOG" 2>&1

###############################################################################
# STEP 5: Method-of-regions test — WITH hint (graph-retrieved techniques)
###############################################################################
echo "" >> "$LOG"
echo "## Step 5: Hint test (with graph-retrieved techniques)" >> "$LOG"

cd /tmp/cold_test

HINTS=$(cat /tmp/relevant_techniques.md)

bash /Users/emmy/Documents/KnowledgeGraph/scripts/codex_worker.sh --out /tmp/hint_test_result.md "You are a physics PhD student solving a QFT problem. You have been given a set of relevant techniques from a knowledge graph. Use them.

RELEVANT TECHNIQUES FROM KNOWLEDGE GRAPH:
$HINTS

PROBLEM:
Evaluate the one-loop scalar integral

I(p², m²) = ∫ d⁴k / [(2π)⁴] · 1 / [(k² - m²)((k-p)² )]

in dimensional regularization (d = 4 - 2ε), in the regime m² ≪ -p² (i.e., m is much smaller than the external momentum scale).

Compute the result keeping all terms through O(ε⁰), including the full dependence on ln(m²/p²). Show your work step by step.

Use the technique hints above to guide your approach. In particular, consider whether the method of regions or asymptotic expansion techniques would help decompose this integral cleanly."

cd /Users/emmy/Documents/KnowledgeGraph
echo "Hint test done: $(date)" >> "$LOG"
echo '```' >> "$LOG"
cat /tmp/hint_test_result.md >> "$LOG"
echo '```' >> "$LOG"

###############################################################################
# STEP 6: Comparison report
###############################################################################
echo "" >> "$LOG"
echo "## Step 6: Final graph stats" >> "$LOG"

.venv/bin/python scripts/validate_graph.py --all-authored 2>&1 >> "$LOG"

echo "" >> "$LOG"
echo "Pipeline complete: $(date)" >> "$LOG"

echo "=== PIPELINE COMPLETE ==="
echo "Full log at /tmp/pipeline_log.md"
echo "Cold test result at /tmp/cold_test_result.md"
echo "Hint test result at /tmp/hint_test_result.md"
