import type {
  AuthToken,
  User,
  Empresa,
  EmpresaList,
  EmpresaCreate,
  Contato,
  ContatoList,
  ContatoCreate,
  Origem,
  Lead,
  LeadDetail,
  LeadList,
  LeadCreate,
  LeadUpdate,
  KanbanResponse,
  Completude,
  HistoricoEtapa,
  Atividade,
  AtividadeList,
  AtividadeCreate,
  DashboardData,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const res = await fetch(`${API_URL}/api${path}`, { ...options, headers });

    if (res.status === 204) return null as T;

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || `Erro ${res.status}`);
    }
    return data as T;
  }

  // Auth
  login(email: string, password: string): Promise<AuthToken> {
    return this.request<AuthToken>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
  }

  register(name: string, email: string, password: string, admin_secret: string): Promise<AuthToken> {
    return this.request<AuthToken>("/auth/register", { method: "POST", body: JSON.stringify({ email, password, name, admin_secret }) });
  }

  getMe(): Promise<User> {
    return this.request<User>("/auth/me");
  }

  logout(): Promise<null> {
    return this.request<null>("/auth/logout", { method: "POST" });
  }

  // Empresas
  getEmpresas(params?: Record<string, string>): Promise<EmpresaList> {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<EmpresaList>(`/empresas${qs}`);
  }

  getEmpresa(id: string): Promise<Empresa> {
    return this.request<Empresa>(`/empresas/${id}`);
  }

  createEmpresa(data: EmpresaCreate): Promise<Empresa> {
    return this.request<Empresa>("/empresas", { method: "POST", body: JSON.stringify(data) });
  }

  updateEmpresa(id: string, data: Partial<EmpresaCreate>): Promise<Empresa> {
    return this.request<Empresa>(`/empresas/${id}`, { method: "PUT", body: JSON.stringify(data) });
  }

  deleteEmpresa(id: string): Promise<null> {
    return this.request<null>(`/empresas/${id}`, { method: "DELETE" });
  }

  enrichCnpj(id: string): Promise<Empresa> {
    return this.request<Empresa>(`/empresas/${id}/enrich-cnpj`, { method: "POST" });
  }

  // Contatos
  getContatos(params?: Record<string, string>): Promise<ContatoList> {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<ContatoList>(`/contatos${qs}`);
  }

  createContato(data: ContatoCreate): Promise<Contato> {
    return this.request<Contato>("/contatos", { method: "POST", body: JSON.stringify(data) });
  }

  getContato(id: string): Promise<Contato> {
    return this.request<Contato>(`/contatos/${id}`);
  }

  updateContato(id: string, data: Partial<ContatoCreate>): Promise<Contato> {
    return this.request<Contato>(`/contatos/${id}`, { method: "PUT", body: JSON.stringify(data) });
  }

  deleteContato(id: string): Promise<null> {
    return this.request<null>(`/contatos/${id}`, { method: "DELETE" });
  }

  // Origens
  getOrigens(): Promise<Origem[]> {
    return this.request<Origem[]>("/origens");
  }

  // Leads
  getKanban(params?: Record<string, string>): Promise<KanbanResponse> {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<KanbanResponse>(`/leads/kanban${qs}`);
  }

  getLeads(params?: Record<string, string>): Promise<LeadList> {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<LeadList>(`/leads${qs}`);
  }

  getLead(id: string): Promise<LeadDetail> {
    return this.request<LeadDetail>(`/leads/${id}`);
  }

  createLead(data: LeadCreate): Promise<Lead> {
    return this.request<Lead>("/leads", { method: "POST", body: JSON.stringify(data) });
  }

  updateLead(id: string, data: LeadUpdate): Promise<Lead> {
    return this.request<Lead>(`/leads/${id}`, { method: "PUT", body: JSON.stringify(data) });
  }

  deleteLead(id: string): Promise<null> {
    return this.request<null>(`/leads/${id}`, { method: "DELETE" });
  }

  changeStage(id: string, nova_etapa: string, motivo_descarte?: string): Promise<Lead> {
    return this.request<Lead>(`/leads/${id}/change-stage`, { method: "POST", body: JSON.stringify({ nova_etapa, motivo_descarte }) });
  }

  getCompletude(id: string): Promise<Completude> {
    return this.request<Completude>(`/leads/${id}/completude`);
  }

  getHistorico(id: string): Promise<HistoricoEtapa[]> {
    return this.request<HistoricoEtapa[]>(`/leads/${id}/historico`);
  }

  calculateScore(id: string): Promise<Lead> {
    return this.request<Lead>(`/leads/${id}/calculate-score`, { method: "POST" });
  }

  // Atividades
  getAtividades(params?: Record<string, string>): Promise<AtividadeList> {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return this.request<AtividadeList>(`/atividades${qs}`);
  }

  createAtividade(data: AtividadeCreate): Promise<Atividade> {
    return this.request<Atividade>("/atividades", { method: "POST", body: JSON.stringify(data) });
  }

  completeAtividade(id: string): Promise<Atividade> {
    return this.request<Atividade>(`/atividades/${id}/complete`, { method: "POST" });
  }

  // Dashboard
  getDashboard(): Promise<DashboardData> {
    return this.request<DashboardData>("/dashboard");
  }
}

export const apiClient = new ApiClient();
