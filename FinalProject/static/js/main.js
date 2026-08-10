document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".layanan-checkbox");

  function syncBox(cb) {
    const box = document.getElementById("detail-" + cb.value);
    if (!box) return;
    box.classList.toggle("show", cb.checked);
  }

  checkboxes.forEach(function (cb) {
    syncBox(cb); // set kondisi awal (berguna saat edit acara)
    cb.addEventListener("change", function () {
      syncBox(cb);
    });
  });

  const flashes = document.querySelectorAll(".flash");
  flashes.forEach(function (f) {
    setTimeout(function () {
      f.style.transition = "opacity 0.5s ease";
      f.style.opacity = "0";
      setTimeout(function () { f.remove(); }, 500);
    }, 4000);
  });
});
