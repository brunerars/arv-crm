interface KpiCardProps {
  label: string;
  value: string | number;
  icon: string;
  change?: { value: string; positive: boolean };
  color: "blue" | "green" | "yellow" | "purple";
}

const COLOR_MAP = {
  blue: { accent: "var(--color-monday-blue)", bg: "rgba(0,115,234,.08)" },
  green: { accent: "var(--color-monday-green)", bg: "rgba(0,202,114,.08)" },
  yellow: { accent: "var(--color-monday-yellow)", bg: "rgba(255,203,0,.1)" },
  purple: { accent: "var(--color-monday-purple)", bg: "rgba(97,97,255,.08)" },
};

export default function KpiCard({ label, value, icon, change, color }: KpiCardProps) {
  const c = COLOR_MAP[color];

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-[3px]" style={{ background: c.accent }} />
      <div className="flex items-center justify-between mb-3.5">
        <span className="text-[12.5px] font-medium text-[var(--color-grey)] uppercase tracking-wider">{label}</span>
        <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: c.bg, color: c.accent }}>
          <span className="material-icons-outlined text-xl">{icon}</span>
        </div>
      </div>
      <div className="text-[28px] font-bold text-[var(--color-almost-black)] tracking-tight leading-none">{value}</div>
      {change && (
        <div className={`inline-flex items-center gap-1 text-xs font-semibold mt-2 px-2 py-0.5 rounded-full ${change.positive ? "text-[var(--color-monday-green)] bg-[rgba(0,202,114,.08)]" : "text-[var(--color-monday-red)] bg-[rgba(228,66,88,.08)]"}`}>
          <span className="material-icons-outlined text-sm">{change.positive ? "arrow_upward" : "arrow_downward"}</span>
          {change.value}
        </div>
      )}
    </div>
  );
}
