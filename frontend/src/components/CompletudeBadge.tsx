interface CompletudeBadgeProps {
  completude: any;
}

export default function CompletudeBadge({ completude }: CompletudeBadgeProps) {
  if (!completude) return null;

  const pct = completude.pct || 0;
  const color = pct >= 80 ? "var(--color-monday-green)" : pct >= 50 ? "var(--color-monday-yellow)" : "var(--color-monday-red)";

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <div className="text-xs font-medium text-[var(--color-grey)] mb-1">Completude</div>
      <div className="text-2xl font-bold" style={{ color }}>{pct}%</div>
      <div className="w-full h-1.5 bg-gray-100 rounded-full mt-2">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
      </div>
      {completude.missing?.length > 0 && (
        <div className="mt-2">
          <div className="text-[10px] font-medium text-[var(--color-grey)] mb-1">Pendente:</div>
          {completude.missing.map((m: string) => (
            <div key={m} className="text-[11px] text-[var(--color-monday-red)]">- {m}</div>
          ))}
        </div>
      )}
    </div>
  );
}
