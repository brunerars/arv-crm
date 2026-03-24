"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import { apiClient } from "@/lib/api";
import { useToast } from "@/contexts/ToastContext";
import ActivityTimeline from "@/components/ActivityTimeline";
import CompletudeBadge from "@/components/CompletudeBadge";
import StageProgress from "@/components/StageProgress";

const ETAPA_LABELS: Record<string, string> = {
  prospeccao: "Prospecção", primeiro_contato: "Primeiro Contato",
  qualificacao: "Qualificação", qualificado: "Qualificado", descartado: "Descartado",
};

export default function DealDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [lead, setLead] = useState<any>(null);
  const [atividades, setAtividades] = useState<any[]>([]);
  const [historico, setHistorico] = useState<any[]>([]);
  const [tab, setTab] = useState("resumo");
  const [error, setError] = useState("");
  const { addToast } = useToast();

  const load = useCallback(async () => {
    try {
      const [l, a, h] = await Promise.all([
        apiClient.getLead(id),
        apiClient.getAtividades({ lead_id: id }),
        apiClient.getHistorico(id),
      ]);
      setLead(l);
      setAtividades(a.items);
      setHistorico(h);
    } catch (err: any) {
      setError(err.message || "Erro ao carregar lead");
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  if (error) return <div className="text-center py-10 text-[var(--color-arv-red)]">{error}</div>;
  if (!lead) return <div className="text-center py-10 text-[var(--color-grey)]">Carregando...</div>;

  async function handleChangeStage(nova_etapa: string) {
    let motivo_descarte;
    if (nova_etapa === "descartado") {
      motivo_descarte = prompt("Motivo do descarte:");
      if (!motivo_descarte) return;
    }
    try {
      const updated = await apiClient.changeStage(id, nova_etapa, motivo_descarte);
      setLead({ ...lead, ...updated });
      load();
      addToast("Etapa atualizada", "success");
    } catch (err: any) {
      addToast(err.message, "error");
    }
  }

  async function handleCalculateScore() {
    try {
      const updated = await apiClient.calculateScore(id);
      setLead({ ...lead, ...updated });
      addToast("Score calculado", "success");
    } catch (err: any) {
      addToast(err.message, "error");
    }
  }

  const tabs = [
    { key: "resumo", label: "Resumo", icon: "summarize" },
    { key: "empresa", label: "Empresa", icon: "business" },
    { key: "atividades", label: "Atividades", icon: "task_alt" },
    { key: "scores", label: "Scores", icon: "stars" },
    { key: "historico", label: "Histórico", icon: "history" },
  ];

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-sm font-semibold text-[var(--color-monday-blue)]">{lead.lead_id}</span>
          <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full ${lead.temperatura === "quente" ? "bg-[#ffe8eb] text-[#c82a2a]" : lead.temperatura === "morno" ? "bg-[#fff5d6] text-[#a67c00]" : "bg-[#e3f0ff] text-[#0062cc]"}`}>
            {lead.temperatura === "quente" ? "Quente" : lead.temperatura === "morno" ? "Morno" : "Frio"}
          </span>
        </div>
        <h1 className="text-xl font-bold mb-1">{lead.empresa?.nome_fantasia || "—"}</h1>
        <p className="text-sm text-[var(--color-grey)]">{lead.produto_interesse || "—"} &middot; R$ {Number(lead.valor_estimado).toLocaleString("pt-BR")}</p>
      </div>

      {/* Stage progress */}
      <StageProgress currentStage={lead.etapa} onChangeStage={handleChangeStage} />

      {/* Completude + Score sidebar-like info */}
      <div className="grid grid-cols-4 gap-4 my-6">
        <CompletudeBadge completude={lead.completude} />
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-xs font-medium text-[var(--color-grey)] mb-1">Lead Score</div>
          <div className="text-2xl font-bold">{lead.lead_score}</div>
          <div className="text-xs text-[var(--color-grey)]">Classificação: {lead.classificacao || "—"}</div>
          <button onClick={handleCalculateScore} className="mt-2 text-xs text-[var(--color-monday-blue)] font-medium hover:underline">Recalcular</button>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-xs font-medium text-[var(--color-grey)] mb-1">Etapa Atual</div>
          <div className="text-lg font-bold">{ETAPA_LABELS[lead.etapa]}</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="text-xs font-medium text-[var(--color-grey)] mb-1">Dias no Pipeline</div>
          <div className="text-2xl font-bold">{Math.floor((Date.now() - new Date(lead.data_entrada).getTime()) / 86400000)}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 border-b border-[var(--color-light-grey)]/50">
        {tabs.map((t) => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${tab === t.key ? "border-[var(--color-arv-red)] text-[var(--color-almost-black)]" : "border-transparent text-[var(--color-grey)] hover:text-[var(--color-dark-grey)]"}`}>
            <span className="material-icons-outlined text-base">{t.icon}</span>
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {tab === "resumo" && (
        <div className="bg-white rounded-lg shadow-sm p-6 grid grid-cols-2 gap-x-8 gap-y-4">
          {[
            ["Lead ID", lead.lead_id],
            ["Temperatura", lead.temperatura],
            ["Produto", lead.produto_interesse],
            ["Área de Atuação", lead.area_atuacao],
            ["Tipo Entrega", lead.tipo_entrega],
            ["Valor Estimado", `R$ ${Number(lead.valor_estimado).toLocaleString("pt-BR")}`],
            ["Data Entrada", new Date(lead.data_entrada).toLocaleDateString("pt-BR")],
            ["Data Qualificação", lead.data_qualificacao ? new Date(lead.data_qualificacao).toLocaleDateString("pt-BR") : "—"],
            ["Próxima Atividade", lead.prox_atividade],
            ["Motivo Descarte", lead.motivo_descarte],
          ].map(([label, value]) => (
            <div key={label as string}>
              <div className="text-xs font-medium text-[var(--color-grey)] mb-0.5">{label}</div>
              <div className="text-sm">{(value as string) || "—"}</div>
            </div>
          ))}
        </div>
      )}

      {tab === "empresa" && lead.empresa && (
        <div className="bg-white rounded-lg shadow-sm p-6 grid grid-cols-2 gap-x-8 gap-y-4">
          {[
            ["Nome", lead.empresa.nome_fantasia],
            ["CNPJ", lead.empresa.cnpj],
            ["Segmento", lead.empresa.segmento],
            ["Funcionários", lead.empresa.num_funcionarios],
            ["Cidade", lead.empresa.cidade ? `${lead.empresa.cidade}/${lead.empresa.estado}` : null],
            ["Telefone", lead.empresa.telefone],
          ].map(([label, value]) => (
            <div key={label as string}>
              <div className="text-xs font-medium text-[var(--color-grey)] mb-0.5">{label}</div>
              <div className="text-sm">{(value as string) || "—"}</div>
            </div>
          ))}
        </div>
      )}

      {tab === "atividades" && (
        <ActivityTimeline leadId={id} atividades={atividades} onReload={load} />
      )}

      {tab === "scores" && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Lead Score: {lead.lead_score}</h3>
            <button onClick={handleCalculateScore} className="text-sm text-[var(--color-monday-blue)] font-medium hover:underline">Recalcular</button>
          </div>
          <p className="text-sm text-[var(--color-grey)]">Classificação: {lead.classificacao || "Não calculado"}</p>
        </div>
      )}

      {tab === "historico" && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="font-semibold mb-4">Histórico de Etapas</h3>
          <div className="space-y-3">
            {historico.length === 0 ? (
              <p className="text-sm text-[var(--color-grey)]">Nenhum histórico</p>
            ) : historico.map((h) => (
              <div key={h.id} className="flex items-start gap-3 pb-3 border-b border-[var(--color-light-grey)]/30 last:border-0">
                <span className="material-icons-outlined text-lg text-[var(--color-monday-blue)] mt-0.5">swap_horiz</span>
                <div>
                  <div className="text-sm font-medium">
                    {h.etapa_anterior ? `${ETAPA_LABELS[h.etapa_anterior]} → ` : ""}{ETAPA_LABELS[h.etapa_nova]}
                  </div>
                  <div className="text-xs text-[var(--color-grey)]">
                    {new Date(h.created_at).toLocaleString("pt-BR")}
                    {h.tempo_na_etapa_segundos && ` · ${Math.round(h.tempo_na_etapa_segundos / 3600)}h na etapa anterior`}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
