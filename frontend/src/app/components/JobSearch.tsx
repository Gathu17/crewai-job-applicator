import { Search, MapPin, Briefcase, DollarSign } from 'lucide-react';
import { useState } from 'react';

interface JobSearchProps {
  onSearch: (filters: SearchFilters) => void;
}

export interface SearchFilters {
  keyword: string;
  location: string;
  jobType: string;
  salaryMin: string;
}

export function JobSearch({ onSearch }: JobSearchProps) {
  const [filters, setFilters] = useState<SearchFilters>({
    keyword: '',
    location: '',
    jobType: '',
    salaryMin: ''
  });

  const handleSearch = () => {
    onSearch(filters);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Search Jobs</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Job title, keywords..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={filters.keyword}
            onChange={(e) => setFilters({ ...filters, keyword: e.target.value })}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </div>
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Location"
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={filters.location}
            onChange={(e) => setFilters({ ...filters, location: e.target.value })}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </div>
        <div className="relative">
          <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <select
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
            value={filters.jobType}
            onChange={(e) => setFilters({ ...filters, jobType: e.target.value })}
          >
            <option value="">All Types</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contract">Contract</option>
            <option value="internship">Internship</option>
          </select>
        </div>
        <div className="relative">
          <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <select
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
            value={filters.salaryMin}
            onChange={(e) => setFilters({ ...filters, salaryMin: e.target.value })}
          >
            <option value="">Any Salary</option>
            <option value="50000">$50k+</option>
            <option value="75000">$75k+</option>
            <option value="100000">$100k+</option>
            <option value="150000">$150k+</option>
          </select>
        </div>
      </div>
      <button
        onClick={handleSearch}
        className="mt-4 w-full md:w-auto px-8 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Search Jobs
      </button>
    </div>
  );
}
