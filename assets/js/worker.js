const jobs = document.querySelectorAll(".job-card");

jobs.forEach(job => {
  const jobId = job.dataset.id;
  const statusText = job.querySelector(".status-text");
  const buttons = job.querySelectorAll("button");

  // Load saved status
  const savedStatus = localStorage.getItem(`status-${jobId}`);
  if (savedStatus) {
    statusText.textContent = savedStatus;
    updateStatusColor(statusText, savedStatus);
  }

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      let newStatus = "Pending";

      if (action === "accept") newStatus = "Accepted";
      if (action === "progress") newStatus = "In Progress";
      if (action === "complete") newStatus = "Completed";

      statusText.textContent = newStatus;
      updateStatusColor(statusText, newStatus);

      // Save to localStorage
      localStorage.setItem(`status-${jobId}`, newStatus);
    });
  });
});

// Helper: update colors
function updateStatusColor(el, status) {
  if (status === "Accepted") el.style.color = "orange";
  else if (status === "In Progress") el.style.color = "blue";
  else if (status === "Completed") el.style.color = "green";
  else el.style.color = "black";
}
