document.addEventListener("DOMContentLoaded", () => {
    const glasses = document.querySelectorAll(".wine-glass");
  
    glasses.forEach((glass, i) => {
      const fill = glass.querySelector(".glass-fill");
      fill.style.backgroundColor = colorOptions[i];
  
      glass.addEventListener("click", () => {
        if (glass.classList.contains("disabled")) return;
  
        const isCorrect = parseInt(glass.dataset.index) === correctIndex;
        console.log(`Clicked glass ${i}, correct: ${isCorrect}`);
  
        if (isCorrect) {
          fill.classList.add("correct-glow");
          glasses.forEach(g => g.classList.add("disabled"));
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
  