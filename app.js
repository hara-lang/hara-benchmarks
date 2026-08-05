const $ = id => document.getElementById(id);
const state = {runs: [], catalog: null, run: null, lifecycleComparator: 'luajit', codeComparator: 'luajit'};

const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const median = values => {if (!values?.length) return null; const sorted=[...values].sort((a,b)=>a-b), middle=Math.floor(sorted.length/2); return sorted.length%2?sorted[middle]:(sorted[middle-1]+sorted[middle])/2;};
const geometricMean = values => values.length ? Math.exp(values.reduce((sum,value)=>sum+Math.log(value),0)/values.length) : null;
const runtimeBase = id => id?.startsWith('hara-') ? 'hara' : id?.split('-')[0];
const runtimeCatalog = () => state.catalog.runtime_catalog || {groups:{},runtimes:{},display_order:[]};
const runtimeInfo = base => runtimeCatalog().runtimes[base] || {name:base,groups:['interpreter'],status:'measured'};
const name = base => runtimeInfo(base).name || base;
const platform = run => [run.environment?.os || run.environment?.platform || 'unknown', run.environment?.architecture || run.environment?.machine || ''].filter(Boolean).join(' / ');
const rows = () => state.run?.measurements?.filter(row => (row.mode || 'prepared') === 'prepared') || [];
const workloads = () => state.catalog?.workloads || [];
const steady = row => row?.status === 'ok' ? median(row.steady_state?.samples_ns) : null;
const option = (value,label=value) => `<option value="${esc(value)}">${esc(label)}</option>`;
const haraRuntime = () => rows().find(row => row.runtime.includes('whole-wasm'))?.runtime || rows().find(row => row.runtime.startsWith('hara-'))?.runtime;
const measured = () => {
  const byBase = new Map();
  for (const row of rows()) if (!byBase.has(runtimeBase(row.runtime))) byBase.set(runtimeBase(row.runtime), row.runtime);
  return byBase;
};
const references = () => runtimeCatalog().display_order.map(base => ({base,runtime:measured().get(base)})).filter(item => item.runtime);
const rowIndex = () => new Map(rows().map(row => [`${row.runtime}|${row.workload}`,row]));

function formatTime(n) {
  if (n == null) return 'not recorded';
  const unit = $('units')?.value || 'auto';
  if (unit === 'ms') return `${(n/1e6).toFixed(3)} ms`;
  if (unit === 'us') return `${(n/1e3).toFixed(2)} µs`;
  if (unit === 'ns') return `${Math.round(n)} ns`;
  return n >= 1e9 ? `${(n/1e9).toFixed(2)} s` : n >= 1e6 ? `${(n/1e6).toFixed(3)} ms` : n >= 1e3 ? `${(n/1e3).toFixed(2)} µs` : `${Math.round(n)} ns`;
}
function formatBytes(n) {
  if (n == null) return 'not recorded';
  if (n >= 1073741824) return `${(n/1073741824).toFixed(2)} GiB`;
  if (n >= 1048576) return `${(n/1048576).toFixed(2)} MiB`;
  if (n >= 1024) return `${(n/1024).toFixed(1)} KiB`;
  return `${Math.round(n)} B`;
}
function ratioText(ratio, reference, short=false) {
  if (ratio == null) return 'No common measurements';
  if (Math.abs(ratio-1) <= .01) return short ? 'approximately equal' : `Hara and ${name(reference)} are approximately equal`;
  if (ratio < 1) return `Hara is ${(1/ratio).toFixed(2)}× faster${short?'':` than ${name(reference)}`}`;
  return `Hara is ${ratio.toFixed(2)}× slower${short?'':` than ${name(reference)}`}`;
}
function compare(reference, selectedWorkloads=workloads()) {
  const index=rowIndex(), hara=haraRuntime(), ref=measured().get(reference), common=[], ratios=[];
  for (const workload of selectedWorkloads) {
    const haraValue=steady(index.get(`${hara}|${workload.id}`));
    const refValue=steady(index.get(`${ref}|${workload.id}`));
    if (haraValue != null && refValue != null) {common.push(workload.id); ratios.push(haraValue/refValue);}
  }
  return {reference, ratio:geometricMean(ratios), common, total:selectedWorkloads.length, excluded:selectedWorkloads.map(w=>w.id).filter(id=>!common.includes(id))};
}
function comparisonCard(item) {
  return `<article class="comparison-card"><header><strong>HARA / ${esc(name(item.reference).toUpperCase())}</strong><span>${item.common.length}/${item.total} shared</span></header><p class="statement">${esc(ratioText(item.ratio,item.reference)).replace('Hara','<b>Hara</b>')}</p><div class="coverage">Included: ${esc(item.common.join(', ')||'none')}<br><span class="excluded">Excluded: ${esc(item.excluded.join(', ')||'none')}</span></div></article>`;
}
function plannedCard(base) {
  const info=runtimeInfo(base), status=info.status === 'planned' ? 'PLANNED LANE' : 'AWAITING NEXT RUN';
  return `<article class="planned-card"><span>${status}</span><strong>${esc(info.name)}</strong><p>${esc((info.groups||[]).map(group=>runtimeCatalog().groups[group]?.short).filter(Boolean).join(' · '))}</p></article>`;
}
function groupSection(groupId, bases) {
  const group=runtimeCatalog().groups[groupId] || {title:groupId,description:''};
  const measuredBases=bases.filter(base=>measured().has(base));
  const missingBases=bases.filter(base=>!measured().has(base));
  return `<section class="class-section runtime-group ${esc(groupId)}"><div class="class-heading"><h3>${esc(group.title)}</h3><p>${esc(group.description)}</p></div><div class="comparison-grid">${measuredBases.map(base=>comparisonCard(compare(base))).join('')}</div>${missingBases.length?`<div class="planned-grid">${missingBases.map(plannedCard).join('')}</div>`:''}</section>`;
}
function groupBases(groupId) {
  return runtimeCatalog().display_order.filter(base => runtimeInfo(base).groups?.includes(groupId));
}

