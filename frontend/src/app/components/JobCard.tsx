import { MapPin, Briefcase, DollarSign, Clock, TrendingUp } from 'lucide-react';

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  type: string;
  salary: string;
  postedDate: string;
  description: string;
  requirements: string[];
  matchScore?: number;
}

interface JobCardProps {
  job: Job;
  onViewDetails: (job: Job) => void;
}

export function JobCard({ job, onViewDetails }: JobCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow border border-gray-100">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{job.title}</h3>
          <p className="text-gray-600">{job.company}</p>
        </div>
        {job.matchScore !== undefined && (
          <div className="flex items-center gap-1 bg-green-50 text-green-700 px-3 py-1 rounded-full">
            <TrendingUp size={16} />
            <span className="text-sm font-medium">{job.matchScore}% Match</span>
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-4">
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

      <p className="text-gray-700 mb-4 line-clamp-2">{job.description}</p>

      <button
        onClick={() => onViewDetails(job)}
        className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        View Details & Apply
      </button>
    </div>
  );
}
