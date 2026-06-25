const LANG_DOTS = {
    Swift: '#F05138', Python: '#3572A5', JavaScript: '#f1e05a',
    TypeScript: '#3178c6', HTML: '#e34c26', CSS: '#563d7c',
    Shell: '#89e051', Java: '#b07219', Go: '#00ADD8', Ruby: '#701516',
    'C++': '#f34b7d', C: '#555555', Rust: '#dea584', Processing: '#0096D8'
};

// Curated metadata, keyed by GitHub repo name. `repo: null` = no public repo.
// `fallback` dates are only used if the GitHub API is unreachable.
const CURATED = [
    { repo: 'vitals', name: 'Total Calories', icon: 'vitals-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/vitals/', ext: true, fallback: '2026-06-15', desc: 'Private calorie and step tracking, straight from Apple Health.' },
    { repo: 'headaches', name: 'One Tap Headache Tracker', icon: 'headaches-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/headaches/', ext: true, fallback: '2026-06-10', desc: 'Log a headache in one tap, with health and weather context.' },
    { repo: 'fitness-streaks', name: 'Streak Finder', icon: 'streaks-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/fitness-streaks/', ext: true, fallback: '2026-06-08', desc: 'Finds your fitness streaks automatically from Apple Health.' },
    { repo: 'sober', name: 'Sober', icon: 'sober-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/sober/', ext: true, fallback: '2026-06-12', desc: 'A day counter with a virtual garden that grows as sober days add up.' },
    { repo: 'simpleglp', name: 'Simple GLP', icon: 'simpleglp-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/simpleglp/', ext: true, fallback: '2026-06-11', desc: 'One-tap GLP-1 shot logging on a simple weekly schedule.' },
    { repo: 'sports', name: 'Gist', icon: 'sports-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/sports/', ext: true, fallback: '2026-06-14', desc: 'Plain-English sports talking points so non-fans can ask one good question.' },
    { repo: 'baseball', name: 'Baseball Savvy StatScout', icon: 'statscout-icon.png', status: 'App Store', cls: 'live', link: 'statscout/', ext: false, fallback: '2026-05-20', desc: 'Mobile-first Statcast player cards and leaderboards.' },
    { repo: 'bond', name: 'Bond', icon: 'bond-icon.png', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/bond/', ext: true, fallback: '2026-05-25', desc: 'Love-language reminders, shared milestones, and a daily check-in for couples.' },
    { repo: 'posture', name: 'Posture', icon: 'posture-icon.png', status: 'Coming soon', cls: 'soon', link: 'https://jackwallner.github.io/posture/', ext: true, fallback: '2026-06-09', desc: 'Reads your alignment from AirPods head-motion sensors and nudges you upright.' },
    { repo: 'nearby-trains', name: 'Nearby Trains', icon: 'trains-icon.png', status: 'Live', cls: 'live', link: 'https://jackwallner.github.io/nearby-trains/', ext: true, fallback: '2026-04-15', desc: 'Track Amtrak, VIA Rail, and Brightline trains near any location.' },
    { repo: 'flight-tracker', name: 'Flight Tracker', icon: 'flight-tracker-icon.png', status: 'Live', cls: 'live', link: 'flight-tracker/', ext: false, fallback: '2026-04-20', desc: 'Local flight tracking on an AWTRIX smart pixel clock.' },
    { repo: 'any-song-clone-hero-cli', name: 'Any Song Clone Hero', icon: 'songhero-icon.png', status: 'Live', cls: 'live', link: 'songhero/', ext: false, fallback: '2026-03-10', desc: 'Generates custom Clone Hero charts from any Spotify link.' },
    { repo: null, name: 'e3fit.me', icon: 'e3fit-icon.png', status: 'Live', cls: 'live', link: 'e3fit/', ext: false, fallback: '2026-05-01', desc: 'A production platform for coaching, booking, and workout delivery.' },
    { repo: 'spotify-daily-trading-bot', name: 'Spotify Daily Trading Bot', icon: 'spotify-bot-icon.png', status: 'Retired', cls: 'unsuccessful', link: 'spotify-bot/', ext: false, fallback: '2026-02-15', desc: "A Kalshi bot for predicting Spotify's daily #1 song. It didn't beat the market." },
];

// Repos folded into a curated entry above — don't list them again in the tail.
// value = repo name of the curated entry whose date should track this repo too.
const FOLDED = { 'statscout': 'baseball', 'flight-tracker-service': 'flight-tracker' };

function fmtDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}

