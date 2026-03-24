// ===== Auth =====
export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "user";
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user: User;
}

// ===== Empresa =====
export interface Empresa {
  id: string;
  nome_fantasia: string;
  razao_social: string | null;
  cnpj: string | null;
  segmento: string | null;
  num_funcionarios: string | null;
  num_plantas: number | null;
  distancia_arv_km: number | null;
  cidade: string | null;
  estado: string | null;
  cep: string | null;
  telefone: string | null;
  site: string | null;
  status_conta: "prospect" | "com_oportunidade" | "cliente_ativo" | "inativo";
  responsavel_id: string | null;
  data_cadastro: string;
  observacoes: string | null;
  created_at: string;
  updated_at: string;
}

export interface EmpresaList {
  items: Empresa[];
  total: number;
}

export interface EmpresaCreate {
  nome_fantasia: string;
  razao_social?: string;
  cnpj?: string;
  segmento?: string;
  num_funcionarios?: string;
  num_plantas?: number;
  distancia_arv_km?: number;
  cidade?: string;
  estado?: string;
  cep?: string;
  telefone?: string;
  site?: string;
  observacoes?: string;
  responsavel_id?: string;
}

// ===== Contato =====
export interface Contato {
  id: string;
  empresa_id: string;
  nome: string;
  cargo: string | null;
  departamento: string | null;
  nivel_influencia: "operacional" | "influenciador" | "decisor";
  email: string | null;
  whatsapp: string | null;
  linkedin: string | null;
  ativo: boolean;
  data_cadastro: string;
  observacoes: string | null;
  created_at: string;
  updated_at: string;
}

export interface ContatoList {
  items: Contato[];
  total: number;
}

export interface ContatoCreate {
  empresa_id: string;
  nome: string;
  cargo?: string;
  departamento?: string;
  nivel_influencia?: string;
  email?: string;
  whatsapp?: string;
  linkedin?: string;
  observacoes?: string;
}

// ===== Origem =====
export interface Origem {
  id: string;
  tipo: "ativa" | "passiva" | "indicacao";
  sub_tipo: string;
  descricao: string | null;
}

// ===== Lead =====
export type LeadEtapa = "prospeccao" | "primeiro_contato" | "qualificacao" | "qualificado" | "descartado";
export type LeadTemperatura = "frio" | "morno" | "quente";

export interface Lead {
  id: string;
  lead_id: string;
  empresa_id: string;
  contato_principal_id: string | null;
  origem_id: string | null;
  responsavel_id: string | null;
  etapa: LeadEtapa;
  sub_status: string | null;
  temperatura: LeadTemperatura;
  produto_interesse: string | null;
  area_atuacao: string | null;
  tipo_entrega: string | null;
  lead_score: number;
  classificacao: string | null;
  valor_estimado: number;
  motivo_descarte: string | null;
  data_entrada: string;
  data_qualificacao: string | null;
  prox_atividade: string | null;
  data_prox_atividade: string | null;
  created_at: string;
  updated_at: string;
}

export interface LeadDetail extends Lead {
  empresa: Empresa | null;
  contato_principal: Contato | null;
  completude: Completude | null;
}

export interface LeadCreate {
  empresa_id: string;
  contato_principal_id?: string;
  origem_id?: string;
  responsavel_id?: string;
  temperatura?: LeadTemperatura;
  produto_interesse?: string;
  area_atuacao?: string;
  tipo_entrega?: string;
  valor_estimado?: number;
}

export interface LeadUpdate {
  contato_principal_id?: string;
  origem_id?: string;
  responsavel_id?: string;
  temperatura?: LeadTemperatura;
  produto_interesse?: string;
  area_atuacao?: string;
  tipo_entrega?: string;
  valor_estimado?: number;
  motivo_descarte?: string;
  prox_atividade?: string;
  data_prox_atividade?: string;
  sub_status?: string;
}

export interface LeadList {
  items: Lead[];
  total: number;
}

// ===== Kanban =====
export interface KanbanColumn {
  etapa: LeadEtapa;
  count: number;
  total_valor: number;
  leads: Lead[];
}

export interface KanbanResponse {
  columns: KanbanColumn[];
  total_leads: number;
  total_valor: number;
}

// ===== Completude =====
export interface Completude {
  etapa: string;
  pct: number;
  filled: string[];
  missing: string[];
  total: number;
}

// ===== Historico =====
export interface HistoricoEtapa {
  id: string;
  etapa_anterior: string | null;
  etapa_nova: string;
  tempo_na_etapa_segundos: number | null;
  created_at: string;
}

// ===== Atividade =====
export interface Atividade {
  id: string;
  lead_id: string;
  responsavel_id: string | null;
  tipo: string;
  descricao: string | null;
  data_prevista: string | null;
  data_conclusao: string | null;
  concluida: boolean;
  created_at: string;
}

export interface AtividadeList {
  items: Atividade[];
  total: number;
}

export interface AtividadeCreate {
  lead_id: string;
  tipo: string;
  descricao?: string;
  data_prevista?: string;
  responsavel_id?: string;
}

// ===== Dashboard =====
export interface DashboardKpis {
  leads_novos_mes: number;
  leads_por_etapa: Record<string, number>;
  valor_pipeline: number;
  taxa_conversao: number;
  por_temperatura: Record<string, number>;
}

export interface SlaAlert {
  lead_id: string;
  lead_display_id: string;
  empresa: string;
  etapa: string;
  dias_na_etapa: number;
  sla_dias: number;
  overdue_dias: number;
  severity: "warning" | "critical";
}

export interface ActivitySummary {
  atividades_hoje: number;
  atividades_atrasadas: number;
  atividades_semana: number;
  leads_sem_atividade: number;
  leads_sem_prox_atividade: number;
}

export interface DashboardData {
  kpis: DashboardKpis;
  sla_alerts: SlaAlert[];
  activity_summary: ActivitySummary;
}
