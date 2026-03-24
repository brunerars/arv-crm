"use client";

interface Column {
  key: string;
  label: string;
  render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
  columns: Column[];
  data: any[];
  onRowClick?: (row: any) => void;
  loading?: boolean;
}

export default function DataTable({ columns, data, onRowClick, loading }: DataTableProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 text-center text-[var(--color-grey)]">
        Carregando...
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-[var(--color-light-grey)]/50">
            {columns.map((col) => (
              <th key={col.key} className="text-left px-4 py-3 text-[12px] font-semibold text-[var(--color-grey)] uppercase tracking-wider">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center text-[var(--color-grey)] text-sm">
                Nenhum registro encontrado
              </td>
            </tr>
          ) : (
            data.map((row, i) => (
              <tr
                key={row.id || i}
                onClick={() => onRowClick?.(row)}
                className={`border-b border-[var(--color-light-grey)]/30 hover:bg-[var(--color-whitesmoke)]/50 transition-colors ${onRowClick ? "cursor-pointer" : ""}`}
              >
                {columns.map((col) => (
                  <td key={col.key} className="px-4 py-3 text-[13px]">
                    {col.render ? col.render(row[col.key], row) : row[col.key] || "—"}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
