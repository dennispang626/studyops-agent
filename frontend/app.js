const CERTIFICATIONS = {
  "AIF-C01": {
    name: "AWS Certified AI Practitioner",
    shortName: "AWS AI Practitioner",
    sources: [
      "https://aws.amazon.com/certification/certified-ai-practitioner/",
      "https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html",
    ],
    domains: [
      "Fundamentals of AI and ML",
      "Fundamentals of generative AI",
      "Applications of foundation models",
      "Guidelines for responsible AI",
      "Security, compliance, and governance for AI solutions",
    ],
    focusTerms: [
      "machine learning",
      "foundation models",
      "generative AI",
      "responsible AI",
      "security",
      "governance",
    ],
  },
  "CLF-C02": {
    name: "AWS Certified Cloud Practitioner",
    shortName: "AWS Cloud Practitioner",
    sources: [
      "https://aws.amazon.com/certification/certified-cloud-practitioner/",
      "https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html",
    ],
    domains: [
      "Cloud concepts",
      "Security and compliance",
      "Cloud technology and services",
      "Billing, pricing, and support",
    ],
    focusTerms: [
      "cloud value proposition",
      "shared responsibility",
      "AWS services",
      "billing",
      "support plans",
    ],
  },
};

const QUESTION_BANK = {
  "AIF-C01": [
    {
      topic: "Fundamentals of AI and ML",
      difficulty: "Foundation",
      stem:
        "A support team has thousands of labeled historical tickets and wants to route new tickets to the correct queue automatically. Which machine learning approach best fits this use case?",
      options: {
        A: "Supervised learning",
        B: "Unsupervised clustering without labels",
        C: "Manual rule writing for every possible ticket",
        D: "Reinforcement learning with a reward signal",
      },
      correct: "A",
      optionExplanations: {
        A: "The historical tickets already include labels, so the model can learn from examples with known outcomes.",
        B: "Clustering can discover groups, but it does not directly learn from the existing queue labels.",
        C: "Manual rules are brittle and do not use the labeled training data effectively.",
        D: "Reinforcement learning is for sequential decisions with rewards, not basic labeled classification.",
      },
    },
    {
      topic: "Fundamentals of generative AI",
      difficulty: "Foundation",
      stem:
        "A marketing team wants to draft product descriptions from short prompts without training its own model. Which AWS service is the most appropriate starting point?",
      options: {
        A: "AWS CloudTrail",
        B: "Amazon Bedrock",
        C: "Amazon Route 53",
        D: "AWS Cost Explorer",
      },
      correct: "B",
      optionExplanations: {
        A: "CloudTrail records account activity and API events; it is not used to generate text.",
        B: "Amazon Bedrock provides access to foundation models for generative AI use cases.",
        C: "Route 53 is DNS networking infrastructure, not a generative AI service.",
        D: "Cost Explorer analyzes spend and usage; it does not create generated content.",
      },
    },
    {
      topic: "Applications of foundation models",
      difficulty: "Scenario",
      stem:
        "A company is building a customer-service assistant that must answer only from approved product documents. Which design choice best reduces unsupported answers?",
      options: {
        A: "Increase the response length for every answer",
        B: "Use retrieval from approved documents and cite the retrieved context",
        C: "Remove all evaluation checks to make the assistant faster",
        D: "Let the model answer from general knowledge when documents are missing",
      },
      correct: "B",
      optionExplanations: {
        A: "Longer answers can still be unsupported if they are not grounded in approved content.",
        B: "Retrieval-grounded generation helps constrain answers to approved sources and gives reviewers citations.",
        C: "Removing evaluations increases quality and safety risk.",
        D: "General knowledge can conflict with current product documents and should not be used for restricted answers.",
      },
    },
    {
      topic: "Guidelines for responsible AI",
      difficulty: "Scenario",
      stem:
        "An HR team wants to use an AI assistant to summarize candidate feedback. Which practice best supports responsible AI for this workflow?",
      options: {
        A: "Use the assistant output as the final hiring decision",
        B: "Avoid reviewing the assistant because summaries are always objective",
        C: "Review outputs for bias, keep humans in the decision loop, and protect sensitive data",
        D: "Store all candidate data in prompts so the assistant has maximum context",
      },
      correct: "C",
      optionExplanations: {
        A: "High-impact decisions need human accountability and should not rely only on generated output.",
        B: "AI summaries can contain bias or omissions, so review is still necessary.",
        C: "Bias review, human oversight, and data protection are core responsible AI practices.",
        D: "Including unnecessary sensitive data increases privacy and security risk.",
      },
    },
    {
      topic: "Security, compliance, and governance for AI solutions",
      difficulty: "Scenario",
      stem:
        "A team uses a generative AI application on AWS and needs to restrict who can invoke models. Which control should they configure first?",
      options: {
        A: "Public access to the model endpoint",
        B: "IAM permissions that follow least privilege",
        C: "A larger context window",
        D: "A lower model temperature",
      },
      correct: "B",
      optionExplanations: {
        A: "Public access would increase risk and is the opposite of controlled access.",
        B: "IAM policies are used to control who can perform actions on AWS resources.",
        C: "Context length affects prompt capacity, not identity-based authorization.",
        D: "Temperature affects response randomness, not access control.",
      },
    },
  ],
  "CLF-C02": [
    {
      topic: "Cloud concepts",
      difficulty: "Foundation",
      stem:
        "A startup wants to avoid buying servers before knowing whether its application will be popular. Which cloud benefit does this best describe?",
      options: {
        A: "Trade fixed expense for variable expense",
        B: "Manually patch all physical hosts",
        C: "Commit to maximum capacity up front",
        D: "Move all responsibility from the customer to AWS",
      },
      correct: "A",
      optionExplanations: {
        A: "Cloud pricing lets customers pay for resources as they use them instead of buying data center capacity up front.",
        B: "Manual physical host management is reduced, but that is not the benefit described here.",
        C: "The cloud helps avoid over-provisioning capacity in advance.",
        D: "The shared responsibility model still gives customers responsibilities.",
      },
    },
    {
      topic: "Security and compliance",
      difficulty: "Scenario",
      stem:
        "Under the AWS shared responsibility model, which task is typically the customer's responsibility?",
      options: {
        A: "Maintaining AWS global infrastructure",
        B: "Replacing physical disks in AWS data centers",
        C: "Managing IAM users and permissions in the AWS account",
        D: "Securing the physical facilities that host AWS Regions",
      },
      correct: "C",
      optionExplanations: {
        A: "AWS is responsible for the security of the cloud, including global infrastructure.",
        B: "AWS manages physical hardware in its data centers.",
        C: "Customers manage identities, permissions, and access decisions inside their own accounts.",
        D: "AWS handles physical security for its facilities.",
      },
    },
    {
      topic: "Cloud technology and services",
      difficulty: "Foundation",
      stem:
        "A company needs durable object storage for images, documents, and backups. Which AWS service should it choose?",
      options: {
        A: "Amazon S3",
        B: "Amazon EC2 Auto Scaling",
        C: "AWS Lambda",
        D: "Amazon Route 53",
      },
      correct: "A",
      optionExplanations: {
        A: "Amazon S3 is object storage designed for durable storage of files and backups.",
        B: "EC2 Auto Scaling adjusts compute capacity, not object storage.",
        C: "Lambda runs code without managing servers; it is not object storage.",
        D: "Route 53 provides DNS and routing features.",
      },
    },
    {
      topic: "Cloud technology and services",
      difficulty: "Scenario",
      stem:
        "A developer wants to run code in response to events without managing servers. Which AWS service is the best fit?",
      options: {
        A: "Amazon VPC",
        B: "AWS Lambda",
        C: "AWS Organizations",
        D: "AWS Artifact",
      },
      correct: "B",
      optionExplanations: {
        A: "Amazon VPC provides networking isolation, not serverless event-driven code execution.",
        B: "AWS Lambda runs code in response to events without requiring server management.",
        C: "AWS Organizations manages multiple AWS accounts.",
        D: "AWS Artifact provides compliance reports and agreements.",
      },
    },
    {
      topic: "Billing, pricing, and support",
      difficulty: "Foundation",
      stem:
        "A finance team wants to estimate monthly AWS costs before launching a workload. Which tool should it use?",
      options: {
        A: "AWS Pricing Calculator",
        B: "AWS CloudTrail",
        C: "Amazon CloudWatch Logs",
        D: "AWS Identity and Access Management",
      },
      correct: "A",
      optionExplanations: {
        A: "AWS Pricing Calculator helps estimate costs before deployment.",
        B: "CloudTrail records API activity and account events.",
        C: "CloudWatch Logs stores and analyzes logs, not pre-launch cost estimates.",
        D: "IAM manages access and permissions.",
      },
    },
  ],
};

