"use client";

import { useState } from "react";

interface EmpresaFormProps {
  initial?: any;
  onSubmit: (data: any) => Promise<void>;
  onCancel: () => void;
}

export default function EmpresaForm({ initial, onSubmit, onCancel }: EmpresaFormProps) {
  const [form, setForm] = useState({
    nome_fantasia: initial?.nome_fantasia || "",
    razao_social: initial?.razao_social || "",
    cnpj: initial?.cnpj || "",
    segmento: initial?.segmento || "",
    num_funcionarios: initial?.num_funcionarios || "",
    num_plantas: initial?.num_plantas || "",
    distancia_arv_km: initial?.distancia_arv_km || "",
    cidade: initial?.cidade || "",
    estado: initial?.estado || "",
    cep: initial?.cep || "",
    telefone: initial?.telefone || "",
    site: initial?.site || "",
    observacoes: initial?.observacoes || "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(key: string, value: string) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await onSubmit({
        ...form,
        num_plantas: form.num_plantas ? Number(form.num_plantas) : null,
        distancia_arv_km: form.distancia_arv_km ? Number(form.distancia_arv_km) : null,
      });
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Erro ao salvar empresa");
    } finally {
      setLoading(false);
    }
  }

  const inputClass = "w-full px-3 py-2 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10";

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Nome Fantasia *</label>
          <input value={form.nome_fantasia} onChange={(e) => handleChange("nome_fantasia", e.target.value)} className={inputClass} required />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Razão Social</label>
          <input value={form.razao_social} onChange={(e) => handleChange("razao_social", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">CNPJ</label>
          <input value={form.cnpj} onChange={(e) => handleChange("cnpj", e.target.value)} className={inputClass} placeholder="00.000.000/0000-00" />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Segmento</label>
          <input value={form.segmento} onChange={(e) => handleChange("segmento", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Funcionários</label>
          <select value={form.num_funcionarios} onChange={(e) => handleChange("num_funcionarios", e.target.value)} className={inputClass}>
            <option value="">Selecione</option>
            <option value="1-50">1-50</option>
            <option value="51-200">51-200</option>
            <option value="201-500">201-500</option>
            <option value="501-1000">501-1000</option>
            <option value="1000+">1000+</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Nº Plantas</label>
          <input type="number" value={form.num_plantas} onChange={(e) => handleChange("num_plantas", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Distância ARV (km)</label>
          <input type="number" step="0.01" value={form.distancia_arv_km} onChange={(e) => handleChange("distancia_arv_km", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Telefone</label>
          <input value={form.telefone} onChange={(e) => handleChange("telefone", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Cidade</label>
          <input value={form.cidade} onChange={(e) => handleChange("cidade", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Estado</label>
          <input value={form.estado} onChange={(e) => handleChange("estado", e.target.value)} className={inputClass} maxLength={2} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">CEP</label>
          <input value={form.cep} onChange={(e) => handleChange("cep", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Site</label>
          <input value={form.site} onChange={(e) => handleChange("site", e.target.value)} className={inputClass} />
        </div>
      </div>
      <div>
        <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Observações</label>
        <textarea value={form.observacoes} onChange={(e) => handleChange("observacoes", e.target.value)} className={`${inputClass} h-20 resize-none`} />
      </div>
      {error && <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</div>}
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="px-4 py-2 text-sm text-[var(--color-dark-grey)] border border-[var(--color-light-grey)] rounded-lg hover:bg-[var(--color-whitesmoke)]">
          Cancelar
        </button>
        <button type="submit" disabled={loading} className="px-4 py-2 text-sm text-white bg-[var(--color-almost-black)] rounded-lg hover:bg-black disabled:opacity-50">
          {loading ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
}
