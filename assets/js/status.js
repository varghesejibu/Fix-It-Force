const steps = document.querySelectorAll(".status-step");

// Assume we’re tracking Job ID = 1 (can extend later)
const jobId = "1";

let currentStep = 0;

// Map status → step index
const statusMap = {
  "Pending": 0,
  "Accepted": 1,
  "In Progress": 2,
  "Completed": 3
};

const updateSteps = (stepIndex) => {
  steps.forEach((step, i) => {
    step.classList.toggle("active", i <= stepIndex);
  });
};

// Load status from localStorage
const savedStatus = localStorage.getItem(`status-${jobId}`) || "Pending";
currentStep = statusMap[savedStatus];
updateSteps(currentStep);
