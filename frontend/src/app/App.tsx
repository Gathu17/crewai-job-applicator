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

type Tab = "search" | "resume" | "applications" | "ai-tailor" | "monitoring";

export default function App() {
    const [activeTab, setActiveTab] = useState<Tab>("search");
    const [jobs, setJobs] = useState<Job[]>([]);
    const [searching, setSearching] = useState(false);
    const [searchError, setSearchError] = useState<string | null>(null);
    const [selectedJob, setSelectedJob] = useState<Job | null>(null);
    const [resume, setResume] = useState<Resume | null>(null);
    const [applications, setApplications] = useState<Application[]>([]);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleSearch = (_filters: SearchFilters) => {
    };

    const handleSearchResults = (results: Job[]) => {
        setJobs(results);
    };

    const handleSearchLoading = (loading: boolean) => {
        setSearching(loading);
    };

    const handleSearchError = (error: string | null) => {
        setSearchError(error);
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
                        <JobSearch
                            onSearch={handleSearch}
                            onResults={handleSearchResults}
                            onLoading={handleSearchLoading}
                            onError={handleSearchError}
                        />

                        {searchError && (
                            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                                <p className="text-red-700 text-sm">{searchError}</p>
                            </div>
                        )}

                        {searching ? (
                            <div className="text-center py-12 text-gray-500">
                                <Briefcase
                                    size={48}
                                    className="mx-auto mb-3 opacity-50 animate-pulse"
                                />
                                <p>Searching for jobs...</p>
                            </div>
                        ) : jobs.length === 0 ? (
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
