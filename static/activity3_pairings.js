const foodDataEl = document.getElementById('food-data');
const nextUrl = foodDataEl.dataset.nextUrl;

const overlay = document.getElementById("feedback-overlay");
const feedbackText = document.getElementById("feedback-text");
const feedbackDesc = document.getElementById("feedback-description");

let waitingForNext = false;
let activityComplete = false;
let lastGuess = null;

var currentCorrectAnswer = foodDataEl.dataset.correct;
var currentExplanation = foodDataEl.dataset.explanation;
var isCorrect;

function handleGuess(guess) {
    if (waitingForNext || activityComplete) return;
    waitingForNext = true;
    isCorrect = guess === currentCorrectAnswer;

    // Display feedback
    const img = document.getElementById("food-image");
    img.style.opacity = "0.5";
    console.log("currentCorrectAnswer: " + currentCorrectAnswer);
    console.log("guess: " + guess);
    feedbackText.textContent = isCorrect ? "CORRECT!" : "WRONG!";
    feedbackText.style.color = isCorrect ? "green" : "red";
    feedbackDesc.textContent = currentExplanation;
    overlay.style.display = "flex";

    // Delay attaching listener to avoid instant trigger
    setTimeout(() => {
        document.body.addEventListener("keydown", stack, { once: true });
    }, 500); // Adjust delay as needed (ms)
}

function stack() {
    // Get current correct answer
    currentCorrectAnswer = foodDataEl.dataset.correct;

    // Remove feedback overlay
    overlay.style.display = "none";

    // Reset opacity
    const img = document.getElementById("food-image");
    img.style.opacity = "1.0";

    // Clone and stack the image after user interaction
    const clone = img.cloneNode(true);
    clone.className = "";  // Remove any animation classes
    clone.removeAttribute('id'); // Remove any ids
    clone.style.opacity = "1.0";
    clone.style.margin = "4px";  // Optional: space between images

    const stack = currentCorrectAnswer === "meh"
        ? document.getElementById("meh-stack")
        : document.getElementById("good-stack");

    stack.appendChild(clone);  // Add the cloned image to the correct stack
    goToNext(img);
}

function goToNext(img) {
    // Fetch the next food item
    fetch(nextUrl, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            console.log("Fetched data:", data); // Log the entire response
            waitingForNext = false;

            if (data.done) {
                activityComplete = true;
                const continueBtn = document.getElementById("continue-btn");
                if (continueBtn) continueBtn.style.display = "inline-block";
                feedbackDesc.textContent = "You've completed this round!";
                // img.style.opacity = "0.5";
                img.style.opacity = "0.0";
            } else {
                console.log("Next image:", img);  // Check the image path
                img.src = ""; // Clear the current image
                img.src = `/static/images/foods/${data.image}`;
                foodDataEl.dataset.correct = data.correct_answer;
                foodDataEl.dataset.explanation = data.explanation;

                // Update currentCorrectAnswer and currentExplanation for the new food item
                currentCorrectAnswer = data.correct_answer;
                currentExplanation = data.explanation;
            }
        });
}

// Arrow and button controls
document.addEventListener("keydown", event => {
    if (event.key === "ArrowLeft") handleGuess("meh");
    else if (event.key === "ArrowRight") handleGuess("good");
});