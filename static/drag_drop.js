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
        dragged.classList.add("sparkle");
        correctContainer.appendChild(dragged);
  
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
  
      // ✅ Force reflow
      xMark.getBoundingClientRect();
  
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
      summaryRow.className = "row justify-content-center text-center fade-in";
  
      const glassCol = document.createElement("div");
      glassCol.className = "col-md-6 position-relative summary-container";
  
      const glassImg = document.createElement("img");
      glassImg.src = "/static/glass_outline.png";
      glassImg.className = "img-fluid";
  
      correctNotes.forEach((note, index) => {
        const img = document.createElement("img");
        img.src = `/static/images/notes/${note}.png`;
        img.alt = note;
        img.className = "summary-note";
        img.style.position = "absolute";
  
        switch (index) {
          case 0:
            img.style.top = "-60px";
            img.style.left = "50%";
            img.style.transform = "translateX(-50%)";
            break;
          case 1:
            img.style.top = "50%";
            img.style.right = "-60px";
            img.style.transform = "translateY(-50%)";
            break;
          case 2:
            img.style.bottom = "-60px";
            img.style.left = "50%";
            img.style.transform = "translateX(-50%)";
            break;
          case 3:
            img.style.top = "50%";
            img.style.left = "-60px";
            img.style.transform = "translateY(-50%)";
            break;
        }
  
        glassCol.appendChild(img);
      });
  
      glassCol.appendChild(glassImg);
      summaryRow.appendChild(glassCol);
      activityWrapper.appendChild(summaryRow);
  
      const backBtn = document.getElementById("summary-back-button");
      if (backBtn) backBtn.style.display = "block";
    }
  });
  