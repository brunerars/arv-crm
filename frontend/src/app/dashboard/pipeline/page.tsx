"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";
import KanbanBoard from "@/components/KanbanBoard";
import FilterBar from "@/components/FilterBar";
import CreateLeadModal from "@/components/CreateLeadModal";

const TEMP_OPTIONS = [
  { value: "frio", label: "Frio" },
  { value: "morno", label: "Morno" },
  { value: "quente", label: "Quente" },
];

export default function PipelinePage() {
  const [kanban, setKanban] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tempFilter, setTempFilter] = useState("");
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const router = useRouter();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (tempFilter) params.temperatura = tempFilter;
      if (search) params.search = search;
      const data = await apiClient.getKanban(params);
      setKanban(data);
    } finally {
      setLoading(false);
    }
  }, [tempFilter, search]);

  useEffect(() => { load(); }, [load]);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-xl font-bold">Pipeline Pré-Vendas</h1>
          {kanban && (
            <div className="flex gap-6 mt-1 text-sm text-[var(--color-dark-grey)]">
              <span>Total leads: <strong className="text-[var(--color-almost-black)]">{kanban.total_leads}</strong></span>
              <span>Valor total: <strong className="text-[var(--color-almost-black)]">R$ {(kanban.total_valor / 1000).toFixed(0)}K</strong></span>
            </div>
          )}
        </div>
        <button onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-[var(--color-almost-black)] text-white rounded-lg text-sm font-semibold hover:bg-black">
          <span className="material-icons-outlined text-lg">add</span>
          Novo Lead
        </button>
      </div>

      <FilterBar
        filters={[
          { key: "temperatura", label: "Temperatura", options: TEMP_OPTIONS, value: tempFilter, onChange: setTempFilter },
        ]}
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Buscar leads..."
      />

      {loading ? (
        <div className="text-center py-10 text-[var(--color-grey)]">Carregando...</div>
      ) : kanban ? (
        <KanbanBoard columns={kanban.columns} onCardClick={(lead) => router.push(`/dashboard/pipeline/${lead.id}`)} />
      ) : null}

      {showCreate && <CreateLeadModal onClose={() => setShowCreate(false)} onCreated={load} />}
    </div>
  );
}
