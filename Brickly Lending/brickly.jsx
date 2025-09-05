import React, { useMemo, useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Plus, Heading, Image as ImageIcon, Text as TextIcon, GripVertical, Trash2, Copy, ChevronUp, ChevronDown, AlignLeft, AlignCenter, AlignRight, Save, Code, Eye, EyeOff, Download } from "lucide-react";

// --- Small utils
const uid = () => Math.random().toString(36).slice(2, 9);
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

// --- Default blocks
const BLOCK_DEFS = {
  heading: {
    name: "Заголовок",
    icon: Heading,
    create: () => ({ id: uid(), type: "heading", props: { text: "Новый заголовок", level: 2, align: "left" } }),
  },
  paragraph: {
    name: "Текст",
    icon: TextIcon,
    create: () => ({ id: uid(), type: "paragraph", props: { text: "Введите текст…", align: "left" } }),
  },
  image: {
    name: "Изображение",
    icon: ImageIcon,
    create: () => ({ id: uid(), type: "image", props: { url: "https://picsum.photos/800/400", alt: "demo", radius: 16 } }),
  },
  button: {
    name: "Кнопка",
    icon: Plus,
    create: () => ({ id: uid(), type: "button", props: { label: "Нажми меня", href: "#", variant: "primary", align: "left" } }),
  },
  divider: {
    name: "Разделитель",
    icon: GripVertical,
    create: () => ({ id: uid(), type: "divider", props: { thickness: 2, opacity: 0.2 } }),
  },
};

// --- Renderer
function BlockView({ block, selected, onSelect }) {
  const common = "w-full";
  const sel = selected ? "ring-2 ring-indigo-400" : "hover:ring-2 hover:ring-indigo-200";
  const wrap = `${common} ${sel} rounded-2xl p-4 transition shadow-sm bg-white`;
  const { type, props } = block;
  const alignment = props.align ? `text-${props.align}` : "";

  if (type === "heading") {
    const Tag = `h${clamp(props.level || 2, 1, 4)}`;
    return (
      <div className={wrap} onClick={onSelect}>
        {React.createElement(Tag, { className: `${alignment} font-semibold tracking-tight` }, props.text)}
      </div>
    );
  }
  if (type === "paragraph") {
    return (
      <div className={wrap} onClick={onSelect}>
        <p className={`${alignment} leading-relaxed`}>{props.text}</p>
      </div>
    );
  }
  if (type === "image") {
    return (
      <div className={wrap} onClick={onSelect}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={props.url} alt={props.alt || ""} className="w-full" style={{ borderRadius: props.radius || 0 }} />
      </div>
    );
  }
  if (type === "button") {
    const base =
      "inline-flex items-center gap-2 px-5 py-3 rounded-2xl text-sm font-medium shadow-sm";
    const variants = {
      primary: "bg-indigo-600 text-white",
      secondary: "bg-slate-200 text-slate-900",
      ghost: "bg-transparent border border-slate-300 text-slate-700",
    };
    return (
      <div className={wrap + " " + (props.align ? `text-${props.align}` : "")} onClick={onSelect}>
        <a href={props.href || "#"} className={`${base} ${variants[props.variant || "primary"]}`}>
          {props.label}
        </a>
      </div>
    );
  }
  if (type === "divider") {
    return (
      <div className="py-2" onClick={onSelect}>
        <div className={`w-full`} style={{ height: props.thickness || 2, opacity: props.opacity ?? 0.2, background: "#0f172a", borderRadius: 9999 }} />
      </div>
    );
  }
  return null;
}