const API_BASE = (
  window.STUDYOPS_API_BASE_URL ||
  localStorage.getItem("studyops_api_base") ||
  ""
).replace(/\/$/, "");

const SESSION_SETTINGS_KEY = "studyops_session_settings";

const state = {
  activeDomainIndex: 0,
  provider: "AWS",
  certification: "AIF-C01",
  learnerId: "demo-learner",
  learnerGoal: "",
  hoursPerWeek: 5,
  questionCount: 5,
  setupDirty: false,
  trace: [],
  sources: [],
  notes: [],
  plan: null,
  quiz: null,
  feedback: [],
  memory: null,
  contextResults: [],
};

const els = {};

document.addEventListener("DOMContentLoaded", () => {
  bindElements();
  loadSetupSettings();
  bindEvents();
  hydrateInputs();
  loadSessionMemory();
  runWorkflow({ preferApi: false });
});

function bindElements() {
  [
    "connectionStatus",
    "exportButton",
    "resetButton",
    "runWorkflowButton",
    "providerSelect",
    "certificationSelect",
    "saveSetupButton",
    "setupStatus",
    "learnerIdInput",
    "goalInput",
    "hoursInput",
    "hoursOutput",
    "questionCountInput",
    "questionCountOutput",
    "sourceUrlInput",
    "classifySourceButton",
    "fileInput",
    "addFilesButton",
    "sourceMetric",
    "sourceList",
    "homeCertificationMetric",
    "homeNoteMetric",
    "homeScoreMetric",
    "homeRetryMetric",
    "traceMetric",
    "traceList",
    "planMetric",
    "planTitle",
    "domainList",
    "activeDomainTitle",
    "activeDomainHours",
    "activeStudyGuide",
    "studyChecklist",
    "noteMetric",
    "ragQueryInput",
    "retrieveButton",
    "noteList",
    "contextResults",
    "quizMetric",
    "quizForm",
    "submitQuizButton",
    "retryButton",
    "feedbackPanel",
    "confidenceValue",
    "confidenceMeter",
    "weakTopicList",
    "retryQueueList",
    "attemptList",
  ].forEach((id) => {
    els[id] = document.getElementById(id);
  });
}

