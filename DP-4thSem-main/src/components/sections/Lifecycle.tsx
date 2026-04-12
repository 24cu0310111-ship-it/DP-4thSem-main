import React from 'react';
import { lifecycleData } from '../../data/mockData';

export interface LifecycleProps {
  readonly className?: string;
}

export const Lifecycle: React.FC<LifecycleProps> = ({ className = '' }) => {
  return (
    <section id="lifecycle" className={`py-28 px-8 md:px-12 bg-navy text-white ${className}`}>
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-20">
          <span className="text-xs font-bold text-cyan uppercase tracking-[0.2em]">{lifecycleData.tagline}</span>
          <h2 className="font-headline text-3xl md:text-4xl font-bold mt-3 text-white">{lifecycleData.title}</h2>
        </div>
        
        <div className="relative">
          {/* Connector line */}
          <div className="hidden md:block absolute top-14 left-[10%] right-[10%] h-[1px] bg-slate-600"></div>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 relative z-10">
            {lifecycleData.steps.map((step, idx) => (
              <div key={idx} className="text-center group">
                <div className="w-[72px] h-[72px] rounded-xl bg-navy-light border border-slate-600 text-white flex items-center justify-center mx-auto mb-6 group-hover:bg-cyan group-hover:text-navy group-hover:border-cyan transition-all duration-300 text-2xl font-headline font-bold">
                  {step.step}
                </div>
                <h4 className="font-headline font-bold text-base mb-1">{step.title}</h4>
                <p className="text-xs text-slate-400">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Lifecycle;