// --- Inspector (right panel)
function Inspector({ block, onChange }) {
  if (!block) return (
    <div className="text-sm text-slate-500">Выберите блок для редактирования</div>
  );
  const { type, props } = block;

  const Field = ({ label, children }) => (
    <label className="flex flex-col gap-1 text-sm">
      <span className="text-slate-600">{label}</span>
      {children}
    </label>
  );

  const AlignControl = () => (
    <div className="flex items-center gap-2">
      {([
        ["left", AlignLeft],
        ["center", AlignCenter],
        ["right", AlignRight],
      ]).map(([val, Icon]) => (
        <button
          key={val}
          className={`p-2 rounded-xl border ${props.align === val ? "border-indigo-500" : "border-slate-200"}`}
          onClick={() => onChange({ ...props, align: val })}
        >
          <Icon size={18} />
        </button>
      ))}
    </div>
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="text-xs uppercase tracking-wide text-slate-500">Свойства блока</div>
      {type === "heading" && (
        <>
          <Field label="Текст">
            <input className="input" value={props.text} onChange={(e) => onChange({ ...props, text: e.target.value })} />
          </Field>
          <Field label="Размер (h1–h4)">
            <input type="number" min={1} max={4} className="input" value={props.level} onChange={(e) => onChange({ ...props, level: Number(e.target.value) })} />
          </Field>
          <Field label="Выравнивание">
            <AlignControl />
          </Field>
        </>
      )}
      {type === "paragraph" && (
        <>
          <Field label="Текст">
            <textarea className="input min-h-[120px]" value={props.text} onChange={(e) => onChange({ ...props, text: e.target.value })} />
          </Field>
          <Field label="Выравнивание">
            <AlignControl />
          </Field>
        </>
      )}
      {type === "image" && (
        <>
          <Field label="URL изображения">
            <input className="input" value={props.url} onChange={(e) => onChange({ ...props, url: e.target.value })} />
          </Field>
          <Field label="ALT">
            <input className="input" value={props.alt || ""} onChange={(e) => onChange({ ...props, alt: e.target.value })} />
          </Field>
          <Field label="Скругление">
            <input type="range" min={0} max={32} value={props.radius || 0} onChange={(e) => onChange({ ...props, radius: Number(e.target.value) })} />
          </Field>
        </>
      )}
      {type === "button" && (
        <>
          <Field label="Надпись">
            <input className="input" value={props.label} onChange={(e) => onChange({ ...props, label: e.target.value })} />
          </Field>
          <Field label="Ссылка (href)">
            <input className="input" value={props.href} onChange={(e) => onChange({ ...props, href: e.target.value })} />
          </Field>
          <Field label="Стиль">
            <select className="input" value={props.variant} onChange={(e) => onChange({ ...props, variant: e.target.value })}>
              <option value="primary">Primary</option>
              <option value="secondary">Secondary</option>
              <option value="ghost">Ghost</option>
            </select>
          </Field>
          <Field label="Выравнивание">
            <AlignControl />
          </Field>
        </>
      )}
      {type === "divider" && (
        <>
          <Field label="Толщина">
            <input type="range" min={1} max={8} value={props.thickness || 2} onChange={(e) => onChange({ ...props, thickness: Number(e.target.value) })} />
          </Field>
          <Field label="Прозрачность">
            <input type="range" min={0} max={1} step={0.05} value={props.opacity ?? 0.2} onChange={(e) => onChange({ ...props, opacity: Number(e.target.value) })} />
          </Field>
        </>
      )}
    </div>
  );
}

// --- Toolbar button
function TButton({ icon: Icon, children, ...rest }) {
  return (
    <button
      className="flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-200 hover:border-slate-300 bg-white shadow-sm text-sm"
      {...rest}
    >
      {Icon && <Icon size={16} />}
      {children}
    </button>
  );
}

