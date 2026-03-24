"use client";

import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

const breadcrumbMap: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/dashboard/empresas": "Empresas",
  "/dashboard/contatos": "Contatos",
  "/dashboard/pipeline": "Pipeline Pré-Vendas",
};

export default function Topbar() {
  const { user } = useAuth();
  const pathname = usePathname();

  const currentPage = Object.entries(breadcrumbMap).reverse().find(([path]) => pathname.startsWith(path));
  const pageTitle = currentPage ? currentPage[1] : "Dashboard";

  return (
    <header
      id="topbar"
      className="fixed top-0 right-0 h-[60px] bg-white border-b border-black/[0.06] flex items-center justify-between px-8 z-40 transition-sidebar shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
      style={{ left: 260 }}
    >
      <div className="flex items-center gap-3">
        <div className="text-[13px] text-[var(--color-grey)]">
          CRM / <strong className="text-[var(--color-almost-black)] font-semibold">{pageTitle}</strong>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative">
          <span className="material-icons-outlined absolute left-3 top-1/2 -translate-y-1/2 text-lg text-[var(--color-grey)]">search</span>
          <input
            type="text"
            placeholder="Buscar..."
            className="w-[260px] h-9 pl-[38px] pr-3.5 border border-[var(--color-light-grey)] rounded-full bg-[var(--color-whitesmoke)] text-[13px] outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10 focus:w-[320px] transition-all"
          />
        </div>

        <div className="relative w-9 h-9 flex items-center justify-center rounded-full cursor-pointer hover:bg-[var(--color-whitesmoke)]">
          <span className="material-icons-outlined text-[22px] text-[var(--color-dark-grey)]">notifications</span>
        </div>

        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-arv-red)] to-[var(--color-monday-orange)] flex items-center justify-center text-white text-xs font-semibold cursor-pointer hover:shadow-[0_0_0_3px_rgba(200,42,42,0.15)]">
          {user?.name?.charAt(0).toUpperCase() || "?"}
        </div>
      </div>
    </header>
  );
}
