document.addEventListener('DOMContentLoaded', () => {
  const themeBtns = document.querySelectorAll('[data-theme-set]');
  const htmlEl = document.documentElement;

  // Retrieve saved theme preference or default to auto
  const savedTheme = localStorage.getItem('theme_preference') || 'auto';
  applyTheme(savedTheme);

  themeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedTheme = btn.getAttribute('data-theme-set');
      localStorage.setItem('theme_preference', selectedTheme);
      applyTheme(selectedTheme);
    });
  });

  /**
   * Applies a theme to the document and marks its corresponding control as active.
   * @param {string} theme - The theme to apply.
   */
  function applyTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    themeBtns.forEach(btn => {
      if (btn.getAttribute('data-theme-set') === theme) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }
});