function initSelectors() {
  const params=new URLSearchParams(location.search);
  state.runs=[...new Map(state.runs.map(run=>[run.run.id,run])).values()].sort((a,b)=>String(b.environment?.timestamp).localeCompare(String(a.environment?.timestamp)));
  if (!state.runs.length) throw new Error('No valid benchmark runs are published');
  $('run').innerHTML=state.runs.map(run=>option(run.run.id,`${run.run.profile} · ${new Date(run.environment?.timestamp||0).toLocaleDateString()}${run.provenance?.hara_dirty?' · dirty':''}`)).join('');
  $('run').value=state.runs.some(run=>run.run.id===params.get('run'))?params.get('run'):state.runs[0].run.id;
  state.run=state.runs.find(run=>run.run.id===$('run').value);
  $('platform').innerHTML=option(platform(state.run));
  const workloadOptions=workloads().map(workload=>option(workload.id,`${workload.id} · ${workload.category}`)).join('');
  for (const id of ['workload-select','lifecycle-workload','code-workload']) $(id).innerHTML=workloadOptions;
  const requested=params.get('workload');
  if (requested && workloads().some(w=>w.id===requested)) for (const id of ['workload-select','lifecycle-workload','code-workload']) $(id).value=requested;
  const refOptions=references().map(ref=>option(ref.base,name(ref.base))).join('');
  $('lifecycle-comparator').innerHTML=refOptions;
  $('code-comparator').innerHTML=refOptions;
  const preferred=base => references().some(ref=>ref.base===base) ? base : references()[0]?.base;
  state.lifecycleComparator=preferred(params.get('lifecycleComparator')||'luajit');
  state.codeComparator=preferred(params.get('codeComparator')||'luajit');
  $('lifecycle-comparator').value=state.lifecycleComparator;
  $('code-comparator').value=state.codeComparator;
  $('units').value=params.get('units')||'auto';
  $('phase').value=params.get('phase')||'steady';
}
function remember() {
  const params=new URLSearchParams(location.search), active=document.querySelector('.tabs [aria-selected=true]');
  params.set('view',active?.dataset.view||'overview'); params.set('run',$('run').value); params.set('units',$('units').value); params.set('workload',$('workload-select').value); params.set('lifecycleComparator',state.lifecycleComparator); params.set('codeComparator',state.codeComparator); params.set('phase',$('phase').value);
  history.replaceState(null,'',`${location.pathname}?${params}`);
}
function renderSummary() {
  const hara=haraRuntime(), haraRows=rows().filter(row=>row.runtime===hara), ok=haraRows.filter(row=>row.status==='ok').length;
  $('run-summary').textContent=`${name('hara')} · ${ok}/${haraRows.length} workloads · ${state.run.run.profile} · ${platform(state.run)}${state.run.environment?.container_image?` · ${state.run.environment.container_image}`:''}`;
}
function renderOverview() {
  const hara=haraRuntime(), values=rows().filter(row=>row.runtime===hara).map(steady).filter(value=>value!=null);
  $('hara-profile').innerHTML=`<article class="hara-profile"><div><span>PRIMARY CLASS</span><strong>Dynamic language + adaptive execution</strong></div><div><span>HARA RUNTIME</span><strong>${esc(hara||'not measured')}</strong></div><div><span>STEADY RANGE</span><strong>${values.length?`${formatTime(Math.min(...values))} – ${formatTime(Math.max(...values))}`:'not recorded'}</strong></div><div><span>MODE</span><strong>Prepared</strong></div></article>`;
  $('overview-cards').innerHTML=groupSection('dynamic-jit',groupBases('dynamic-jit').filter(base=>base!=='hara'));
  $('lisp-cards').innerHTML=groupSection('lisp',groupBases('lisp').filter(base=>base!=='hara'));
  $('reference-cards').innerHTML=groupSection('reference-native',groupBases('reference-native'))+groupSection('reference-managed',groupBases('reference-managed'))+groupSection('interpreter',groupBases('interpreter'));
}
function aggregate(runtime, field) {
  const values=rows().filter(row=>row.runtime===runtime && row.status==='ok').map(row=>row[field]).filter(value=>value!=null);
  return median(values);
}
function renderFootprint() {
  const order=['hara',...runtimeCatalog().display_order.filter(base=>measured().has(base))], fields=[['peak_rss_bytes','Peak RSS'],['runtime_executable_bytes','Executable'],['runtime_bundle_bytes','Bundle'],['artifact_bytes','Artifact'],['source_bytes','Source']];
  $('footprint-content').innerHTML=`<div class="footprint-grid"><div class="footprint-row header"><span>Runtime</span>${fields.map(([,label])=>`<span>${label}</span>`).join('')}</div>${order.filter((base,index,array)=>array.indexOf(base)===index).map(base=>{const runtime=base==='hara'?haraRuntime():measured().get(base);return `<article class="footprint-row ${base==='hara'?'hara':''}"><strong>${esc(name(base))}</strong>${fields.map(([field,label])=>{const value=aggregate(runtime,field);return `<span class="${value==null?'missing':''}" data-label="${esc(label)}">${formatBytes(value)}</span>`}).join('')}</article>`}).join('')}</div><p class="footprint-note">Rows show the median recorded value across successful workloads. Missing values remain missing; source, generated artifact and runtime distribution are not interchangeable.</p>`;
}
function renderWorkload() {
  const workload=workloads().find(item=>item.id===$('workload-select').value), index=rowIndex(), hara=haraRuntime(), haraRow=index.get(`${hara}|${workload.id}`), haraValue=steady(haraRow);
  $('workload-content').innerHTML=`<div class="workload-layout"><article class="hara-result"><p class="eyebrow">HARA // ${esc(workload.category.toUpperCase())}</p><strong>${esc(workload.id)}</strong><span class="value">${haraValue==null?'unsupported':formatTime(haraValue)}</span><p class="meta">${haraValue==null?esc(haraRow?.reason||'not measured'):`${workload.operations?.toLocaleString()||'—'} operations · checksum ${esc(workload.expected)}`}</p></article><div class="reference-list">${references().map(ref=>{const value=steady(index.get(`${ref.runtime}|${workload.id}`));const statement=haraValue==null?'Hara unsupported':value==null?`${name(ref.base)} unsupported`:ratioText(haraValue/value,ref.base);return `<article class="reference-row ${esc(runtimeInfo(ref.base).groups?.[0]||'')}" ><strong>${esc(name(ref.base))}</strong><span>${value==null?'unsupported':formatTime(value)}</span><span class="delta">${esc(statement).replace('Hara','<b>Hara</b>')}</span></article>`}).join('')}</div></div>`;
}
function phaseValue(row, phase) {if (row?.status!=='ok') return null; if (phase==='steady') return steady(row); if (phase==='warmup') return median(row.warmup_samples_ns); return row[phase]??null;}
function renderLifecycle() {
  const workload=$('lifecycle-workload').value, phase=$('phase').value, index=rowIndex(), hara=haraRuntime(), reference=references().find(ref=>ref.base===state.lifecycleComparator), pair=[{runtime:hara,base:'hara'},{runtime:reference?.runtime,base:reference?.base}];
  const bytePhase=phase.endsWith('_bytes'), values=pair.map(item=>phaseValue(index.get(`${item.runtime}|${workload}`),phase)), max=Math.max(...values.filter(value=>value!=null),1);
  $('lifecycle-content').innerHTML=`<div class="lifecycle-pair">${pair.map((item,indexPair)=>{const value=values[indexPair];return `<article class="lifecycle-row ${item.base==='hara'?'hara':''}"><div><strong>${esc(name(item.base))}</strong><div class="meta">${esc(phase.replaceAll('_',' '))}</div></div><div class="bar"><i style="width:${value==null?0:Math.max(2,value/max*100)}%"></i></div><div>${value==null?'not recorded':bytePhase?formatBytes(value):formatTime(value)}</div></article>`}).join('')}</div>`;
}
function codeSide(workload, base, isHara) {
  const implementation=workload.implementations[base];
  if (!implementation) return `<article class="code-side"><strong>${esc(name(base))}</strong><p>Source adapter not available for this workload.</p></article>`;
  return `<article class="code-side ${isHara?'hara':''}"><header><strong>${esc(name(base))}</strong><button class="copy" data-copy="${base}-source">COPY SOURCE</button></header><pre id="${base}-source"></pre><div class="code-meta"><strong>Preparation</strong><br>${esc(implementation.prepare.description)}<br><code>${esc(implementation.prepare.command)}</code><br>Expected checksum: ${esc(workload.expected)}</div><details><summary>FULL RUNNER HARNESS</summary><pre id="${base}-harness"></pre></details></article>`;
}
function renderCode() {
  const workload=workloads().find(item=>item.id===$('code-workload').value), ref=state.codeComparator, ids=['hara',ref];
  $('code-content').innerHTML=`<div class="code-pair">${codeSide(workload,'hara',true)}${codeSide(workload,ref,false)}</div>`;
  for (const id of ids) {const implementation=workload.implementations[id]; if (!implementation) continue; $(`${id}-source`).textContent=implementation.source; $(`${id}-harness`).textContent=implementation.harness;}
  document.querySelectorAll('[data-copy]').forEach(button=>button.onclick=async()=>{await navigator.clipboard.writeText($(button.dataset.copy).textContent);button.textContent='COPIED';});
}
function renderRuns() {
  const run=state.run, env=run.environment||{}, provenance=run.provenance||{}, versions=run.versions||{}, facts=[['Run ID',run.run.id],['Profile',run.run.profile],['Platform',platform(run)],['Container',env.container_image],['Timestamp',env.timestamp],['Hara revision',provenance.hara_revision||env.git_revision],['Benchmark revision',provenance.benchmark_revision],['GitHub run',env.github_run_id||provenance.github_run_id]];
  $('runs-content').innerHTML=`<div class="cards">${facts.map(([key,value])=>`<div class="card"><span>${esc(key.toUpperCase())}</span><strong>${esc(value??'not recorded')}</strong></div>`).join('')}</div><h3 class="version-heading">Runtime versions</h3><div class="version-grid">${Object.entries(versions).map(([key,value])=>`<div class="card"><span>${esc(name(key).toUpperCase())}</span><code>${esc(value)}</code></div>`).join('')}</div>`;
}
function renderAll() {state.run=state.runs.find(run=>run.run.id===$('run').value)||state.runs[0]; renderSummary(); renderOverview(); renderFootprint(); renderWorkload(); renderLifecycle(); renderCode(); renderRuns(); remember();}
function activate(view) {document.querySelectorAll('.view').forEach(panel=>panel.classList.toggle('active',panel.id===view)); document.querySelectorAll('.tabs [role=tab]').forEach(button=>button.setAttribute('aria-selected',String(button.dataset.view===view))); remember();}
function wire() {
  document.querySelectorAll('.tabs [role=tab]').forEach(button=>button.onclick=()=>activate(button.dataset.view));
  $('run').onchange=()=>{state.run=state.runs.find(run=>run.run.id===$('run').value);$('platform').innerHTML=option(platform(state.run));renderAll();};
  $('units').onchange=renderAll; $('workload-select').onchange=()=>{renderWorkload();remember();}; $('lifecycle-workload').onchange=()=>{renderLifecycle();remember();}; $('phase').onchange=()=>{renderLifecycle();remember();}; $('lifecycle-comparator').onchange=()=>{state.lifecycleComparator=$('lifecycle-comparator').value;renderLifecycle();remember();}; $('code-comparator').onchange=()=>{state.codeComparator=$('code-comparator').value;renderCode();remember();}; $('code-workload').onchange=()=>{renderCode();remember();};
}

Promise.all([fetch('data/runs.json').then(response=>response.json()),fetch('data/catalog.json').then(response=>response.json())]).then(([runData,catalog])=>{state.runs=runData.runs;state.catalog=catalog;initSelectors();wire();renderAll();const requested=new URLSearchParams(location.search).get('view');if(requested&&$(requested))activate(requested);}).catch(error=>{$('run-summary').textContent=`Benchmark data unavailable: ${error.message}`;console.error(error);});