function bindEvents() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => setPage(button.dataset.page));
  });

  els.providerSelect.addEventListener("change", markSetupDirty);
  els.certificationSelect.addEventListener("change", markSetupDirty);
  els.learnerIdInput.addEventListener("change", () => {
    els.learnerIdInput.value = normalizeLearnerId(els.learnerIdInput.value);
    markSetupDirty();
  });
  els.goalInput.addEventListener("input", markSetupDirty);
  els.hoursInput.addEventListener("input", () => {
    els.hoursOutput.textContent = els.hoursInput.value;
    markSetupDirty();
  });
  els.questionCountInput.addEventListener("input", () => {
    els.questionCountOutput.textContent = els.questionCountInput.value;
    markSetupDirty();
  });
  els.saveSetupButton.addEventListener("click", () => {
    saveSetup({ preferApi: false });
  });
  els.runWorkflowButton.addEventListener("click", () => {
    saveSetup({ preferApi: true });
  });
  els.classifySourceButton.addEventListener("click", classifyEnteredSource);
  els.addFilesButton.addEventListener("click", addSelectedFilesAsNotes);
  els.retrieveButton.addEventListener("click", retrieveContext);
  els.quizForm.addEventListener("submit", submitQuiz);
  els.retryButton.addEventListener("click", retryWeakTopics);
  els.exportButton.addEventListener("click", exportWorkflowJson);
  els.resetButton.addEventListener("click", resetMemory);
}

function setPage(pageId) {
  document.querySelectorAll(".page").forEach((page) => {
    page.classList.toggle("active", page.id === pageId);
  });
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.page === pageId);
  });
}

function hydrateInputs() {
  state.provider = els.providerSelect.value;
  state.certification = els.certificationSelect.value;
  state.learnerId = normalizeLearnerId(els.learnerIdInput.value);
  state.learnerGoal = els.goalInput.value.trim();
  state.hoursPerWeek = Number(els.hoursInput.value);
  state.questionCount = Number(els.questionCountInput.value);
  els.hoursOutput.textContent = String(state.hoursPerWeek);
  els.questionCountOutput.textContent = String(state.questionCount);
}

function loadSetupSettings() {
  const raw = localStorage.getItem(SESSION_SETTINGS_KEY);
  if (!raw) {
    return;
  }

  try {
    const settings = JSON.parse(raw);
    if (settings.provider && optionExists(els.providerSelect, settings.provider)) {
      els.providerSelect.value = settings.provider;
    }
    if (settings.certification && optionExists(els.certificationSelect, settings.certification)) {
      els.certificationSelect.value = settings.certification;
    }
    if (settings.learnerId) {
      els.learnerIdInput.value = normalizeLearnerId(settings.learnerId);
    }
    if (typeof settings.learnerGoal === "string") {
      els.goalInput.value = settings.learnerGoal;
    }
    if (settings.hoursPerWeek) {
      els.hoursInput.value = String(clamp(settings.hoursPerWeek, 1, 20));
    }
    if (settings.questionCount) {
      els.questionCountInput.value = String(clamp(settings.questionCount, 1, 10));
    }
  } catch (error) {
    localStorage.removeItem(SESSION_SETTINGS_KEY);
  }
}

function saveSetupSettings() {
  localStorage.setItem(
    SESSION_SETTINGS_KEY,
    JSON.stringify({
      provider: state.provider,
      certification: state.certification,
      learnerId: state.learnerId,
      learnerGoal: state.learnerGoal,
      hoursPerWeek: state.hoursPerWeek,
      questionCount: state.questionCount,
      savedAt: new Date().toISOString(),
    }),
  );
}

async function saveSetup({ preferApi }) {
  hydrateInputs();
  state.activeDomainIndex = 0;
  saveSetupSettings();
  await runWorkflow({ preferApi });
  state.setupDirty = false;
  renderSetupStatus();
  setConnectionStatus(`Setup saved: ${state.certification}`);
}

function markSetupDirty() {
  state.setupDirty = true;
  renderSetupStatus();
}

function renderSetupStatus() {
  els.setupStatus.textContent = state.setupDirty ? "Unsaved changes" : "Saved";
  els.setupStatus.classList.toggle("dirty", state.setupDirty);
  els.setupStatus.classList.toggle("saved", !state.setupDirty);
}

