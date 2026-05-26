import { useState } from "react";
import {
    Briefcase,
    FileText,
    ListChecks,
    Menu,
    X,
    Sparkles,
    Activity,
} from "lucide-react";
import { JobSearch, SearchFilters } from "./components/JobSearch";
import { JobCard, Job } from "./components/JobCard";
import { JobDetails, Resume } from "./components/JobDetails";
import { ResumeManager } from "./components/ResumeManager";
import {
    ApplicationTracker,
    Application,
} from "./components/ApplicationTracker";
import { AIWorkflow } from "./components/AIWorkflow";
import { MonitoringDashboard } from "./components/MonitoringDashboard";
import { mockJobs } from "./components/mockData";

type Tab = "search" | "resume" | "applications" | "ai-tailor" | "monitoring";

export default function App() {
    const [activeTab, setActiveTab] = useState<Tab>("search");
    const [jobs, setJobs] = useState<Job[]>(mockJobs);
    const [selectedJob, setSelectedJob] = useState<Job | null>(null);
    const [resume, setResume] = useState<Resume | null>(null);
    const [applications, setApplications] = useState<Application[]>([]);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleSearch = (filters: SearchFilters) => {
        let filteredJobs = [...mockJobs];

        if (filters.keyword) {
            filteredJobs = filteredJobs.filter(
                (job) =>
                    job.title
                        .toLowerCase()
                        .includes(filters.keyword.toLowerCase()) ||
                    job.description
                        .toLowerCase()
                        .includes(filters.keyword.toLowerCase()),
            );
        }

        if (filters.location) {
            filteredJobs = filteredJobs.filter((job) =>
                job.location
                    .toLowerCase()
                    .includes(filters.location.toLowerCase()),
            );
        }

        if (filters.jobType) {
            filteredJobs = filteredJobs.filter(
                (job) => job.type === filters.jobType,
            );
        }

        if (filters.salaryMin) {
            const minSalary = parseInt(filters.salaryMin);
            filteredJobs = filteredJobs.filter((job) => {
                const salaryMatch = job.salary.match(/\$(\d+)k/);
                if (salaryMatch) {
                    const jobSalary = parseInt(salaryMatch[1]) * 1000;
                    return jobSalary >= minSalary;
                }
                return true;
            });
        }

        if (resume) {
            filteredJobs = filteredJobs.map((job) => ({
                ...job,
                matchScore: calculateMatchScore(job, resume),
            }));
            filteredJobs.sort(
                (a, b) => (b.matchScore || 0) - (a.matchScore || 0),
            );
        }

        setJobs(filteredJobs);
    };

    const handleApply = (jobId: string) => {
        const job = jobs.find((j) => j.id === jobId);
        if (!job) return;

        const newApplication: Application = {
            id: Date.now().toString(),
            jobTitle: job.title,
            company: job.company,
            appliedDate: new Date().toLocaleDateString(),
            status: "pending",
        };

        setApplications([newApplication, ...applications]);
        setSelectedJob(null);
        setActiveTab("applications");
    };

    const calculateMatchScore = (job: Job, resume: Resume): number => {
        const jobText = (
            job.description +
            " " +
            job.requirements.join(" ")
        ).toLowerCase();
        const matchingSkills = resume.skills.filter((skill) =>
            jobText.includes(skill.toLowerCase()),
        );

        if (resume.skills.length === 0) return 75;
        return Math.round((matchingSkills.length / resume.skills.length) * 100);
    };

    const tabs = [
        { id: "search" as Tab, label: "Job Search", icon: Briefcase },
        { id: "ai-tailor" as Tab, label: "AI Tailor", icon: Sparkles },
        { id: "resume" as Tab, label: "Resume", icon: FileText },
        { id: "applications" as Tab, label: "Applications", icon: ListChecks },
        { id: "monitoring" as Tab, label: "Monitoring", icon: Activity },
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-3">
                            <Briefcase className="text-blue-600" size={32} />
                            <h1 className="text-2xl font-bold text-gray-900">
                                JobMatch
                            </h1>
                        </div>

                        <button
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="md:hidden p-2 text-gray-600 hover:text-gray-900"
                        >
                            {mobileMenuOpen ? (
                                <X size={24} />
                            ) : (
                                <Menu size={24} />
                            )}
                        </button>

                        <nav className="hidden md:flex gap-1">
                            {tabs.map((tab) => {
                                const Icon = tab.icon;
                                return (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveTab(tab.id)}
                                        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                                            activeTab === tab.id
                                                ? "bg-blue-50 text-blue-600"
                                                : "text-gray-600 hover:bg-gray-50"
                                        }`}
                                    >
                                        <Icon size={20} />
                                        <span>{tab.label}</span>
                                        {tab.id === "applications" &&
                                            applications.length > 0 && (
                                                <span className="bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full">
                                                    {applications.length}
                                                </span>
                                            )}
                                    </button>
                                );
                            })}
                        </nav>
                    </div>

                    {mobileMenuOpen && (
                        <div className="md:hidden py-4 border-t border-gray-200">
                            <nav className="flex flex-col gap-2">
                                {tabs.map((tab) => {
                                    const Icon = tab.icon;
                                    return (
                                        <button
                                            key={tab.id}
                                            onClick={() => {
                                                setActiveTab(tab.id);
                                                setMobileMenuOpen(false);
                                            }}
                                            className={`flex items-center gap-2 px-4 py-3 rounded-lg transition-colors ${
                                                activeTab === tab.id
                                                    ? "bg-blue-50 text-blue-600"
                                                    : "text-gray-600 hover:bg-gray-50"
                                            }`}
                                        >
                                            <Icon size={20} />
                                            <span>{tab.label}</span>
                                            {tab.id === "applications" &&
                                                applications.length > 0 && (
                                                    <span className="bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full ml-auto">
                                                        {applications.length}
                                                    </span>
                                                )}
                                        </button>
                                    );
                                })}
                            </nav>
                        </div>
                    )}
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {activeTab === "search" && (
                    <>
                        <JobSearch onSearch={handleSearch} />

                        {jobs.length === 0 ? (
                            <div className="text-center py-12 text-gray-500">
                                <Briefcase
                                    size={48}
                                    className="mx-auto mb-3 opacity-50"
                                />
                                <p>
                                    No jobs found. Try adjusting your search
                                    filters.
                                </p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {jobs.map((job) => (
                                    <JobCard
                                        key={job.id}
                                        job={job}
                                        onViewDetails={setSelectedJob}
                                    />
                                ))}
                            </div>
                        )}
                    </>
                )}

                {activeTab === "ai-tailor" && <AIWorkflow />}

                {activeTab === "resume" && (
                    <ResumeManager resume={resume} onSaveResume={setResume} />
                )}

                {activeTab === "applications" && (
                    <ApplicationTracker applications={applications} />
                )}

                {activeTab === "monitoring" && <MonitoringDashboard />}
            </main>

            {selectedJob && (
                <JobDetails
                    job={selectedJob}
                    onClose={() => setSelectedJob(null)}
                    onApply={handleApply}
                    resume={resume}
                />
            )}
        </div>
    );
}
