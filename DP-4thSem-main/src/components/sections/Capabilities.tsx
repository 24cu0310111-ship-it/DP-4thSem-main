import React from 'react';
import { capabilitiesData } from '../../data/mockData';

export interface CapabilitiesProps {
  readonly className?: string;
}

export const Capabilities: React.FC<CapabilitiesProps> = ({ className = '' }) => {
  return (
    <section id="capabilities" className={`py-28 px-8 md:px-12 bg-slate-50 ${className}`}>
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-16">
          <h2 className="font-headline text-3xl md:text-4xl font-bold text-navy">{capabilitiesData.title}</h2>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6">
          {capabilitiesData.items.map((item, idx) => (
            <div 
              key={idx} 
              className="bg-white p-8 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-5">
                <span className="material-symbols-outlined text-blue-600 text-2xl">{item.icon}</span>
              </div>
              <h3 className="font-headline text-lg font-bold mb-2 text-navy">{item.title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Capabilities;
