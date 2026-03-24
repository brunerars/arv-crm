"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";
import DataTable from "@/components/DataTable";
import FilterBar from "@/components/FilterBar";
import EmpresaForm from "@/components/EmpresaForm";

const STATUS_OPTIONS = [
  { value: "prospect", label: "Prospect" },
  { value: "com_oportunidade", label: "Com Oportunidade" },
  { value: "cliente_ativo", label: "Cliente Ativo" },
  { value: "inativo", label: "Inativo" },
];

const STATUS_COLORS: Record<string, string> = {
  prospect: "bg-[rgba(0,115,234,.1)] text-[var(--color-monday-blue)]",
  com_oportunidade: "bg-[rgba(255,203,0,.15)] text-[#a67c00]",
  cliente_ativo: "bg-[rgba(0,202,114,.1)] text-[#007a3d]",
  inativo: "bg-[rgba(0,0,0,.06)] text-[var(--color-grey)]",
};

export default function EmpresasPage() {
  const [empresas, setEmpresas] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [showForm, setShowForm] = useState(false);
  const router = useRouter();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (search) params.search = search;
      if (statusFilter) params.status_conta = statusFilter;
      const data = await apiClient.getEmpresas(params);
      setEmpresas(data.items);
      setTotal(data.total);
    } finally {
      setLoading(false);
    }
  }, [search, statusFilter]);

  useEffect(() => { load(); }, [load]);

  const columns = [
    { key: "nome_fantasia", label: "Empresa", render: (v: string) => <span className="font-semibold">{v}</span> },
    { key: "cnpj", label: "CNPJ" },
    { key: "segmento", label: "Segmento" },
    { key: "cidade", label: "Cidade", render: (v: string, row: any) => v ? `${v}/${row.estado || ""}` : "—" },
    { key: "status_conta", label: "Status", render: (v: string) => (
      <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${STATUS_COLORS[v] || ""}`}>
        {STATUS_OPTIONS.find((o) => o.value === v)?.label || v}
      </span>
    )},
    { key: "telefone", label: "Telefone" },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">Empresas</h1>
          <p className="text-sm text-[var(--color-grey)]">{total} empresas cadastradas</p>
        </div>
        <button onClick={() => setShowForm(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-[var(--color-almost-black)] text-white rounded-lg text-sm font-semibold hover:bg-black">
          <span className="material-icons-outlined text-lg">add</span>
          Nova Empresa
        </button>
      </div>

      <FilterBar
        filters={[
          { key: "status", label: "Status", options: STATUS_OPTIONS, value: statusFilter, onChange: setStatusFilter },
        ]}
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Buscar empresas..."
      />

      <DataTable
        columns={columns}
        data={empresas}
        loading={loading}
        onRowClick={(row) => router.push(`/dashboard/empresas/${row.id}`)}
      />

      {showForm && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl p-6 w-full max-w-[700px] max-h-[90vh] overflow-y-auto shadow-xl">
            <h2 className="text-lg font-bold mb-4">Nova Empresa</h2>
            <EmpresaForm
              onSubmit={async (data) => { await apiClient.createEmpresa(data); setShowForm(false); load(); }}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