async function runWorkflow({ preferApi }) {
  hydrateInputs();
  loadSessionMemory();
  setConnectionStatus(preferApi && API_BASE ? "Connecting to backend" : "Local demo mode");

  if (preferApi && API_BASE) {
    try {
      const response = await fetch(`${API_BASE}/api/studyops/workflow`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          learner_id: state.learnerId,
          certification: state.certification,
          learner_goal: state.learnerGoal,
          uploaded_file_paths: [],
          hours_per_week: state.hoursPerWeek,
          question_count: state.questionCount,
        }),
      });
      if (!response.ok) {
        throw new Error(`Workflow request failed with ${response.status}`);
      }
      applyBackendWorkflow(await response.json());
      setConnectionStatus("Backend workflow");
      renderAll();
      return;
    } catch (error) {
      setConnectionStatus("Local fallback");
    }
  }

  applyLocalWorkflow();
  renderAll();
}

function applyBackendWorkflow(payload) {
  const quiz = payload.practice_quiz || payload.quiz || {};
  state.trace = payload.trace || [];
  state.sources = (payload.source_map && payload.source_map.sources) || [];
  state.plan = payload.study_plan || null;
  state.quiz = enrichQuiz(quiz);
  state.notes = [
    noteFromSourceMap(payload),
    ...state.notes.filter((note) => note.kind === "upload" || note.kind === "manual"),
  ].filter(Boolean);
  state.memory = normalizeMemory(payload.memory || state.memory || createEmptyMemory());
  saveSessionMemory();
}

function applyLocalWorkflow() {
  const cert = currentCertification();
  const sourceMapNote = buildSourceMapNote(cert);
  state.sources = cert.sources.map((url) => classifySource(url));
  state.notes = [
    sourceMapNote,
    ...state.notes.filter((note) => note.kind === "upload" || note.kind === "manual"),
  ];
  state.plan = buildStudyPlan(cert);
  state.quiz = buildPracticeQuiz(cert, state.questionCount);
  state.trace = buildTrace(cert);
  state.feedback = [];
  setConnectionStatus(API_BASE ? "Local fallback" : "Local demo mode");
}

function currentCertification() {
  return CERTIFICATIONS[state.certification] || CERTIFICATIONS["AIF-C01"];
}

function buildTrace(cert) {
  return [
    {
      agent: "Source Curator Agent",
      action: "Selected official certification source candidates",
      output: `${cert.sources.length} source candidates for ${state.certification}`,
    },
    {
      agent: "Trust and Noise Filter Agent",
      action: "Checked source trust and blocked exam-dump patterns",
      output: `${state.sources.filter((source) => source.allowed).length} sources allowed`,
    },
    {
      agent: "Knowledge Architect Agent",
      action: "Created Obsidian-style notes and refreshed local RAG context",
      output: `${state.notes.length} notes ready`,
    },
    {
      agent: "Study Planner Agent",
      action: "Converted blueprint domains into weekly focus blocks",
      output: `${cert.domains.length} domains planned`,
    },
    {
      agent: "Practice Coach Agent",
      action: "Generated safe exam-style practice questions",
      output: `${state.questionCount} questions generated`,
    },
    {
      agent: "Examiner and Remediation Agent",
      action: "Loaded weak topics, attempts, and retry queue",
      output: `${state.memory.retryQueue.length} pending retry items`,
    },
  ];
}

function buildSourceMapNote(cert) {
  return {
    id: `${state.certification}-source-map`,
    kind: "source_map",
    title: `${cert.shortName} official source map`,
    source: cert.sources[0],
    citation: cert.sources[0],
    domain: "source_map",
    body: [
      `Certification: ${cert.name} (${state.certification})`,
      `Domains: ${cert.domains.join(", ")}`,
      `Focus terms: ${cert.focusTerms.join(", ")}`,
      "Safety: no real exam dumps, no guaranteed-pass claims, cite sources.",
    ].join("\n"),
  };
}

function buildStudyPlan(cert) {
  const hours = clamp(Number(state.hoursPerWeek), 1, 40);
  const domainHours = Math.max(1, Math.round((hours / cert.domains.length) * 10) / 10);
  return {
    certification: state.certification,
    certification_name: cert.name,
    learner_goal: state.learnerGoal,
    hours_per_week: hours,
    weekly_plan: cert.domains.map((domain, index) => ({
      week: index + 1,
      focus: domain,
      estimated_hours: domainHours,
      key_terms: cert.focusTerms.slice(index, index + 3).concat(cert.focusTerms.slice(0, 2)).slice(0, 3),
      tasks: [
        "Read cited source notes",
        "Write one concise Obsidian note",
        "Answer practice questions",
        "Retry missed topics",
      ],
    })),
  };
}

function buildPracticeQuiz(cert, count, retryTopics = []) {
  const boundedCount = clamp(Number(count), 1, 10);
  const questions = Array.from({ length: boundedCount }, (_, index) => {
    const retryTopic = retryTopics[index % Math.max(retryTopics.length, 1)];
    return buildQuestion(cert, retryTopic, index + 1);
  });
  return {
    certification: state.certification,
    disclaimer: "Generated exam-style practice, not official questions.",
    question_count: questions.length,
    questions,
    citations: [...new Set(questions.map((question) => question.citation).filter(Boolean))],
    retrieval_backend: "browser-local",
  };
}

