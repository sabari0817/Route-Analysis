import React, { useState } from 'react';
import { ArrowRightLeft, Sparkles, Bell, Moon, Loader2 } from 'lucide-react';
import './Header.css';

const Header = ({ onAnalyze, isLoading }) => {
  const [fromCity, setFromCity] = useState("Mumbai");
  const [toCity, setToCity] = useState("Pune");

  const handleSwap = () => {
    setFromCity(toCity);
    setToCity(fromCity);
  };

  const handleAnalyze = () => {
    if (fromCity && toCity) {
      onAnalyze(`${fromCity} to ${toCity}`);
    }
  };

  return (
    <header className="header">
      <div className="route-inputs glass-panel">
        <div className="input-group">
          <label className="text-muted text-xs font-medium">From</label>
          <input 
            type="text" 
            value={fromCity} 
            onChange={(e) => setFromCity(e.target.value)} 
            className="route-input" 
            placeholder="Origin City"
          />
        </div>
        
        <button className="swap-btn" onClick={handleSwap} disabled={isLoading}>
          <ArrowRightLeft size={16} />
        </button>

        <div className="input-group">
          <label className="text-muted text-xs font-medium">To</label>
          <input 
            type="text" 
            value={toCity} 
            onChange={(e) => setToCity(e.target.value)} 
            className="route-input" 
            placeholder="Destination City"
          />
        </div>
      </div>

      <button className="analyze-btn" onClick={handleAnalyze} disabled={isLoading || !fromCity || !toCity}>
        {isLoading ? (
          <>
            <Loader2 size={18} className="animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Sparkles size={18} />
            Analyze Route
          </>
        )}
      </button>

      <div className="header-actions">
        <button className="icon-btn relative">
          <Bell size={20} />
          <span className="notification-badge">3</span>
        </button>
        <button className="icon-btn">
          <Moon size={20} />
        </button>
        <img src="https://i.pravatar.cc/150?img=11" alt="Profile" className="header-avatar" />
      </div>
    </header>
  );
};

export default Header;
