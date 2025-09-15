// Fake authentication for demo only
document.getElementById("workerLoginForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("✅ Login successful! Redirecting to dashboard...");
  window.location.href = "dashboard.html";
});

document.getElementById("workerRegisterForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("✅ Registration successful! You can now log in.");
  window.location.href = "login.html";
});
