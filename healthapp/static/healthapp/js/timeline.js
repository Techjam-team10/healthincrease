(function () {
  const counters = document.querySelectorAll("[data-counter]");
  counters.forEach((counter) => {
    const targetId = counter.getAttribute("data-counter");
    if (!targetId) {
      return;
    }
    const textarea = document.getElementById(targetId);
    if (!(textarea instanceof HTMLTextAreaElement)) {
      return;
    }
    const max = textarea.getAttribute("maxlength");
    const maxValue = max ? Number(max) : null;
    const update = () => {
      const length = textarea.value.length;
      counter.textContent = maxValue ? `${length} / ${maxValue}` : `${length}`;
    };
    textarea.addEventListener("input", update);
    update();
  });
})();
