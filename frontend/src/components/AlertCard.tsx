interface AlertCardProps {
  alert: {
    lead_id: string;
    lead_display_id: string;
    empresa: string;
    etapa: string;
    dias_na_etapa: number;
    sla_dias: number;
    overdue_dias: number;
    severity: string;
  };
  onClick: () => void;
}

export default function AlertCard({ alert, onClick }: AlertCardProps) {
  const isCritical = alert.severity === "critical";

  return (
    <div onClick={onClick}
      className={`p-3 rounded-lg cursor-pointer transition-colors border-l-[3px] ${isCritical ? "bg-red-50 border-l-[var(--color-monday-red)] hover:bg-red-100" : "bg-yellow-50 border-l-[var(--color-monday-yellow)] hover:bg-yellow-100"}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-semibold">{alert.lead_display_id} — {alert.empresa}</span>
        <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${isCritical ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"}`}>
          +{alert.overdue_dias}d
        </span>
      </div>
      <div className="text-xs text-[var(--color-grey)]">
        {alert.etapa} &middot; {alert.dias_na_etapa}d (SLA: {alert.sla_dias}d)
      </div>
    </div>
  );
}
