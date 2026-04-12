import React from 'react';
import { dashboardData } from '../../data/mockData';

export interface DashboardProps {
  readonly className?: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ className = '' }) => {
  return (
    <section id="dashboard" className={`py-28 px-8 md:px-12 bg-white ${className}`}>
      <div className="max-w-[1200px] mx-auto flex flex-col items-center">
        <div className="text-center mb-14">
          <span className="text-xs font-bold text-blue-600 uppercase tracking-[0.2em]">{dashboardData.tagline}</span>
          <h2 className="font-headline text-3xl md:text-4xl font-bold mt-3 text-navy">{dashboardData.title}</h2>
        </div>
        
        <div className="w-full max-w-[900px] bg-white rounded-2xl border border-slate-200 shadow-lg overflow-hidden flex min-h-[500px]">
          {/* Sidebar */}
          <div className="w-52 bg-white border-r border-slate-200 p-6 hidden md:flex flex-col">
            <div className="flex items-center gap-2.5 mb-10">
              <div className="w-7 h-7 rounded bg-navy"></div>
              <span className="font-bold font-headline text-sm text-navy">SCMS OS</span>
            </div>
            <div className="space-y-5">
              <div className="flex items-center gap-2.5 text-blue-600">
                <span className="material-symbols-outlined text-lg">dashboard</span>
                <span className="text-sm font-semibold">Dashboard</span>
              </div>
              <div className="flex items-center gap-2.5 text-slate-400">
                <span className="material-symbols-outlined text-lg">table_chart</span>
                <span className="text-sm">Strategic Reports</span>
              </div>
              <div className="flex items-center gap-2.5 text-slate-400">
                <span className="material-symbols-outlined text-lg">corporate_fare</span>
                <span className="text-sm">Facilities</span>
              </div>
            </div>
          </div>
          
          {/* Main */}
          <div className="flex-1 flex flex-col">
            <div className="px-6 py-5 border-b border-slate-200 flex justify-between items-center">
              <h3 className="font-headline font-bold text-lg text-navy">Executive Oversight</h3>
              <span className="px-3 py-1 bg-green-50 text-success text-[10px] font-bold rounded-full uppercase tracking-wider border border-green-100">System Normal</span>
            </div>
            
            <div className="p-6">
              {/* Stats */}
              <div className="grid grid-cols-2 gap-5 mb-6">
                <div className="p-5 bg-white rounded-xl border border-slate-200">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Active Incidents</span>
                  <div className="text-3xl font-bold text-navy mt-1 font-headline">{dashboardData.stats.activeIncidents}</div>
                  <div className="mt-3 h-1 bg-slate-100 rounded-full overflow-hidden">
                    <div className="w-1/4 h-full bg-blue-600 rounded-full"></div>
                  </div>
                </div>
                <div className="p-5 bg-white rounded-xl border border-slate-200">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Avg Resolution Time</span>
                  <div className="text-3xl font-bold text-navy mt-1 font-headline">{dashboardData.stats.avgResolutionTime}</div>
                  <div className="mt-3 h-1 bg-slate-100 rounded-full overflow-hidden">
                    <div className="w-3/4 h-full bg-success rounded-full"></div>
                  </div>
                </div>
              </div>
              
              {/* Table */}
              <table className="w-full text-left">
                <thead className="text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                  <tr>
                    <th className="pb-3 pl-1">Complaint ID</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3">Priority</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {dashboardData.incidents.map((incident, idx) => (
                    <tr key={idx} className="border-b border-slate-100 last:border-0">
                      <td className="py-3.5 pl-1 font-bold text-navy">{incident.id}</td>
                      <td className="py-3.5">
                        <span className={`text-[10px] font-bold uppercase tracking-wider ${
                          incident.status === 'PENDING' ? 'text-error' :
                          incident.status === 'ACTIVE' ? 'text-blue-600' :
                          'text-success'
                        }`}>
                          {incident.status}
                        </span>
                      </td>
                      <td className={`py-3.5 text-xs font-bold ${
                        incident.priority === 'CRITICAL' ? 'text-error' :
                        incident.priority === 'HIGH' ? 'text-blue-600' : 'text-success'
                      }`}>
                        {incident.priority}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Dashboard;
