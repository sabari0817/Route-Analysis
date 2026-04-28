import React from 'react';
import { MapPin, Target, ArrowRight, Loader2 } from 'lucide-react';
import './MapArea.css';

const MapArea = ({ routeData, isLoading }) => {
  // Safe defaults
  const distance = routeData?.distances?.[0]?.km || "18.4";
  const startCity = routeData?.distances?.[0]?.from || "Bandra";
  const endCity = routeData?.distances?.[0]?.to || "Andheri";

  // Mock calculation for time based on distance (assumes ~40km/h avg speed)
  const timeHours = (Number(distance) / 40).toFixed(1);
  const timeMins = Math.round(Number(distance) / 40 * 60);
  const formattedTime = timeMins > 60 ? `${Math.floor(timeMins / 60)}h ${timeMins % 60}m` : `${timeMins} min`;

  return (
    <div className="map-container glass-panel">
      {/* Mock Map Background */}
      <div className="map-background">
        <div className="map-grid"></div>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-20" style={{position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 20}}>
            <Loader2 className="animate-spin text-accent" size={48} color="#3b82f6" />
          </div>
        )}
        
        {/* Mock Route Path SVG */}
        <svg className="route-path" viewBox="0 0 800 400" preserveAspectRatio="none">
          <defs>
            <linearGradient id="routeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" /> {/* Green */}
              <stop offset="50%" stopColor="#f59e0b" /> {/* Orange/Yellow */}
              <stop offset="100%" stopColor="#ef4444" /> {/* Red */}
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          <path 
            d="M 150 250 Q 200 280 250 220 T 350 280 T 450 240 T 550 150 L 650 160" 
            fill="none" 
            stroke="url(#routeGradient)" 
            strokeWidth="6" 
            strokeLinecap="round"
            strokeLinejoin="round"
            filter="url(#glow)"
            style={{ opacity: isLoading ? 0.3 : 1, transition: 'opacity 0.3s' }}
          />
        </svg>

        {/* Start Pin */}
        <div className="map-pin start-pin" style={{ left: '150px', top: '250px' }}>
          <div className="pin-pulse start-pulse"></div>
          <MapPin size={24} color="#10b981" fill="#fff" />
          <div className="pin-label text-xs font-bold mt-1 text-center" style={{color: '#fff', textShadow: '0 1px 3px rgba(0,0,0,0.8)'}}>{startCity}</div>
        </div>

        {/* End Pin */}
        <div className="map-pin end-pin" style={{ left: '650px', top: '160px' }}>
          <div className="pin-pulse end-pulse"></div>
          <MapPin size={28} color="#ef4444" fill="#fff" />
          <div className="pin-label text-xs font-bold mt-1 text-center" style={{color: '#fff', textShadow: '0 1px 3px rgba(0,0,0,0.8)'}}>{endCity}</div>
        </div>
      </div>

      {/* Route Options Overlay */}
      <div className="route-options-card">
        <h3 className="options-title">Route Options</h3>
        
        <div className="route-option active">
          <div className="option-header">
            <span className="option-name">AI Recommended</span>
            <span className="badge best">Best</span>
          </div>
          <div className="option-stats">
            <span>{distance} km</span>
            <span>{formattedTime}</span>
          </div>
          <div className="progress-bar-container">
            <div className="progress-bar ai-progress"></div>
          </div>
        </div>

        <div className="route-option">
          <div className="option-header">
            <span className="option-name text-secondary">Alternate Route 1</span>
          </div>
          <div className="option-stats text-muted">
            <span>{(Number(distance) * 1.1).toFixed(1)} km</span>
            <span>{Math.round(timeMins * 1.15)} min</span>
          </div>
          <div className="progress-bar-container">
            <div className="progress-bar alt1-progress"></div>
          </div>
        </div>

        <div className="route-option">
          <div className="option-header">
            <span className="option-name text-secondary">Alternate Route 2</span>
          </div>
          <div className="option-stats text-muted">
            <span>{(Number(distance) * 1.25).toFixed(1)} km</span>
            <span>{Math.round(timeMins * 1.3)} min</span>
          </div>
          <div className="progress-bar-container">
            <div className="progress-bar alt2-progress"></div>
          </div>
        </div>

        <button className="view-all-routes text-accent text-sm font-medium mt-2">
          View All Routes <ArrowRight size={14} className="ml-1" />
        </button>
      </div>
      
      {/* Map Controls */}
      <div className="map-controls">
        <button className="control-btn"><Target size={18} /></button>
        <div className="zoom-controls">
          <button className="control-btn">+</button>
          <div className="divider"></div>
          <button className="control-btn">-</button>
        </div>
      </div>
    </div>
  );
};

export default MapArea;
