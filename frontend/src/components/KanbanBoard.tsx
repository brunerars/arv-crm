"use client";

import KanbanCard from "./KanbanCard";

const ETAPA_LABELS: Record<string, string> = {
  prospeccao: "Prospecção",
  primeiro_contato: "Primeiro Contato",
  qualificacao: "Qualificação",
  qualificado: "Qualificado",
  descartado: "Descartado",
};

const ETAPA_COLORS: Record<string, string> = {
  prospeccao: "var(--color-monday-blue)",
  primeiro_contato: "var(--color-monday-purple)",
  qualificacao: "var(--color-monday-yellow)",
  qualificado: "var(--color-monday-green)",
  descartado: "var(--color-monday-red)",
};

interface KanbanBoardProps {
  columns: any[];
  onCardClick: (lead: any) => void;
}

export default function KanbanBoard({ columns, onCardClick }: KanbanBoardProps) {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4" style={{ minHeight: "calc(100vh - 280px)" }}>
      {columns.map((col) => (
        <div key={col.etapa} className="min-w-[296px] max-w-[296px] flex flex-col bg-[#f0f0f0] rounded-xl overflow-hidden">
          {/* Column header */}
          <div className="px-4 pt-4 pb-3 relative">
            <div className="absolute top-0 left-0 right-0 h-[3px] rounded-t-xl" style={{ background: ETAPA_COLORS[col.etapa] }} />
            <div className="flex items-center gap-2 text-[13.5px] font-bold text-[var(--color-almost-black)]">
              {ETAPA_LABELS[col.etapa] || col.etapa}
              <span className="bg-black/[0.08] text-[var(--color-dark-grey)] text-[11px] font-semibold px-2 py-0.5 rounded-full">{col.count}</span>
            </div>
            <div className="text-xs text-[var(--color-grey)] mt-1 font-medium">
              R$ {(col.total_valor / 1000).toFixed(0)}K
            </div>
          </div>

          {/* Cards */}
          <div className="flex-1 overflow-y-auto px-2.5 pb-2.5 flex flex-col gap-2.5">
            {col.leads.map((lead: any) => (
              <KanbanCard key={lead.id} lead={lead} onClick={() => onCardClick(lead)} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
