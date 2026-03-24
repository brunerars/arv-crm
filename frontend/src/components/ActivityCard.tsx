interface ActivityCardProps {
  label: string;
  value: number;
  icon: string;
  color?: string;
}

export default function ActivityCard({ label, value, icon, color }: ActivityCardProps) {
  return (
    <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
      <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: color ? `${color}15` : "rgba(0,0,0,.04)", color: color || "var(--color-dark-grey)" }}>
        <span className="material-icons-outlined text-xl">{icon}</span>
      </div>
      <div>
        <div className="text-lg font-bold">{value}</div>
        <div className="text-xs text-[var(--color-grey)]">{label}</div>
      </div>
    </div>
  );
}
