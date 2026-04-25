const TYPE_ICONS = {
    architect: '.',
    detective: '?',
    advocate: '!',
    explorer: '~',
    reporter: ':',
    collector: '&',
    improviser: '—',
    wanderer: '…',
};

const TYPE_ORDER = [
    'architect', 'detective', 'advocate', 'explorer',
    'reporter', 'collector', 'improviser', 'wanderer',
];

let currentUnit = null;
let classData = null;

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
        document.getElementById('tab-' + tab.dataset.tab).style.display = 'block';

        if (tab.dataset.tab === 'students') loadStudents();
        if (tab.dataset.tab === 'grouping') loadGrouping();
        if (tab.dataset.tab === 'alerts') loadAlerts();
        if (tab.dataset.tab === 'knowledge') loadKnowledge();
    });
});

// No unit filter — always show All Units

// Overview
async function loadOverview() {
    const url = currentUnit ? `/api/class-overview?unit_id=${currentUnit}` : '/api/class-overview';
    const res = await fetch(url);
    classData = await res.json();
    renderStats();
    renderTypeGrid();
}

function renderStats() {
    const dist = classData.distribution;
    let deepCount = 0, surfaceCount = 0, boundaryCount = 0;

    Object.entries(dist).forEach(([type, info]) => {
        info.students.forEach(s => {
            if (s.secondary_type) boundaryCount++;
            else if (['architect','detective','advocate','explorer'].includes(type)) deepCount++;
            else surfaceCount++;
        });
    });

    const activeTypes = Object.keys(dist);
    const activeStudents = [];
    Object.values(dist).forEach(info => activeStudents.push(...info.students));
    const boundaryStudents = activeStudents.filter(s => s.secondary_type);

    document.getElementById('statsRow').innerHTML = `
        <div class="stat-card stat-card-clickable" id="statTotal">
            <div class="stat-value">${classData.total_students}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-card stat-card-clickable" id="statActiveTypes">
            <div class="stat-value">${activeTypes.length}</div>
            <div class="stat-label">Active Types</div>
        </div>
        <div class="stat-card stat-card-clickable" id="statBoundary">
            <div class="stat-value">${boundaryCount}</div>
            <div class="stat-label">Boundary Profiles</div>
        </div>
    `;

    document.getElementById('statActiveTypes').addEventListener('click', () => {
        let body = '';
        activeTypes.forEach(t => {
            const m = classData.type_meta[t];
            const students = dist[t].students;
            body += `<div style="margin-bottom:16px">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                    <img src="/static/img/${t}.png" style="width:28px;height:28px;object-fit:contain">
                    <span style="font-weight:600;color:${m.color};font-size:14px">${m.label}</span>
                    <span style="font-size:12px;color:var(--text-muted)">${students.length} student${students.length!==1?'s':''}</span>
                </div>`;
            students.forEach(s => {
                body += `<div class="type-modal-student-row" style="cursor:pointer" onclick="document.getElementById('listModal').classList.remove('visible');openStudentModal('${s.id}')">
                    <div style="display:flex;align-items:center;gap:10px;flex:1">
                        <div class="type-modal-student-dot" style="background:${m.color}"></div>
                        <div style="font-weight:500;font-size:13px">${s.name}</div>
                    </div>
                    <div class="type-modal-student-scores">
                        <span>D:${s.depth.toFixed(1)}</span>
                        <span>S:${s.structure.toFixed(1)}</span>
                        <span>E:${s.evidence.toFixed(1)}</span>
                    </div>
                </div>`;
            });
            body += `</div>`;
        });
        openListModal('All Students by Type', body);
    });

    document.getElementById('statBoundary').addEventListener('click', () => {
        if (!boundaryStudents.length) return;
        openListModal('Boundary Profiles', `
            <div style="font-size:13px;color:var(--text-secondary);margin-bottom:12px">
                These students scored in the boundary zone (4.0–6.0) on one or more dimensions, so their type is less certain.
            </div>` +
            boundaryStudents.map(s => `
                <div class="type-modal-student-row" style="cursor:pointer" onclick="document.getElementById('listModal').classList.remove('visible');openStudentModal('${s.id}')">
                    <div style="display:flex;align-items:center;gap:10px;flex:1">
                        <div class="type-modal-student-dot" style="background:var(--text-muted)"></div>
                        <div>
                            <div style="font-weight:500">${s.name}</div>
                            <span style="font-size:11px;color:var(--text-muted)">Also shows ${s.secondary_type} traits</span>
                        </div>
                    </div>
                    <div class="type-modal-student-scores">
                        <span>D:${s.depth.toFixed(1)}</span>
                        <span>S:${s.structure.toFixed(1)}</span>
                        <span>E:${s.evidence.toFixed(1)}</span>
                    </div>
                </div>
            `).join(''));
    });
}

