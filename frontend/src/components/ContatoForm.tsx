"use client";

import { useState } from "react";

interface ContatoFormProps {
  empresaId: string;
  initial?: any;
  onSubmit: (data: any) => Promise<void>;
  onCancel: () => void;
}

export default function ContatoForm({ empresaId, initial, onSubmit, onCancel }: ContatoFormProps) {
  const [form, setForm] = useState({
    nome: initial?.nome || "",
    cargo: initial?.cargo || "",
    departamento: initial?.departamento || "",
    nivel_influencia: initial?.nivel_influencia || "operacional",
    email: initial?.email || "",
    whatsapp: initial?.whatsapp || "",
    linkedin: initial?.linkedin || "",
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
      await onSubmit({ ...form, empresa_id: empresaId });
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Erro ao salvar contato");
    } finally {
      setLoading(false);
    }
  }

  const inputClass = "w-full px-3 py-2 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10";

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Nome *</label>
          <input value={form.nome} onChange={(e) => handleChange("nome", e.target.value)} className={inputClass} required />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Cargo</label>
          <input value={form.cargo} onChange={(e) => handleChange("cargo", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Departamento</label>
          <input value={form.departamento} onChange={(e) => handleChange("departamento", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Nível de Influência</label>
          <select value={form.nivel_influencia} onChange={(e) => handleChange("nivel_influencia", e.target.value)} className={inputClass}>
            <option value="operacional">Operacional</option>
            <option value="influenciador">Influenciador</option>
            <option value="decisor">Decisor</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">Email</label>
          <input type="email" value={form.email} onChange={(e) => handleChange("email", e.target.value)} className={inputClass} />
        </div>
        <div>
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">WhatsApp</label>
          <input value={form.whatsapp} onChange={(e) => handleChange("whatsapp", e.target.value)} className={inputClass} />
        </div>
        <div className="col-span-2">
          <label className="block text-xs font-medium text-[var(--color-dark-grey)] mb-1">LinkedIn</label>
          <input value={form.linkedin} onChange={(e) => handleChange("linkedin", e.target.value)} className={inputClass} />
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
