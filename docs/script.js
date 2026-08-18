// The project table and cards are generated at build time by
// scripts/build_site.py from projects.json, so the page renders with no JS.
// This file only adds the two bits of interactivity on top.

// ---- Filter chips over the project table ----
(function () {
    const chips = document.querySelectorAll('.chip');
    const rows = document.querySelectorAll('.proj-tr');
    if (!chips.length || !rows.length) return;

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const filter = chip.dataset.filter;
            chips.forEach(c => c.classList.toggle('active', c === chip));
            rows.forEach(row => {
                row.classList.toggle('hidden', filter !== 'all' && row.dataset.group !== filter);
            });
            history.replaceState(null, '', filter === 'all' ? '#all' : '#all-' + filter);
        });
    });

    // Deep link: /#all-ios opens the table pre-filtered to iOS.
    const fromHash = (location.hash.match(/^#all-(\w+)$/) || [])[1];
    if (fromHash) {
        const chip = document.querySelector(`.chip[data-filter="${fromHash}"]`);
        if (chip) chip.click();
    }
})();

// ---- Whole table rows are clickable, not just the project name ----
(function () {
    document.querySelectorAll('.proj-tr').forEach(row => {
        const link = row.querySelector('.proj-name');
        if (!link) return;
        row.addEventListener('click', ev => {
            // Let real clicks on the link (or any other link) behave normally.
            if (ev.target.closest('a')) return;
            link.click();
        });
    });
})();
