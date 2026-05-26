import { X, MapPin, Briefcase, DollarSign, Clock, CheckCircle2, AlertCircle, TrendingUp, FileText } from 'lucide-react';
import { Job } from './JobCard';
import { useState } from 'react';

interface JobDetailsProps {
  job: Job;
  onClose: () => void;
  onApply: (jobId: string) => void;
  resume: Resume | null;
}

export interface Resume {
  name: string;
  email: string;
  phone: string;
  skills: string[];
  experience: string[];
  education: string[];
}

export function JobDetails({ job, onClose, onApply, resume }: JobDetailsProps) {
  const [showAnalysis, setShowAnalysis] = useState(true);

  const analysis = analyzeJobDescription(job, resume);
  const matchScore = calculateMatchScore(job, resume);

  const handleApply = () => {
    onApply(job.id);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-start">
          <div className="flex-1">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">{job.title}</h2>
            <p className="text-lg text-gray-600">{job.company}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        <div className="p-6">
          <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-6">
            <div className="flex items-center gap-1">
              <MapPin size={16} />
              <span>{job.location}</span>
            </div>
            <div className="flex items-center gap-1">
              <Briefcase size={16} />
              <span className="capitalize">{job.type}</span>
            </div>
            <div className="flex items-center gap-1">
              <DollarSign size={16} />
              <span>{job.salary}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock size={16} />
              <span>{job.postedDate}</span>
            </div>
          </div>

          {resume && (
            <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-6 mb-6 border border-blue-100">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <TrendingUp className="text-blue-600" size={24} />
                  <h3 className="text-lg font-semibold">Resume Match Analysis</h3>
                </div>
                <div className="text-3xl font-bold text-green-600">{matchScore}%</div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <CheckCircle2 size={18} className="text-green-600" />
                    Matching Skills ({analysis.matchingSkills.length})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.matchingSkills.map((skill, idx) => (
                      <span key={idx} className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <AlertCircle size={18} className="text-orange-600" />
                    Missing Skills ({analysis.missingSkills.length})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.missingSkills.map((skill, idx) => (
                      <span key={idx} className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-sm">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-3">Job Description</h3>
            <p className="text-gray-700 whitespace-pre-line">{job.description}</p>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-3">Requirements</h3>
            <ul className="space-y-2">
              {job.requirements.map((req, idx) => (
                <li key={idx} className="flex items-start gap-2 text-gray-700">
                  <CheckCircle2 size={18} className="text-blue-600 mt-0.5 flex-shrink-0" />
                  <span>{req}</span>
                </li>
              ))}
            </ul>
          </div>

          {showAnalysis && (
            <div className="mb-6 bg-blue-50 rounded-lg p-6 border border-blue-100">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <FileText size={20} className="text-blue-600" />
                AI-Powered Job Analysis
              </h3>
              <div className="space-y-3 text-gray-700">
                <div>
                  <h4 className="font-medium mb-1">Key Responsibilities:</h4>
                  <p>{analysis.keyResponsibilities}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Growth Opportunities:</h4>
                  <p>{analysis.growthOpportunities}</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Application Tips:</h4>
                  <p>{analysis.applicationTips}</p>
                </div>
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleApply}
              className="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Apply Now
            </button>
            <button
              onClick={() => setShowAnalysis(!showAnalysis)}
              className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              {showAnalysis ? 'Hide' : 'Show'} Analysis
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function analyzeJobDescription(job: Job, resume: Resume | null) {
  const jobSkills = extractSkills(job.description + ' ' + job.requirements.join(' '));
  const resumeSkills = resume?.skills || [];

  const matchingSkills = jobSkills.filter(skill =>
    resumeSkills.some(rSkill => rSkill.toLowerCase().includes(skill.toLowerCase()) ||
                                 skill.toLowerCase().includes(rSkill.toLowerCase()))
  );

  const missingSkills = jobSkills.filter(skill => !matchingSkills.includes(skill)).slice(0, 5);

  return {
    matchingSkills,
    missingSkills,
    keyResponsibilities: 'This role focuses on developing and maintaining software applications, collaborating with cross-functional teams, and contributing to technical architecture decisions.',
    growthOpportunities: 'Excellent opportunity to work with modern technologies, mentor junior developers, and potentially move into technical leadership roles.',
    applicationTips: 'Highlight your experience with the matching skills in your cover letter. Consider taking online courses for the missing skills to strengthen your application.'
  };
}

function extractSkills(text: string): string[] {
  const commonSkills = [
    'JavaScript', 'TypeScript', 'React', 'Node.js', 'Python', 'Java', 'C++',
    'AWS', 'Docker', 'Kubernetes', 'SQL', 'MongoDB', 'Git', 'Agile',
    'REST API', 'GraphQL', 'CI/CD', 'TDD', 'Microservices', 'Leadership',
    'Communication', 'Problem Solving', 'Team Collaboration'
  ];

  return commonSkills.filter(skill =>
    text.toLowerCase().includes(skill.toLowerCase())
  );
}

function calculateMatchScore(job: Job, resume: Resume | null): number {
  if (!resume) return 0;

  const jobSkills = extractSkills(job.description + ' ' + job.requirements.join(' '));
  const resumeSkills = resume.skills;

  if (jobSkills.length === 0) return 75;

  const matchingCount = jobSkills.filter(skill =>
    resumeSkills.some(rSkill => rSkill.toLowerCase().includes(skill.toLowerCase()) ||
                                 skill.toLowerCase().includes(rSkill.toLowerCase()))
  ).length;

  return Math.round((matchingCount / jobSkills.length) * 100);
}