function buildQuestion(cert, preferredTopic, questionNumber) {
  const template = pickQuestionTemplate(preferredTopic, questionNumber);
  const citation = state.notes[0] ? state.notes[0].citation : cert.sources[0];
  return {
    question_id: `${state.certification}-PRACTICE-${String(questionNumber).padStart(3, "0")}`,
    certification: state.certification,
    topic: template.topic,
    difficulty: template.difficulty,
    question: template.stem,
    options: template.options,
    correct_answer: template.correct,
    explanation: template.optionExplanations[template.correct],
    option_explanations: template.optionExplanations,
    citation,
  };
}

function pickQuestionTemplate(preferredTopic, questionNumber) {
  const bank = QUESTION_BANK[state.certification] || QUESTION_BANK["AIF-C01"];
  const matching = preferredTopic
    ? bank.find((question) => question.topic === preferredTopic)
    : null;
  return matching || bank[(questionNumber - 1) % bank.length];
}

function enrichQuiz(quiz) {
  const cert = currentCertification();
  return {
    ...quiz,
    questions: (quiz.questions || []).map((question, index) => ({
      ...buildQuestion(cert, question.topic || cert.domains[index % cert.domains.length], index + 1),
      ...question,
      option_explanations:
        question.option_explanations ||
        buildQuestion(cert, question.topic || cert.domains[index % cert.domains.length], index + 1)
          .option_explanations,
    })),
  };
}

function classifySource(url) {
  const lowered = String(url || "").toLowerCase();
  const hasBlockedLanguage =
    lowered.includes("dump") ||
    lowered.includes("braindump") ||
    lowered.includes("guaranteed-pass") ||
    lowered.includes("guaranteed pass") ||
    lowered.includes("real exam") ||
    lowered.includes("real-exam");
  const official = lowered.includes("aws.amazon.com") || lowered.includes("docs.aws.amazon.com");
  const trusted = official || lowered.includes("github.com");
  return {
    url,
    domain: domainFromUrl(url),
    trust_level: official ? "official" : trusted ? "trusted" : "unverified",
    allowed: Boolean(url) && !hasBlockedLanguage,
    reasons: [
      official ? "Official AWS source" : trusted ? "Trusted technical source" : "Needs review",
    ],
    flags: hasBlockedLanguage ? ["exam_dump_language"] : [],
  };
}

function classifyEnteredSource() {
  const url = els.sourceUrlInput.value.trim();
  if (!url) {
    return;
  }
  const source = classifySource(url);
  state.sources = [source, ...state.sources.filter((item) => item.url !== url)];
  if (source.allowed) {
    state.notes = [
      {
        id: `manual-${Date.now()}`,
        kind: "manual",
        title: `Reviewed source: ${domainFromUrl(url)}`,
        source: url,
        citation: url,
        domain: "manual_source",
        body: `Source candidate classified as ${source.trust_level}. Review before using for study.`,
      },
      ...state.notes,
    ];
  }
  els.sourceUrlInput.value = "";
  renderAll();
}

async function addSelectedFilesAsNotes() {
  const files = Array.from(els.fileInput.files || []);
  if (!files.length) {
    return;
  }
  const notes = [];
  for (const file of files) {
    let body = "";
    try {
      body = await file.text();
    } catch (error) {
      body = `${file.name} selected for future backend parsing.`;
    }
    notes.push({
      id: `upload-${file.name}-${Date.now()}`,
      kind: "upload",
      title: file.name,
      source: "Browser upload",
      citation: file.name,
      domain: "user_upload",
      body: body.slice(0, 4000) || `${file.name} selected for StudyOps ingestion.`,
    });
  }
  state.notes = [...notes, ...state.notes];
  els.fileInput.value = "";
  retrieveContext();
  renderAll();
}

