/**
 * API Service Layer
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// ============================================
// Type Definitions
// ============================================

export interface JobAnalysis {
  role: string;
  company: string;
  location: string;
  experience_level: string;
  required_skills: string[];
  nice_to_have_skills: string[];
  responsibilities: string[];
  salary_range?: string;
  key_requirements: string[];
}

export interface CompanyResearch {
  company_name: string;
  industry: string;
  size: string;
  culture: string;
  values: string[];
  interview_tips: string[];
  glassdoor_rating?: number;
}

export interface TailorResult {
  optimized_content: string;
  key_changes: string[];
  skills_highlighted: string[];
  recommendations: string[];
}

export interface GeneratedResume {
  resume_id: string;
  format: string;
  content: string;
  created_at: string;
}

export interface WorkflowReport {
  summary: string;
  recommendations: string[];
}

export interface ResumeCrewResponse {
  job_analysis: JobAnalysis;
  company_research: CompanyResearch;
  tailor_recommendations: TailorResult;
  generated_resume: GeneratedResume;
  workflow_report: WorkflowReport;
}

export interface MonitoringStats {
  total_calls: number;
  total_tokens: number;
  prompt_tokens: number;
  completion_tokens: number;
  total_cost: number;
  error_count: number;
  success_rate: number;
}

export interface LLMCall {
  timestamp: string;
  model: string;
  total_tokens: number;
  prompt_tokens: number;
  completion_tokens: number;
  cost: number;
  duration: number;
  success: boolean;
}

// ============================================
// API Client
// ============================================

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    console.log(`🚀 ${options.method || 'GET'} ${endpoint}`);

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log(`✅ ${options.method || 'GET'} ${endpoint}`, data);
      return data;
    } catch (error) {
      console.error(`❌ ${options.method || 'GET'} ${endpoint}`, error);
      throw error;
    }
  }

  // Health Check
  async healthCheck() {
    return this.request<{ status: string; llm_provider: string; llm_model: string }>('/health');
  }

  // Resume Crew - Full Workflow
  async runResumeCrew(data: {
    job_input: string;
    base_resume: string;
    company_name?: string;
  }): Promise<ResumeCrewResponse> {
    return this.request<ResumeCrewResponse>('/jobs/resume-crew', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Monitoring
  async getMonitoringStats(): Promise<MonitoringStats> {
    return this.request<MonitoringStats>('/monitoring/usage');
  }

  async getMonitoringSummary(): Promise<{ calls: LLMCall[] } & MonitoringStats> {
    return this.request('/monitoring/summary');
  }

  async resetMonitoring(): Promise<{ message: string }> {
    return this.request('/monitoring/reset', { method: 'POST' });
  }
}

// ============================================
// Export Singleton Instance
// ============================================

const api = new APIClient(API_BASE_URL);
export default api;