function renderTypeGrid() {
    const dist = classData.distribution;
    const grid = document.getElementById('typeGrid');
    let html = '';

    TYPE_ORDER.forEach(type => {
        const info = dist[type];
        const meta = classData.type_meta[type];
        const count = info ? info.students.length : 0;
        const color = meta.color;

        html += `
            <div class="type-card" data-type="${type}">
                <div class="type-color-bar" style="background:${color}"></div>
                <div class="type-card-top">
                    <div style="flex:1;min-width:0">
                        <div class="type-card-header">
                            <span class="type-name" style="color:${color}">${meta.label}</span>
                            <span class="type-count" style="color:${color}">${count}</span>
                        </div>
                        <div class="type-desc">${meta.description}</div>
                    </div>
                    <img src="/static/img/${type}.png" class="type-card-img" alt="${meta.label}">
                </div>
                <div class="type-students">
                    ${info ? info.students.map(s =>
                        `<span class="type-student-chip" data-student="${s.id}" style="border-color:${color}40">${s.name}</span>`
                    ).join('') : '<span style="color:var(--text-muted);font-size:11px">No students</span>'}
                </div>
            </div>
        `;
    });

    grid.innerHTML = html;

    grid.querySelectorAll('.type-card').forEach(card => {
        card.addEventListener('click', () => {
            openTypeModal(card.dataset.type);
        });
    });

    grid.querySelectorAll('.type-student-chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
            e.stopPropagation();
            openStudentModal(chip.dataset.student);
        });
    });
}

// List Modal (for stat card clicks)
function openListModal(title, bodyHtml) {
    document.getElementById('listModalTitle').textContent = title;
    document.getElementById('listModalBody').innerHTML = bodyHtml;
    document.getElementById('listModal').classList.add('visible');
}

