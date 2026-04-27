import React from 'react';
import { Route, Clock, Fuel, Activity, ShieldAlert, Navigation, Bookmark, Loader2 } from 'lucide-react';
import './RouteSummary.css';

const RouteSummary = ({ routeData, isLoading }) => {
  // Safe defaults or calculated fields
  const distance = routeData?.distances?.[0]?.km || "18.4";
  const trafficLoad = routeData?.transport?.bus || 36; // Just mock mapping transport load to traffic load
  
  const timeMins = Math.round(Number(distance) / 40 * 60);
  const formattedTime = timeMins > 60 ? `${Math.floor(timeMins / 60)}h ${timeMins % 60}m` : `${timeMins} min`;
  
  const fuelCost = Math.round(Number(distance) * 5.5); // ~₹5.5 per km

  return (
    <div className="route-summary glass-panel relative" style={{position: 'relative'}}>
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-panel/80 backdrop-blur-sm z-10 rounded-md" style={{position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(17, 24, 40, 0.7)', zIndex: 10, backdropFilter: 'blur(4px)', borderRadius: '12px'}}>
          <Loader2 className="animate-spin text-accent" size={32} color="#3b82f6" />
        </div>
      )}

      <div className="summary-header">
        <h2 className="summary-title">Route Summary</h2>
        <span className="badge best">{routeData ? 'Live Data' : 'Good to go'}</span>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <div className="card-icon-container blue">
            <Route size={20} />
          </div>
          <div className="card-content">
            <div className="card-label">Distance</div>
            <div className="card-value">{distance} km</div>
          </div>
          <div className="card-trend positive">↘ 12% shorter</div>
        </div>

        <div className="summary-card">
          <div className="card-icon-container purple">
            <Clock size={20} />
          </div>
          <div className="card-content">
            <div className="card-label">ETA</div>
            <div className="card-value">{formattedTime}</div>
          </div>
          <div className="card-trend positive">↘ 8 min faster</div>
        </div>

        <div className="summary-card">
          <div className="card-icon-container orange">
            <Fuel size={20} />
          </div>
          <div className="card-content">
            <div className="card-label">Fuel Cost</div>
            <div className="card-value">₹{fuelCost}</div>
          </div>
          <div className="card-trend positive">↘ ₹20 saved</div>
        </div>

        <div className="summary-card">
          <div className="card-icon-container green">
            <Activity size={20} />
          </div>
          <div className="card-content">
            <div className="card-label">Traffic Load</div>
            <div className="card-value">{trafficLoad > 50 ? 'Heavy' : trafficLoad > 30 ? 'Moderate' : 'Low'}</div>
          </div>
          <div className="card-trend circular">
            <div className="circle-progress" style={{
              borderColor: `rgba(245, 158, 11, 0.2)`,
              borderTopColor: trafficLoad > 50 ? '#ef4444' : trafficLoad > 30 ? '#f59e0b' : '#10b981',
              color: trafficLoad > 50 ? '#ef4444' : trafficLoad > 30 ? '#f59e0b' : '#10b981'
            }}>
              <span>{trafficLoad}%</span>
            </div>
          </div>
        </div>

        <div className="summary-card">
          <div className="card-icon-container red">
            <ShieldAlert size={20} />
          </div>
          <div className="card-content">
            <div className="card-label">Risk Level</div>
            <div className="card-value">{trafficLoad > 50 ? 'High' : 'Low'}</div>
          </div>
          <div className="card-trend positive">{trafficLoad > 50 ? 'Caution Advised' : 'Safe Route'}</div>
        </div>
      </div>

      <div className="summary-actions">
        <button className="start-nav-btn">
          <Navigation size={18} />
          Start Navigation
        </button>
        <button className="save-route-btn">
          <Bookmark size={18} />
          Save Route
        </button>
      </div>
    </div>
  );
};

export default RouteSummary;