function stripEmoji(s) {
    if (!s) return '';
    return s.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{1F1E6}-\u{1F1FF}]/gu, '').trim();
}

function escapeHtml(s) {
    return (s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function projectRow(e) {
    const tr = document.createElement('tr');
    tr.className = 'proj-tr';
    tr.tabIndex = 0;
    tr.dataset.href = e.link;
    if (e.ext) tr.dataset.ext = '1';

    const iconHtml = e.icon
        ? `<img src="assets/${e.icon}" alt="" class="proj-icon">`
        : `<span class="proj-icon ph">${escapeHtml((e.name[0] || '#').toUpperCase())}</span>`;
    const langHtml = e.lang
        ? `<span class="lang-dot" style="background:${LANG_DOTS[e.lang] || '#7a766c'}"></span>${escapeHtml(e.lang)}`
        : '';

    tr.innerHTML = `
        <td class="col-proj">
            <div class="proj-cell">
                ${iconHtml}
                <div class="proj-body">
                    <span class="proj-name">${escapeHtml(e.name)}</span>
                    ${e.desc ? `<span class="proj-desc">${escapeHtml(e.desc)}</span>` : ''}
                </div>
            </div>
        </td>
        <td class="col-status">
            <span class="project-stamp ${e.cls}">${escapeHtml(e.status)}</span>
        </td>
        <td class="col-date">
            <span class="proj-when">${e.date ? fmtDate(e.date) : ''}</span>
            ${langHtml ? `<span class="proj-lang">${langHtml}</span>` : ''}
        </td>
    `;
    return tr;
}

function renderTable(entries) {
    const body = document.getElementById('proj-rows');
    if (!body) return;
    const sorted = entries.slice().sort((a, b) => new Date(b.date || b.fallback) - new Date(a.date || a.fallback));
    body.innerHTML = '';
    sorted.forEach(e => body.appendChild(projectRow(e)));

    body.querySelectorAll('.proj-tr').forEach(row => {
        const go = () => {
            const href = row.dataset.href;
            if (row.dataset.ext) window.open(href, '_blank', 'noopener');
            else window.location.href = href;
        };
        row.addEventListener('click', go);
        row.addEventListener('keydown', ev => { if (ev.key === 'Enter') go(); });
    });
}

async function loadProjects() {
    const body = document.getElementById('proj-rows');
    if (!body) return;

    // Static render first, so the page is useful even if GitHub is unreachable.
    renderTable(CURATED);

    try {
        const res = await fetch('https://api.github.com/users/jackwallner/repos?type=public&sort=updated&per_page=100');
        if (!res.ok) throw new Error('GitHub API ' + res.status);
        const repos = await res.json();

        const byRepo = {};
        CURATED.forEach(e => { if (e.repo) byRepo[e.repo] = e; });

        const entries = CURATED.map(e => ({ ...e }));
        const entryByRepo = {};
        entries.forEach(e => { if (e.repo) entryByRepo[e.repo] = e; });

        repos.filter(r => !r.fork && !r.archived).forEach(r => {
            const key = r.name.toLowerCase();
            if (FOLDED[key]) {
                const target = entryByRepo[FOLDED[key]];
                if (target && new Date(r.pushed_at) > new Date(target.date || 0)) target.date = r.pushed_at;
                return;
            }
            if (entryByRepo[key]) {
                entryByRepo[key].date = r.pushed_at;
                if (!entryByRepo[key].lang) entryByRepo[key].lang = r.language || '';
                return;
            }
            // Long tail: real repo with no curated entry.
            entries.push({
                name: r.name,
                desc: stripEmoji(r.description),
                icon: null,
                status: 'Code',
                cls: 'code',
                link: r.html_url,
                ext: true,
                date: r.pushed_at,
                lang: r.language || ''
            });
        });

        renderTable(entries);
    } catch (err) {
        // Curated table already rendered; nothing more to do.
    }
}

loadProjects();

const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

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
