import { useState, useEffect } from 'react';
import { Activity, DollarSign, Zap, TrendingUp, RefreshCw, Trash2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import api, { MonitoringStats, LLMCall } from '../../services/api';

export function MonitoringDashboard() {
  const [stats, setStats] = useState<MonitoringStats | null>(null);
  const [calls, setCalls] = useState<LLMCall[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await api.getMonitoringSummary();
      setStats(data);
      setCalls((data.calls || []).slice(-20).reverse());
    } catch (error) {
      console.error('Failed to fetch monitoring data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset all monitoring statistics?')) {
      return;
    }
    try {
      await api.resetMonitoring();
      await fetchData();
    } catch (error) {
      console.error('Failed to reset stats:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatNumber = (num: number) => num?.toLocaleString() || '0';
  const formatDate = (timestamp: string) => new Date(timestamp).toLocaleString();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">LLM Monitoring</h2>
          <p className="text-gray-600">Track AI usage, costs, and performance</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={fetchData} variant="outline" disabled={loading}>
            <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button onClick={handleReset} variant="destructive" size="sm">
            <Trash2 className="mr-2 h-4 w-4" />
            Reset
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Calls</p>
                <p className="text-3xl font-bold mt-2">{stats?.total_calls || 0}</p>
              </div>
              <Activity className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Tokens</p>
                <p className="text-3xl font-bold mt-2">{formatNumber(stats?.total_tokens || 0)}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {formatNumber(stats?.prompt_tokens || 0)} / {formatNumber(stats?.completion_tokens || 0)}
                </p>
              </div>
              <Zap className="h-8 w-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Cost</p>
                <p className="text-3xl font-bold mt-2">${stats?.total_cost?.toFixed(4) || '0.0000'}</p>
              </div>
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Success Rate</p>
                <p className="text-3xl font-bold mt-2">{((stats?.success_rate || 0) * 100).toFixed(1)}%</p>
                <p className="text-xs text-gray-500 mt-1">
                  {stats?.error_count || 0} errors
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-indigo-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Calls Table */}
      <Card>
        <CardHeader>
          <CardTitle>Recent LLM Calls</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Model</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tokens</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cost</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Duration</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {calls.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                      No LLM calls recorded yet
                    </td>
                  </tr>
                ) : (
                  calls.map((call, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm">{formatDate(call.timestamp)}</td>
                      <td className="px-4 py-3 text-sm font-mono">{call.model}</td>
                      <td className="px-4 py-3 text-sm">
                        <div>{call.total_tokens}</div>
                        <div className="text-xs text-gray-500">
                          {call.prompt_tokens}/{call.completion_tokens}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm">${call.cost?.toFixed(4)}</td>
                      <td className="px-4 py-3 text-sm">{call.duration?.toFixed(2)}s</td>
                      <td className="px-4 py-3 text-sm">
                        {call.success ? (
                          <Badge className="bg-green-100 text-green-800">Success</Badge>
                        ) : (
                          <Badge variant="destructive">Error</Badge>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
