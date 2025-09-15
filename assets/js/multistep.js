const form = document.getElementById("bookingForm");
const fieldsets = form.querySelectorAll("fieldset");
const steps = document.querySelectorAll("#progressbar .step");

let current = 0;
fieldsets[current].classList.add("active");
steps[current].classList.add("active");

const showStep = (index) => {
  fieldsets.forEach((fs, i) => fs.classList.toggle("active", i === index));
  steps.forEach((s, i) => s.classList.toggle("active", i <= index));
};

form.addEventListener("click", (e) => {
  if (e.target.classList.contains("next")) {
    if (current < fieldsets.length - 1) {
      current++;
      showStep(current);
    }
  }
  if (e.target.classList.contains("prev")) {
    if (current > 0) {
      current--;
      showStep(current);
    }
  }
});

// Review Step
form.addEventListener("click", (e) => {
  if (e.target.classList.contains("next") && current === 3) {
    const data = new FormData(form);
    const reviewDiv = document.getElementById("review");
    reviewDiv.innerHTML = `
      <p><strong>Service:</strong> ${data.get("service")}</p>
      <p><strong>Address:</strong> ${data.get("address")}, ${data.get("city")} - ${data.get("pincode")}</p>
      <p><strong>Name:</strong> ${data.get("name")}</p>
      <p><strong>Phone:</strong> ${data.get("phone")}</p>
      <p><strong>Notes:</strong> ${data.get("notes")}</p>
    `;
  }
});

// Handle submit
form.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("✅ Booking confirmed! A worker will contact you shortly.");
  form.reset();
  current = 0;
  showStep(current);
});
