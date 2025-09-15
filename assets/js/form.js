document.getElementById("bookingForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const address = document.getElementById("address").value;
  const service = document.getElementById("service").value;

  // Save booking details in localStorage (for demo)
  localStorage.setItem("lastBooking", JSON.stringify({
    name,
    phone,
    address,
    service
  }));

  // Redirect to confirmation page
  window.location.href = "confirm.html";
});
