import { useState } from "react";
import { Sparkles, Loader2, Copy, Check, AlertCircle } from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Input } from "./ui/input";
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
} from "./ui/card";
import { Alert, AlertDescription } from "./ui/alert";
import { Badge } from "./ui/badge";
import api, { ResumeCrewResponse } from "../../services/api";

export function AIWorkflow() {
    const [jobInput, setJobInput] = useState("");
    const [baseResume, setBaseResume] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [results, setResults] = useState<ResumeCrewResponse | null>(null);
    const [copied, setCopied] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await api.runResumeCrew({
                job_input: jobInput,
                base_resume: baseResume,
                company_name: companyName || undefined,
            });
            setResults(response);
        } catch (err: any) {
            setError(
                err.message ||
                    "An error occurred while processing your request",
            );
        } finally {
            setLoading(false);
        }
    };

    const handleCopy = () => {
        if (results?.generated_resume?.content) {
            navigator.clipboard.writeText(results.generated_resume.content);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <div className="flex items-center justify-center gap-2">
                    <Sparkles className="w-8 h-8 text-blue-600" />
                    <h2 className="text-3xl font-bold">AI Resume Tailor</h2>
                </div>
                <p className="text-gray-600">
                    Let AI analyze the job and tailor your resume perfectly
                </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Job Details</CardTitle>
                        <CardDescription>
                            Paste the job URL or the complete job description
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Textarea
                            placeholder="https://linkedin.com/jobs/view/123456 or paste full job description..."
                            value={jobInput}
                            onChange={(e) => setJobInput(e.target.value)}
                            rows={4}
                            required
                            className="font-mono text-sm"
                        />
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Your Base Resume</CardTitle>
                        <CardDescription>
                            Paste your complete resume content (plain text or
                            markdown)
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Textarea
                            placeholder="John Doe&#10;Software Engineer&#10;&#10;Experience:&#10;- Company A (2020-2023)..."
                            value={baseResume}
                            onChange={(e) => setBaseResume(e.target.value)}
                            rows={12}
                            required
                            className="font-mono text-sm"
                        />
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Company Name (Optional)</CardTitle>
                        <CardDescription>
                            Leave blank to auto-extract from job description
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Input
                            placeholder="e.g., Google, Microsoft, etc."
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                        />
                    </CardContent>
                </Card>

                <Button
                    type="submit"
                    disabled={loading}
                    className="w-full"
                    size="lg"
                >
                    {loading ? (
                        <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Processing (30-60 seconds)...
                        </>
                    ) : (
                        <>
                            <Sparkles className="mr-2 h-4 w-4" />
                            Generate Tailored Resume
                        </>
                    )}
                </Button>
            </form>

            {loading && (
                <Card className="border-blue-200 bg-blue-50">
                    <CardContent className="pt-6">
                        <div className="space-y-3">
                            <p className="font-medium text-blue-900">
                                AI agents are working...
                            </p>
                            <div className="space-y-2 text-sm text-blue-800">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                                    <span>Analyzing job requirements...</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                                    <span>
                                        Researching company information...
                                    </span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                                    <span>Tailoring your resume...</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                                    <span>Generating final document...</span>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}

            {error && (
                <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}

            {results && (
                <ResultsDisplay
                    results={results}
                    onCopy={handleCopy}
                    copied={copied}
                />
            )}
        </div>
    );
}

// Results Display Component
interface ResultsDisplayProps {
    results: ResumeCrewResponse;
    onCopy: () => void;
    copied: boolean;
}

function ResultsDisplay({ results, onCopy, copied }: ResultsDisplayProps) {
    return (
        <div className="space-y-6">
            {/* Success Banner */}
            <Alert className="border-green-200 bg-green-50">
                <Check className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">
                    ✨ Your tailored resume has been generated successfully!
                </AlertDescription>
            </Alert>

            {/* Job Analysis */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        📋 Job Analysis
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Role
                            </p>
                            <p className="text-base font-semibold">
                                {results.job_analysis.role}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Company
                            </p>
                            <p className="text-base font-semibold">
                                {results.job_analysis.company}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Location
                            </p>
                            <p className="text-base">
                                {results.job_analysis.location}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Experience Level
                            </p>
                            <p className="text-base">
                                {results.job_analysis.experience_level}
                            </p>
                        </div>
                    </div>

                    <div>
                        <p className="text-sm font-medium text-gray-500 mb-2">
                            Required Skills
                        </p>
                        <div className="flex flex-wrap gap-2">
                            {results.job_analysis.required_skills.map(
                                (skill, idx) => (
                                    <Badge key={idx} variant="secondary">
                                        {skill}
                                    </Badge>
                                ),
                            )}
                        </div>
                    </div>

                    {results.job_analysis.key_requirements.length > 0 && (
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-2">
                                Key Requirements
                            </p>
                            <ul className="list-disc list-inside space-y-1 text-sm">
                                {results.job_analysis.key_requirements.map(
                                    (req, idx) => (
                                        <li key={idx}>{req}</li>
                                    ),
                                )}
                            </ul>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Company Research */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        🏢 Company Research
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Industry
                            </p>
                            <p className="text-base">
                                {results.company_research.industry}
                            </p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">
                                Company Size
                            </p>
                            <p className="text-base">
                                {results.company_research.size}
                            </p>
                        </div>
                    </div>

                    <div>
                        <p className="text-sm font-medium text-gray-500 mb-1">
                            Culture
                        </p>
                        <p className="text-sm text-gray-700">
                            {results.company_research.culture}
                        </p>
                    </div>

                    {results.company_research.interview_tips.length > 0 && (
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-2">
                                Interview Tips
                            </p>
                            <ul className="list-disc list-inside space-y-1 text-sm">
                                {results.company_research.interview_tips.map(
                                    (tip, idx) => (
                                        <li key={idx}>{tip}</li>
                                    ),
                                )}
                            </ul>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Tailoring Recommendations */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        ✨ Resume Tailoring
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <p className="text-sm font-medium text-gray-500 mb-2">
                            Skills Highlighted
                        </p>
                        <div className="flex flex-wrap gap-2">
                            {results.tailor_recommendations.skills_highlighted.map(
                                (skill, idx) => (
                                    <Badge
                                        key={idx}
                                        className="bg-green-100 text-green-800 hover:bg-green-200"
                                    >
                                        ✓ {skill}
                                    </Badge>
                                ),
                            )}
                        </div>
                    </div>

                    {results.tailor_recommendations.key_changes.length > 0 && (
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-2">
                                Key Changes Made
                            </p>
                            <ul className="list-disc list-inside space-y-1 text-sm">
                                {results.tailor_recommendations.key_changes.map(
                                    (change, idx) => (
                                        <li key={idx}>{change}</li>
                                    ),
                                )}
                            </ul>
                        </div>
                    )}

                    {results.tailor_recommendations.recommendations.length >
                        0 && (
                        <div>
                            <p className="text-sm font-medium text-gray-500 mb-2">
                                Recommendations
                            </p>
                            <ul className="list-disc list-inside space-y-1 text-sm">
                                {results.tailor_recommendations.recommendations.map(
                                    (rec, idx) => (
                                        <li key={idx}>{rec}</li>
                                    ),
                                )}
                            </ul>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Generated Resume */}
            <Card>
                <CardHeader>
                    <div className="flex justify-between items-center">
                        <CardTitle className="flex items-center gap-2">
                            📄 Generated Resume
                        </CardTitle>
                        <Button onClick={onCopy} variant="outline" size="sm">
                            {copied ? (
                                <>
                                    <Check className="mr-2 h-4 w-4" />
                                    Copied!
                                </>
                            ) : (
                                <>
                                    <Copy className="mr-2 h-4 w-4" />
                                    Copy Resume
                                </>
                            )}
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 max-h-96 overflow-y-auto">
                        <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800">
                            {results.generated_resume.content}
                        </pre>
                    </div>
                </CardContent>
            </Card>

            {/* Workflow Summary */}
            {results.workflow_report?.summary && (
                <Card className="border-blue-200 bg-blue-50">
                    <CardHeader>
                        <CardTitle className="text-blue-900">
                            📊 Workflow Summary
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-blue-800">
                            {results.workflow_report.summary}
                        </p>
                        {results.workflow_report.recommendations.length > 0 && (
                            <div className="mt-4">
                                <p className="text-sm font-medium text-blue-900 mb-2">
                                    Additional Recommendations:
                                </p>
                                <ul className="list-disc list-inside space-y-1 text-sm text-blue-800">
                                    {results.workflow_report.recommendations.map(
                                        (rec, idx) => (
                                            <li key={idx}>{rec}</li>
                                        ),
                                    )}
                                </ul>
                            </div>
                        )}
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
