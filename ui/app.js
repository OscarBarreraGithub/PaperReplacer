const state = {
  batchId: null,
  bundle: null,
  relationType: "requires_for_use",
  viewMode: "full",
  targetNodeId: null,
  includePartonomy: true,
  selectedNodeId: null
};

const elements = {
  batchSelect: document.getElementById("batch-select"),
  relationSelect: document.getElementById("relation-select"),
  viewSelect: document.getElementById("view-select"),
  targetSelect: document.getElementById("target-select"),
  partonomyToggle: document.getElementById("partonomy-toggle"),
  searchInput: document.getElementById("search-input"),
  refreshButton: document.getElementById("refresh-button"),
  fitButton: document.getElementById("fit-button"),
  batchSummary: document.getElementById("batch-summary"),
  nodeDetails: document.getElementById("node-details"),
  statusBar: document.getElementById("status-bar"),
  graphContainer: document.getElementById("graph")
};

if (!window.ForceGraph3D) {
  setStatus("Graph library failed to load. Check network access to the CDN.");
  throw new Error("ForceGraph3D is not available on window.");
}

const graph = new window.ForceGraph3D(elements.graphContainer, {
  controlType: "trackball"
})
  .backgroundColor("#0b1016")
  .nodeRelSize(6)
  .nodeOpacity(0.95)
  .linkOpacity(0.55)
  .linkWidth(link => (link.kind === "partonomy" ? 1 : 2.6))
  .linkDirectionalParticles(link => (link.kind === "dependency" ? 2 : 0))
  .linkDirectionalParticleSpeed(0.004)
  .linkDirectionalParticleWidth(2.4)
  .nodeLabel(node => buildNodeLabel(node))
  .linkLabel(link => `${link.kind}: ${link.relationType}`)
  .linkColor(link => (link.kind === "partonomy" ? "#68c5db" : "rgba(255,255,255,0.65)"))
  .nodeColor(node => nodeColor(node))
  .nodeVal(node => (state.selectedNodeId === node.id ? 12 : node.val ?? 6))
  .onNodeClick(node => {
    state.selectedNodeId = node.id;
    renderNodeDetails(node);
    focusNode(node);
    refreshGraph(false);
  })
  .onBackgroundClick(() => {
    state.selectedNodeId = null;
    renderNodeDetails(null);
    refreshGraph(false);
  });

window.addEventListener("resize", () => {
  graph.width(elements.graphContainer.clientWidth);
  graph.height(elements.graphContainer.clientHeight);
});

window.addEventListener("error", event => {
  setStatus(`UI error: ${event.message}`);
});

window.addEventListener("unhandledrejection", event => {
  const message = event.reason?.message ?? String(event.reason);
  setStatus(`UI error: ${message}`);
});

init().catch(error => {
  console.error(error);
  setStatus(`Failed to load UI: ${error.message}`);
});

async function init() {
  graph.width(elements.graphContainer.clientWidth);
  graph.height(elements.graphContainer.clientHeight);

  wireControls();

  const batches = await fetchJson("/api/batches");
  elements.batchSelect.innerHTML = "";
  for (const batch of batches) {
    const option = document.createElement("option");
    option.value = batch.batch_id;
    option.textContent = batch.batch_id;
    elements.batchSelect.appendChild(option);
  }
  if (!batches.length) {
    setStatus("No batches found.");
    return;
  }
  state.batchId = batches[0].batch_id;
  elements.batchSelect.value = state.batchId;
  await loadBatch(state.batchId);
}

