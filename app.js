const state = { reports: [], education: [] };
const rssUrl = 'https://www.korea.kr/rss/dept_mois.xml';
const el = (id) => document.getElementById(id);
const nf = new Intl.NumberFormat('ko-KR');
const n = (v) => nf.format(v ?? 0);
const data = window.__DATA__ || { reports: [], education: [] };

function options(values, label) {
  return [`${label} 전체`, ...Array.from(new Set(values.filter(Boolean))).sort()];
}

function renderFilters() {
  el('typeFilter').innerHTML = options(state.reports.map((r) => r['신고유형']), '신고유형')
    .map((v) => `<option value="${v === '신고유형 전체' ? '' : v}">${v}</option>`).join('');
  el('statusFilter').innerHTML = options(state.reports.map((r) => r['처리상태']), '처리상태')
    .map((v) => `<option value="${v === '처리상태 전체' ? '' : v}">${v}</option>`).join('');
}

function card(row) {
  return `<article class="card">
    <div class="top">
      <strong>${row['사건ID'] || '-'}</strong>
      <span class="pill status-${row['처리상태']}">${row['처리상태'] || '-'}</span>
    </div>
    <div class="meta">
      <div><span class="meta-label muted">신고유형</span> ${row['신고유형'] || '-'}</div>
      <div><span class="meta-label muted">지역</span> ${row['지역'] || '-'}</div>
      <div><span class="meta-label muted">조치 결과</span> ${row['조치결과'] || '미상'}</div>
    </div>
    <div class="card-footer">
      <time>${row['신고일자'] || '-'}</time>
    </div>
  </article>`;
}

function renderReports() {
  const type = el('typeFilter').value;
  const status = el('statusFilter').value;
  const rows = state.reports.filter((r) => (!type || r['신고유형'] === type) && (!status || r['처리상태'] === status));
  el('cards').innerHTML = rows.map(card).join('') || '<div class="muted">조건에 맞는 사건이 없습니다.</div>';
  el('resultCount').textContent = `결과 ${rows.length}건`;
}

function renderEducation() {
  const valid = state.education.filter((r) => r['교육이수율'] != null);
  const avg = valid.length ? (valid.reduce((s, r) => s + r['교육이수율'], 0) / valid.length).toFixed(1) : '-';
  const totalParticipants = state.education.reduce((s, r) => s + (r['교육참여자수'] || 0), 0);
  const avgHours = (state.education.reduce((s, r) => s + (r['연간교육시간'] || 0), 0) / Math.max(state.education.length, 1)).toFixed(1);

  el('totalCases').textContent = n(state.reports.length);
  el('avgEduRate').textContent = avg + (avg === '-' ? '' : '%');
  el('excellentRate').textContent = (state.education.filter((r) => r['청렴우수기관'] === 'Y').length / Math.max(state.education.length, 1) * 100).toFixed(1) + '%';
  el('eduSummary').innerHTML = `
    <div class="edu-item"><strong>${avg}${avg === '-' ? '' : '%'}</strong><span>평균 교육이수율</span></div>
    <div class="edu-item"><strong>${n(totalParticipants)}명</strong><span>교육 참여자 수 합계</span></div>
    <div class="edu-item"><strong>${avgHours}시간</strong><span>연간 교육시간 평균</span></div>
  `;
}

async function loadRss() {
  try {
    if (Array.isArray(window.__RSS_ITEMS__) && window.__RSS_ITEMS__.length) {
      const items = window.__RSS_ITEMS__.slice(0, 5);
      el('rssStatus').textContent = `최신 ${items.length}건 표시`;
      el('rssList').innerHTML = items.map((item) => `<li><a href="${item.link}" target="_blank" rel="noreferrer">${item.title}</a><div class="rss-meta"><time>${item.date || ''}</time></div><p class="rss-desc">${(item.desc || '').substring(0, 120)}</p></li>`).join('');
      return;
    }

    const res = await fetch(rssUrl);
    const xml = await res.text();
    const doc = new DOMParser().parseFromString(xml, 'text/xml');
    const items = [...doc.querySelectorAll('item')].slice(0, 5).map((item) => ({
      title: item.querySelector('title')?.textContent || '',
      link: item.querySelector('link')?.textContent || '#',
      date: item.querySelector('pubDate')?.textContent || '',
      desc: item.querySelector('description')?.textContent || '',
    }));
    el('rssStatus').textContent = `최신 ${items.length}건 표시`;
    el('rssList').innerHTML = items.map((item) => `<li><a href="${item.link}" target="_blank" rel="noreferrer">${item.title}</a><div class="rss-meta"><time>${item.date}</time></div><p class="rss-desc">${item.desc.replace(/<[^>]*>/g, '').slice(0, 120)}</p></li>`).join('');
  } catch (e) {
    el('rssStatus').textContent = 'RSS를 직접 불러오지 못했습니다. 링크로 확인해 주세요.';
    el('rssList').innerHTML = `<li><a href="${rssUrl}" target="_blank" rel="noreferrer">행안부 보도자료 RSS</a></li>`;
  }
}

async function boot() {
  state.reports = data.reports || [];
  state.education = data.education || [];
  renderFilters();
  renderReports();
  renderEducation();
  el('typeFilter').addEventListener('change', renderReports);
  el('statusFilter').addEventListener('change', renderReports);
  await loadRss();
}

boot();
