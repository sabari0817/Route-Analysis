import React from 'react';
import { AlertCircle, CloudRain, Clock, ArrowRight } from 'lucide-react';
import './BottomWidgets.css';

const BottomWidgets = ({ routeData }) => {
  const distance = routeData?.distances?.[0]?.km || "18.4";
  const startCity = routeData?.distances?.[0]?.from || "Bandra, Mumbai";
  const endCity = routeData?.distances?.[0]?.to || "Andheri, Mumbai";
  const timeMins = Math.round(Number(distance) / 40 * 60);

  const suggestion = routeData?.suggestion || "Heavy traffic on Western Express Hwy. Slow moving traffic reported near Andheri Flyover.";

  return (
    <>
      <div className="glass-panel bottom-widget">
        <div className="widget-header">
          <h3>Live Traffic Updates</h3>
          <span className="live-indicator">
            <span className="live-dot"></span> Live
          </span>
        </div>
        <div className="widget-content flex items-center gap-4 mt-2">
          <div className="icon-circle red-bg" style={{minWidth: '36px'}}>
            <AlertCircle size={18} />
          </div>
          <div className="flex-1" style={{overflow: 'hidden'}}>
            <div className="text-sm font-medium truncate whitespace-nowrap overflow-hidden text-ellipsis">{routeData ? 'AI Analysis Active' : 'Heavy traffic on Western Express Hwy'}</div>
            <div className="text-xs text-muted mt-1 truncate whitespace-nowrap overflow-hidden text-ellipsis">{suggestion}</div>
          </div>
          <div className="text-xs text-muted whitespace-nowrap">Just now</div>
        </div>
      </div>

      <div className="glass-panel bottom-widget">
        <div className="widget-header">
          <h3>Weather Impact</h3>
        </div>
        <div className="widget-content flex items-center gap-4 mt-2">
          <div className="icon-circle blue-bg">
            <CloudRain size={20} />
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-center">
              <div className="text-sm font-medium">Light Rain</div>
              <div className="text-accent text-sm font-medium">24°C</div>
            </div>
            <div className="text-xs text-muted mt-1">Slight impact on travel time</div>
          </div>
        </div>
      </div>

      <div className="glass-panel bottom-widget">
        <div className="widget-header">
          <h3>Recent Search</h3>
          <button className="text-accent text-xs font-medium">View All</button>
        </div>
        <div className="widget-content flex items-center gap-4 mt-2">
          <div className="icon-circle dark-bg">
            <Clock size={16} />
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium flex items-center gap-2">
              <span className="truncate">{startCity}</span> 
              <ArrowRight size={12} className="text-muted flex-shrink-0" /> 
              <span className="truncate">{endCity}</span>
            </div>
            <div className="text-xs text-muted mt-1">Today, Just now</div>
          </div>
          <div className="text-right whitespace-nowrap">
            <div className="text-sm font-medium">{distance} km</div>
            <div className="text-xs text-success mt-1">{timeMins} min</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default BottomWidgets;