function retrieveContext() {
  const query = els.ragQueryInput.value.trim().toLowerCase();
  const cert = currentCertification();
  const activeDomain = getActiveWeek();
  const fallbackQuery = [activeDomain.focus, ...cert.focusTerms].join(" ");
  const terms = tokenize(query || fallbackQuery);
  state.contextResults = state.notes
    .map((note) => {
      const haystack = `${note.title} ${note.body}`.toLowerCase();
      const score = terms.reduce((total, term) => total + (haystack.includes(term) ? 1 : 0), 0);
      return { note, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 4);
  renderContext();
}

function submitQuiz(event) {
  event.preventDefault();
  if (!state.quiz || !state.quiz.questions.length) {
    return;
  }

  const results = state.quiz.questions.map((question) => {
    const selected = (
      document.querySelector(`input[name="${question.question_id}"]:checked`) || {}
    ).value;
    return {
      question_id: question.question_id,
      selected_answer: selected || "",
      correct_answer: question.correct_answer,
      correct: selected === question.correct_answer,
      topic: question.topic,
      explanation: question.explanation,
      question,
    };
  });

  const correctCount = results.filter((result) => result.correct).length;
  const score = Math.round((correctCount / results.length) * 100);
  const attempt = {
    id: Date.now(),
    certification: state.certification,
    score,
    created_at: new Date().toISOString(),
  };

  state.memory.attempts.unshift(attempt);
  results.forEach((result) => updateTopicMemory(result));
  state.feedback = results;
  saveSessionMemory();
  renderMemory();
  renderFeedback();
  setConnectionStatus(`Scored ${score}%`);
}

function updateTopicMemory(result) {
  const existing = state.memory.weakTopics[result.topic] || {
    topic: result.topic,
    misses: 0,
    mastery_score: 0,
    last_seen_at: "",
  };
  existing.last_seen_at = new Date().toISOString();
  if (result.correct) {
    existing.mastery_score = clamp(existing.mastery_score + 0.15, 0, 1);
  } else {
    existing.misses += 1;
    existing.mastery_score = clamp(existing.mastery_score - 0.35, 0, 1);
    state.memory.retryQueue.unshift({
      id: Date.now() + Math.random(),
      certification: state.certification,
      topic: result.topic,
      status: "pending",
      due_at: existing.last_seen_at,
    });
  }
  state.memory.weakTopics[result.topic] = existing;
}

function retryWeakTopics() {
  const cert = currentCertification();
  const retryTopics = state.memory.retryQueue
    .filter((item) => item.certification === state.certification)
    .map((item) => item.topic);
  if (!retryTopics.length) {
    setConnectionStatus("No retry items");
    return;
  }
  state.quiz = buildPracticeQuiz(cert, Math.min(retryTopics.length, state.questionCount), retryTopics);
  state.feedback = [];
  renderQuiz();
  renderFeedback();
  setConnectionStatus("Retry queue loaded");
}

function renderAll() {
  renderSetupStatus();
  renderHomeMetrics();
  renderSources();
  renderDomains();
  renderActiveStudy();
  renderNotes();
  renderContext();
  renderQuiz();
  renderFeedback();
  renderTrace();
  renderMemory();
}

function renderHomeMetrics() {
  els.homeCertificationMetric.textContent = state.certification;
  els.homeNoteMetric.textContent = String(state.notes.length);
  els.homeRetryMetric.textContent = String((state.memory.retryQueue || []).length);
  const latestAttempt = (state.memory.attempts || [])[0];
  els.homeScoreMetric.textContent = latestAttempt ? `${latestAttempt.score}%` : "0%";
}

function renderSources() {
  els.sourceMetric.textContent = `${state.sources.length} sources`;
  els.sourceList.innerHTML = "";
  if (!state.sources.length) {
    els.sourceList.append(emptyState("No sources yet."));
    return;
  }
  state.sources.forEach((source) => {
    const row = document.createElement("div");
    row.className = "source-row";
    const chipClass = source.allowed
      ? source.trust_level === "unverified"
        ? "trust-chip warning"
        : "trust-chip"
      : "trust-chip blocked";
    row.innerHTML = `
      <strong>${escapeHtml(source.domain || "Unknown source")}</strong>
      <span>${escapeHtml(source.url)}</span>
      <span class="${chipClass}">${source.allowed ? source.trust_level : "blocked"}</span>
    `;
    els.sourceList.append(row);
  });
}

function renderDomains() {
  const plan = state.plan || buildStudyPlan(currentCertification());
  els.planTitle.textContent = `${plan.certification} weekly study plan`;
  els.planMetric.textContent = `${plan.weekly_plan.length} domains`;
  els.domainList.innerHTML = "";
  plan.weekly_plan.forEach((week, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `domain-row ${index === state.activeDomainIndex ? "active" : ""}`;
    button.innerHTML = `
      <strong>Week ${week.week}: ${escapeHtml(week.focus)}</strong>
      <span>${week.estimated_hours} hours target</span>
    `;
    button.addEventListener("click", () => {
      state.activeDomainIndex = index;
      renderDomains();
      renderActiveStudy();
      retrieveContext();
    });
    els.domainList.append(button);
  });
}

function renderActiveStudy() {
  const cert = currentCertification();
  const week = getActiveWeek();
  const terms = week.key_terms || cert.focusTerms.slice(0, 3);
  els.activeDomainTitle.textContent = week.focus;
  els.activeDomainHours.textContent = `${week.estimated_hours}h`;
  els.activeStudyGuide.innerHTML = "";

  [
    {
      title: "Study objective",
      body: `Explain ${week.focus} using your own examples and cite at least one trusted source.`,
      bullets: [
        `Connect this domain to ${state.certification} exam readiness.`,
        "Write one short note that could teach the concept to another learner.",
      ],
    },
    {
      title: "Key terms to master",
      body: terms.join(", "),
      bullets: terms.map((term) => `Define ${term} and give a workplace example.`),
    },
    {
      title: "Active recall prompt",
      body: `Without looking at notes, explain how ${terms[0]} affects a real AWS decision.`,
      bullets: [
        "Compare your answer against retrieved context.",
        "Turn missing details into retry questions.",
      ],
    },
  ].forEach((card) => {
    const node = document.createElement("article");
    node.className = "study-card";
    node.innerHTML = `
      <strong>${escapeHtml(card.title)}</strong>
      <span>${escapeHtml(card.body)}</span>
      <ul>${card.bullets.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    `;
    els.activeStudyGuide.append(node);
  });

  els.studyChecklist.innerHTML = "";
  [
    "Read one trusted source or uploaded note.",
    "Write the concept in your own words.",
    "Retrieve context and verify citations.",
    "Answer at least one practice question for this domain.",
    "Move missed concepts into the retry queue.",
  ].forEach((item, index) => {
    const id = `check-${state.certification}-${state.activeDomainIndex}-${index}`;
    const row = document.createElement("label");
    row.className = "check-row";
    row.innerHTML = `<input type="checkbox" id="${id}" /> <span>${escapeHtml(item)}</span>`;
    els.studyChecklist.append(row);
  });
}

function renderNotes() {
  els.noteMetric.textContent = `${state.notes.length} notes`;
  els.noteList.innerHTML = "";
  if (!state.notes.length) {
    els.noteList.append(emptyState("No notes yet."));
    return;
  }
  state.notes.slice(0, 10).forEach((note) => {
    const row = document.createElement("div");
    row.className = "note-row";
    row.innerHTML = `
      <strong>${escapeHtml(note.title)}</strong>
      <span>${escapeHtml(note.domain)} | ${escapeHtml(note.citation || note.source)}</span>
      <span>${escapeHtml(note.body.slice(0, 190))}</span>
    `;
    els.noteList.append(row);
  });
}

function renderContext() {
  els.contextResults.innerHTML = "";
  if (!state.contextResults.length) {
    els.contextResults.append(emptyState("Run retrieval to view cited context for the active domain."));
    return;
  }
  state.contextResults.forEach((item) => {
    const row = document.createElement("div");
    row.className = "context-row";
    row.innerHTML = `
      <strong>${escapeHtml(item.note.title)}</strong>
      <span>Score ${item.score} | Citation: ${escapeHtml(item.note.citation)}</span>
      <span>${escapeHtml(item.note.body.slice(0, 220))}</span>
    `;
    els.contextResults.append(row);
  });
}

function renderQuiz() {
  const questions = (state.quiz && state.quiz.questions) || [];
  els.quizMetric.textContent = `${questions.length} ready`;
  els.quizForm.innerHTML = "";
  if (!questions.length) {
    els.quizForm.append(emptyState("Run workflow to generate practice."));
    return;
  }
  questions.forEach((question, index) => {
    const fieldset = document.createElement("fieldset");
    fieldset.className = "question-block";
    const options = Object.entries(question.options)
      .map(
        ([key, value]) => `
          <label class="question-option">
            <input type="radio" name="${escapeHtml(question.question_id)}" value="${key}" />
            <span><strong>${key}.</strong> ${escapeHtml(value)}</span>
          </label>
        `,
      )
      .join("");
    fieldset.innerHTML = `
      <legend>${index + 1}. ${escapeHtml(question.question)}</legend>
      <div class="question-meta">
        <span class="difficulty-chip">${escapeHtml(question.topic)}</span>
        <span class="difficulty-chip">${escapeHtml(question.difficulty || "Practice")}</span>
      </div>
      <div class="question-options">${options}</div>
    `;
    els.quizForm.append(fieldset);
  });
}

function renderFeedback() {
  els.feedbackPanel.innerHTML = "";
  if (!state.feedback.length) {
    return;
  }
  state.feedback.forEach((item) => {
    const question = item.question;
    const row = document.createElement("div");
    row.className = `feedback-row ${item.correct ? "correct" : "incorrect"}`;
    row.innerHTML = `
      <strong>${item.correct ? "Correct" : "Needs review"}: ${escapeHtml(item.topic)}</strong>
      <span>Selected ${escapeHtml(item.selected_answer || "none")} | Correct ${escapeHtml(item.correct_answer)}</span>
      <span>${escapeHtml(buildAnswerSummary(item))}</span>
      <div class="option-explanations">
        ${Object.keys(question.options)
          .map((key) => renderOptionExplanation(question, item, key))
          .join("")}
      </div>
    `;
    els.feedbackPanel.append(row);
  });
}

function renderOptionExplanation(question, item, key) {
  const correct = key === question.correct_answer;
  const selectedWrong = key === item.selected_answer && !item.correct;
  const label = correct ? "correct" : selectedWrong ? "selected-wrong" : "";
  return `
    <div class="option-explanation-row ${label}">
      <strong>${key} ${correct ? "is correct" : "is wrong"}</strong>
      <span>${escapeHtml(question.option_explanations[key] || "")}</span>
    </div>
  `;
}

function buildAnswerSummary(item) {
  const question = item.question;
  const selected = item.selected_answer || "none";
  const selectedExplanation =
    question.option_explanations[selected] || "No answer was selected, so this should be retried.";
  const correctExplanation = question.option_explanations[item.correct_answer] || item.explanation;

  if (item.correct) {
    return `Correct is ${item.correct_answer}, because ${correctExplanation}`;
  }
  return `Correct is ${item.correct_answer}, because ${correctExplanation} Your selected answer ${selected} is wrong because ${selectedExplanation}`;
}

function renderTrace() {
  els.traceMetric.textContent = `${state.trace.length} steps`;
  els.traceList.innerHTML = "";
  if (!state.trace.length) {
    els.traceList.append(emptyState("No agent trace yet."));
    return;
  }
  state.trace.forEach((step, index) => {
    const item = document.createElement("div");
    item.className = "trace-item";
    item.innerHTML = `
      <div class="trace-index">${index + 1}</div>
      <div>
        <strong>${escapeHtml(step.agent)}</strong>
        <span>${escapeHtml(step.action)}</span>
        <span>${escapeHtml(step.output)}</span>
      </div>
    `;
    els.traceList.append(item);
  });
}

function renderMemory() {
  const attempts = state.memory.attempts || [];
  const weakTopics = Object.values(state.memory.weakTopics || {}).sort(
    (a, b) => b.misses - a.misses,
  );
  const retryQueue = state.memory.retryQueue || [];
  const confidence = calculateConfidence(attempts);

  els.confidenceValue.textContent = `${confidence}%`;
  els.confidenceMeter.style.width = `${confidence}%`;

  renderCompactRows(
    els.weakTopicList,
    weakTopics,
    (topic) => `${topic.topic}`,
    (topic) => `${topic.misses} misses | mastery ${Math.round(topic.mastery_score * 100)}%`,
    "No weak topics recorded.",
  );
  renderCompactRows(
    els.retryQueueList,
    retryQueue.slice(0, 8),
    (item) => item.topic,
    (item) => item.status,
    "Retry queue is clear.",
  );
  renderCompactRows(
    els.attemptList,
    attempts.slice(0, 8),
    (attempt) => `${attempt.certification} score ${attempt.score}%`,
    (attempt) => new Date(attempt.created_at).toLocaleString(),
    "No attempts yet.",
  );
}

function renderCompactRows(container, items, titleFn, subtitleFn, emptyText) {
  container.innerHTML = "";
  if (!items.length) {
    container.append(emptyState(emptyText));
    return;
  }
  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "compact-row";
    row.innerHTML = `
      <strong>${escapeHtml(titleFn(item))}</strong>
      <span>${escapeHtml(subtitleFn(item))}</span>
    `;
    container.append(row);
  });
}

