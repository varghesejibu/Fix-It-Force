const selects = document.querySelectorAll(".job-table select");

selects.forEach((select) => {
  select.addEventListener("change", (e) => {
    const row = e.target.closest("tr");
    const statusCell = row.querySelector("td:nth-child(5)");
    const newStatus = e.target.value;

    // Update badge
    statusCell.innerHTML = `<span class="badge ${newStatus.toLowerCase().replace(" ", "")}">${newStatus}</span>`;
    
    alert(`✅ Job status updated to: ${newStatus}`);
  });
});
