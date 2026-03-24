"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";

interface CreateLeadModalProps {
  onClose: () => void;
  onCreated: () => void;
}

export default function CreateLeadModal({ onClose, onCreated }: CreateLeadModalProps) {
  const [empresas, setEmpresas] = useState<any[]>([]);
  const [origens, setOrigens] = useState<any[]>([]);
  const [form, setForm] = useState({
    empresa_id: "",
    origem_id: "",
    temperatura: "frio",
    produto_interesse: "",
    valor_estimado: "",
  });
  const [loading, setLoading] = useState(false);
  const [loadingSelects, setLoadingSelects] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([apiClient.getEmpresas({ limit: "100" }), apiClient.getOrigens()])
      .then(([emp, ori]) => { setEmpresas(emp.items); setOrigens(ori); })
      .catch((err: any) => { setError(err?.message || "Erro ao carregar dados do formulário"); })
      .finally(() => setLoadingSelects(false));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await apiClient.createLead({
        empresa_id: form.empresa_id,
        origem_id: form.origem_id || null,
        temperatura: form.temperatura,
        produto_interesse: form.produto_interesse || null,
        valor_estimado: form.valor_estimado ? Number(form.valor_estimado) : 0,
      });
      onCreated();
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Erro ao criar lead");
    } finally {
      setLoading(false);
    }
  }

  const inputClass = "w-full px-3 py-2 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)]";

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div className="bg-white rounded-xl p-6 w-full max-w-[500px] shadow-xl">
        <h2 className="text-lg font-bold mb-4">Novo Lead</h2>
        {loadingSelects && <div className="text-sm text-[var(--color-grey)] mb-3">Carregando dados...</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Empresa *</label>
            <select value={form.empresa_id} onChange={(e) => setForm({ ...form, empresa_id: e.target.value })} className={inputClass} required>
              <option value="">Selecione</option>
              {empresas.map((e) => <option key={e.id} value={e.id}>{e.nome_fantasia}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Origem</label>
            <select value={form.origem_id} onChange={(e) => setForm({ ...form, origem_id: e.target.value })} className={inputClass}>
              <option value="">Selecione</option>
              {origens.map((o) => <option key={o.id} value={o.id}>{o.tipo} / {o.sub_tipo}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Temperatura</label>
              <select value={form.temperatura} onChange={(e) => setForm({ ...form, temperatura: e.target.value })} className={inputClass}>
                <option value="frio">Frio</option>
                <option value="morno">Morno</option>
                <option value="quente">Quente</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Valor Estimado</label>
              <input type="number" value={form.valor_estimado} onChange={(e) => setForm({ ...form, valor_estimado: e.target.value })} className={inputClass} placeholder="0" />
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Produto de Interesse</label>
            <input value={form.produto_interesse} onChange={(e) => setForm({ ...form, produto_interesse: e.target.value })} className={inputClass} />
          </div>
          {error && <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</div>}
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-[var(--color-dark-grey)] border border-[var(--color-light-grey)] rounded-lg hover:bg-[var(--color-whitesmoke)]">Cancelar</button>
            <button type="submit" disabled={loading} className="px-4 py-2 text-sm text-white bg-[var(--color-almost-black)] rounded-lg hover:bg-black disabled:opacity-50">{loading ? "Criando..." : "Criar Lead"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
