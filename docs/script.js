/* Hundun Robotics — interactions */

(function () {
  "use strict";

  const canvas = document.getElementById("stars");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let stars = [];
    let w, h, dpr;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = window.innerWidth;
      h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      initStars();
    }

    function initStars() {
      const count = Math.floor((w * h) / 9000);
      stars = [];
      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          r: Math.random() * 1.2 + 0.2,
          a: Math.random() * 0.6 + 0.15,
          s: Math.random() * 0.15 + 0.02,
        });
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (const s of stars) {
        s.y += s.s;
        if (s.y > h) {
          s.y = 0;
          s.x = Math.random() * w;
        }
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200, 220, 255, ${s.a})`;
        ctx.fill();
      }
      requestAnimationFrame(draw);
    }

    resize();
    draw();
    window.addEventListener("resize", resize);
  }

  const nav = document.querySelector(".nav");
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.querySelector(".nav-links");

  function onScroll() {
    if (window.scrollY > 40) {
      nav.classList.add("scrolled");
    } else {
      nav.classList.remove("scrolled");
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
    navLinks.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => navLinks.classList.remove("open"));
    });
  }

  const revealEls = document.querySelectorAll(
    ".section-header, .mission-text, .m-card, .swarm-content, .swarm-visual, .ship-stage, .feature, .tl-item, .philosophy blockquote, .phil-text, .contact-text, .contact-form"
  );

  revealEls.forEach((el) => el.classList.add("reveal"));

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  revealEls.forEach((el) => io.observe(el));

  window.handleSubmit = function (e) {
    e.preventDefault();
    const note = document.getElementById("formNote");
    const form = document.getElementById("contactForm");
    if (note) note.hidden = false;
    if (form) form.reset();
    return false;
  };
})();
