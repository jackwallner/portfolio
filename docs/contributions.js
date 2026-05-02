// Fetch and render 2026 GitHub contributions
async function renderContributions() {
    const container = document.getElementById('github-chart-2026');
    if (!container) return;

    try {
        const res = await fetch('https://github-contributions.vercel.app/api/v1/jackwallner?year=2026');
        if (!res.ok) throw new Error('API error');
        const data = await res.json();
        
        const yearData = data.years.find(y => y.year === '2026');
        const total = yearData ? yearData.total : 0;
        const contributions = data.contributions.filter(c => c.date.startsWith('2026'));
        
        // Group by week for display
        const weeks = [];
        let currentWeek = [];
        contributions.forEach((day, index) => {
            const date = new Date(day.date);
            const dayOfWeek = date.getDay();
            if (dayOfWeek === 0 && currentWeek.length > 0) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
            currentWeek.push(day);
        });
        if (currentWeek.length > 0) weeks.push(currentWeek);
        
        // Limit to reasonable width (~26 weeks visible)
        const displayWeeks = weeks.slice(0, 26);
        
        // Build HTML
        let html = `
            <div class="contributions-header">
                <span class="contributions-total">${total.toLocaleString()} contributions in 2026</span>
                <a href="https://github.com/jackwallner" target="_blank" rel="noopener">View full profile →</a>
            </div>
            <div class="contributions-grid">
        `;
        
        // Day labels
        const days = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
        html += '<div class="contributions-column day-labels">';
        days.forEach(d => {
            html += `<div class="day-label">${d}</div>`;
        });
        html += '</div>';
        
        // Contribution squares
        displayWeeks.forEach(week => {
            html += '<div class="contributions-column">';
            week.forEach(day => {
                const intensity = parseInt(day.intensity);
                let level = 0;
                if (intensity === 4) level = 4;
                else if (intensity === 3) level = 3;
                else if (intensity === 2) level = 2;
                else if (intensity === 1) level = 1;
                
                html += `<div class="contribution-square level-${level}" title="${day.date}: ${day.count} contributions"></div>`;
            });
            // Fill empty days at end
            while (week.length < 7) {
                html += '<div class="contribution-square empty"></div>';
                week.push(null);
            }
            html += '</div>';
        });
        
        html += '</div>';
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
        container.innerHTML = `
            <div class="contributions-error">
                <a href="https://github.com/jackwallner" target="_blank" rel="noopener">
                    View contributions on GitHub →
                </a>
            </div>
        `;
    }
}

renderContributions();
