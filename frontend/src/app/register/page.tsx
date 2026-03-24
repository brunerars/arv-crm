"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [adminSecret, setAdminSecret] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await apiClient.register(name, email, password, adminSecret);
      router.push("/");
    } catch (err: any) {
      setError(err.message || "Erro ao registrar");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-whitesmoke)]">
      <div className="w-full max-w-[400px] p-8">
        <div className="flex items-center gap-3 mb-8 justify-center">
          <div className="w-10 h-10 bg-[var(--color-arv-red)] rounded-lg flex items-center justify-center text-white font-bold text-lg">A</div>
          <span className="text-2xl font-bold tracking-tight">ARV CRM</span>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-lg font-semibold mb-6 text-center">Registrar</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--color-dark-grey)] mb-1.5">Nome</label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2.5 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10"
                placeholder="Seu nome" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--color-dark-grey)] mb-1.5">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2.5 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10"
                placeholder="seu@email.com" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--color-dark-grey)] mb-1.5">Senha</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2.5 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10"
                placeholder="••••••••" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--color-dark-grey)] mb-1.5">Admin Secret</label>
              <input type="password" value={adminSecret} onChange={(e) => setAdminSecret(e.target.value)}
                className="w-full px-3 py-2.5 border border-[var(--color-light-grey)] rounded-lg text-sm focus:outline-none focus:border-[var(--color-monday-blue)] focus:ring-2 focus:ring-[var(--color-monday-blue)]/10"
                placeholder="Secret de administração" required />
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-2.5 bg-[var(--color-almost-black)] text-white rounded-lg font-semibold text-sm hover:bg-black transition-colors disabled:opacity-50">
              {loading ? "Registrando..." : "Registrar"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
