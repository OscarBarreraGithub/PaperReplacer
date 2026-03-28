const state = {
  knowledgeCheck: null,
  savedProfile: null,
  summaryProfile: null,
  ratings: [],
  currentIndex: 0,
  loading: true,
  submitting: false,
  generating: false,
  status: null
};

const elements = {
  paperTitle: document.getElementById("paper-title"),
  paperSubtitle: document.getElementById("paper-subtitle"),
  savedBanner: document.getElementById("saved-banner"),
  progressLabel: document.getElementById("progress-label"),
  progressCaption: document.getElementById("progress-caption"),
  progressFill: document.getElementById("progress-fill"),
  statusMessage: document.getElementById("status-message"),
  stage: document.getElementById("quiz-stage")
};

init().catch(error => {
  console.error(error);
  state.loading = false;
  setStatus(error.message || "Failed to load the knowledge check.", "error");
  render();
});

async function init() {
  const knowledgeCheck = await fetchJson("/api/quiz");
  state.knowledgeCheck = knowledgeCheck;
  state.ratings = new Array(knowledgeCheck.prerequisites.length).fill(null);
  if (knowledgeCheck.profile_exists) {
    try {
      const profileResponse = await fetchJson("/api/profile");
      state.savedProfile = profileResponse.profile;
    } catch (error) {
      console.warn(error);
    }
  }
  state.loading = false;
  render();
}

function render() {
  updateHeader();
  renderStatus();

  if (state.loading) {
    renderLoading("Loading prerequisite topics…");
    return;
  }

  if (!state.knowledgeCheck || !state.knowledgeCheck.prerequisites.length) {
    renderEmptyState(
      "This paper does not have prerequisite topics yet.",
      "Rewrite the paper analysis with a prerequisites list, then reload this page."
    );
    return;
  }

  if (state.submitting) {
    renderLoading("Saving your knowledge profile…");
    return;
  }

  if (state.summaryProfile) {
    renderSummary(state.summaryProfile);
    return;
  }

  renderTopic();
}

function updateHeader() {
  if (!state.knowledgeCheck) {
    elements.paperTitle.textContent = "Loading knowledge check…";
    elements.paperSubtitle.textContent = "Rate the background topics this paper assumes.";
    updateProgress(0, 0, "Preparing check");
    elements.savedBanner.classList.add("hidden");
    return;
  }

  const prerequisiteCount = state.knowledgeCheck.prerequisite_count;
  elements.paperTitle.textContent = state.knowledgeCheck.title;
  elements.paperSubtitle.textContent =
    `${state.knowledgeCheck.paper_id} · ${prerequisiteCount} prerequisite topics`;

  if (state.savedProfile?.summary && !state.summaryProfile && state.currentIndex === 0) {
    elements.savedBanner.innerHTML = `
      Saved profile found: <strong>${escapeHtml(state.savedProfile.summary.summary_text)}</strong>
      Retaking the knowledge check will overwrite it.
    `;
    elements.savedBanner.classList.remove("hidden");
  } else {
    elements.savedBanner.classList.add("hidden");
  }

  if (state.submitting) {
    updateProgress(prerequisiteCount, prerequisiteCount, "Saving profile");
    return;
  }
  if (state.summaryProfile?.summary) {
    updateProgress(prerequisiteCount, prerequisiteCount, "Check complete");
    return;
  }
  updateProgress(state.currentIndex + 1, prerequisiteCount, "Progress");
}

function updateProgress(current, total, caption) {
  const safeTotal = total || 0;
  const clampedCurrent = Math.min(Math.max(current, 0), safeTotal);
  const percent = safeTotal ? (clampedCurrent / safeTotal) * 100 : 0;
  elements.progressLabel.textContent = `${clampedCurrent}/${safeTotal}`;
  elements.progressCaption.textContent = caption;
  elements.progressFill.style.width = `${percent}%`;
}

function renderStatus() {
  if (!state.status) {
    elements.statusMessage.className = "status hidden";
    elements.statusMessage.textContent = "";
    return;
  }
  elements.statusMessage.textContent = state.status.message;
  elements.statusMessage.className = `status ${state.status.kind}`;
}

function renderLoading(message) {
  elements.stage.innerHTML = `
    <div class="surface loading-state">
      <div>
        <h2 class="summary-title">Working…</h2>
        <p>${escapeHtml(message)}</p>
      </div>
    </div>
  `;
  animateStage();
}

