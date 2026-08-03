function defaultChatEndpoint() {
  const host = window.location.hostname;
  if (
    host === "sbilmis.org" ||
    host === "www.sbilmis.org" ||
    host.endsWith(".github.io")
  ) {
    return "https://api.sbilmis.org/truba-assistant/chat";
  }
  return "/truba-assistant/chat";
}

const CHAT_ENDPOINT =
  window.TRUBA_ASSISTANT_API_URL || defaultChatEndpoint();

const STORAGE_KEYS = {
  conversationId: "trubaAssistantConversationId",
  userId: "trubaAssistantUserId",
};

const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const sendButton = document.querySelector("#send-button");
const resetButton = document.querySelector("#reset-button");
const statusDot = document.querySelector("#status-dot");
const statusText = document.querySelector("#status-text");
const promptButtons = document.querySelectorAll(".prompt-chip");
const templateCopyButtons = document.querySelectorAll(".template-copy");

let conversationId = localStorage.getItem(STORAGE_KEYS.conversationId) || "";
let userId = localStorage.getItem(STORAGE_KEYS.userId);

if (!userId) {
  userId = `web-${crypto.randomUUID()}`;
  localStorage.setItem(STORAGE_KEYS.userId, userId);
}

function setStatus(label, state = "ready") {
  statusText.textContent = label;
  statusDot.classList.toggle("busy", state === "busy");
  statusDot.classList.toggle("error", state === "error");
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatAnswer(text) {
  const safe = escapeHtml(text.trim());
  const blocks = safe.split(/\n{2,}/).map((block) => {
    const withBreaks = block.replaceAll("\n", "<br>");
    return `<p>${withBreaks}</p>`;
  });
  return blocks.join("");
}

function addMessage(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "You" : "T";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = formatAnswer(text);

  article.append(avatar, bubble);
  messages.append(article);
  messages.scrollTop = messages.scrollHeight;
}

function setBusy(isBusy) {
  sendButton.disabled = isBusy;
  input.disabled = isBusy;
  setStatus(isBusy ? "Thinking" : "Ready", isBusy ? "busy" : "ready");
}

function autosizeTextarea() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 190)}px`;
}

function setInputValue(value) {
  input.value = value.trim();
  autosizeTextarea();
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
}

function flashCopyButton(button, label) {
  const originalLabel = button.textContent;
  button.textContent = label;
  window.setTimeout(() => {
    button.textContent = originalLabel;
  }, 1600);
}

async function copyTemplateToClipboard(button) {
  const template = button
    .closest(".template-card")
    ?.querySelector(".template-text")
    ?.textContent.trim();

  if (!template) return;

  try {
    await navigator.clipboard.writeText(template);
    flashCopyButton(button, "Copied");
  } catch {
    setInputValue(template);
    flashCopyButton(button, "Copied below");
  }
}

async function sendMessage(message) {
  const response = await fetch(CHAT_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId || null,
      user_id: userId,
    }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "The assistant is unavailable right now.");
  }

  if (data.conversation_id) {
    conversationId = data.conversation_id;
    localStorage.setItem(STORAGE_KEYS.conversationId, conversationId);
  }

  return data.answer || "I could not produce an answer for that request.";
}

async function submitMessage(rawMessage) {
  const message = rawMessage.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";
  autosizeTextarea();
  setBusy(true);

  try {
    const answer = await sendMessage(message);
    addMessage("assistant", answer);
  } catch (error) {
    setStatus("Error", "error");
    addMessage(
      "assistant",
      error.message ||
        "Sorry, I could not reach the assistant. Please try again later.",
    );
  } finally {
    setBusy(false);
    input.focus();
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitMessage(input.value.trim());
});

input.addEventListener("input", autosizeTextarea);

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

resetButton.addEventListener("click", () => {
  conversationId = "";
  localStorage.removeItem(STORAGE_KEYS.conversationId);
  messages.replaceChildren();
  addMessage(
    "assistant",
    "Started a new conversation. What would you like to ask about TRUBA?",
  );
  setStatus("Ready");
  input.focus();
});

promptButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setInputValue(button.textContent);
  });
});

templateCopyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    await copyTemplateToClipboard(button);
  });
});

autosizeTextarea();
