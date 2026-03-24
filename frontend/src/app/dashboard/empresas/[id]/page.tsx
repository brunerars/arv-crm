"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import { apiClient } from "@/lib/api";
import EmpresaForm from "@/components/EmpresaForm";
import ContatoForm from "@/components/ContatoForm";
import { useToast } from "@/contexts/ToastContext";

const INFLUENCE_BADGE: Record<string, string> = {
  decisor: "bg-red-100 text-red-700",
  influenciador: "bg-yellow-100 text-yellow-700",
  operacional: "bg-gray-100 text-gray-600",
};

export default function EmpresaDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [empresa, setEmpresa] = useState<any>(null);
  const [contatos, setContatos] = useState<any[]>([]);
  const [tab, setTab] = useState("dados");
  const [editing, setEditing] = useState(false);
  const [showContatoForm, setShowContatoForm] = useState(false);
  const [enriching, setEnriching] = useState(false);
  const [error, setError] = useState("");
  const { addToast } = useToast();

  const load = useCallback(async () => {
    try {
      const [emp, cont] = await Promise.all([
        apiClient.getEmpresa(id),
        apiClient.getContatos({ empresa_id: id }),
      ]);
      setEmpresa(emp);
      setContatos(cont.items);
    } catch (err: any) {
      setError(err.message || "Erro ao carregar empresa");
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  if (error) return <div className="text-center py-10 text-[var(--color-arv-red)]">{error}</div>;
  if (!empresa) return <div className="text-center py-10 text-[var(--color-grey)]">Carregando...</div>;

  async function handleEnrich() {
    setEnriching(true);
    try {
      const updated = await apiClient.enrichCnpj(id);
      setEmpresa(updated);
      addToast("CNPJ enriquecido com sucesso", "success");
    } catch (err: any) {
      addToast(err.message, "error");
    } finally {
      setEnriching(false);
    }
  }

  const tabs = [
    { key: "dados", label: "Dados", icon: "info" },
    { key: "contatos", label: "Contatos", icon: "contacts" },
    { key: "leads", label: "Leads", icon: "view_kanban" },
  ];

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">{empresa.nome_fantasia}</h1>
          <p className="text-sm text-[var(--color-grey)]">{empresa.cnpj || "Sem CNPJ"} &middot; {empresa.cidade || "—"}/{empresa.estado || "—"}</p>
        </div>
        <div className="flex gap-2">
          {empresa.cnpj && (
            <button onClick={handleEnrich} disabled={enriching}
              className="flex items-center gap-1.5 px-3 py-2 text-sm border border-[var(--color-light-grey)] rounded-lg hover:bg-[var(--color-whitesmoke)] disabled:opacity-50">
              <span className="material-icons-outlined text-base">auto_fix_high</span>
              {enriching ? "Enriquecendo..." : "Enriquecer CNPJ"}
            </button>
          )}
          <button onClick={() => { setEditing(true); setTab("dados"); }}
            className="flex items-center gap-1.5 px-3 py-2 text-sm bg-[var(--color-almost-black)] text-white rounded-lg hover:bg-black">
            <span className="material-icons-outlined text-base">edit</span>
            Editar
          </button>
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
      {tab === "dados" && !editing && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="grid grid-cols-2 gap-x-8 gap-y-4">
            {[
              ["Razão Social", empresa.razao_social],
              ["CNPJ", empresa.cnpj],
              ["Segmento", empresa.segmento],
              ["Funcionários", empresa.num_funcionarios],
              ["Plantas", empresa.num_plantas],
              ["Distância ARV", empresa.distancia_arv_km ? `${empresa.distancia_arv_km} km` : null],
              ["Telefone", empresa.telefone],
              ["Site", empresa.site],
              ["CEP", empresa.cep],
              ["Status", empresa.status_conta],
            ].map(([label, value]) => (
              <div key={label as string}>
                <div className="text-xs font-medium text-[var(--color-grey)] mb-0.5">{label}</div>
                <div className="text-sm">{(value as string) || "—"}</div>
              </div>
            ))}
          </div>
          {empresa.observacoes && (
            <div className="mt-4 pt-4 border-t border-[var(--color-light-grey)]/30">
              <div className="text-xs font-medium text-[var(--color-grey)] mb-0.5">Observações</div>
              <div className="text-sm whitespace-pre-wrap">{empresa.observacoes}</div>
            </div>
          )}
        </div>
      )}

      {tab === "dados" && editing && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <EmpresaForm
            initial={empresa}
            onSubmit={async (data) => { const updated = await apiClient.updateEmpresa(id, data); setEmpresa(updated); setEditing(false); addToast("Empresa atualizada", "success"); }}
            onCancel={() => setEditing(false)}
          />
        </div>
      )}

      {tab === "contatos" && (
        <div>
          <div className="flex justify-end mb-4">
            <button onClick={() => setShowContatoForm(true)}
              className="flex items-center gap-1.5 px-3 py-2 text-sm bg-[var(--color-almost-black)] text-white rounded-lg hover:bg-black">
              <span className="material-icons-outlined text-base">add</span>
              Novo Contato
            </button>
          </div>
          <div className="grid gap-3">
            {contatos.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm p-8 text-center text-[var(--color-grey)] text-sm">Nenhum contato cadastrado</div>
            ) : contatos.map((c) => (
              <div key={c.id} className="bg-white rounded-lg shadow-sm p-4 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-sm">{c.nome}</div>
                  <div className="text-xs text-[var(--color-grey)]">{c.cargo || "—"} &middot; {c.departamento || "—"}</div>
                  <div className="text-xs text-[var(--color-grey)] mt-1">{c.email || "—"} &middot; {c.whatsapp || "—"}</div>
                </div>
                <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${INFLUENCE_BADGE[c.nivel_influencia] || ""}`}>
                  {c.nivel_influencia === "decisor" ? "Decisor" : c.nivel_influencia === "influenciador" ? "Influenciador" : "Operacional"}
                </span>
              </div>
            ))}
          </div>
          {showContatoForm && (
            <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
              <div className="bg-white rounded-xl p-6 w-full max-w-[600px] shadow-xl">
                <h2 className="text-lg font-bold mb-4">Novo Contato</h2>
                <ContatoForm empresaId={id}
                  onSubmit={async (data) => { await apiClient.createContato(data); setShowContatoForm(false); load(); addToast("Contato criado", "success"); }}
                  onCancel={() => setShowContatoForm(false)}
                />
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "leads" && (
        <div className="bg-white rounded-lg shadow-sm p-8 text-center text-[var(--color-grey)] text-sm">
          Leads serão exibidos aqui quando disponíveis
        </div>
      )}
    </div>
  );
}