// --- Main Editor
export default function BricklyMVP() {
  const [blocks, setBlocks] = useState([
    BLOCK_DEFS.heading.create(),
    BLOCK_DEFS.paragraph.create(),
    BLOCK_DEFS.image.create(),
  ]);
  const [selectedId, setSelectedId] = useState(null);
  const [preview, setPreview] = useState(false);

  // history for undo/redo
  const [past, setPast] = useState([]);
  const [future, setFuture] = useState([]);
  const commit = (next) => {
    setPast((p) => [...p, blocks]);
    setBlocks(next);
    setFuture([]);
  };
  const undo = () => {
    setPast((p) => {
      if (!p.length) return p;
      const prev = p[p.length - 1];
      setFuture((f) => [blocks, ...f]);
      setBlocks(prev);
      setSelectedId(null);
      return p.slice(0, -1);
    });
  };
  const redo = () => {
    setFuture((f) => {
      if (!f.length) return f;
      const next = f[0];
      setPast((p) => [...p, blocks]);
      setBlocks(next);
      setSelectedId(null);
      return f.slice(1);
    });
  };

  const selected = useMemo(() => blocks.find((b) => b.id === selectedId) || null, [blocks, selectedId]);

  const updateBlockProps = (id, nextProps) => {
    commit(blocks.map((b) => (b.id === id ? { ...b, props: nextProps } : b)));
  };

  const addBlock = (type) => {
    const def = BLOCK_DEFS[type];
    if (!def) return;
    const nb = def.create();
    commit([...blocks, nb]);
    setSelectedId(nb.id);
  };

  const duplicateBlock = (id) => {
    const b = blocks.find((x) => x.id === id);
    if (!b) return;
    const clone = { ...b, id: uid() };
    const idx = blocks.findIndex((x) => x.id === id);
    const next = [...blocks.slice(0, idx + 1), clone, ...blocks.slice(idx + 1)];
    commit(next);
    setSelectedId(clone.id);
  };

  const removeBlock = (id) => {
    commit(blocks.filter((b) => b.id !== id));
    if (selectedId === id) setSelectedId(null);
  };

  const move = (id, dir) => {
    const idx = blocks.findIndex((b) => b.id === id);
    if (idx < 0) return;
    const ni = clamp(idx + dir, 0, blocks.length - 1);
    if (ni === idx) return;
    const next = [...blocks];
    const [item] = next.splice(idx, 1);
    next.splice(ni, 0, item);
    commit(next);
  };

  const exportJSON = () => {
    const data = JSON.stringify({ version: 1, blocks }, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "brickly-page.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const [htmlOpen, setHtmlOpen] = useState(false);
  const htmlString = useMemo(() => renderHTML(blocks), [blocks]);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Top bar */}
      <div className="sticky top-0 z-10 backdrop-blur bg-white/70 border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-2 justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-2xl bg-indigo-600" />
            <div className="font-semibold">
              Brickly <span className="text-slate-400">MVP Editor</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <TButton icon={Save} onClick={exportJSON}>Экспорт JSON</TButton>
            <TButton icon={Code} onClick={() => setHtmlOpen(true)}>Показать HTML</TButton>
            <TButton icon={preview ? EyeOff : Eye} onClick={() => setPreview((v) => !v)}>
              {preview ? "Редактировать" : "Превью"}
            </TButton>
            <TButton onClick={undo}>Undo</TButton>
            <TButton onClick={redo}>Redo</TButton>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-6 grid grid-cols-12 gap-4">
        {/* Palette */}
        <aside className="col-span-3 lg:col-span-2">
          <div className="sticky top-20">
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-2">Блоки</div>
            <div className="grid grid-cols-2 sm:grid-cols-1 gap-2">
              {Object.entries(BLOCK_DEFS).map(([type, def]) => (
                <button key={type} onClick={() => addBlock(type)} className="flex items-center gap-2 p-3 rounded-2xl border border-slate-200 hover:border-slate-300 bg-white shadow-sm text-sm">
                  <def.icon size={16} /> {def.name}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Canvas */}
        <main className="col-span-6 lg:col-span-8">
          <div className="bg-white rounded-2xl shadow p-6">
            {!blocks.length && (
              <div className="text-center text-slate-500">Добавьте блоки из панели слева</div>
            )}
            <div className="flex flex-col gap-3">
              {blocks.map((b) => (
                <motion.div key={b.id} layout initial={{ opacity: 0.2, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                  <div className={`group relative ${selectedId === b.id ? "ring-2 ring-indigo-400 rounded-2xl" : ""}`}>
                    {!preview && (
                      <div className="absolute -left-14 top-2 hidden md:flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition">
                        <button title="Вверх" className="icon-btn" onClick={() => move(b.id, -1)}><ChevronUp size={16} /></button>
                        <button title="Вниз" className="icon-btn" onClick={() => move(b.id, +1)}><ChevronDown size={16} /></button>
                        <button title="Дублировать" className="icon-btn" onClick={() => duplicateBlock(b.id)}><Copy size={16} /></button>
                        <button title="Удалить" className="icon-btn" onClick={() => removeBlock(b.id)}><Trash2 size={16} /></button>
                      </div>
                    )}
                    <BlockView block={b} selected={selectedId === b.id} onSelect={() => !preview && setSelectedId(b.id)} />
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </main>

        {/* Inspector */}
        <aside className="col-span-3 lg:col-span-2">
          <div className="sticky top-20 bg-white rounded-2xl shadow p-4">
            <Inspector
              block={selected}
              onChange={(next) => selected && updateBlockProps(selected.id, next)}
            />
          </div>
        </aside>
      </div>

      {/* HTML Modal */}
      {htmlOpen && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center p-6">
          <div className="bg-white rounded-2xl shadow-xl max-w-3xl w-full p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="font-medium">Экспорт HTML (статический рендер)</div>
              <button className="icon-btn" onClick={() => setHtmlOpen(false)}>✕</button>
            </div>
            <pre className="bg-slate-900 text-slate-100 rounded-xl p-4 max-h-[60vh] overflow-auto text-xs whitespace-pre-wrap">{htmlString}</pre>
            <div className="mt-3 flex justify-end">
              <TButton icon={Download} onClick={() => downloadText(htmlString, "brickly-page.html")}>
                Скачать HTML
              </TButton>
            </div>
          </div>
        </div>
      )}

      {/* Styles */}
      <style>{`
        .input{ @apply px-3 py-2 rounded-xl border border-slate-200 bg-white shadow-sm outline-none focus:ring-2 focus:ring-indigo-300; }
        .icon-btn{ @apply p-2 rounded-xl border border-slate-200 bg-white shadow-sm hover:border-slate-300; }
      `}</style>
    </div>
  );
}

// --- HTML export
function renderHTML(blocks){
  const esc = (s) => String(s).replaceAll('&', '&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  const H = [];
  H.push('<!doctype html>');
  H.push('<html lang="ru"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Brickly Page</title>');
  H.push('<style>body{font-family:ui-sans-serif,system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f8fafc;margin:0;padding:40px;} .wrap{max-width:860px;margin:0 auto;} img{max-width:100%;height:auto;display:block}</style>');
  H.push('</head><body><div class="wrap">');
  for(const b of blocks){
    if(b.type==='heading'){
      const lvl = Math.max(1, Math.min(4, b.props.level||2));
      H.push(`<h${lvl} style="text-align:${b.props.align||'left'}">${esc(b.props.text)}</h${lvl}>`);
    } else if(b.type==='paragraph'){
      H.push(`<p style="text-align:${b.props.align||'left'};line-height:1.75">${esc(b.props.text)}</p>`);
    } else if(b.type==='image'){
      H.push(`<img src="${esc(b.props.url)}" alt="${esc(b.props.alt||'')}" style="border-radius:${b.props.radius||0}px"/>`);
    } else if(b.type==='button'){
      const styles = b.props.variant==='secondary'? 'background:#e2e8f0;color:#0f172a' : b.props.variant==='ghost' ? 'background:transparent;border:1px solid #cbd5e1;color:#334155' : 'background:#4f46e5;color:#fff';
      H.push(`<div style="text-align:${b.props.align||'left'}"><a href="${esc(b.props.href||'#')}" style="${styles};padding:10px 16px;border-radius:16px;text-decoration:none;display:inline-block">${esc(b.props.label||'Кнопка')}</a></div>`);
    } else if(b.type==='divider'){
      H.push(`<div style="height:${b.props.thickness||2}px;background:#0f172a;opacity:${b.props.opacity??0.2};border-radius:9999px;margin:12px 0"></div>`);
    }
  }
  H.push('</div></body></html>');
  return H.join('\n');
}

function downloadText(text, filename){
  const blob = new Blob([text], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}
