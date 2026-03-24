"use client";

import { useState, useEffect, useCallback } from "react";
import { apiClient } from "@/lib/api";
import DataTable from "@/components/DataTable";
import FilterBar from "@/components/FilterBar";

const INFLUENCE_BADGE: Record<string, string> = {
  decisor: "bg-red-100 text-red-700",
  influenciador: "bg-yellow-100 text-yellow-700",
  operacional: "bg-gray-100 text-gray-600",
};

export default function ContatosPage() {
  const [contatos, setContatos] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (search) params.search = search;
      const data = await apiClient.getContatos(params);
      setContatos(data.items);
      setTotal(data.total);
    } finally {
      setLoading(false);
    }
  }, [search]);

  useEffect(() => { load(); }, [load]);

  const columns = [
    { key: "nome", label: "Nome", render: (v: string) => <span className="font-semibold">{v}</span> },
    { key: "cargo", label: "Cargo" },
    { key: "departamento", label: "Departamento" },
    { key: "email", label: "Email" },
    { key: "whatsapp", label: "WhatsApp" },
    { key: "nivel_influencia", label: "Influência", render: (v: string) => (
      <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${INFLUENCE_BADGE[v] || ""}`}>
        {v === "decisor" ? "Decisor" : v === "influenciador" ? "Influenciador" : "Operacional"}
      </span>
    )},
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">Contatos</h1>
          <p className="text-sm text-[var(--color-grey)]">{total} contatos</p>
        </div>
      </div>

      <FilterBar
        filters={[]}
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Buscar contatos..."
      />

      <DataTable columns={columns} data={contatos} loading={loading} />
    </div>
  );
}
