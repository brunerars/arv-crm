"use client";

const TEMP_STYLES: Record<string, { border: string; badge: string; label: string }> = {
  frio: { border: "border-l-[var(--color-monday-blue)]", badge: "bg-[#e3f0ff] text-[#0062cc]", label: "Frio" },
  morno: { border: "border-l-[var(--color-monday-yellow)]", badge: "bg-[#fff5d6] text-[#a67c00]", label: "Morno" },
  quente: { border: "border-l-[var(--color-monday-red)]", badge: "bg-[#ffe8eb] text-[#c82a2a]", label: "Quente" },
};

const SCORE_COLORS: Record<string, string> = {
  A: "bg-[#e3fbef] text-[#007a3d]",
  B: "bg-[#fff5d6] text-[#a67c00]",
  C: "bg-[#ffe8eb] text-[#c82a2a]",
  D: "bg-[#ffe8eb] text-[#c82a2a]",
};

interface KanbanCardProps {
  lead: any;
  onClick: () => void;
}

export default function KanbanCard({ lead, onClick }: KanbanCardProps) {
  const temp = TEMP_STYLES[lead.temperatura] || TEMP_STYLES.frio;
  const isDiscarded = lead.etapa === "descartado";
  const daysInStage = Math.max(0, Math.floor((Date.now() - new Date(lead.data_entrada).getTime()) / 86400000));

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-lg p-3.5 cursor-pointer transition-all hover:-translate-y-0.5 hover:shadow-md shadow-sm border-l-[3px] ${temp.border} ${isDiscarded ? "opacity-55" : ""}`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full ${temp.badge}`}>
          {temp.label}
        </span>
        <span className={`text-[11px] font-medium flex items-center gap-1 ${daysInStage > 7 ? "text-[var(--color-monday-orange)]" : "text-[var(--color-grey)]"}`}>
          {daysInStage}d
          {daysInStage > 7 && <span className="material-icons-outlined text-sm">warning</span>}
        </span>
      </div>

      <div className={`text-[13.5px] font-bold mb-0.5 leading-tight ${isDiscarded ? "line-through text-[var(--color-grey)]" : ""}`}>
        {lead.lead_id}
      </div>
      <div className="text-xs text-[var(--color-grey)] mb-2">{lead.produto_interesse || "—"}</div>
      <div className="text-[15px] font-bold mb-2.5">
        R$ {Number(lead.valor_estimado).toLocaleString("pt-BR")}
      </div>

      <div className="h-px bg-[#eee] mb-2.5" />

      <div className="flex items-center justify-between">
        <div className="text-xs text-[var(--color-dark-grey)] font-medium">{lead.responsavel_nome || lead.etapa || "—"}</div>
        {lead.lead_score > 0 && (
          <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${SCORE_COLORS[lead.classificacao] || "bg-gray-100 text-gray-600"}`}>
            LS: {lead.lead_score}
          </span>
        )}
      </div>
    </div>
  );
}