// Type Detail Modal
function openTypeModal(type) {
    const meta = classData.type_meta[type];
    const dist = classData.distribution[type];
    const students = dist ? dist.students : [];
    const color = meta.color;

    document.getElementById('typeModalHeader').innerHTML = `
        <div style="font-size:18px;font-weight:600;color:${color}">${meta.label}</div>
        <div style="font-size:13px;color:var(--text-secondary);margin-top:2px">${students.length} student${students.length !== 1 ? 's' : ''}</div>
    `;

    let html = `
        <div class="type-modal-hero">
            <img src="/static/img/${type}.png" class="type-modal-img" alt="${meta.label}">
            <div class="type-modal-info">
                <div style="font-size:15px;color:var(--text-primary);line-height:1.6;margin-bottom:16px">
                    ${meta.description}
                </div>
                <div class="grid-2">
                    <div class="info-block">
                        <div class="info-block-label">Strengths</div>
                        <div class="info-block-value">${meta.strengths}</div>
                    </div>
                    <div class="info-block">
                        <div class="info-block-label">Growth Opportunities</div>
                        <div class="info-block-value">${meta.growth}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Teacher tip
    html += `
        <div class="teacher-tip" style="margin-top:16px;background:${color}10;border-color:${color}30">
            <div class="teacher-tip-header" style="color:${color}">Teacher Tip</div>
            <div class="teacher-tip-body">${meta.teacher_tip}</div>
        </div>
    `;

    if (students.length) {
        html += `
            <div style="margin-top:20px">
                <div class="info-block-label" style="margin-bottom:10px">Students (${students.length})</div>
                <div class="type-modal-students">
        `;
        students.forEach(s => {
            const secHtml = s.secondary_type
                ? `<span style="font-size:11px;color:var(--text-muted)">Also shows ${s.secondary_type} traits</span>`
                : '';
            html += `
                <div class="type-modal-student-row" data-student="${s.id}">
                    <div style="display:flex;align-items:center;gap:10px;flex:1">
                        <div class="type-modal-student-dot" style="background:${color}"></div>
                        <div>
                            <div style="font-weight:500;font-size:14px">${s.name}</div>
                            ${secHtml}
                        </div>
                    </div>
                    <div class="type-modal-student-scores">
                        <span title="Depth">D:${s.depth.toFixed(1)}</span>
                        <span title="Structure">S:${s.structure.toFixed(1)}</span>
                        <span title="Evidence">E:${s.evidence.toFixed(1)}</span>
                        <span title="Confidence" style="color:var(--text-secondary)">${Math.round(s.confidence * 100)}%</span>
                    </div>
                </div>
            `;
        });
        html += '</div></div>';
    }

    document.getElementById('typeModalBody').innerHTML = html;
    document.getElementById('typeModal').classList.add('visible');

    document.querySelectorAll('.type-modal-student-row').forEach(row => {
        row.addEventListener('click', () => {
            document.getElementById('typeModal').classList.remove('visible');
            openStudentModal(row.dataset.student);
        });
    });
}

// Close type modal on overlay click
document.getElementById('typeModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        e.currentTarget.classList.remove('visible');
    }
});

// Student Modal
async function openStudentModal(studentId) {
    const res = await fetch(`/api/student/${studentId}`);
    const data = await res.json();

    document.getElementById('modalStudentName').textContent =
        `${data.first_name} ${data.last_name}`;

    const t = data.overall;
    const info = data.type_info;

    document.getElementById('modalStudentMeta').textContent = 'Grade 6';

    let bodyHtml = '';

    // Type header with character
    if (t) {
        bodyHtml += `
        <div class="modal-type-header" style="margin-bottom:20px">
            <div>
                <div style="margin-bottom:8px">
                    <span class="type-badge" style="background:${info.color}">${info.label}</span>
                    <span class="type-badge" style="background:var(--bg);color:var(--text-secondary);font-weight:500">${Math.round(t.confidence * 100)}% confidence</span>
                    ${t.secondary_type ? `<span class="type-badge type-badge-secondary">Also shows ${t.secondary_type} traits</span>` : ''}
                </div>
                <div style="font-size:14px;color:var(--text-secondary);line-height:1.5">${info.description}</div>
            </div>
            <img src="/static/img/${t.primary_type}.png" class="modal-character-img" alt="${info.label}">
        </div>`;
    }

    // Dimension bars
    if (t) {
        bodyHtml += `<div style="margin-bottom:24px">`;
        bodyHtml += renderDimensionBar('Depth', 'Surface', 'Deep', t.depth_score, info.color);
        bodyHtml += renderDimensionBar('Structure', 'Systematic', 'Exploratory', t.structure_score, info.color);
        bodyHtml += renderDimensionBar('Evidence', 'Convergent', 'Divergent', t.evidence_score, info.color);
        bodyHtml += `</div>`;
    }

    // Type info
    if (info) {
        bodyHtml += `
            <div class="grid-2" style="margin-bottom:24px">
                <div class="info-block">
                    <div class="info-block-label">Strengths</div>
                    <div class="info-block-value">${info.strengths}</div>
                </div>
                <div class="info-block">
                    <div class="info-block-label">Growth Opportunities</div>
                    <div class="info-block-value">${info.growth}</div>
                </div>
            </div>
        `;
    }

    // Timeline
    if (data.per_unit && data.per_unit.length > 1) {
        bodyHtml += `
            <div class="info-block">
                <div class="info-block-label">Thinking Type Over Time</div>
                <div class="timeline" style="margin-top:12px">
        `;
        data.per_unit.forEach((pu, i) => {
            const typeColor = classData.type_meta[pu.primary_type]?.color || '#666';
            const label = classData.type_meta[pu.primary_type]?.label || pu.primary_type;
            const initial = label.charAt(0);

            if (i > 0) {
                bodyHtml += `<div class="timeline-connector"></div>`;
            }
            bodyHtml += `
                <div class="timeline-node">
                    <div class="timeline-dot" style="background:${typeColor}">${initial}</div>
                    <div class="timeline-unit">${pu.unit_id}</div>
                    <div class="timeline-type" style="color:${typeColor}">${label}</div>
                </div>
            `;
        });
        bodyHtml += `</div></div>`;
    }

    document.getElementById('modalBody').innerHTML = bodyHtml;

    const overlay = document.getElementById('studentModal');
    overlay.classList.add('visible');

    var typeColor = (info && info.color) ? info.color : '#f37321';
    loadStudentKnowledge(studentId, document.getElementById('modalBody'), typeColor);
}

function renderDimensionBar(label, leftPole, rightPole, score, color) {
    const pct = (score / 10) * 100;
    const inBoundary = score >= 4.0 && score <= 6.0;
    const boundaryClass = inBoundary ? 'opacity:0.6' : '';

    return `
        <div class="dimension-row">
            <div class="dimension-label">${label}</div>
            <div class="dimension-pole left">${leftPole}</div>
            <div class="dimension-bar-container">
                <div class="dimension-bar-bg">
                    <div class="dimension-bar-fill" style="width:${pct}%;background:${color};${boundaryClass}"></div>
                    <div class="dimension-bar-boundary low"></div>
                    <div class="dimension-bar-boundary high"></div>
                </div>
            </div>
            <div class="dimension-pole right">${rightPole}</div>
            <div class="dimension-score">${score.toFixed(1)}</div>
        </div>
    `;
}

// Close modal
document.getElementById('modalClose').addEventListener('click', () => {
    document.getElementById('studentModal').classList.remove('visible');
});
document.getElementById('studentModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        e.currentTarget.classList.remove('visible');
    }
});

// Pair image lookup — values are the canonical filename key
const PAIR_IMAGES = {
    'architect_wanderer': 'architect_wanderer',
    'wanderer_architect': 'architect_wanderer',
    'detective_improviser': 'detective_improviser',
    'improviser_detective': 'detective_improviser',
    'advocate_collector': 'advocate_collector',
    'collector_advocate': 'advocate_collector',
    'explorer_reporter': 'explorer_reporter',
    'reporter_explorer': 'explorer_reporter',
};

function getPairImageKey(typeA, typeB) {
    return PAIR_IMAGES[`${typeA}_${typeB}`] || PAIR_IMAGES[`${typeB}_${typeA}`] || null;
}

// Grouping
async function loadGrouping() {
    const url = currentUnit ? `/api/grouping?unit_id=${currentUnit}` : '/api/grouping';
    const res = await fetch(url);
    const data = await res.json();

    const container = document.getElementById('pairsContainer');

    if (!data.pairs.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-title">No grouping suggestions yet</div></div>';
        return;
    }

    // Split into featured (with pair images) and remaining
    const usedImages = new Set();
    const featured = [];
    const remaining = [];

    data.pairs.forEach(pair => {
        const imgKey = getPairImageKey(pair.student_a.type, pair.student_b.type);
        if (imgKey && !usedImages.has(imgKey)) {
            usedImages.add(imgKey);
            featured.push({ ...pair, imgKey });
        } else {
            remaining.push(pair);
        }
    });

    let html = '';

    // Featured pairs with illustrations
    if (featured.length) {
        html += '<div class="grid-2" style="margin-bottom:24px">';
        featured.forEach(pair => {
            html += `
                <div class="pair-card">
                    <img src="/static/img/pair_${pair.imgKey}.png" class="pair-illustration" alt="pair">
                    <div class="pair-students">
                        <div class="pair-student">
                            <img src="/static/img/${pair.student_a.type}.png" class="pair-student-avatar" alt="">
                            <div>
                                <div class="pair-student-name">${pair.student_a.name}</div>
                                <div class="pair-student-type" style="color:${pair.student_a.color}">${pair.student_a.label}</div>
                            </div>
                        </div>
                        <div class="pair-connector">&harr;</div>
                        <div class="pair-student">
                            <img src="/static/img/${pair.student_b.type}.png" class="pair-student-avatar" alt="">
                            <div>
                                <div class="pair-student-name">${pair.student_b.name}</div>
                                <div class="pair-student-type" style="color:${pair.student_b.color}">${pair.student_b.label}</div>
                            </div>
                        </div>
                    </div>
                    <div class="pair-reason">${pair.pairing_reason}</div>
                </div>
            `;
        });
        html += '</div>';
    }

    // Remaining pairs without illustrations
    if (remaining.length) {
        html += `
            <div style="margin-top:8px">
                <div style="font-size:13px;font-weight:600;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px">Additional Pairs</div>
                <div class="pair-list">
        `;
        remaining.forEach(pair => {
            html += `
                <div class="pair-list-row">
                    <div class="pair-list-student">
                        <img src="/static/img/${pair.student_a.type}.png" class="pair-list-avatar" alt="">
                        <span class="pair-list-name">${pair.student_a.name}</span>
                        <span class="pair-list-type" style="color:${pair.student_a.color}">${pair.student_a.label}</span>
                    </div>
                    <span class="pair-list-arrow">&harr;</span>
                    <div class="pair-list-student">
                        <img src="/static/img/${pair.student_b.type}.png" class="pair-list-avatar" alt="">
                        <span class="pair-list-name">${pair.student_b.name}</span>
                        <span class="pair-list-type" style="color:${pair.student_b.color}">${pair.student_b.label}</span>
                    </div>
                    <span class="pair-list-reason">${pair.pairing_reason}</span>
                </div>
            `;
        });
        html += '</div></div>';
    }

    container.innerHTML = html;
}

// Alerts
async function loadAlerts() {
    const res = await fetch('/api/alerts');
    const data = await res.json();

    const container = document.getElementById('alertsContainer');

    if (!data.alerts.length) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-title">No alerts at this time</div></div>';
        return;
    }

    let html = '';
    data.alerts.forEach(alert => {
        html += `
            <div class="alert-card ${alert.alert_type}">
                <div class="alert-header">
                    <span class="alert-name">${alert.first_name} ${alert.last_name}</span>
                    <span class="alert-badge ${alert.alert_type}">
                        ${alert.alert_type === 'warning' ? 'Needs Attention' :
                          alert.alert_type === 'stable' ? 'Stable Pattern' : 'Positive Growth'}
                    </span>
                </div>
                <div class="alert-message">${alert.message}</div>
                <div class="alert-timeline">
                    ${alert.type_sequence.map((ts, i) => `
                        ${i > 0 ? '<span class="alert-timeline-arrow">&rarr;</span>' : ''}
                        <span class="alert-timeline-step">
                            <img src="/static/img/${ts.type}.png" class="alert-timeline-img" alt="">
                            <span class="alert-timeline-label" style="color:${ts.color}">${ts.label}</span>
                            <span class="alert-timeline-unit">${ts.unit_id}</span>
                        </span>
                    `).join('')}
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

// Close list modal on overlay click
document.getElementById('listModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        e.currentTarget.classList.remove('visible');
    }
});

