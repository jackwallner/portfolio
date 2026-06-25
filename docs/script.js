// Curated metadata, keyed by GitHub repo name. `repo: null` = no public repo.
// `start`/`updated` are fallback dates, used only if the GitHub API is unreachable;
// real created_at / pushed_at dates override them when the fetch succeeds.
const CURATED = [
    { repo: 'vitals', name: 'Total Calories', icon: 'vitals-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/vitals/', ext: true, start: '2026-05-01', updated: '2026-06-15', desc: 'Private calorie and step tracking, straight from Apple Health.' },
    { repo: 'headaches', name: 'One Tap Headache Tracker', icon: 'headaches-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/headaches/', ext: true, start: '2026-05-20', updated: '2026-06-10', desc: 'Log a headache in one tap, with health and weather context.' },
    { repo: 'fitness-streaks', name: 'Streak Finder', icon: 'streaks-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/fitness-streaks/', ext: true, start: '2026-05-22', updated: '2026-06-08', desc: 'Finds your fitness streaks automatically from Apple Health.' },
    { repo: 'sober', name: 'Sober', icon: 'sober-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/sober/', ext: true, start: '2026-05-15', updated: '2026-06-12', desc: 'A day counter with a virtual garden that grows as sober days add up.' },
    { repo: 'simpleglp', name: 'Simple GLP', icon: 'simpleglp-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/simpleglp/', ext: true, start: '2026-05-28', updated: '2026-06-11', desc: 'One-tap GLP-1 shot logging on a simple weekly schedule.' },
    { repo: 'sports', name: 'Gist', icon: 'sports-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/sports/', ext: true, start: '2026-05-30', updated: '2026-06-14', desc: 'Plain-English sports talking points so non-fans can ask one good question.' },
    { repo: 'baseball', name: 'Baseball Savvy StatScout', icon: 'statscout-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'statscout/', ext: false, start: '2026-04-10', updated: '2026-05-20', desc: 'Mobile-first Statcast player cards and leaderboards.' },
    { repo: 'bond', name: 'Bond', icon: 'bond-icon.png', type: 'iOS App', status: 'App Store', cls: 'live', link: 'https://jackwallner.github.io/bond/', ext: true, start: '2026-04-20', updated: '2026-05-25', desc: 'Love-language reminders, shared milestones, and a daily check-in for couples.' },
    { repo: 'posture', name: 'Posture', icon: 'posture-icon.png', type: 'iOS App', status: 'Coming soon', cls: 'soon', link: 'https://jackwallner.github.io/posture/', ext: true, start: '2026-06-01', updated: '2026-06-09', desc: 'Reads your alignment from AirPods head-motion sensors and nudges you upright.' },
    { repo: 'nearby-trains', name: 'Nearby Trains', icon: 'trains-icon.png', type: 'Web app', status: 'Live', cls: 'live', link: 'https://jackwallner.github.io/nearby-trains/', ext: true, start: '2026-04-01', updated: '2026-04-15', desc: 'Track Amtrak, VIA Rail, and Brightline trains near any location.' },
    { repo: 'flight-tracker', name: 'Flight Tracker', icon: 'flight-tracker-icon.png', type: 'Hardware', status: 'Live', cls: 'live', link: 'flight-tracker/', ext: false, start: '2026-03-15', updated: '2026-04-20', desc: 'Local flight tracking on an AWTRIX smart pixel clock.' },
    { repo: 'any-song-clone-hero-cli', name: 'Any Song Clone Hero', icon: 'songhero-icon.png', type: 'Tool', status: 'Live', cls: 'live', link: 'songhero/', ext: false, start: '2026-02-20', updated: '2026-03-10', desc: 'Generates custom Clone Hero charts from any Spotify link.' },
    { repo: null, name: 'e3fit.me', icon: 'e3fit-icon.png', type: 'Web app', status: 'Live', cls: 'live', link: 'e3fit/', ext: false, start: '2026-03-01', updated: '2026-05-01', desc: 'A production platform for coaching, booking, and workout delivery.' },
    { repo: 'spotify-daily-trading-bot', name: 'Spotify Daily Trading Bot', icon: 'spotify-bot-icon.png', type: 'Bot', status: 'Retired', cls: 'unsuccessful', link: 'spotify-bot/', ext: false, start: '2026-01-20', updated: '2026-02-15', desc: "A Kalshi bot for predicting Spotify's daily #1 song. It didn't beat the market." },
];

// Repos folded into a curated entry above — don't list them again in the tail.
// value = repo name of the curated entry whose dates should also track this repo.
const FOLDED = { 'statscout': 'baseball', 'flight-tracker-service': 'flight-tracker' };

function fmtDate(iso) {
    if (!iso) return '';
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
        <td class="col-type"><span class="proj-type">${escapeHtml(e.type || '')}</span></td>
        <td class="col-status"><span class="project-stamp ${e.cls}">${escapeHtml(e.status)}</span></td>
        <td class="col-started"><span class="proj-when">${fmtDate(e.start)}</span></td>
        <td class="col-updated"><span class="proj-when">${fmtDate(e.updated)}</span></td>
    `;
    return tr;
}

function renderTable(entries) {
    const body = document.getElementById('proj-rows');
    if (!body) return;
    const sorted = entries.slice().sort((a, b) => new Date(b.start || 0) - new Date(a.start || 0));
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

function olderOf(a, b) { return new Date(a) < new Date(b) ? a : b; }
function newerOf(a, b) { return new Date(a) > new Date(b) ? a : b; }

async function loadProjects() {
    const body = document.getElementById('proj-rows');
    if (!body) return;

    // Static render first, so the page is useful even if GitHub is unreachable.
    renderTable(CURATED);

    try {
        const res = await fetch('https://api.github.com/users/jackwallner/repos?type=public&sort=updated&per_page=100');
        if (!res.ok) throw new Error('GitHub API ' + res.status);
        const repos = await res.json();

        const entries = CURATED.map(e => ({ ...e }));
        const entryByRepo = {};
        entries.forEach(e => { if (e.repo) entryByRepo[e.repo] = e; });

        repos.filter(r => !r.fork && !r.archived).forEach(r => {
            const key = r.name.toLowerCase();
            if (FOLDED[key]) {
                const t = entryByRepo[FOLDED[key]];
                if (t) { t.start = olderOf(t.start, r.created_at); t.updated = newerOf(t.updated, r.pushed_at); }
                return;
            }
            if (entryByRepo[key]) {
                entryByRepo[key].start = r.created_at;
                entryByRepo[key].updated = r.pushed_at;
                return;
            }
            // Long tail: real repo with no curated entry.
            entries.push({
                name: r.name,
                desc: stripEmoji(r.description),
                icon: null,
                type: 'Repo',
                status: 'Code',
                cls: 'code',
                link: r.html_url,
                ext: true,
                start: r.created_at,
                updated: r.pushed_at
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
