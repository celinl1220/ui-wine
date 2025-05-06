document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.querySelector(".drop-zone");
  const correctContainer = document.querySelector(".correct-notes");
  const notesGrid = document.querySelector(".notes-grid");
  const notesGridWrapper = notesGrid.parentElement;
  const dropZoneWrapper = dropZone.parentElement;
  const activityWrapper = document.querySelector(".activity-wrapper");

  let matchedNotes = [];

  // Dynamically generate draggable items
  noteOptions.forEach(note => {
    const wrapper = document.createElement("div");
    wrapper.className = "drag-item";
    wrapper.setAttribute("draggable", "true");
    wrapper.dataset.note = note;

    const img = document.createElement("img");
    img.src = `/static/images/notes/${note}.png`;
    img.alt = note;

    const label = document.createElement("div");
    label.className = "note-label";
    label.textContent = note
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");

    wrapper.appendChild(img);
    wrapper.appendChild(label);
    notesGrid.appendChild(wrapper);
  });

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
      
      const wrappedNote = document.createElement("div");
      wrappedNote.className = "note-item text-center";
      const imgClone = dragged.querySelector("img").cloneNode(true);
      const labelClone = dragged.querySelector(".note-label").cloneNode(true);

      wrappedNote.appendChild(imgClone);
      wrappedNote.appendChild(labelClone);
      correctContainer.appendChild(wrappedNote);

      showSparkleAtDrop(e);
      dragged.remove();

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

  function showSparkleAtDrop(event) {
    const sparkle = document.createElement("div");
    sparkle.textContent = "✨";
    sparkle.className = "x-feedback-drag";
  
    // Use page-relative coordinates
    sparkle.style.left = `${event.pageX}px`;
    sparkle.style.top = `${event.pageY}px`;
  
    document.body.appendChild(sparkle);
    sparkle.getBoundingClientRect(); // force reflow
  
    requestAnimationFrame(() => {
      sparkle.style.opacity = "0";
      sparkle.style.transform = "translateY(-30px)";
    });
  
    setTimeout(() => sparkle.remove(), 1000);
  }
  
  function showXAtDrop(event) {
    const xMark = document.createElement("div");
    xMark.textContent = "✖";
    xMark.className = "x-feedback-drag";
  
    xMark.style.left = `${event.pageX}px`;
    xMark.style.top = `${event.pageY}px`;
  
    document.body.appendChild(xMark);
    xMark.getBoundingClientRect(); // force reflow
  
    requestAnimationFrame(() => {
      xMark.style.opacity = "0";
      xMark.style.transform = "translateY(-30px)";
    });
  
    setTimeout(() => xMark.remove(), 1000);
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
      const wrapper = document.createElement("div");
      wrapper.className = "note-item text-center mb-3";
  
      const img = document.createElement("img");
      img.src = `/static/images/notes/${note}.png`;
      img.alt = note;
      img.className = "summary-note";
  
      const label = document.createElement("div");
      label.className = "note-label mt-1";
      label.textContent = note
        .split("_")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
  
      wrapper.appendChild(img);
      wrapper.appendChild(label);
  
      if (correctNotes.length === 3 && index === 2) {
        rightContainer.appendChild(wrapper);
      } else if (index < 2) {
        leftContainer.appendChild(wrapper);
      } else {
        rightContainer.appendChild(wrapper);
      }
    });
  
    summaryRow.appendChild(leftContainer);
    summaryRow.appendChild(glassContainer);
    summaryRow.appendChild(rightContainer);
    activityWrapper.appendChild(summaryRow);
    document.getElementById("drag-drop-row")?.classList.remove("drag-phase-row");
  
    const backBtn = document.getElementById("summary-back-button");
    if (backBtn) backBtn.style.display = "block";
  
    const continueBtn = document.getElementById("continue-btn");
    if (continueBtn) continueBtn.style.display = "inline-block";
  }
});