// Students tab
let studentsData = null;

async function loadStudents() {
    if (!studentsData) {
        const res = await fetch('/api/students');
        studentsData = await res.json();
    }
    renderStudentTable(studentsData.students);

    const search = document.getElementById('studentSearch');
    search.oninput = () => {
        const q = search.value.toLowerCase();
        const filtered = studentsData.students.filter(s =>
            `${s.first_name} ${s.last_name}`.toLowerCase().includes(q) ||
            s.label.toLowerCase().includes(q)
        );
        renderStudentTable(filtered);
    };
}

function renderStudentTable(students) {
    const tbody = document.getElementById('studentTableBody');
    let html = '';

    students.forEach(s => {
        const historyDots = s.per_unit.map((pu, i) => {
            const arrow = i > 0 ? '<span class="student-history-arrow">&rarr;</span>' : '';
            return `${arrow}<span class="student-history-dot" style="background:${pu.color}" title="${pu.label} (${pu.unit_id})">${pu.label.charAt(0)}</span>`;
        }).join('');

        const confPct = Math.round(s.confidence * 100);
        const secHtml = s.secondary_type ? `<span style="font-size:11px;color:var(--text-muted);margin-left:6px">(+ ${s.secondary_type})</span>` : '';

        html += `
            <tr data-student="${s.student_id}">
                <td>
                    <div class="student-name-cell">
                        <img src="/static/img/${s.type}.png" alt="">
                        ${s.first_name} ${s.last_name}
                    </div>
                </td>
                <td><span class="student-type-badge" style="background:${s.color}">${s.label}</span>${secHtml}</td>
                <td class="student-score-cell">${s.depth.toFixed(1)}</td>
                <td class="student-score-cell">${s.structure.toFixed(1)}</td>
                <td class="student-score-cell">${s.evidence.toFixed(1)}</td>
                <td class="student-score-cell">${confPct}%</td>
                <td><div class="student-history-dots">${historyDots}</div></td>
            </tr>
        `;
    });

    tbody.innerHTML = html;

    tbody.querySelectorAll('tr').forEach(row => {
        row.addEventListener('click', () => openStudentModal(row.dataset.student));
    });
}

