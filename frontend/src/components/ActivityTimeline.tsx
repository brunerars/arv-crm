"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/contexts/ToastContext";

interface ActivityTimelineProps {
  leadId: string;
  atividades: any[];
  onReload: () => void;
}

const TIPO_OPTIONS = ["Ligação", "Email", "Reunião", "Visita", "Reunião Interna", "Follow-up", "Outro"];

export default function ActivityTimeline({ leadId, atividades, onReload }: ActivityTimelineProps) {
  const [showForm, setShowForm] = useState(false);
  const [tipo, setTipo] = useState("Ligação");
  const [descricao, setDescricao] = useState("");
  const [dataPrevista, setDataPrevista] = useState("");
  const [loading, setLoading] = useState(false);
  const { addToast } = useToast();

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      await apiClient.createAtividade({
        lead_id: leadId,
        tipo,
        descricao: descricao || null,
        data_prevista: dataPrevista ? new Date(dataPrevista).toISOString() : null,
      });
      setShowForm(false);
      setDescricao("");
      setDataPrevista("");
      onReload();
      addToast("Atividade criada", "success");
    } finally {
      setLoading(false);
    }
  }

  async function handleComplete(id: string) {
    try {
      await apiClient.completeAtividade(id);
      onReload();
      addToast("Atividade concluída", "success");
    } catch (err: any) {
      addToast(err?.response?.data?.detail || err?.message || "Erro ao concluir atividade", "error");
    }
  }

  const inputClass = "w-full px-3 py-2 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)]";

  return (
    <div>
      <div className="flex justify-end mb-4">
        <button onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-1.5 px-3 py-2 text-sm bg-[var(--color-almost-black)] text-white rounded-lg hover:bg-black">
          <span className="material-icons-outlined text-base">add</span>
          Nova Atividade
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
          <form onSubmit={handleCreate} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Tipo</label>
                <select value={tipo} onChange={(e) => setTipo(e.target.value)} className={inputClass}>
                  {TIPO_OPTIONS.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Data Prevista</label>
                <input type="datetime-local" value={dataPrevista} onChange={(e) => setDataPrevista(e.target.value)} className={inputClass} />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Descrição</label>
              <textarea value={descricao} onChange={(e) => setDescricao(e.target.value)} className={`${inputClass} h-16 resize-none`} />
            </div>
            <div className="flex justify-end gap-2">
              <button type="button" onClick={() => setShowForm(false)} className="px-3 py-1.5 text-xs text-[var(--color-dark-grey)] border border-[var(--color-light-grey)] rounded-lg">Cancelar</button>
              <button type="submit" disabled={loading} className="px-3 py-1.5 text-xs text-white bg-[var(--color-almost-black)] rounded-lg disabled:opacity-50">{loading ? "..." : "Criar"}</button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-3">
        {atividades.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center text-[var(--color-grey)] text-sm">Nenhuma atividade registrada</div>
        ) : atividades.map((a) => (
          <div key={a.id} className={`bg-white rounded-lg shadow-sm p-4 flex items-start gap-3 ${a.concluida ? "opacity-60" : ""}`}>
            <span className={`material-icons-outlined text-lg mt-0.5 ${a.concluida ? "text-[var(--color-monday-green)]" : "text-[var(--color-monday-blue)]"}`}>
              {a.concluida ? "check_circle" : "radio_button_unchecked"}
            </span>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold">{a.tipo}</span>
                {a.data_prevista && (
                  <span className="text-xs text-[var(--color-grey)]">
                    {new Date(a.data_prevista).toLocaleDateString("pt-BR")}
                  </span>
                )}
              </div>
              {a.descricao && <p className="text-sm text-[var(--color-dark-grey)]">{a.descricao}</p>}
              <div className="text-xs text-[var(--color-grey)] mt-1">{new Date(a.created_at).toLocaleString("pt-BR")}</div>
            </div>
            {!a.concluida && (
              <button onClick={() => handleComplete(a.id)} className="text-xs text-[var(--color-monday-green)] font-medium hover:underline">
                Concluir
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
