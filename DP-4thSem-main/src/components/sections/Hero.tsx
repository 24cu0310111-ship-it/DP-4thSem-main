import React from 'react';
import { heroData } from '../../data/mockData';

export interface HeroProps {
  readonly className?: string;
}

export const Hero: React.FC<HeroProps> = ({ className = '' }) => {
  return (
    <header className={`relative pt-28 pb-16 px-8 md:px-12 bg-slate-50 overflow-hidden ${className}`}>
      {/* Subtle background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/40 via-transparent to-cyan/5 pointer-events-none"></div>

      <div className="max-w-[1200px] mx-auto grid lg:grid-cols-2 gap-12 items-start relative z-10">
        {/* Left - Text content */}
        <div className="flex flex-col pt-8">
          {/* Tag pill */}
          <div className="mb-6">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 border border-blue-100 rounded-full text-xs font-semibold text-blue-600 uppercase tracking-wider">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
              {heroData.tagline}
            </span>
          </div>

          {/* Title */}
          <h1 className="font-headline text-[3.5rem] md:text-[4.2rem] font-bold text-navy leading-[1.08] tracking-tight mb-6">
            Smarter<br />
            Complaint<br />
            Management<br />
            <span className="text-blue-600">Starts Here</span>
          </h1>

          {/* Description */}
          <p className="text-base text-slate-500 max-w-[480px] mb-8 leading-relaxed">
            {heroData.description}
          </p>

          {/* Buttons */}
          <div className="flex gap-4 mb-16">
            <button className="bg-blue-600 text-white font-semibold px-8 py-3.5 rounded-xl hover:bg-blue-700 transition-all text-sm shadow-lg shadow-blue-600/20">
              {heroData.primaryCta}
            </button>
            <button className="bg-white text-navy font-semibold px-8 py-3.5 rounded-xl border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all text-sm">
              {heroData.secondaryCta}
            </button>
          </div>

          {/* Stats row */}
          <div className="flex gap-16 border-t border-slate-200 pt-8">
            {heroData.stats.map((stat, idx) => (
              <div key={idx} className="flex flex-col">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">{stat.label}</span>
                <span className="text-3xl font-bold text-navy font-headline">{stat.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right - Chart illustration */}
        <div className="relative flex justify-center lg:justify-end items-start pt-4">
          <div className="w-full max-w-[520px] bg-gradient-to-br from-slate-50 to-white rounded-2xl border border-slate-200/80 shadow-xl shadow-slate-200/50 overflow-hidden">
            {/* Bar chart area */}
            <div className="px-10 pt-12 pb-6 flex items-end justify-center gap-5 h-[320px]">
              <div className="w-12 h-[100px] bg-navy rounded-[4px]"></div>
              <div className="w-12 h-[180px] bg-navy-light rounded-[4px]"></div>
              <div className="w-12 h-[140px] bg-blue-600 rounded-[4px]"></div>
              <div className="w-12 h-[200px] bg-blue-200 rounded-[4px]"></div>
              <div className="w-12 h-[110px] bg-cyan rounded-[4px]"></div>
              <div className="w-12 h-[160px] bg-blue-100 rounded-[4px]"></div>
            </div>

            {/* Health Index pill */}
            <div className="mx-8 mb-8 bg-slate-50 border border-slate-200 rounded-xl p-4 flex justify-between items-center">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Strategic Health Index</span>
              <span className="text-sm font-bold text-success">+12.5%</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Hero;