// Guide rendering
function renderGuide() {
    if (!classData || !classData.type_meta) return;

    // Hero characters removed for cleaner look

    // Types grid
    const grid = document.getElementById('guideTypesGrid');
    if (!grid) return;

    const FORMULAS = {
        architect: 'Deep + Systematic + Convergent',
        detective: 'Deep + Systematic + Divergent',
        advocate: 'Deep + Exploratory + Convergent',
        explorer: 'Deep + Exploratory + Divergent',
        reporter: 'Surface + Systematic + Convergent',
        collector: 'Surface + Systematic + Divergent',
        improviser: 'Surface + Exploratory + Convergent',
        wanderer: 'Surface + Exploratory + Divergent',
    };

    grid.innerHTML = TYPE_ORDER.map(type => {
        const meta = classData.type_meta[type];
        return `
            <div class="guide-type-card-v2" data-type="${type}" style="border-top: 3px solid ${meta.color}">
                <img src="/static/img/${type}.png" class="guide-type-img-v2" alt="${meta.label}">
                <div class="guide-type-name-v2" style="color:${meta.color}">${meta.label}</div>
                <div class="guide-type-formula-v2">${FORMULAS[type]}</div>
                <div class="guide-type-desc-v2">${meta.description}</div>
            </div>
        `;
    }).join('');

    grid.querySelectorAll('.guide-type-card-v2').forEach(card => {
        card.addEventListener('click', () => openTypeModal(card.dataset.type));
    });
}

