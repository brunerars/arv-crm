"use client";

const STAGES = [
  { key: "prospeccao", label: "Prospecção", color: "var(--color-monday-blue)" },
  { key: "primeiro_contato", label: "1º Contato", color: "var(--color-monday-purple)" },
  { key: "qualificacao", label: "Qualificação", color: "var(--color-monday-yellow)" },
  { key: "qualificado", label: "Qualificado", color: "var(--color-monday-green)" },
];

interface StageProgressProps {
  currentStage: string;
  onChangeStage: (stage: string) => void;
}

export default function StageProgress({ currentStage, onChangeStage }: StageProgressProps) {
  const currentIdx = STAGES.findIndex((s) => s.key === currentStage);
  const isDiscarded = currentStage === "descartado";

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <div className="flex items-center gap-1">
        {STAGES.map((stage, i) => {
          const isPast = !isDiscarded && i <= currentIdx;
          const isCurrent = !isDiscarded && i === currentIdx;
          return (
            <div key={stage.key} className="flex-1 flex items-center">
              <button
                onClick={() => onChangeStage(stage.key)}
                className={`flex-1 py-2 text-center text-xs font-semibold rounded transition-all ${isCurrent ? "text-white shadow-sm" : isPast ? "text-white/80" : "text-[var(--color-grey)] bg-gray-100 hover:bg-gray-200"}`}
                style={isPast || isCurrent ? { background: stage.color } : undefined}
              >
                {stage.label}
              </button>
              {i < STAGES.length - 1 && <div className="w-2" />}
            </div>
          );
        })}
      </div>
      {!isDiscarded && currentStage !== "qualificado" && (
        <button onClick={() => onChangeStage("descartado")}
          className="mt-2 text-xs text-[var(--color-monday-red)] font-medium hover:underline">
          Descartar lead
        </button>
      )}
      {isDiscarded && (
        <div className="mt-2 text-xs text-[var(--color-monday-red)] font-semibold">Lead descartado</div>
      )}
    </div>
  );
}
