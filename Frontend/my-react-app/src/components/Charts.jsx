import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import './Charts.css';

const defaultTrafficData = [
  { time: '12 AM', value: 10 },
  { time: '4 AM', value: 25 },
  { time: '8 AM', value: 65, peak: true },
  { time: '12 PM', value: 40 },
  { time: '4 PM', value: 85 },
  { time: '8 PM', value: 50 },
  { time: '12 AM', value: 15 },
];

const defaultTravelTimeData = [
  { time: '12 AM', timeVal: 10 },
  { time: '6 AM', timeVal: 18 },
  { time: '10 AM', timeVal: 48, active: true },
  { time: '12 PM', timeVal: 35 },
  { time: '2 PM', timeVal: 30 },
  { time: '4 PM', timeVal: 40 },
  { time: '6 PM', timeVal: 55 },
  { time: '8 PM', timeVal: 35 },
  { time: '12 AM', timeVal: 15 },
];

const Charts = ({ routeData }) => {
  // If we have transport data from backend, let's map it to something visually interesting
  // The transport object has {"bus": 60, "train": 25, "private": 15}
  // Let's create a dynamic "Mode Share" chart instead of "Travel Time" if data is present
  const transportData = routeData?.transport 
    ? [
        { mode: 'Bus', share: routeData.transport.bus, active: routeData.transport.bus > 50 },
        { mode: 'Train', share: routeData.transport.train, active: routeData.transport.train > 50 },
        { mode: 'Private', share: routeData.transport.private, active: routeData.transport.private > 50 }
      ]
    : null;

  return (
    <>
      {/* Traffic Trends */}
      <div className="glass-panel chart-widget">
        <div className="widget-header">
          <h3>Traffic Trends</h3>
          <select className="widget-select">
            <option>Today</option>
          </select>
        </div>
        <div className="chart-container" style={{ width: '100%', height: '100%', minHeight: 0, minWidth: 0 }}>
          <ResponsiveContainer width="99%" height="100%">
            <AreaChart data={defaultTrafficData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorTraffic" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="50%" stopColor="#f59e0b" stopOpacity={0.5}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} tickFormatter={(val) => `${val}%`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111828', borderColor: '#1e293b', borderRadius: '8px' }}
                itemStyle={{ color: '#fff' }}
              />
              <Area type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={3} fillOpacity={1} fill="url(#colorTraffic)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Dynamic Bar Chart: Travel Time OR Transport Mode Share */}
      <div className="glass-panel chart-widget">
        <div className="widget-header">
          <h3>{transportData ? 'Transport Mode Share' : 'Travel Time by Hour'}</h3>
          <select className="widget-select">
            <option>Today</option>
          </select>
        </div>
        <div className="chart-container" style={{ width: '100%', height: '100%', minHeight: 0, minWidth: 0 }}>
          <ResponsiveContainer width="99%" height="100%">
            <BarChart data={transportData || defaultTravelTimeData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
              <XAxis dataKey={transportData ? "mode" : "time"} axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 10}} tickFormatter={(val) => transportData ? `${val}%` : `${val} min`} />
              <Tooltip 
                cursor={{fill: 'rgba(255,255,255,0.05)'}}
                contentStyle={{ backgroundColor: '#111828', borderColor: '#1e293b', borderRadius: '8px' }}
              />
              <Bar dataKey={transportData ? "share" : "timeVal"} radius={[4, 4, 4, 4]}>
                {(transportData || defaultTravelTimeData).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.active ? '#3b82f6' : '#1e3a8a'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Recommended Time */}
      <div className="glass-panel chart-widget ai-time-widget">
        <div className="widget-header">
          <h3>AI Recommended Time</h3>
        </div>
        <div className="ai-time-content">
          <div className="radial-chart">
            <svg viewBox="0 0 100 100" className="radial-svg">
              <circle cx="50" cy="50" r="40" className="radial-bg" />
              <circle cx="50" cy="50" r="40" className="radial-progress" strokeDasharray="251.2" strokeDashoffset="62.8" />
              <text x="50" y="55" className="radial-text">🕒</text>
            </svg>
          </div>
          <div className="ai-time-details">
            <div className="text-muted text-sm">Start at</div>
            <div className="text-xl font-bold">10:00 AM</div>
            <p className="text-xs text-muted mt-2">Optimal time to reach faster & avoid traffic.</p>
          </div>
        </div>
        <div className="confidence-badge">96% Confidence</div>
      </div>
    </>
  );
};

export default Charts;