// Knowledge Graph
let kgData = null;

async function loadKnowledge() {
    var res = await fetch('/api/knowledge-graph?t=' + Date.now());
    kgData = await res.json();
    renderKnowledgeGraph();
    loadKnowledgeByType();
}

function masteryOrange(val) {
    var lightness = 85 - val * 40;
    return 'hsl(25, 90%, ' + Math.round(lightness) + '%)';
}

function masteryFromTypeColor(val, hexColor) {
    var r = parseInt(hexColor.slice(1,3), 16);
    var g = parseInt(hexColor.slice(3,5), 16);
    var b = parseInt(hexColor.slice(5,7), 16);
    var mix = 0.3 + val * 0.7;
    var bg = 230;
    var fr = Math.round(bg + (r - bg) * mix);
    var fg = Math.round(bg + (g - bg) * mix);
    var fb = Math.round(bg + (b - bg) * mix);
    return 'rgb(' + fr + ',' + fg + ',' + fb + ')';
}

function renderKnowledgeGraph() {
    const container = document.getElementById('knowledgeTree');
    const mastery = kgData.class_mastery;

    const levelMap = {
        'r-decode': 0, 'r-vocab': 0, 'r-literal': 1, 'r-inference': 2,
        'r-main-idea': 3, 'r-text-structure': 3, 'r-cross-text': 4,
        'w-conventions': 0, 'w-organization': 1, 'w-evidence': 2,
        'w-elaboration': 3, 'w-counterargument': 3, 'w-revision': 4,
        'h-synthesis': 0, 'h-argumentation': 1,
    };

    const columns = [
        { key: 'reading', label: 'Reading', nodes: [] },
        { key: 'writing', label: 'Writing', nodes: [] },
        { key: 'thinking', label: 'Higher-Order Thinking', nodes: [] },
    ];

    const domainMap = {};
    columns.forEach(c => { domainMap[c.key] = c; });
    kgData.nodes.forEach(n => {
        if (domainMap[n.domain]) domainMap[n.domain].nodes.push(n);
    });

    const crossEdges = kgData.edges.filter(e => {
        const fromNode = kgData.nodes.find(n => n.node_id === e.parent_id);
        const toNode = kgData.nodes.find(n => n.node_id === e.child_id);
        return fromNode && toNode && fromNode.domain !== toNode.domain;
    });

    let html = '';

    columns.forEach(col => {
        html += `<div class="kg-column">`;
        html += `<div class="kg-col-header">${col.label}</div>`;

        const levels = {};
        col.nodes.forEach(n => {
            const lv = levelMap[n.node_id] ?? 0;
            if (!levels[lv]) levels[lv] = [];
            levels[lv].push(n);
        });

        const levelKeys = Object.keys(levels).map(Number).sort((a, b) => a - b);

        levelKeys.forEach(lv => {
            const nodesAtLevel = levels[lv];
            html += `<div class="kg-level"><div class="kg-level-cards">`;

            nodesAtLevel.forEach(n => {
                const m = mastery[n.node_id];
                const avg = m ? m.avg_mastery : 0;
                const pct = Math.round(avg * 100);
                const color = masteryOrange(avg);

                html += `
                    <div class="kg-skill-card" data-node="${n.node_id}" onclick="showKgNodeDetail('${n.node_id}')">
                        <div class="kg-skill-name">${n.label}</div>
                        <div class="kg-skill-bar-track">
                            <div class="kg-skill-bar-fill" style="width:${pct}%;background:${color}"></div>
                        </div>
                        <span class="kg-skill-pct" style="color:${color}">${pct}%</span>
                        <span class="kg-skill-grade">Gr ${n.grade_level}</span>
                    </div>`;
            });

            html += `</div></div>`;
        });

        const feedsInto = crossEdges.filter(e => {
            const fromNode = kgData.nodes.find(n => n.node_id === e.parent_id);
            return fromNode && fromNode.domain === col.key;
        });

        if (feedsInto.length) {
            const targets = feedsInto.map(e => {
                const toNode = kgData.nodes.find(n => n.node_id === e.child_id);
                return toNode ? toNode.label : '';
            }).filter(Boolean);
            html += `<div class="kg-feeds-into"><span class="kg-feeds-arrow">&darr;</span> Feeds into: ${targets.join(', ')}</div>`;
        }

        html += `</div>`;
    });

    container.innerHTML = html;
}

