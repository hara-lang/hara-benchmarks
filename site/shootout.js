const shootoutRatio = (base, workloadId) => {
  const index = rowIndex();
  const hara = haraRuntime();
  const reference = measured().get(base);
  const haraValue = steady(index.get(`${hara}|${workloadId}`));
  const referenceValue = steady(index.get(`${reference}|${workloadId}`));
  return haraValue != null && referenceValue != null ? haraValue / referenceValue : null;
};

const shootoutResult = ratio => {
  if (ratio == null) return {status: 'pending', value: '—', label: 'not shared'};
  if (Math.abs(ratio - 1) <= .01) return {status: 'parity', value: '1.00×', label: 'parity'};
  return ratio < 1
    ? {status: 'ahead', value: `${(1 / ratio).toFixed(2)}×`, label: 'Hara ahead'}
    : {status: 'behind', value: `${ratio.toFixed(2)}×`, label: 'Hara behind'};
};

const shootoutBases = () => {
  const order = runtimeCatalog().display_order.filter(base => base !== 'hara');
  const extras = [...measured().keys()].filter(base => base !== 'hara' && !order.includes(base));
  return [...order, ...extras].filter(base => measured().has(base));
};

const shootoutClass = base => {
  const groups = runtimeInfo(base).groups || [];
  return groups
    .map(group => runtimeCatalog().groups[group]?.short || group)
    .filter(Boolean)
    .join(' · ');
};

const shootoutRows = () => shootoutBases().map(base => {
  const overall = compare(base);
  const ratios = workloads().map(workload => shootoutRatio(base, workload.id));
  return {
    base,
    runtime: measured().get(base),
    ...overall,
    ratios,
    haraWins: ratios.filter(ratio => ratio != null && ratio < .985).length,
    competitorWins: ratios.filter(ratio => ratio != null && ratio > 1.015).length,
  };
});

const shootoutMetric = (label, value, note) =>
  `<article><span>${esc(label)}</span><strong>${esc(value)}</strong><p>${esc(note)}</p></article>`;

const shootoutButton = (base, kind, result, workloadId = '') =>
  `<button type="button" class="shootout-cell ${esc(result.status)}" data-shootout-cell data-base="${esc(base)}" data-kind="${esc(kind)}" data-workload="${esc(workloadId)}" aria-pressed="false"><strong>${esc(result.value)}</strong><span>${esc(result.label)}</span></button>`;

function renderShootoutSummary(items) {
  const measuredCount = items.length;
  const haraLeads = items.filter(item => item.ratio != null && item.ratio < .985);
  const sweeps = items.filter(item => item.ratios.filter(ratio => ratio != null).length > 0
    && item.ratios.filter(ratio => ratio != null).every(ratio => ratio < .985));
  const closest = items.reduce((best, item) => {
    if (item.ratio == null) return best;
    if (!best) return item;
    return Math.abs(Math.log(item.ratio)) < Math.abs(Math.log(best.ratio)) ? item : best;
  }, null);
  const widest = haraLeads.reduce((best, item) => !best || item.ratio < best.ratio ? item : best, null);
  $('shootout-summary').innerHTML = `<div class="shootout-metrics">
    ${shootoutMetric('Measured field', `${measuredCount}`, 'prepared language and runtime lanes')}
    ${shootoutMetric('Hara ahead overall', `${haraLeads.length}/${measuredCount}`, 'pairwise geometric means over shared workloads')}
    ${shootoutMetric('Complete sweeps', `${sweeps.length}`, 'Hara ahead on every shared workload')}
    ${shootoutMetric('Widest lead', widest ? shootoutResult(widest.ratio).value : '—', widest ? `against ${name(widest.base)}` : 'no overall lead recorded')}
    ${shootoutMetric('Closest match', closest ? shootoutResult(closest.ratio).value : '—', closest ? `against ${name(closest.base)}` : 'no shared measurements')}
  </div>`;
}

