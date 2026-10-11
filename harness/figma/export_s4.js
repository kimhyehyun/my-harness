// S4 → S5 다리: Figma 화면의 노드 값을 뽑아 runs/{flow}/s4/export.json을 만든다.
// 사용: ui-designer가 PAGE_ID·FRAME_IDS를 바꿔 use_figma로 실행하고, return 값을 그대로 저장한다.
// 판정 스크립트(gate_s5.py)는 이 JSON만 읽고 Figma에는 접근하지 않는다.
// 컴포넌트 인스턴스 내부는 디자인 시스템 원본이므로 텍스트와 이미지 노드만 기록한다.
// use_figma 반환 한도(20KB) 때문에 화면 1개씩 실행하고, 결과의 screens[]를 합쳐 저장한다.
const FILE_KEY = 'EDcJ9a4nsLkEYJDmZPGi80';
const PAGE_ID = '35:2';
const FRAME_IDS = ['37:22']; // 한 번에 1개 (예: '37:22', '37:23', '37:24', '37:25')

const page = await figma.getNodeByIdAsync(PAGE_ID);
await figma.setCurrentPageAsync(page);
const vcache = {}, scache = {};
async function vname(id) {
  if (!id) return null;
  if (!(id in vcache)) { const x = await figma.variables.getVariableByIdAsync(id); vcache[id] = x ? x.name : null; }
  return vcache[id];
}
async function sname(id) {
  if (!id || typeof id !== 'string') return null;
  if (!(id in scache)) { const s = await figma.getStyleByIdAsync(id); scache[id] = s ? s.name : null; }
  return scache[id];
}
async function paintList(arr) {
  if (!Array.isArray(arr)) return [];
  const out = [];
  for (const p of arr) {
    out.push({ type: p.type, visible: p.visible !== false,
      var: p.boundVariables && p.boundVariables.color ? await vname(p.boundVariables.color.id) : null,
      imageHash: p.imageHash || null });
  }
  return out;
}
const hasImage = n => 'fills' in n && Array.isArray(n.fills) && n.fills.some(f => f.type === 'IMAGE');
async function rec(n, inside) {
  const o = { id: n.id, name: n.name, type: n.type, in_instance: inside, visible: n.visible, height: Math.round(n.height * 10) / 10 };
  if ((!inside && n.type !== 'INSTANCE') || hasImage(n)) {
    if ('fills' in n) o.fills = await paintList(n.fills);
    if ('strokes' in n) o.strokes = await paintList(n.strokes);
  }
  if (!inside) {
    if ('cornerRadius' in n && n.type !== 'TEXT') {
      const r = n.cornerRadius === figma.mixed ? [n.topLeftRadius, n.topRightRadius, n.bottomLeftRadius, n.bottomRightRadius] : [n.cornerRadius];
      if (r.some(x => x)) o.radius = r;
    }
    if (n.type === 'FRAME' && 'layoutMode' in n && n.layoutMode !== 'NONE') {
      o.padding = [n.paddingTop, n.paddingRight, n.paddingBottom, n.paddingLeft];
      o.gap = n.itemSpacing;
    }
    if (n.type !== 'INSTANCE' && 'effects' in n) o.effects = n.effects.map(e => ({ type: e.type, visible: e.visible }));
  }
  if (n.type === 'TEXT') { o.characters = n.characters; o.textStyle = await sname(n.textStyleId); }
  if (n.type === 'INSTANCE') {
    const mc = await n.getMainComponentAsync();
    if (mc) { if (mc.parent && mc.parent.type === 'COMPONENT_SET') { o.component = mc.parent.name; o.variant = mc.name; } else o.component = mc.name; }
  }
  return compact(o);
}
function compact(o) {
  for (const k of Object.keys(o)) {
    const v = o[k];
    if (v === null || v === undefined || (Array.isArray(v) && !v.length)) delete o[k];
    else if (Array.isArray(v)) o[k] = v.map(x => (x && typeof x === 'object' ? compact(x) : x));
  }
  if (o.visible === true) delete o.visible;
  if (o.in_instance === false) delete o.in_instance;
  return o;
}
const screens = [];
for (const id of FRAME_IDS) {
  const f = await figma.getNodeByIdAsync(id);
  const nodes = [await rec(f, false)];
  async function walk(n, inside) {
    for (const c of n.children || []) {
      const childInside = inside;
      if (!childInside || c.type === 'TEXT' || hasImage(c)) nodes.push(await rec(c, childInside));
      if ('children' in c) await walk(c, inside || c.type === 'INSTANCE');
    }
  }
  await walk(f, false);
  screens.push({ id: f.id, name: f.name, width: f.width, height: f.height, nodes });
}
return { exported_from: { fileKey: FILE_KEY, page: PAGE_ID }, screens };
