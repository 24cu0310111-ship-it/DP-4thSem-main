import React from 'react';
import { obstaclesData } from '../../data/mockData';

const iconMap: Record<string, string> = {
  schedule: 'schedule',
  search_off: 'search_off',
  inventory: 'inventory_2',
};

export interface ObstaclesProps {
  readonly className?: string;
}

export const Obstacles: React.FC<ObstaclesProps> = ({ className = '' }) => {
  return (
    <section id="obstacles" className={`py-24 px-8 md:px-12 bg-slate-50 ${className}`}>
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-16">
          <span className="text-xs font-bold text-blue-600 uppercase tracking-[0.2em]">{obstaclesData.tagline}</span>
          <h2 className="font-headline text-3xl md:text-4xl font-bold mt-3 text-navy">{obstaclesData.title}</h2>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6">
          {obstaclesData.items.map((item, idx) => (
            <div 
              key={idx} 
              className="bg-white p-8 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center mb-5">
                <span className="material-symbols-outlined text-navy text-2xl">{iconMap[item.icon] || item.icon}</span>
              </div>
              <h3 className="font-headline text-xl font-bold mb-3 text-navy">{item.title}</h3>
              <p className="text-slate-500 leading-relaxed text-sm">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Obstacles;
