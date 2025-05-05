document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.querySelector(".drop-zone");
  const correctContainer = document.querySelector(".correct-notes");
  const notesGridWrapper = document.querySelector(".notes-grid").parentElement;
  const dropZoneWrapper = dropZone.parentElement;
  const activityWrapper = document.querySelector(".activity-wrapper");

  let matchedNotes = [];

  document.querySelectorAll(".drag-item").forEach(img => {
    img.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("text/plain", img.dataset.note);
    });
  });

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("highlight");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("highlight");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("highlight");

    const note = e.dataTransfer.getData("text/plain");
    const dragged = document.querySelector(`.drag-item[data-note="${note}"]`);

    if (!dragged) return;

    if (correctNotes.includes(note)) {
      dragged.draggable = false;
      dragged.classList.remove("drag-item");
      correctContainer.appendChild(dragged);
      showSparkleAtDrop(e);

      if (!matchedNotes.includes(note)) {
        matchedNotes.push(note);
      }

      if (matchedNotes.length === correctNotes.length) {
        setTimeout(() => {
          showSummaryState();
        }, 300);
      }
    } else {
      showXAtDrop(e);
      dragged.remove();
    }
  });

  function showXAtDrop(event) {
    const xMark = document.createElement("div");
    xMark.textContent = "✖";
    xMark.className = "x-feedback-drag";

    const rect = dropZone.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    xMark.style.left = `${x}px`;
    xMark.style.top = `${y}px`;

    dropZone.appendChild(xMark);
    xMark.getBoundingClientRect();

    requestAnimationFrame(() => {
      xMark.style.opacity = "0";
      xMark.style.transform = "translateY(-30px)";
    });

    setTimeout(() => xMark.remove(), 1000);
  }

  function showSparkleAtDrop(event) {
    const sparkle = document.createElement("div");
    sparkle.textContent = "✨";
    sparkle.className = "x-feedback-drag";

    const rect = dropZone.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    sparkle.style.left = `${x}px`;
    sparkle.style.top = `${y}px`;

    dropZone.appendChild(sparkle);
    sparkle.getBoundingClientRect();

    requestAnimationFrame(() => {
      sparkle.style.opacity = "0";
      sparkle.style.transform = "translateY(-30px)";
    });

    setTimeout(() => sparkle.remove(), 1000);
  }

  function showSummaryState() {
    notesGridWrapper.remove();
    dropZoneWrapper.remove();

    const summaryRow = document.createElement("div");
    summaryRow.className = "d-flex justify-content-center align-items-center fade-in";

    const leftContainer = document.createElement("div");
    leftContainer.className = "d-flex flex-column align-items-end me-3";

    const glassContainer = document.createElement("div");
    glassContainer.className = "text-center";
    glassContainer.style.maxWidth = "180px";

    const glassImg = document.createElement("img");
    glassImg.src = "/static/glass_outline.png";
    glassImg.alt = "Wine Glass";
    glassImg.className = "img-fluid";
    glassContainer.appendChild(glassImg);

    const rightContainer = document.createElement("div");
    rightContainer.className = "d-flex flex-column align-items-start ms-3";

    correctNotes.forEach((note, index) => {
      const img = document.createElement("img");
      img.src = `/static/images/notes/${note}.png`;
      img.alt = note;
      img.className = "summary-note mb-2";

      if (correctNotes.length === 3 && index === 2) {
        rightContainer.appendChild(img);
      } else if (index < 2) {
        leftContainer.appendChild(img);
      } else {
        rightContainer.appendChild(img);
      }
    });

    summaryRow.appendChild(leftContainer);
    summaryRow.appendChild(glassContainer);
    summaryRow.appendChild(rightContainer);
    activityWrapper.appendChild(summaryRow);

    const backBtn = document.getElementById("summary-back-button");
    if (backBtn) backBtn.style.display = "block";

    const continueBtn = document.getElementById("continue-btn");
    if (continueBtn) continueBtn.style.display = "inline-block";
  }
});
