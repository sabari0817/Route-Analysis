import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MapArea from './components/MapArea';
import RouteSummary from './components/RouteSummary';
import Charts from './components/Charts';
import BottomWidgets from './components/BottomWidgets';
import './App.css';

function App() {
  const [routeData, setRouteData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeRoute = async (routeString) => {
    if (!routeString.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setRouteData(null); // Clear previous data
    
    try {
      // Proxy handles /testing -> http://localhost:8000/testing
      const response = await fetch(`/testing/?route=${encodeURIComponent(routeString)}`);
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      
      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      setRouteData(result.data);
    } catch (err) {
      console.error("Failed to analyze route:", err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <Header onAnalyze={analyzeRoute} isLoading={isLoading} />
        
        {error && (
          <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', padding: '12px', borderRadius: '8px', border: '1px solid #ef4444' }}>
            {error}
          </div>
        )}

        <div className="dashboard-grid">
          <div className="dashboard-main-column">
            <MapArea routeData={routeData} isLoading={isLoading} />
            
            <div className="dashboard-bottom-row">
              <Charts routeData={routeData} />
            </div>

            <div className="dashboard-footer-row">
              <BottomWidgets routeData={routeData} />
            </div>
          </div>
          
          <div className="dashboard-side-column">
            <RouteSummary routeData={routeData} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
