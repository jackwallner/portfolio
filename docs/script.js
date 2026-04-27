const FEATURED = new Set([
    'vitals', 'headaches', 'fitness-streaks', 'baseball',
    'elsa-fitness-website', 'flight-tracker', 'my-flights', 'portfolio', 'jackwallner',
    'qa-bot', 'spotify-daily-trading-bot'
].map(s => s.toLowerCase()));

const LANG_DOTS = {
    Swift: '#F05138', Python: '#3572A5', JavaScript: '#f1e05a',
    TypeScript: '#3178c6', HTML: '#e34c26', CSS: '#563d7c',
    Shell: '#89e051', Java: '#b07219', Go: '#00ADD8', Ruby: '#701516',
    'C++': '#f34b7d', C: '#555555', Rust: '#dea584'
};

function fmtDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}

function stripEmoji(s) {
    if (!s) return '';
    return s.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{1F1E6}-\u{1F1FF}]/gu, '').trim();
}

async function loadRepos() {
    const el = document.getElementById('repos');
    if (!el) return;
    try {
        const res = await fetch('https://api.github.com/users/jackwallner/repos?type=public&sort=updated&per_page=100');
        if (!res.ok) throw new Error('GitHub API ' + res.status);
        const repos = await res.json();
        const filtered = repos
            .filter(r => !r.fork && !r.archived && !FEATURED.has(r.name.toLowerCase()))
            .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at));

        if (!filtered.length) {
            el.innerHTML = '<div class="loading">No additional public repositories.</div>';
            return;
        }

        const list = document.createElement('div');
        list.className = 'repo-list';
        filtered.forEach(r => {
            const row = document.createElement('a');
            row.className = 'repo-row';
            row.href = r.html_url;
            row.target = '_blank';
            row.rel = 'noopener';

            const lang = r.language || '—';
            const dotColor = LANG_DOTS[lang] || '#7a766c';
            const desc = stripEmoji(r.description);

            row.innerHTML = `
                <div>
                    <span class="repo-name">${r.name}</span>${desc ? `<span class="repo-desc">— ${desc}</span>` : ''}
                </div>
                <div class="repo-tail">
                    <span class="lang-dot" style="background:${dotColor}"></span>${lang}
                    &nbsp;·&nbsp; ${fmtDate(r.pushed_at)}
                    ${r.stargazers_count ? `&nbsp;·&nbsp; ★ ${r.stargazers_count}` : ''}
                </div>
            `;
            list.appendChild(row);
        });
        el.innerHTML = '';
        el.appendChild(list);
    } catch (err) {
        el.innerHTML = `<div class="error">Couldn't load live repo data (${err.message}). See <a href="https://github.com/jackwallner" style="color:inherit">github.com/jackwallner</a>.</div>`;
    }
}

const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

loadRepos();

/* ---- Scroll reveal ---- */
function initReveal() {
    const reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });

    reveals.forEach(el => observer.observe(el));
}

initReveal();
