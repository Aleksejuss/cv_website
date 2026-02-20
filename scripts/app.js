const state = {
  lang: "en",
  data: { en: null, lt: null },
  observers: {
    section: null,
    reveal: null
  }
};

function get(obj, path) {
  return path.split(".").reduce((acc, part) => (acc ? acc[part] : undefined), obj);
}

async function loadContent() {
  const fetchJson = async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Unable to load ${url}: ${response.status}`);
    }
    return response.json();
  };

  const [en, lt] = await Promise.all([fetchJson("content/cv.en.json"), fetchJson("content/cv.lt.json")]);

  state.data.en = en;
  state.data.lt = lt;
}

function fillStaticLabels(content) {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.getAttribute("data-i18n");
    const value = get(content.ui, key);
    if (value) {
      node.textContent = value;
    }
  });

  const linkedinLink = document.getElementById("linkedin-link");
  linkedinLink.textContent = content.ui.labels.viewLinkedin;
}

function renderHero(profile) {
  const hero = document.getElementById("hero");
  hero.innerHTML = `
    <div class="hero-copy" data-reveal>
      <p class="eyebrow">${profile.location}</p>
      <h1 id="name">${profile.name}</h1>
      <p class="title">${profile.title}</p>
      <p class="intro">${profile.summary}</p>
    </div>
    <figure class="hero-photo" data-reveal>
      <img src="${profile.photo.src}" alt="${profile.photo.alt}" loading="lazy" width="420" height="500">
    </figure>
  `;
}

function renderExperience(entries) {
  const container = document.getElementById("experience-list");
  container.innerHTML = entries
    .map(
      (item) => `
        <article class="entry-card" data-reveal>
          <header>
            <h3>${item.role}</h3>
            <p class="entry-meta">${item.company} · ${item.location}</p>
            <p class="entry-period">${item.period}</p>
          </header>
          <ul>
            ${item.highlights.map((highlight) => `<li>${highlight}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function renderEducation(entries) {
  const container = document.getElementById("education-list");
  container.innerHTML = entries
    .map(
      (item) => `
        <article class="entry-card compact" data-reveal>
          <h3>${item.degree}</h3>
          <p class="entry-meta">${item.institution}</p>
          <p class="entry-period">${item.period}</p>
        </article>
      `
    )
    .join("");
}

function renderSkills(skills) {
  const container = document.getElementById("skills-groups");
  const labels =
    state.lang === "lt"
      ? { technical: "Techniniai", tools: "Įrankiai", languages: "Kalbos" }
      : { technical: "Technical", tools: "Tools", languages: "Languages" };
  const groups = [
    { key: "technical", label: labels.technical },
    { key: "tools", label: labels.tools },
    { key: "languages", label: labels.languages }
  ];

  container.innerHTML = groups
    .map(
      (group) => `
        <article class="skill-group" data-reveal>
          <h3>${group.label}</h3>
          <ul>
            ${(skills[group.key] || []).map((skill) => `<li>${skill}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function renderProjects(projects) {
  const container = document.getElementById("projects-list");
  container.innerHTML = projects
    .map(
      (item) => `
        <article class="entry-card compact" data-reveal>
          <h3>${item.name}</h3>
          <p>${item.summary}</p>
        </article>
      `
    )
    .join("");
}

function renderCertifications(certifications) {
  const container = document.getElementById("certifications-list");
  container.innerHTML = `
    <ul class="cert-list" data-reveal>
      ${certifications.map((cert) => `<li>${cert}</li>`).join("")}
    </ul>
  `;
}

function renderContact(contact) {
  const emailLink = document.getElementById("email-link");
  emailLink.href = contact.email ? `mailto:${contact.email}` : "#";
  emailLink.setAttribute("aria-disabled", contact.email ? "false" : "true");

  const linkedinLink = document.getElementById("linkedin-link");
  linkedinLink.href = contact.linkedin || "#";
  linkedinLink.setAttribute("aria-disabled", contact.linkedin ? "false" : "true");

  document.getElementById("contact-text").textContent = contact.note;
}

function setupReveal() {
  if (state.observers.reveal) {
    state.observers.reveal.disconnect();
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const revealNodes = Array.from(document.querySelectorAll("[data-reveal]"));

  if (reduceMotion) {
    revealNodes.forEach((node) => node.classList.add("is-visible"));
    return;
  }

  state.observers.reveal = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.18 }
  );

  revealNodes.forEach((node, index) => {
    node.style.setProperty("--delay", `${Math.min(index * 40, 320)}ms`);
    state.observers.reveal.observe(node);
  });
}

function setupActiveNavTracking() {
  if (state.observers.section) {
    state.observers.section.disconnect();
  }

  const navLinks = Array.from(document.querySelectorAll(".main-nav a"));
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  state.observers.section = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visible) {
        return;
      }

      navLinks.forEach((link) => {
        const active = link.getAttribute("href") === `#${visible.target.id}`;
        link.classList.toggle("active", active);
        if (active) {
          link.setAttribute("aria-current", "true");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    },
    { threshold: [0.3, 0.6, 0.85], rootMargin: "-22% 0px -55% 0px" }
  );

  sections.forEach((section) => state.observers.section.observe(section));
}

function setupSmoothAnchorScrolling() {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const href = link.getAttribute("href");
      if (!href || href === "#") {
        return;
      }

      const target = document.querySelector(href);
      if (!target) {
        return;
      }

      event.preventDefault();
      target.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "start"
      });

      history.replaceState(null, "", href);
    });
  });
}

function updateLanguageControls(content) {
  document.documentElement.lang = state.lang;
  const langToggle = document.getElementById("lang-toggle");

  if (state.lang === "en") {
    langToggle.textContent = "LT";
    langToggle.setAttribute("aria-label", "Switch to Lithuanian");
  } else {
    langToggle.textContent = "EN";
    langToggle.setAttribute("aria-label", "Switch to English");
  }

  fillStaticLabels(content);
}

function renderFatalError(message) {
  const hero = document.getElementById("hero");
  hero.innerHTML = `<div class="error-banner"><h1 id="name">Content Load Error</h1><p>${message}</p></div>`;
}

function render(content) {
  renderHero(content.profile);
  renderExperience(content.experience);
  renderEducation(content.education);
  renderSkills(content.skills);
  renderProjects(content.projects);
  renderCertifications(content.certifications);
  renderContact(content.contact);
  updateLanguageControls(content);
  setupReveal();
}

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("cv_lang", lang);

  render(state.data[lang]);
}

function setupLanguageToggle() {
  const toggle = document.getElementById("lang-toggle");
  toggle.addEventListener("click", () => {
    const next = state.lang === "en" ? "lt" : "en";
    setLanguage(next);
  });
}

async function init() {
  await loadContent();
  setupLanguageToggle();
  setupSmoothAnchorScrolling();
  setupActiveNavTracking();
  document.getElementById("footer-year").textContent = String(new Date().getFullYear());

  const saved = localStorage.getItem("cv_lang");
  setLanguage(saved === "lt" ? "lt" : "en");
}

init().catch((error) => {
  console.error("Could not initialize CV website", error);
  renderFatalError("The CV content files could not be loaded. Please verify content JSON files.");
});