function renderShootoutDetail(button) {
  document.querySelectorAll('[data-shootout-cell]').forEach(cell =>
    cell.setAttribute('aria-pressed', String(cell === button)));
  const base = button.dataset.base;
  const kind = button.dataset.kind;
  const detail = $('shootout-detail');
  const competitor = name(base);
  state.shootoutSelection = {base, kind, workload: button.dataset.workload || ''};
  if (kind === 'overall') {
    const item = compare(base);
    const result = shootoutResult(item.ratio);
    const competitorTime = item.ratio == null ? 'not measured' : `${(1 / item.ratio).toFixed(2)}× Hara time`;
    detail.innerHTML = `<p class="eyebrow">SELECTED COMPARISON</p><h3>Hara / ${esc(competitor)}</h3><p>${esc(item.common.length)} of ${esc(item.total)} workloads are shared. The overall figure is their geometric mean.</p><dl><div><dt>Hara</dt><dd>1.00× baseline</dd></div><div><dt>${esc(competitor)}</dt><dd>${esc(competitorTime)}</dd></div><div><dt>Result</dt><dd class="${esc(result.status)}">${esc(ratioText(item.ratio, base))}</dd></div><div><dt>Included</dt><dd>${esc(item.common.join(', ') || 'none')}</dd></div><div><dt>Excluded</dt><dd>${esc(item.excluded.join(', ') || 'none')}</dd></div></dl>`;
    return;
  }

  const workloadId = button.dataset.workload;
  const workload = workloads().find(item => item.id === workloadId);
  const index = rowIndex();
  const haraValue = steady(index.get(`${haraRuntime()}|${workloadId}`));
  const referenceValue = steady(index.get(`${measured().get(base)}|${workloadId}`));
  const ratio = haraValue != null && referenceValue != null ? haraValue / referenceValue : null;
  const result = shootoutResult(ratio);
  detail.innerHTML = `<p class="eyebrow">SELECTED WORKLOAD</p><h3>Hara / ${esc(competitor)}</h3><p><strong>${esc(workloadId)}</strong> · ${esc(workload?.category || 'algorithm')} · checksum ${esc(workload?.expected || '—')}</p><dl><div><dt>Hara</dt><dd>${haraValue == null ? 'not measured' : formatTime(haraValue)}</dd></div><div><dt>${esc(competitor)}</dt><dd>${referenceValue == null ? 'not measured' : formatTime(referenceValue)}</dd></div><div><dt>Result</dt><dd class="${esc(result.status)}">${esc(ratioText(ratio, base))}</dd></div></dl>`;
}

function wireShootout() {
  const cells = [...document.querySelectorAll('[data-shootout-cell]')];
  cells.forEach(cell => cell.onclick = () => renderShootoutDetail(cell));
  const selected = state.shootoutSelection;
  const initial = cells.find(cell => selected
    && cell.dataset.base === selected.base
    && cell.dataset.kind === selected.kind
    && (cell.dataset.workload || '') === selected.workload)
    || cells.find(cell => cell.dataset.base === 'rust' && cell.dataset.kind === 'overall')
    || cells.find(cell => cell.dataset.kind === 'overall')
    || cells[0];
  if (initial) renderShootoutDetail(initial);
}

function renderShootout() {
  const items = shootoutRows();
  renderShootoutSummary(items);
  const hara = haraRuntime();
  const header = workloads().map(workload => `<th scope="col"><span>${esc(workload.id)}</span></th>`).join('');
  const baseline = workloads().map(workload => {
    const value = steady(rowIndex().get(`${hara}|${workload.id}`));
    return value == null
      ? '<td><span class="shootout-baseline pending"><strong>—</strong><span>n/a</span></span></td>'
      : '<td><span class="shootout-baseline"><strong>1.00×</strong><span>baseline</span></span></td>';
  }).join('');
  const body = items.map(item => {
    const overall = shootoutResult(item.ratio);
    const cells = workloads().map((workload, index) => `<td>${shootoutButton(item.base, 'workload', shootoutResult(item.ratios[index]), workload.id)}</td>`).join('');
    return `<tr><th scope="row"><strong>${esc(name(item.base))}</strong><code>${esc(item.runtime)}</code></th><td><span class="shootout-class">${esc(shootoutClass(item.base) || 'Measured')}</span></td><td>${shootoutButton(item.base, 'overall', overall)}</td><td><span class="shootout-coverage"><strong>${esc(item.common.length)}/${esc(item.total)}</strong><span>${esc(item.haraWins)} Hara · ${esc(item.competitorWins)} peer</span></span></td>${cells}</tr>`;
  }).join('');
  $('shootout-content').innerHTML = items.length ? `<div class="shootout-stage"><div class="shootout-scroll" tabindex="0" aria-label="Scrollable Hara language comparison matrix"><table class="shootout-table"><thead><tr><th scope="col">Runtime</th><th scope="col">Class</th><th scope="col">Overall</th><th scope="col">Shared</th>${header}</tr></thead><tbody><tr class="shootout-hara"><th scope="row"><strong>${esc(name('hara'))}</strong><code>${esc(hara)}</code></th><td><span class="shootout-class">Baseline</span></td><td><span class="shootout-baseline"><strong>1.00×</strong><span>baseline</span></span></td><td><span class="shootout-coverage"><strong>${esc(workloads().filter(workload => steady(rowIndex().get(`${hara}|${workload.id}`)) != null).length)}/${esc(workloads().length)}</strong><span>verified</span></span></td>${baseline}</tr>${body}</tbody></table></div><aside class="shootout-detail" id="shootout-detail" aria-live="polite"></aside></div>` : '<p class="muted">No comparable prepared language measurements are available in this run.</p>';
  wireShootout();
}

const renderAllWithoutShootout = renderAll;
renderAll = function renderAllWithShootout() {
  renderAllWithoutShootout();
  renderShootout();
};

if (state.catalog && state.run) renderShootout();