function renderEmptyState(title, copy) {
  elements.stage.innerHTML = `
    <div class="surface empty-state">
      <div>
        <h2 class="summary-title">${escapeHtml(title)}</h2>
        <p>${escapeHtml(copy)}</p>
      </div>
    </div>
  `;
  animateStage();
}

function renderTopic() {
  const prerequisite = state.knowledgeCheck.prerequisites[state.currentIndex];
  if (!prerequisite) {
    renderEmptyState("No topic available.", "Reload the page to try again.");
    return;
  }

  elements.stage.innerHTML = `
    <div class="surface">
      <div class="meta-row">
        <span class="chip importance-chip ${importanceClass(prerequisite.importance)}">
          ${escapeHtml(prerequisite.importance_label || "Important")}
        </span>
      </div>
      <p class="question-index">Topic ${state.currentIndex + 1} of ${state.knowledgeCheck.prerequisite_count}</p>
      <h2 class="question-text">${escapeHtml(prerequisite.topic)}</h2>
      ${prerequisite.description ? `<p class="topic-description">${escapeHtml(prerequisite.description)}</p>` : ""}
      ${prerequisite.why_important ? `<p class="why-important">${escapeHtml(prerequisite.why_important)}</p>` : ""}
      <p class="rating-prompt">How comfortable are you with this topic?</p>
      <div class="rating-grid" id="rating-grid">
        ${state.knowledgeCheck.rating_levels
          .map(
            level => `
              <button
                class="rating-button level-${escapeHtml(String(level.value))}"
                data-rating="${escapeHtml(String(level.value))}"
                title="${escapeHtml(level.label)}"
                type="button"
              >
                <span class="rating-number">${escapeHtml(String(level.value))}</span>
                <span class="rating-text">${escapeHtml(level.short_label)}</span>
              </button>
            `
          )
          .join("")}
      </div>
      <div class="rating-scale-copy">
        <span>1 = Never heard of it</span>
        <span>2 = Heard the name</span>
        <span>3 = Could explain the idea</span>
        <span>4 = Could use it in a calculation</span>
        <span>5 = Could derive/prove it</span>
      </div>
    </div>
  `;

  for (const button of elements.stage.querySelectorAll(".rating-button")) {
    button.addEventListener("click", () => {
      const ratingValue = Number(button.dataset.rating);
      if (Number.isInteger(ratingValue)) {
        handleRating(ratingValue);
      }
    });
  }

  animateStage();
}

function renderSummary(profile) {
  const summary = profile.summary || {};
  const knownTopics = getKnownTopics(profile).slice(0, 6);
  const gapTopics = getGapTopics(profile).slice(0, 8);
  const generatedOutputs = profile.generated_outputs;
  const paperDir = profile.paper_dir || "data/papers/...";
  const profilePath = `${paperDir}/user_profile.yaml`;

  elements.stage.innerHTML = `
    <div class="surface">
      <p class="summary-eyebrow">Knowledge Check Complete</p>
      <h2 class="summary-title">${escapeHtml(summary.summary_text || "Profile saved.")}</h2>
      <p class="summary-copy">
        The knowledge profile is saved to <strong>${escapeHtml(profilePath)}</strong> and can now drive
        personalized annotation and condensation for this paper.
      </p>

      <div class="summary-metrics">
        <div class="metric-card">
          <p class="metric-label">Topics rated</p>
          <p class="metric-value">${escapeHtml(String(summary.topic_count || summary.rated_topic_count || 0))}</p>
        </div>
        <div class="metric-card">
          <p class="metric-label">Gaps identified</p>
          <p class="metric-value">${escapeHtml(String(summary.gap_count || 0))}</p>
        </div>
        <div class="metric-card">
          <p class="metric-label">Known topics</p>
          <p class="metric-value">${escapeHtml(String(summary.known_count || 0))}</p>
        </div>
      </div>

      <div class="summary-section">
        <h3>Gap topics</h3>
        <div class="topic-list">
          ${gapTopics.length ? gapTopics.map(renderTopicPill).join("") : '<span class="topic-pill">No gaps flagged.</span>'}
        </div>
      </div>

      <div class="summary-section">
        <h3>Known topics</h3>
        <div class="topic-list">
          ${knownTopics.length ? knownTopics.map(renderTopicPill).join("") : '<span class="topic-pill">No known topics saved yet.</span>'}
        </div>
      </div>

      <div class="summary-actions">
        <button class="action-button primary" id="generate-button" type="button" ${state.generating ? "disabled" : ""}>
          ${generatedOutputs ? "Regenerate Personalized Paper" : "Generate Personalized Paper"}
        </button>
        <button class="action-button secondary" id="retake-button" type="button">
          Retake Knowledge Check
        </button>
      </div>

      ${generatedOutputs ? renderGeneratedBlock(generatedOutputs) : ""}
    </div>
  `;

  elements.stage.querySelector("#generate-button")?.addEventListener("click", generatePersonalizedPaper);
  elements.stage.querySelector("#retake-button")?.addEventListener("click", retakeKnowledgeCheck);
  animateStage();
}

