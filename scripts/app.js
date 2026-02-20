const state = {
  lang: "en",
  data: { en: null, lt: null }
};

async function loadContent() {
  const [en, lt] = await Promise.all([
    fetch("content/cv.en.json").then((r) => r.json()),
    fetch("content/cv.lt.json").then((r) => r.json())
  ]);

  state.data.en = en;
  state.data.lt = lt;
}

function translateStaticText(content) {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const value = key.split(".").reduce((acc, part) => (acc ? acc[part] : undefined), content.ui);
    if (value) {
      el.textContent = value;
    }
  });
}

function render(content) {
  const profile = content.profile;

  const hero = document.getElementById("hero");
  hero.innerHTML = `
    <p class="eyebrow">${profile.location}</p>
    <h1 id="name">${profile.name}</h1>
    <p>${profile.title}</p>
  `;

  document.getElementById("profile-summary").textContent = profile.summary;
  document.getElementById("contact-text").textContent = content.contact.note;

  const email = document.getElementById("email-link");
  email.href = `mailto:${content.contact.email}`;

  const linkedin = document.getElementById("linkedin-link");
  linkedin.href = content.contact.linkedin;

  translateStaticText(content);
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("cv_lang", lang);

  const content = state.data[lang];
  render(content);

  const toggle = document.getElementById("lang-toggle");
  toggle.textContent = lang === "en" ? "LT" : "EN";
}

function initLanguageToggle() {
  const toggle = document.getElementById("lang-toggle");
  toggle.addEventListener("click", () => {
    setLanguage(state.lang === "en" ? "lt" : "en");
  });
}

async function init() {
  await loadContent();
  initLanguageToggle();

  const saved = localStorage.getItem("cv_lang");
  const initialLang = saved === "lt" ? "lt" : "en";
  setLanguage(initialLang);
}

init().catch((error) => {
  console.error("Could not initialize site", error);
});
