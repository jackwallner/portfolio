// Fetch and render 2026 GitHub contributions
async function renderContributions() {
    const container = document.getElementById('github-chart-2026');
    if (!container) return;

    try {
        const res = await fetch('https://github-contributions.vercel.app/api/v1/jackwallner?year=2026');
        if (!res.ok) throw new Error('API error: ' + res.status);
        const data = await res.json();
        
        const yearData = data.years.find(y => y.year === '2026');
        const total = yearData ? yearData.total : 0;
        
        // Get only 2026 dates, in chronological order
        const contributions = data.contributions
            .filter(c => c.date.startsWith('2026'))
            .sort((a, b) => new Date(a.date) - new Date(b.date));
        
        // Build simple week grid
        // Find the first Sunday to start
        const firstDate = new Date(contributions[0].date);
        const firstDayOfWeek = firstDate.getDay(); // 0 = Sunday
        
        // Pad with empty days at start to align weeks
        const grid = [];
        for (let i = 0; i < firstDayOfWeek; i++) {
            grid.push(null);
        }
        
        // Add all days
        contributions.forEach(day => {
            grid.push(day);
        });
        
        // Build HTML
        const weeks = [];
        let currentWeek = [];
        
        grid.forEach(day => {
            currentWeek.push(day);
            if (currentWeek.length === 7) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
        });
        
        // Don't add partial last week if too small
        if (currentWeek.length > 0 && currentWeek.length < 3) {
            // pad with nulls
            while (currentWeek.length < 7) currentWeek.push(null);
            weeks.push(currentWeek);
        } else if (currentWeek.length > 0) {
            weeks.push(currentWeek);
        }
        
        // Limit to ~28 weeks for display width
        const displayWeeks = weeks.slice(0, 28);
        
        let html = `
            <div class="contributions-header">
                <span class="contributions-total">${total.toLocaleString()} contributions in 2026</span>
                <a href="https://github.com/jackwallner" target="_blank" rel="noopener">View full profile →</a>
            </div>
            <div class="contributions-grid">
        `;
        
        // Day labels on left
        const dayLabels = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
        html += '<div class="contributions-column day-labels">';
        for (let i = 0; i < 7; i++) {
            html += `<div class="day-label">${dayLabels[i]}</div>`;
        }
        html += '</div>';
        
        // Render weeks
        displayWeeks.forEach(week => {
            html += '<div class="contributions-column">';
            for (let i = 0; i < 7; i++) {
                const day = week[i];
                if (!day) {
                    html += '<div class="contribution-square empty"></div>';
                } else {
                    const level = parseInt(day.intensity) || 0;
                    const tooltip = `${day.date}: ${day.count} contributions`;
                    html += `<div class="contribution-square level-${level}" title="${tooltip}"></div>`;
                }
            }
            html += '</div>';
        });
        
        html += '</div>';
        
        // Legend
        html += `
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
        
    } catch (err) {
        console.error('Contributions error:', err);
        container.innerHTML = `
            <div class="contributions-error">
                <a href="https://github.com/jackwallner" target="_blank" rel="noopener">
                    View contributions on GitHub →
                </a>
            </div>
        `;
    }
}

// Run when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderContributions);
} else {
    renderContributions();
}