function wireControls() {
  elements.batchSelect.addEventListener("change", async event => {
    await loadBatch(event.target.value);
  });

  elements.relationSelect.addEventListener("change", () => {
    state.relationType = elements.relationSelect.value;
    refreshGraph();
  });

  elements.viewSelect.addEventListener("change", () => {
    state.viewMode = elements.viewSelect.value;
    refreshGraph();
  });

  elements.targetSelect.addEventListener("change", () => {
    state.targetNodeId = elements.targetSelect.value || null;
    refreshGraph();
  });

  elements.partonomyToggle.addEventListener("change", () => {
    state.includePartonomy = elements.partonomyToggle.checked;
    refreshGraph();
  });

  elements.refreshButton.addEventListener("click", async () => {
    if (state.batchId) {
      await loadBatch(state.batchId);
    }
  });

  elements.fitButton.addEventListener("click", () => {
    graph.zoomToFit(600, 40);
  });

  elements.searchInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      const needle = event.target.value.trim().toLowerCase();
      if (!needle || !state.bundle) {
        return;
      }
      const match = state.bundle.nodes.find(node =>
        node.id.toLowerCase().includes(needle) ||
        node.label.toLowerCase().includes(needle)
      );
      if (!match) {
        setStatus(`No node matched "${needle}".`);
        return;
      }
      state.targetNodeId = match.id;
      state.selectedNodeId = match.id;
      elements.targetSelect.value = match.id;
      renderNodeDetails(match);
      refreshGraph();
    }
  });
}

async function loadBatch(batchId) {
  setStatus(`Loading ${batchId}…`);
  state.batchId = batchId;
  state.bundle = await fetchJson(`/api/batch/${encodeURIComponent(batchId)}`);
  state.selectedNodeId = null;

  const relationOptions = new Set(["all"]);
  for (const edge of state.bundle.dependencies) {
    relationOptions.add(edge.relation_type);
  }
  const currentRelation = relationOptions.has(state.relationType)
    ? state.relationType
    : "requires_for_use";
  elements.relationSelect.innerHTML = "";
  for (const relation of relationOptions) {
    const option = document.createElement("option");
    option.value = relation;
    option.textContent = relation;
    elements.relationSelect.appendChild(option);
  }
  state.relationType = currentRelation;
  elements.relationSelect.value = currentRelation;

  const sortedNodes = [...state.bundle.nodes].sort((a, b) =>
    a.label.localeCompare(b.label)
  );
  elements.targetSelect.innerHTML = '<option value="">(none)</option>';
  for (const node of sortedNodes) {
    const option = document.createElement("option");
    option.value = node.id;
    option.textContent = `${node.label} (${node.id})`;
    elements.targetSelect.appendChild(option);
  }
  state.targetNodeId = sortedNodes[0]?.id ?? null;
  elements.targetSelect.value = state.targetNodeId ?? "";

  renderBatchSummary();
  renderNodeDetails(null);
  refreshGraph();
}

function renderBatchSummary() {
  const { bundle } = state;
  if (!bundle) return;
  const html = `
    <h2>Batch</h2>
    <div class="kv">
      <strong>ID</strong><span>${escapeHtml(bundle.batch_id)}</span>
      <strong>Nodes</strong><span>${bundle.nodes.length}</span>
      <strong>Dependencies</strong><span>${bundle.dependencies.length}</span>
      <strong>Partonomy</strong><span>${bundle.partonomy.length}</span>
      <strong>Overlays</strong><span>${bundle.overlays.length}</span>
    </div>
    <p class="subtle" style="margin-top:12px;">
      ${escapeHtml(bundle.contract.description ?? "Compiled batch graph.")}
    </p>
  `;
  elements.batchSummary.innerHTML = html;
}

function renderNodeDetails(node) {
  if (!node) {
    elements.nodeDetails.innerHTML = `
      <h2>Node Details</h2>
      <div class="subtle">Click a node to inspect it.</div>
    `;
    return;
  }
  const incoming = (state.bundle?.dependencies ?? []).filter(edge => edge.to === node.id);
  const outgoing = (state.bundle?.dependencies ?? []).filter(edge => edge.from === node.id);
  const overlays = (state.bundle?.overlays ?? []).filter(
    overlay => overlay.target_topic === node.id || overlay.presumed_node === node.id
  );
  elements.nodeDetails.innerHTML = `
    <h2>${escapeHtml(node.label)}</h2>
    <div class="kv">
      <strong>ID</strong><span>${escapeHtml(node.id)}</span>
      <strong>Kind</strong><span>${escapeHtml(node.knowledge_kind ?? "n/a")}</span>
      <strong>Granularity</strong><span>${escapeHtml(node.granularity_level ?? "n/a")}</span>
      <strong>Status</strong><span>${escapeHtml(node.status ?? "n/a")}</span>
    </div>
    <p style="margin-top:12px;">${escapeHtml(node.summary ?? "No summary.")}</p>
    <div>
      ${(node.mastery_modes_supported ?? []).map(mode => `<span class="pill">${escapeHtml(mode)}</span>`).join("")}
    </div>
    <p class="subtle" style="margin-top:12px;">
      Incoming dependencies: ${incoming.length} · Outgoing dependencies: ${outgoing.length} · Overlays: ${overlays.length}
    </p>
  `;
}

