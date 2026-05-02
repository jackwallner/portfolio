// Fetch and render 2026 GitHub contributions
async function renderContributions() {
    const container = document.getElementById('github-chart-2026');
    if (!container) {
        console.error('Container not found: github-chart-2026');
        return;
    }

    // Show loading state
    container.innerHTML = '<div class="loading">Loading contributions...</div>';

    try {
        const res = await fetch('https://github-contributions.vercel.app/api/v1/jackwallner?year=2026');
        
        if (!res.ok) {
            throw new Error('API error: ' + res.status);
        }
        
        const data = await res.json();
        console.log('Contributions data:', data);
        
        if (!data.contributions || !Array.isArray(data.contributions)) {
            throw new Error('Invalid data structure');
        }
        
        const yearData = data.years.find(y => y.year === '2026');
        const total = yearData ? yearData.total : 0;
        
        // Get 2026 dates in chronological order
        const contributions = data.contributions
            .filter(c => c.date && c.date.startsWith('2026'))
            .sort((a, b) => new Date(a.date) - new Date(b.date));
        
        console.log('Filtered contributions:', contributions.length);
        
        if (contributions.length === 0) {
            throw new Error('No 2026 contributions found');
        }
        
        // Build week-based grid
        // Start from first Sunday before or on Jan 1
        const firstDate = new Date('2026-01-01');
        const startDay = firstDate.getDay(); // 0 = Sunday
        
        // Build complete grid with null padding
        const grid = [];
        
        // Pad start to align with Sunday
        for (let i = 0; i < startDay; i++) {
            grid.push(null);
        }
        
        // Add all actual days
        contributions.forEach(day => {
            grid.push(day);
        });
        
        // Split into weeks
        const weeks = [];
        for (let i = 0; i < grid.length; i += 7) {
            weeks.push(grid.slice(i, i + 7));
        }
        
        // Limit display weeks
        const displayWeeks = weeks.slice(0, 27);
        
        // Build HTML
        let html = '<div class="contributions-wrapper">';
        
        html += `
            <div class="contributions-header">
                <span class="contributions-total">${total.toLocaleString()} contributions in 2026</span>
                <a href="https://github.com/jackwallner" target="_blank" rel="noopener">View full profile →</a>
            </div>
        `;
        
        html += '<div class="contributions-grid">';
        
        // Day labels
        const dayLabels = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
        html += '<div class="contributions-column day-labels">';
        for (let i = 0; i < 7; i++) {
            html += `<div class="day-label">${dayLabels[i]}</div>`;
        }
        html += '</div>';
        
        // Render each week
        displayWeeks.forEach((week, weekIndex) => {
            html += '<div class="contributions-column">';
            for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
                const day = week[dayIndex];
                if (!day) {
                    html += '<div class="contribution-square empty"></div>';
                } else {
                    const level = parseInt(day.intensity) || 0;
                    const count = day.count || 0;
                    const tooltip = `${day.date}: ${count} contributions`;
                    html += `<div class="contribution-square level-${level}" title="${tooltip}"></div>`;
                }
            }
            html += '</div>';
        });
        
        html += '</div>'; // end grid
        
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
        
        html += '</div>'; // end wrapper
        
        container.innerHTML = html;
        console.log('Contributions rendered successfully');
        
    } catch (err) {
        console.error('Failed to render contributions:', err);
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