// Knowledge by Type comparison
let kgActiveTypes = new Set();

function loadKnowledgeByType() {
    if (!kgData || !kgData.by_type) return;
    if (kgActiveTypes.size === 0) {
        var types = Object.keys(kgData.by_type);
        if (types.indexOf('architect') >= 0) kgActiveTypes.add('architect');
        if (types.indexOf('wanderer') >= 0) kgActiveTypes.add('wanderer');
    }
    renderTypeFilters();
    renderTypeChart();
}

function renderTypeFilters() {
    var container = document.getElementById('kgTypeFilters');
    if (!container) return;
    var types = Object.keys(kgData.by_type);

    container.innerHTML = types.map(function(t) {
        var label = kgData.type_labels[t];
        var color = kgData.type_colors[t];
        var active = kgActiveTypes.has(t);
        return '<button class="kg-type-toggle ' + (active ? 'active' : '') + '"'
            + ' data-type="' + t + '"'
            + ' style="' + (active ? 'background:' + color + ';border-color:' + color : 'border-color:' + color + '40;color:' + color) + '">'
            + '<img src="/static/img/' + t + '.png" alt="">' + label
            + '</button>';
    }).join('');

    container.querySelectorAll('.kg-type-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const t = btn.dataset.type;
            if (kgActiveTypes.has(t)) kgActiveTypes.delete(t);
            else kgActiveTypes.add(t);
            renderTypeFilters();
            renderTypeChart();
        });
    });
}

