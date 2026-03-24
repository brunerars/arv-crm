"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";
import KpiCard from "@/components/KpiCard";
import AlertCard from "@/components/AlertCard";
import ActivityCard from "@/components/ActivityCard";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    apiClient.getDashboard()
      .then(setData)
      .catch((err: any) => { setError(err?.message || "Erro ao carregar dashboard"); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-10 text-[var(--color-grey)]">Carregando...</div>;
  if (error) return <div className="text-center py-10 text-red-600">{error}</div>;
  if (!data) return <div className="text-center py-10 text-[var(--color-grey)]">Erro ao carregar dashboard</div>;

  const { kpis, sla_alerts, activity_summary } = data;

  return (
    <div>
      <h1 className="text-xl font-bold mb-6">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-5 mb-8">
        <KpiCard label="Leads Novos (Mês)" value={kpis.leads_novos_mes} icon="group_add" color="blue" />
        <KpiCard label="Valor no Pipeline" value={`R$ ${(kpis.valor_pipeline / 1000).toFixed(0)}K`} icon="payments" color="green" />
        <KpiCard label="Taxa de Conversão" value={`${kpis.taxa_conversao}%`} icon="percent" color="yellow" />
        <KpiCard
          label="Alertas SLA"
          value={sla_alerts.length}
          icon="warning"
          color="purple"
          change={sla_alerts.length > 0 ? { value: `${sla_alerts.length} ativos`, positive: false } : undefined}
        />
      </div>

      {/* Two column grid */}
      <div className="grid grid-cols-2 gap-6">
        {/* SLA Alerts */}
        <div>
          <h2 className="text-sm font-semibold mb-3 text-[var(--color-dark-grey)] uppercase tracking-wider">Alertas SLA</h2>
          <div className="space-y-2">
            {sla_alerts.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm p-6 text-center text-[var(--color-grey)] text-sm">
                Nenhum alerta de SLA
              </div>
            ) : sla_alerts.slice(0, 10).map((alert: any) => (
              <AlertCard key={alert.lead_id} alert={alert} onClick={() => router.push(`/dashboard/pipeline/${alert.lead_id}`)} />
            ))}
          </div>
        </div>

        {/* Activity Summary */}
        <div>
          <h2 className="text-sm font-semibold mb-3 text-[var(--color-dark-grey)] uppercase tracking-wider">Atividades</h2>
          <div className="grid grid-cols-2 gap-3">
            <ActivityCard label="Atividades Hoje" value={activity_summary.atividades_hoje} icon="today" color="var(--color-monday-blue)" />
            <ActivityCard label="Atrasadas" value={activity_summary.atividades_atrasadas} icon="warning" color="var(--color-monday-red)" />
            <ActivityCard label="Esta Semana" value={activity_summary.atividades_semana} icon="date_range" color="var(--color-monday-green)" />
            <ActivityCard label="Leads s/ Atividade" value={activity_summary.leads_sem_atividade} icon="person_off" color="var(--color-monday-orange)" />
          </div>
          <div className="mt-3">
            <ActivityCard label="Leads sem próxima atividade" value={activity_summary.leads_sem_prox_atividade} icon="event_busy" color="var(--color-monday-yellow)" />
          </div>
        </div>
      </div>
    </div>
  );
}