function getActiveWeek() {
  const plan = state.plan || buildStudyPlan(currentCertification());
  return plan.weekly_plan[state.activeDomainIndex] || plan.weekly_plan[0];
}

function loadSessionMemory() {
  const raw = localStorage.getItem(memoryKey());
  state.memory = raw ? normalizeMemory(JSON.parse(raw)) : createEmptyMemory();
}

function saveSessionMemory() {
  localStorage.setItem(memoryKey(), JSON.stringify(state.memory));
}

function resetMemory() {
  localStorage.removeItem(memoryKey());
  state.memory = createEmptyMemory();
  state.feedback = [];
  applyLocalWorkflow();
  renderAll();
}

function createEmptyMemory() {
  return {
    learner_id: state.learnerId,
    certification: state.certification,
    attempts: [],
    weakTopics: {},
    retryQueue: [],
  };
}

function normalizeMemory(memory) {
  return {
    learner_id: memory.learner_id || state.learnerId,
    certification: memory.certification || state.certification,
    attempts: memory.attempts || [],
    weakTopics: Array.isArray(memory.weak_topics)
      ? Object.fromEntries(memory.weak_topics.map((item) => [item.topic, item]))
      : memory.weakTopics || {},
    retryQueue: memory.retry_queue || memory.retryQueue || [],
  };
}

