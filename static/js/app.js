// Auto-dismiss flash messages after 4 seconds
document.querySelectorAll(".flash").forEach(function(el) {
  setTimeout(function() {
    el.style.transition = "opacity .4s ease";
    el.style.opacity = "0";
    setTimeout(function() { el.remove(); }, 400);
  }, 4000);
});

// Set today as minimum for date inputs so users can't pick past dates
var today = new Date().toISOString().split("T")[0];
document.querySelectorAll("input[type='date']").forEach(function(el) {
  if (!el.value) el.min = today;
});