function renderTopicPill(item) {
  const importance = item.importance_label ? ` · ${escapeHtml(item.importance_label)}` : "";
  const ratingLabel = item.rating_label || item.mastery_label || "Saved";
  return `
    <span class="topic-pill">
      <strong>${escapeHtml(item.topic)}</strong>
      <span>${escapeHtml(ratingLabel)}${importance}</span>
    </span>
  `;
}

function renderGeneratedBlock(generatedOutputs) {
  const personalizedGapCount = generatedOutputs.personalized_gap_count ?? 0;
  return `
    <div class="generated-block">
      <h3>Personalized outputs generated</h3>
      <p>
        Built from your saved profile with ${escapeHtml(String(personalizedGapCount))} targeted gaps.
      </p>
      <div class="generated-paths">
        <div class="generated-path">${escapeHtml(generatedOutputs.analysis_path)}</div>
        <div class="generated-path">${escapeHtml(generatedOutputs.annotated_output)}</div>
        <div class="generated-path">${escapeHtml(generatedOutputs.condensed_output)}</div>
      </div>
    </div>
  `;
}

async function handleRating(ratingValue) {
  const prerequisite = state.knowledgeCheck.prerequisites[state.currentIndex];
  state.ratings[state.currentIndex] = {
    prerequisite_id: prerequisite.id,
    rating: ratingValue
  };
  clearStatus();

  if (state.currentIndex < state.knowledgeCheck.prerequisites.length - 1) {
    state.currentIndex += 1;
    render();
    return;
  }

  await submitKnowledgeCheck();
}

async function submitKnowledgeCheck() {
  state.submitting = true;
  render();

  try {
    const response = await fetchJson("/api/submit-quiz", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        ratings: state.ratings
      })
    });
    state.savedProfile = response.profile;
    state.summaryProfile = response.profile;
    state.submitting = false;
    setStatus("Knowledge check results saved.", "success");
    render();
  } catch (error) {
    state.submitting = false;
    setStatus(error.message || "Failed to save knowledge-check results.", "error");
    render();
  }
}

async function generatePersonalizedPaper() {
  if (state.generating) {
    return;
  }

  state.generating = true;
  setStatus("Generating personalized annotation and condensation…", "info");
  render();

  try {
    const response = await fetchJson("/api/generate-personalized-paper", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({})
    });
    state.generating = false;
    state.summaryProfile = {
      ...state.summaryProfile,
      generated_outputs: response.generated_outputs
    };
    state.savedProfile = {
      ...state.savedProfile,
      generated_outputs: response.generated_outputs
    };
    setStatus("Personalized paper outputs generated.", "success");
    render();
  } catch (error) {
    state.generating = false;
    setStatus(error.message || "Failed to generate personalized paper.", "error");
    render();
  }
}

function retakeKnowledgeCheck() {
  state.ratings = new Array(state.knowledgeCheck.prerequisites.length).fill(null);
  state.currentIndex = 0;
  state.generating = false;
  state.summaryProfile = null;
  clearStatus();
  render();
}

function getKnownTopics(profile) {
  const items = profile.known_topics || profile.strengths || [];
  return Array.isArray(items) ? items : [];
}

function getGapTopics(profile) {
  const items = profile.gap_topics || profile.gaps || [];
  return Array.isArray(items) ? items : [];
}

function importanceClass(importance) {
  const value = String(importance || "important").toLowerCase();
  if (value === "essential" || value === "important" || value === "supporting") {
    return value;
  }
  return "important";
}

function animateStage() {
  elements.stage.classList.remove("stage-enter");
  void elements.stage.offsetWidth;
  elements.stage.classList.add("stage-enter");
}

function setStatus(message, kind) {
  state.status = { message, kind };
}

function clearStatus() {
  state.status = null;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`Request failed: ${response.status}`);
  }
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.message || `Request failed: ${response.status}`);
  }
  return payload;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