function noteFromSourceMap(payload) {
  const note = payload.source_map && payload.source_map.note;
  if (!note) {
    return null;
  }
  return {
    id: note.path || `${payload.certification}-source-map`,
    kind: "source_map",
    title: note.title || `${payload.certification} source map`,
    source: note.source_url || "",
    citation: note.path || note.source_url || "",
    domain: "source_map",
    body: `${payload.certification_name || payload.certification} source map generated by backend workflow.`,
  };
}

function memoryKey() {
  return `studyops_memory:${state.learnerId}:${state.certification}`;
}

function normalizeLearnerId(value) {
  return String(value || "demo-learner").trim() || "demo-learner";
}

function calculateConfidence(attempts) {
  if (!attempts.length) {
    return 0;
  }
  const recent = attempts.slice(0, 5);
  const average = recent.reduce((sum, attempt) => sum + Number(attempt.score || 0), 0) / recent.length;
  return Math.round(average);
}

function exportWorkflowJson() {
  const payload = {
    provider: state.provider,
    certification: state.certification,
    learner_id: state.learnerId,
    trace: state.trace,
    sources: state.sources,
    notes: state.notes,
    study_plan: state.plan,
    practice_quiz: state.quiz,
    memory: state.memory,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `studyops-${state.certification.toLowerCase()}-workflow.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function setConnectionStatus(text) {
  els.connectionStatus.textContent = text;
}

function emptyState(text) {
  const node = document.createElement("div");
  node.className = "empty-state";
  node.textContent = text;
  return node;
}

function domainFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch (error) {
    return "";
  }
}

function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .match(/[a-z][a-z0-9+-]{1,}/g) || [];
}

function clamp(value, minimum, maximum) {
  return Math.min(Math.max(Number(value), minimum), maximum);
}

function optionExists(select, value) {
  return Array.from(select.options).some((option) => option.value === value);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
