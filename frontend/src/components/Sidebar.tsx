"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

const NAV_ITEMS = [
  { href: "/dashboard", icon: "dashboard", label: "Dashboard" },
  {
    icon: "view_kanban", label: "Pipeline", children: [
      { href: "/dashboard/pipeline", label: "Pré Vendas" },
    ],
  },
  { href: "/dashboard/empresas", icon: "business", label: "Empresas" },
  { href: "/dashboard/contatos", icon: "contacts", label: "Contatos" },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [openSubs, setOpenSubs] = useState<Record<string, boolean>>({ Pipeline: true });
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const width = collapsed ? 72 : 260;

  function toggleSub(label: string) {
    setOpenSubs((prev) => ({ ...prev, [label]: !prev[label] }));
  }

  return (
    <aside
      className="fixed top-0 left-0 h-screen flex flex-col z-50 transition-sidebar overflow-hidden"
      style={{ width, background: "#111111" }}
    >
      {/* Toggle button */}
      <button
        onClick={() => {
          const newCollapsed = !collapsed;
          setCollapsed(newCollapsed);
          const main = document.getElementById("main-content");
          const topbar = document.getElementById("topbar");
          if (main) main.style.marginLeft = newCollapsed ? "72px" : "260px";
          if (topbar) topbar.style.left = newCollapsed ? "72px" : "260px";
        }}
        className="absolute top-[22px] -right-[14px] w-7 h-7 bg-white border border-[var(--color-light-grey)] rounded-full flex items-center justify-center z-[110] shadow-sm hover:bg-[var(--color-whitesmoke)] cursor-pointer"
      >
        <span className={`material-icons-outlined text-[16px] text-[var(--color-dark-grey)] transition-transform ${collapsed ? "rotate-180" : ""}`}>
          chevron_left
        </span>
      </button>

      {/* Logo */}
      <div className="flex items-center gap-3 px-5 pt-5 pb-4 border-b border-white/[0.08] min-h-[64px] shrink-0">
        <div className="w-8 h-8 bg-[var(--color-arv-red)] rounded-lg flex items-center justify-center shrink-0">
          <span className="text-white font-bold text-[15px]">A</span>
        </div>
        <span className={`text-white text-lg font-bold tracking-tight whitespace-nowrap transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>
          ARV CRM
        </span>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto overflow-x-hidden py-3">
        {NAV_ITEMS.map((item) => {
          if (item.children) {
            const isOpen = openSubs[item.label] && !collapsed;
            return (
              <div key={item.label}>
                <button
                  onClick={() => toggleSub(item.label)}
                  className={`w-full flex items-center gap-3.5 px-5 py-2.5 text-white/60 text-[13.5px] font-medium whitespace-nowrap hover:bg-white/[0.06] hover:text-white/85 border-l-[3px] border-transparent`}
                >
                  <span className="material-icons-outlined text-xl shrink-0 w-5 text-center">{item.icon}</span>
                  <span className={`transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>{item.label}</span>
                  <span className={`material-icons-outlined text-lg ml-auto transition-transform ${collapsed ? "opacity-0" : ""} ${isOpen ? "rotate-180" : ""}`}>expand_more</span>
                </button>
                <div className={`overflow-hidden transition-all ${isOpen ? "max-h-[120px]" : "max-h-0"}`}>
                  {item.children.map((child) => (
                    <Link key={child.href} href={child.href}
                      className={`flex items-center pl-[57px] pr-5 py-2 text-[13px] whitespace-nowrap border-l-[3px] ${pathname === child.href ? "text-white border-[var(--color-arv-red)]" : "text-white/45 border-transparent hover:text-white/80 hover:bg-white/[0.04]"}`}>
                      <span className={`w-[5px] h-[5px] rounded-full mr-3 shrink-0 ${pathname === child.href ? "bg-[var(--color-arv-red)]" : "bg-white/30"}`} />
                      <span className={`transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>{child.label}</span>
                    </Link>
                  ))}
                </div>
              </div>
            );
          }

          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href!}
              className={`flex items-center gap-3.5 px-5 py-2.5 text-[13.5px] font-medium whitespace-nowrap border-l-[3px] transition-colors ${isActive ? "text-white border-[var(--color-arv-red)] bg-white/[0.04]" : "text-white/60 border-transparent hover:bg-white/[0.06] hover:text-white/85"}`}>
              <span className="material-icons-outlined text-xl shrink-0 w-5 text-center">{item.icon}</span>
              <span className={`transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>{item.label}</span>
            </Link>
          );
        })}

        <div className="h-px bg-white/[0.08] mx-5 my-3" />

        <Link href="#"
          className="flex items-center gap-3.5 px-5 py-2.5 text-white/60 text-[13.5px] font-medium whitespace-nowrap hover:bg-white/[0.06] hover:text-white/85 border-l-[3px] border-transparent">
          <span className="material-icons-outlined text-xl shrink-0 w-5 text-center">settings</span>
          <span className={`transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>Configurações</span>
        </Link>
      </nav>

      {/* User footer */}
      <div className="shrink-0 border-t border-white/[0.08] py-2">
        <div className="flex items-center gap-3 px-5 py-3">
          <div className="w-[34px] h-[34px] rounded-full bg-gradient-to-br from-[var(--color-arv-red)] to-[var(--color-monday-orange)] flex items-center justify-center shrink-0 text-white text-[13px] font-semibold">
            {user?.name?.charAt(0).toUpperCase() || "?"}
          </div>
          <div className={`whitespace-nowrap transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>
            <div className="text-white text-[13px] font-semibold">{user?.name}</div>
            <div className="text-white/40 text-[11.5px]">{user?.role === "admin" ? "Administrador" : "Usuário"}</div>
          </div>
        </div>
        <button onClick={logout}
          className={`w-full flex items-center gap-3.5 px-5 py-2 text-white/40 text-[13px] hover:text-white/70 transition-opacity ${collapsed ? "justify-center" : ""}`}>
          <span className="material-icons-outlined text-lg">logout</span>
          <span className={`transition-opacity ${collapsed ? "opacity-0 pointer-events-none" : ""}`}>Sair</span>
        </button>
      </div>
    </aside>
  );
}
