(function () {
  const apiBase = window.API_BASE_URL || "http://localhost:8000";
  const widget = document.getElementById("chatWidget");
  if (!widget) return;

  const labels = {
    en: { title: "JanMitra Assistant", placeholder: "Type your question…", send: "Send", welcome: "Hello! Ask me about government schemes." },
    hi: { title: "जनमित्र सहायक", placeholder: "अपना सवाल लिखें…", send: "भेजें", welcome: "नमस्ते! सरकारी योजनाओं के बारे में पूछें।" }
  };
  let language = "en";
  let history = [];

  const create = (tag, className, text) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };
  const trigger = create("button", "chat-trigger", "💬");
  trigger.type = "button";
  trigger.setAttribute("aria-label", "Open JanMitra Assistant");
  const notification = create("span", "chat-notification");
  notification.setAttribute("aria-hidden", "true");
  trigger.appendChild(notification);

  const panel = create("section", "chat-panel");
  panel.hidden = true;
  panel.setAttribute("aria-label", "JanMitra Assistant");
  const header = create("header", "chat-header");
  const title = create("strong", "chat-title");
  const actions = create("div", "chat-header-actions");
  const enButton = create("button", "chat-language active", "EN");
  const hiButton = create("button", "chat-language", "हिं");
  const close = create("button", "chat-close", "×");
  [enButton, hiButton, close].forEach((button) => { button.type = "button"; actions.appendChild(button); });
  header.append(title, actions);
  const messages = create("div", "chat-messages");
  const form = create("form", "chat-form");
  const input = create("input", "chat-input");
  input.type = "text";
  input.maxLength = 500;
  const send = create("button", "chat-send");
  send.type = "submit";
  form.append(input, send);
  panel.append(header, messages, form);
  widget.append(trigger, panel);

  const addMessage = (role, text) => {
    const bubble = create("div", `chat-message ${role}`, text);
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  };
  const updateLabels = () => {
    const current = labels[language];
    title.textContent = current.title;
    input.placeholder = current.placeholder;
    send.textContent = current.send;
    enButton.classList.toggle("active", language === "en");
    hiButton.classList.toggle("active", language === "hi");
  };
  const setLanguage = (next) => {
    language = next;
    updateLabels();
  };
  const open = () => {
    panel.hidden = false;
    notification.hidden = true;
    trigger.hidden = true;
    input.focus();
  };
  const closePanel = () => {
    panel.hidden = true;
    trigger.hidden = false;
  };
  trigger.addEventListener("click", open);
  close.addEventListener("click", closePanel);
  enButton.addEventListener("click", () => setLanguage("en"));
  hiButton.addEventListener("click", () => setLanguage("hi"));
  input.addEventListener("input", () => { send.disabled = !input.value.trim(); });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    const priorHistory = history.slice(-5);
    addMessage("user", message);
    history.push({ role: "user", content: message });
    input.value = "";
    send.disabled = true;
    try {
      const response = await fetch(`${apiBase}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: priorHistory })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Chat service unavailable.");
      addMessage("assistant", data.reply);
      history.push({ role: "assistant", content: data.reply });
    } catch (error) {
      addMessage("assistant", language === "hi" ? "चैट सेवा उपलब्ध नहीं। हेल्पलाइन पर कॉल करें।" : error.message);
    } finally {
      send.disabled = !input.value.trim();
      input.focus();
    }
  });
  addMessage("assistant", labels.en.welcome);
  updateLabels();
  send.disabled = true;
})();
