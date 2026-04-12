import React from 'react';
import { protocolData } from '../../data/mockData';

export interface ProtocolProps {
  readonly className?: string;
}

export const Protocol: React.FC<ProtocolProps> = ({ className = '' }) => {
  return (
    <section id="protocol" className={`py-28 px-8 md:px-12 bg-white ${className}`}>
      <div className="max-w-[1200px] mx-auto grid md:grid-cols-2 gap-16 items-center">
        {/* Left - Text */}
        <div>
          <span className="text-xs font-bold text-blue-600 uppercase tracking-[0.2em]">{protocolData.tagline}</span>
          <h2 className="font-headline text-3xl md:text-[2.8rem] font-bold mt-4 mb-6 text-navy leading-tight">{protocolData.title}</h2>
          <p className="text-slate-500 leading-relaxed mb-8">
            {protocolData.description}
          </p>
          <ul className="space-y-4">
            {protocolData.features.map((feature, idx) => (
              <li key={idx} className="flex items-center gap-3 text-navy font-medium text-sm">
                <span className="material-symbols-outlined text-blue-600 text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Right - Dark AI illustration */}
        <div className="flex justify-center">
          <div className="w-full max-w-[460px] aspect-square bg-navy rounded-2xl overflow-hidden relative flex items-center justify-center shadow-2xl shadow-navy/20">
            {/* Orbital rings */}
            <div className="absolute w-52 h-52 border border-cyan/20 rounded-full animate-spin-slow"></div>
            <div className="absolute w-72 h-72 border border-cyan/10 rounded-full animate-spin-slower"></div>
            
            {/* Center icon */}
            <div className="text-center z-10">
              <span className="material-symbols-outlined text-cyan text-5xl block mb-2">hub</span>
              <p className="text-[10px] text-cyan tracking-[0.25em] uppercase font-semibold">AI Core Active</p>
            </div>

            {/* Floating dots */}
            <div className="absolute top-[15%] right-[20%] w-2.5 h-2.5 bg-cyan rounded-full shadow-[0_0_12px_rgba(34,211,238,0.6)] animate-pulse-slow"></div>
            <div className="absolute bottom-[20%] left-[15%] w-1.5 h-1.5 bg-blue-400 rounded-full shadow-[0_0_8px_rgba(59,130,246,0.5)] animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
            <div className="absolute bottom-[35%] left-[18%] w-1 h-1 bg-cyan/60 rounded-full"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Protocol;