async function refreshGraph(zoomAfter = true) {
  if (!state.bundle) return;
  const data =
    state.viewMode === "focus" && state.targetNodeId
      ? await buildFocusedGraph()
      : buildFullGraph();

  graph.graphData(data);
  setStatus(
    `${state.batchId} · ${data.nodes.length} nodes · ${data.links.length} links · ${state.viewMode} view`
  );
  if (zoomAfter) {
    graph.zoomToFit(700, 60);
  }
}

async function buildFocusedGraph() {
  const slice = await fetchJson(
    `/api/neighborhood?batch=${encodeURIComponent(state.batchId)}&target=${encodeURIComponent(
      state.targetNodeId
    )}&relation_type=${encodeURIComponent(activeRelationType())}`
  );
  const allowedNodes = new Set(slice.nodes);
  const nodeMap = new Map(state.bundle.nodes.map(node => [node.id, node]));
  const nodes = [...allowedNodes].map(id => augmentNode(nodeMap.get(id) ?? { id, label: id }));
  const links = [];
  for (const edge of slice.dependencies) {
    if (state.relationType !== "all" && edge.relation_type !== state.relationType) continue;
    links.push(toLink(edge, "dependency"));
  }
  if (state.includePartonomy) {
    for (const edge of slice.partonomy) {
      links.push(toPartonomyLink(edge));
    }
  }
  return { nodes, links };
}

function buildFullGraph() {
  const nodes = state.bundle.nodes.map(augmentNode);
  const links = [];
  for (const edge of state.bundle.dependencies) {
    if (state.relationType !== "all" && edge.relation_type !== state.relationType) continue;
    links.push(toLink(edge, "dependency"));
  }
  if (state.includePartonomy) {
    for (const edge of state.bundle.partonomy) {
      links.push(toPartonomyLink(edge));
    }
  }
  return { nodes, links };
}

function augmentNode(node) {
  const namespace = node.id.includes(".") ? node.id.split(".")[0] : "other";
  const val = state.selectedNodeId === node.id ? 12 : 7;
  return { ...node, namespace, val };
}

function toLink(edge, kind) {
  return {
    source: edge.from,
    target: edge.to,
    relationType: edge.relation_type,
    kind,
    color: kind === "partonomy" ? "#68c5db" : "#ffffff"
  };
}

function toPartonomyLink(edge) {
  return {
    source: edge.child,
    target: edge.parent,
    relationType: "part_of",
    kind: "partonomy",
    color: "#68c5db"
  };
}

function nodeColor(node) {
  if (state.selectedNodeId === node.id) return "#ffffff";
  if (node.namespace === "complex_analysis" || node.namespace === "math") return "#f3b43f";
  if (node.namespace === "qft") return "#68c5db";
  return "#d96c75";
}

function buildNodeLabel(node) {
  const summary = escapeHtml(node.summary ?? "");
  return `
    <div style="max-width: 280px; padding: 8px 10px; background: rgba(10,14,20,0.9); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;">
      <div style="font-weight: 700; margin-bottom: 4px;">${escapeHtml(node.label ?? node.id)}</div>
      <div style="color: #9eb0c2; font-size: 12px; margin-bottom: 6px;">${escapeHtml(node.id)}</div>
      <div style="font-size: 12px; line-height: 1.45;">${summary}</div>
    </div>
  `;
}

function focusNode(node) {
  const distance = 90;
  const distRatio = 1 + distance / Math.hypot(node.x || 1, node.y || 1, node.z || 1);
  graph.cameraPosition(
    {
      x: (node.x || 0) * distRatio,
      y: (node.y || 0) * distRatio,
      z: (node.z || 0) * distRatio
    },
    node,
    900
  );
}

function activeRelationType() {
  return state.relationType === "all" ? "requires_for_use" : state.relationType;
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return response.json();
}

function setStatus(text) {
  elements.statusBar.textContent = text;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
