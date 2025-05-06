document.addEventListener("DOMContentLoaded", () => {
  const glasses = document.querySelectorAll(".wine-glass");

  glasses.forEach((glass, i) => {
    const fill = glass.querySelector(".glass-fill");
    fill.style.backgroundColor = colorOptions[i];

    glass.addEventListener("click", (event) => {
      if (glass.classList.contains("disabled")) return;

      const isCorrect = parseInt(glass.dataset.index) === correctIndex;
      console.log(`Clicked glass ${i}, correct: ${isCorrect}`);

      if (isCorrect) {
        fill.classList.add("correct-glow");
        glasses.forEach(g => g.classList.add("disabled"));

        // ✨ Sparkle effect
        const sparkle = document.createElement("div");
        sparkle.textContent = "✨";
        sparkle.className = "x-feedback-drag"; // reuse existing sparkle animation class

        // Position it above the clicked glass
        const rect = glass.getBoundingClientRect();
        sparkle.style.left = `${rect.left + rect.width / 2}px`;
        sparkle.style.top = `${rect.top}px`;

        document.body.appendChild(sparkle);
        sparkle.getBoundingClientRect(); // force reflow

        requestAnimationFrame(() => {
          sparkle.style.opacity = "0";
          sparkle.style.transform = "translateY(-30px)";
        });

        setTimeout(() => sparkle.remove(), 1000);

        // ✅ Show continue button when correct glass is clicked
        const continueBtn = document.getElementById("continue-btn");
        if (continueBtn) {
          setTimeout(() => {
            continueBtn.style.display = "inline-block";
          }, 500);
        }
      } else {
        const x = document.createElement("div");
        x.textContent = "✖";
        x.className = "x-feedback-match";
        glass.appendChild(x);

        requestAnimationFrame(() => {
          x.style.opacity = "0";
          x.style.transform = "translateY(-30px)";
        });

        setTimeout(() => x.remove(), 1000);
      }
    });
  });
});