function renderTypeChart() {
    var container = document.getElementById('kgTypeChart');
    if (!container) return;
    var selected = Array.from(kgActiveTypes);

    if (selected.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-title">Select thinking types above to compare their skill profiles</div></div>';
        return;
    }

    var nodes = kgData.nodes;
    var domains = { reading: 'Reading', writing: 'Writing', thinking: 'Higher-Order' };

    var html = '<table class="kg-compare-table"><thead><tr><th>Skill</th>';

    selected.forEach(function(t) {
        var color = kgData.type_colors[t];
        html += '<th><span style="color:' + color + '">' + kgData.type_labels[t] + '</span></th>';
    });

    html += '</tr></thead><tbody>';

    var currentDomain = '';

    nodes.forEach(function(n) {
        if (n.domain !== currentDomain) {
            currentDomain = n.domain;
            html += '<tr><td colspan="' + (selected.length + 1) + '" style="padding:12px 12px 6px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:var(--text-muted);background:var(--bg);border-bottom:1px solid var(--border)">' + (domains[n.domain] || n.domain) + '</td></tr>';
        }

        html += '<tr><td class="kg-compare-skill-name">' + n.label + '</td>';

        selected.forEach(function(t) {
            var typeData = kgData.by_type[t];
            var val = typeData ? typeData[n.node_id] : null;
            if (val == null) {
                html += '<td class="kg-compare-cell"><span style="color:var(--text-muted)">—</span></td>';
                return;
            }
            var pct = Math.round(val * 100);
            var typeColor = kgData.type_colors[t];
            var barColor = masteryFromTypeColor(val, typeColor);

            html += '<td class="kg-compare-cell">'
                + '<div class="kg-compare-bar-row">'
                + '<div class="kg-compare-bar-track">'
                + '<div class="kg-compare-bar-fill" style="width:' + pct + '%;background:' + barColor + '"></div>'
                + '</div>'
                + '<span class="kg-compare-bar-value" style="color:' + typeColor + '">' + pct + '%</span>'
                + '</div></td>';
        });

        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

async function showKgNodeDetail(nodeId) {
    const node = kgData.nodes.find(n => n.node_id === nodeId);
    if (!node) return;

    const m = kgData.class_mastery[nodeId];
    const avg = m ? m.avg_mastery : 0;

    const res = await fetch(`/api/knowledge-node/${nodeId}/students`);
    const studentMasteries = (await res.json()).students.map(s => ({
        student_id: s.student_id,
        name: `${s.first_name} ${s.last_name}`,
        mastery: s.mastery_level,
    }));

    const prereqs = kgData.edges
        .filter(e => e.child_id === nodeId)
        .map(e => kgData.nodes.find(n => n.node_id === e.parent_id))
        .filter(Boolean);

    const dependents = kgData.edges
        .filter(e => e.parent_id === nodeId)
        .map(e => kgData.nodes.find(n => n.node_id === e.child_id))
        .filter(Boolean);

    let html = `
        <div class="kg-detail-header">
            <div>
                <div class="kg-detail-title">${node.label}</div>
                <div class="kg-detail-meta">${node.domain} · Grade ${node.grade_level}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:24px;font-weight:700;color:${masteryOrange(avg)}">${Math.round(avg * 100)}%</div>
                <div style="font-size:11px;color:var(--text-muted)">Class Average</div>
            </div>
        </div>
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;color:var(--text-muted);margin-bottom:8px">
            Student Mastery (${studentMasteries.length})
        </div>
    `;

    studentMasteries.forEach(s => {
        const pct = Math.round(s.mastery * 100);
        const color = masteryOrange(s.mastery);
        html += `
            <div class="kg-detail-bar-row">
                <div class="kg-detail-bar-name" onclick="openStudentModal('${s.student_id}')">${s.name}</div>
                <div class="kg-detail-bar-track">
                    <div class="kg-detail-bar-fill" style="width:${pct}%;background:${color}"></div>
                </div>
                <div class="kg-detail-bar-value">${pct}%</div>
            </div>
        `;
    });

    if (prereqs.length) {
        html += `
            <div class="kg-prereq-section">
                <div class="kg-prereq-label">Prerequisites</div>
                <div class="kg-prereq-chips">
                    ${prereqs.map(p => `<span class="kg-prereq-chip">${p.label}</span>`).join('')}
                </div>
            </div>`;
    }

    if (dependents.length) {
        html += `
            <div class="kg-prereq-section" style="margin-top:12px;padding-top:12px">
                <div class="kg-prereq-label">Unlocks</div>
                <div class="kg-prereq-chips">
                    ${dependents.map(p => `<span class="kg-prereq-chip">${p.label}</span>`).join('')}
                </div>
            </div>`;
    }

    const detail = document.getElementById('kgNodeDetail');
    detail.innerHTML = html;
    detail.style.display = 'block';
    detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Also add knowledge graph to student modal
async function loadStudentKnowledge(studentId, containerEl, typeColor) {
    var res = await fetch('/api/student/' + studentId + '/knowledge');
    var data = await res.json();

    if (!data.mastery || !Object.keys(data.mastery).length) return;

    var baseColor = typeColor || '#f37321';

    var html = '<div class="info-block" style="margin-top:24px">'
        + '<div class="info-block-label">Skill Mastery</div>'
        + '<div style="margin-top:8px">';

    var domains = { reading: 'Reading', writing: 'Writing', thinking: 'Higher-Order' };

    Object.entries(domains).forEach(function(entry) {
        var domain = entry[0], label = entry[1];
        var domainNodes = data.nodes.filter(function(n) { return n.domain === domain; });
        if (!domainNodes.length) return;

        html += '<div style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin:12px 0 6px">' + label + '</div>';

        domainNodes.forEach(function(n) {
            var m = data.mastery[n.node_id];
            var val = m ? m.mastery_level : 0;
            var pct = Math.round(val * 100);
            var color = masteryFromTypeColor(val, baseColor);
            html += '<div class="kg-detail-bar-row">'
                + '<div class="kg-detail-bar-name" style="cursor:default">' + n.label + '</div>'
                + '<div class="kg-detail-bar-track">'
                + '<div class="kg-detail-bar-fill" style="width:' + pct + '%;background:' + color + '"></div>'
                + '</div>'
                + '<div class="kg-detail-bar-value">' + pct + '%</div>'
                + '</div>';
        });
    });

    html += '</div></div>';
    containerEl.insertAdjacentHTML('beforeend', html);
}

// Init
loadOverview().then(() => renderGuide());
