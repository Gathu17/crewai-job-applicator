import { CheckCircle2, Clock, XCircle, Send } from 'lucide-react';

export interface Application {
  id: string;
  jobTitle: string;
  company: string;
  appliedDate: string;
  status: 'pending' | 'interviewing' | 'rejected' | 'accepted';
}

interface ApplicationTrackerProps {
  applications: Application[];
}

export function ApplicationTracker({ applications }: ApplicationTrackerProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="text-yellow-600" size={20} />;
      case 'interviewing':
        return <Send className="text-blue-600" size={20} />;
      case 'rejected':
        return <XCircle className="text-red-600" size={20} />;
      case 'accepted':
        return <CheckCircle2 className="text-green-600" size={20} />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'interviewing':
        return 'bg-blue-100 text-blue-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      case 'accepted':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold mb-4">Your Applications</h2>

      {applications.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <Send size={48} className="mx-auto mb-3 opacity-50" />
          <p>No applications yet. Start applying to jobs!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {applications.map((app) => (
            <div key={app.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{app.jobTitle}</h3>
                  <p className="text-gray-600">{app.company}</p>
                </div>
                <div className="flex items-center gap-2">
                  {getStatusIcon(app.status)}
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(app.status)}`}>
                    {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                  </span>
                </div>
              </div>
              <p className="text-sm text-gray-500">Applied on {app.appliedDate}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
