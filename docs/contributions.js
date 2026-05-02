// Render 2026 GitHub contributions using fetched data
function renderContributions() {
    const container = document.getElementById('github-chart-2026');
    if (!container) return;

    // Show loading
    container.innerHTML = '<div style="padding: 2rem; font-family: IBM Plex Mono, monospace; font-size: 0.75rem; color: #888;">Loading...</div>';

    fetch('https://github-contributions.vercel.app/api/v1/jackwallner?year=2026')
        .then(res => {
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        })
        .then(data => {
            if (!data.contributions || !Array.isArray(data.contributions)) {
                throw new Error('Invalid data');
            }

            const yearData = data.years.find(y => y.year === '2026');
            const total = yearData ? yearData.total : 0;

            // Get 2026 contributions, sorted by date
            const contributions = data.contributions
                .filter(c => c.date && c.date.startsWith('2026'))
                .sort((a, b) => new Date(a.date) - new Date(b.date));

            if (contributions.length === 0) {
                throw new Error('No data');
            }

            // Build week columns (53 weeks max, show ~26)
            const weeks = [];
            let currentWeek = [];

            // Pad to start from Sunday
            const firstDate = new Date(contributions[0].date);
            const startPadding = firstDate.getDay();
            for (let i = 0; i < startPadding; i++) {
                currentWeek.push(null);
            }

            // Add all days
            contributions.forEach(day => {
                currentWeek.push(day);
                if (currentWeek.length === 7) {
                    weeks.push(currentWeek);
                    currentWeek = [];
                }
            });

            // Add remaining days
            if (currentWeek.length > 0) {
                while (currentWeek.length < 7) currentWeek.push(null);
                weeks.push(currentWeek);
            }

            // Take first 27 weeks
            const displayWeeks = weeks.slice(0, 27);

            // Build HTML
            let html = `
                <div class="contributions-header">
                    <span class="contributions-total">${total.toLocaleString()} contributions in 2026</span>
                    <a href="https://github.com/jackwallner" target="_blank" rel="noopener">View full profile →</a>
                </div>
                <div class="contributions-grid">
                    <div class="contributions-column day-labels">
                        <div class="day-label">S</div>
                        <div class="day-label">M</div>
                        <div class="day-label">T</div>
                        <div class="day-label">W</div>
                        <div class="day-label">T</div>
                        <div class="day-label">F</div>
                        <div class="day-label">S</div>
                    </div>
            `;

            displayWeeks.forEach(week => {
                html += '<div class="contributions-column">';
                week.forEach(day => {
                    if (!day) {
                        html += '<div class="contribution-square empty"></div>';
                    } else {
                        const level = parseInt(day.intensity) || 0;
                        html += `<div class="contribution-square level-${level}" title="${day.date}: ${day.count} contributions"></div>`;
                    }
                });
                html += '</div>';
            });

            html += `
                </div>
                <div class="contributions-legend">
                    <span>Less</span>
                    <div class="legend-square level-0"></div>
                    <div class="legend-square level-1"></div>
                    <div class="legend-square level-2"></div>
                    <div class="legend-square level-3"></div>
                    <div class="legend-square level-4"></div>
                    <span>More</span>
                </div>
            `;

            container.innerHTML = html;
        })
        .catch(err => {
            console.error('Contributions error:', err);
            container.innerHTML = `
                <div class="contributions-error">
                    <a href="https://github.com/jackwallner" target="_blank" rel="noopener">View contributions on GitHub →</a>
                </div>
            `;
        });
}

// Run immediately
renderContributions();
