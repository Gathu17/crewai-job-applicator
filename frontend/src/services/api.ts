/**
 * API Service Layer
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// ============================================
// Type Definitions (aligned with backend schemas)
// ============================================

export interface JobSearchCriteria {
  role: string;
  location?: string;
  remote?: boolean;
  experience_level?: string;
  skills?: string[];
  salary_min?: number;
  salary_max?: number;
}

export interface JobPosting {
  id?: string;
  title: string;
  company: string;
  location?: string;
  description: string;
  requirements?: string[];
  url?: string;
  salary_range?: string;
  posted_date?: string;
  source?: string;
  metadata?: Record<string, any>;
}

export interface JobSearchResponse {
  jobs: JobPosting[];
  total: number;
  message: string;
}

export interface JobAnalysis {
  job_id?: string;
  title: string;
  summary?: string;
  requirements: string[];
  key_skills: string[];
  seniority?: string;
  apply_url?: string;
}

export interface CompanyResearch {
  company: string;
  size?: string;
  industry?: string;
  culture?: string;
  recent_news: string[];
  interview_tips: string[];
}

export interface TailorResult {
  highlights: string[];
  changes: string[];
  score_before?: number;
  score_after?: number;
  metadata?: Record<string, any>;
}

export interface GeneratedResume {
  resume_id: string;
  format: string;
  content: string;
  created_at: string;
}

export interface WorkflowReport {
  job: JobPosting;
  analysis: JobAnalysis;
  company: CompanyResearch;
  tailor: TailorResult;
  resume: GeneratedResume;
  report_id?: string;
  summary?: string;
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
  successful_calls: number;
  failed_calls: number;
  total_tokens: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_cost: number;
  average_tokens_per_call: number;
  average_cost_per_call: number;
}

export interface LLMCall {
  call_number: number;
  timestamp: string;
  model: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  cost: number;
  latency: number;
  success: boolean;
  error?: string;
}

export interface MonitoringSummary {
  model: string;
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
  total_tokens: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_cost: number;
  average_tokens_per_call: number;
  average_cost_per_call: number;
  calls: LLMCall[];
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

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API ${options.method || 'GET'} ${endpoint}`, error);
      throw error;
    }
  }

  // ============================================
  // System
  // ============================================

  async healthCheck() {
    return this.request<{ status: string; llm_provider: string; llm_model: string }>('/health');
  }

  // ============================================
  // Job Search
  // ============================================

  async searchJobs(criteria: JobSearchCriteria, config?: Record<string, any>): Promise<JobSearchResponse> {
    return this.request<JobSearchResponse>('/jobs/search', {
      method: 'POST',
      body: JSON.stringify({ criteria, config: config || {} }),
    });
  }

  // ============================================
  // Job Analysis
  // ============================================

  async analyzeJob(jobDescription: string, jobUrl?: string): Promise<JobAnalysis> {
    return this.request<JobAnalysis>('/jobs/analyze', {
      method: 'POST',
      body: JSON.stringify({ job_description: jobDescription, job_url: jobUrl }),
    });
  }

  // ============================================
  // Company Research
  // ============================================

  async researchCompany(companyName: string): Promise<CompanyResearch> {
    return this.request<CompanyResearch>('/jobs/research-company', {
      method: 'POST',
      body: JSON.stringify({ company_name: companyName }),
    });
  }

  // ============================================
  // Resume Tailoring
  // ============================================

  async tailorOptimize(baseResume: string, jobAnalysis: Record<string, any>): Promise<TailorResult> {
    return this.request<TailorResult>('/jobs/tailor-optimize', {
      method: 'POST',
      body: JSON.stringify({ base_resume: baseResume, job_analysis: jobAnalysis }),
    });
  }

  // ============================================
  // Resume Generation
  // ============================================

  async generateResume(optimizedContent: Record<string, any>, outputFormat: string = 'markdown'): Promise<GeneratedResume> {
    return this.request<GeneratedResume>('/jobs/generate-resume', {
      method: 'POST',
      body: JSON.stringify({ optimized_content: optimizedContent, output_format: outputFormat }),
    });
  }

  // ============================================
  // Full Workflow
  // ============================================

  async processJob(jobUrl: string, baseResume: string, options?: Record<string, any>): Promise<WorkflowReport> {
    return this.request<WorkflowReport>('/jobs/process', {
      method: 'POST',
      body: JSON.stringify({ job_url: jobUrl, base_resume: baseResume, options: options || {} }),
    });
  }

  // ============================================
  // Resume Crew - Full Workflow (decorator pattern)
  // ============================================

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

  // ============================================
  // Monitoring
  // ============================================

  async getMonitoringStats(): Promise<MonitoringStats> {
    return this.request<MonitoringStats>('/monitoring/usage');
  }

  async getMonitoringSummary(): Promise<MonitoringSummary> {
    return this.request<MonitoringSummary>('/monitoring/summary');
  }

  async resetMonitoring(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/monitoring/reset', { method: 'POST' });
  }
}

// ============================================
// Export Singleton Instance
// ============================================

const api = new APIClient(API_BASE_URL);
export default api;
