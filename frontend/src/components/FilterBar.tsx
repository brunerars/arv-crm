"use client";

interface FilterOption {
  value: string;
  label: string;
}

interface FilterBarProps {
  filters: {
    key: string;
    label: string;
    options: FilterOption[];
    value: string;
    onChange: (value: string) => void;
  }[];
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  searchPlaceholder?: string;
  actions?: React.ReactNode;
}

export default function FilterBar({ filters, searchValue, onSearchChange, searchPlaceholder, actions }: FilterBarProps) {
  return (
    <div className="flex items-center gap-3 flex-wrap mb-5">
      {filters.map((f) => (
        <select
          key={f.key}
          value={f.value}
          onChange={(e) => f.onChange(e.target.value)}
          className="px-3.5 py-[7px] rounded-lg border border-[var(--color-light-grey)] text-[12.5px] text-[var(--color-dark-grey)] bg-white cursor-pointer outline-none focus:border-[var(--color-monday-blue)] min-w-[140px] appearance-none bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2710%27%20height%3D%276%27%20viewBox%3D%270%200%2010%206%27%20fill%3D%27none%27%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%3E%3Cpath%20d%3D%27M1%201L5%205L9%201%27%20stroke%3D%27%239f9f9f%27%20stroke-width%3D%271.5%27%20stroke-linecap%3D%27round%27%20stroke-linejoin%3D%27round%27%2F%3E%3C%2Fsvg%3E')] bg-no-repeat bg-[right_12px_center] pr-8"
        >
          <option value="">{f.label}</option>
          {f.options.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      ))}

      {onSearchChange && (
        <div className="relative ml-auto">
          <span className="material-icons-outlined absolute left-2.5 top-1/2 -translate-y-1/2 text-lg text-[var(--color-grey)]">search</span>
          <input
            type="text"
            value={searchValue}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder={searchPlaceholder || "Buscar..."}
            className="pl-9 pr-3.5 py-[7px] rounded-lg border border-[var(--color-light-grey)] text-[12.5px] text-[var(--color-almost-black)] bg-white outline-none focus:border-[var(--color-monday-blue)] min-w-[220px]"
          />
        </div>
      )}

      {actions}
    </div>
  );
}
