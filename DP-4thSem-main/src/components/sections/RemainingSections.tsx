import React from 'react';
import { 
  performanceData, 
  testimonialsData, 
  feedbackData,
  footerData
} from '../../data/mockData';

// PERFORMANCE COMPONENT
export interface PerformanceProps {
  readonly className?: string;
}
export const Performance: React.FC<PerformanceProps> = ({ className = '' }) => (
  <section id="performance" className={`py-28 px-8 md:px-12 bg-slate-50 ${className}`}>
    <div className="max-w-[1200px] mx-auto">
      <div className="text-center mb-16">
        <h2 className="font-headline text-3xl md:text-4xl font-bold text-navy">{performanceData.title}</h2>
      </div>
      <div className="grid md:grid-cols-3 gap-6">
        {performanceData.items.map((item, idx) => (
          <div key={idx} className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden hover:shadow-md hover:-translate-y-1 transition-all duration-300">
            {/* Blue top bar */}
            <div className="h-1.5 bg-blue-600"></div>
            <div className="p-8 text-center">
              <span className="text-xs font-bold text-blue-600 uppercase tracking-[0.15em]">{item.tagline}</span>
              <p className="font-headline text-xl font-bold text-navy mt-2 mb-3">{item.title}</p>
              <p className="text-sm text-slate-500 leading-relaxed">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

// TESTIMONIALS COMPONENT
export interface TestimonialsProps {
  readonly className?: string;
}
export const Testimonials: React.FC<TestimonialsProps> = ({ className = '' }) => (
  <section id="testimonials" className={`py-28 px-8 md:px-12 bg-white ${className}`}>
    <div className="max-w-[1200px] mx-auto">
      <div className="text-center mb-16">
        <span className="text-xs font-bold text-blue-600 uppercase tracking-[0.2em]">{testimonialsData.tagline}</span>
        <h2 className="font-headline text-3xl md:text-4xl font-bold mt-3 text-navy">{testimonialsData.title}</h2>
      </div>
      <div className="grid md:grid-cols-3 gap-6">
        {testimonialsData.items.map((testimonial, idx) => (
          <div key={idx} className="bg-white p-8 rounded-2xl border border-slate-200/80 shadow-sm relative hover:-translate-y-1 transition-transform duration-300">
            <span className="material-symbols-outlined text-slate-100 text-6xl absolute top-4 right-4 select-none pointer-events-none">format_quote</span>
            <p className="text-navy text-sm leading-relaxed mb-8 relative z-10">{`"${testimonial.quote}"`}</p>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-navy flex items-center justify-center text-white">
                <span className="material-symbols-outlined text-sm">{testimonial.icon}</span>
              </div>
              <div>
                <p className="font-bold text-sm text-navy">{testimonial.name}</p>
                <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">{testimonial.role}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
);

// FEEDBACK FORM COMPONENT
export interface FeedbackProps {
  readonly className?: string;
}
export const Feedback: React.FC<FeedbackProps> = ({ className = '' }) => {
  const [submitted, setSubmitted] = React.useState(false);
  const [rating, setRating] = React.useState(4);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <section id="feedback" className={`py-28 px-8 md:px-12 bg-slate-50 ${className}`}>
      <div className="max-w-[700px] mx-auto">
        <div className="text-center mb-10">
          <h2 className="font-headline text-3xl md:text-4xl font-bold text-navy">{feedbackData.title}</h2>
          <p className="mt-3 text-slate-500 text-sm">{feedbackData.description}</p>
        </div>
        
        <div className="relative">
          <form 
            onSubmit={handleSubmit}
            className={`bg-white border border-slate-200 p-8 md:p-10 rounded-2xl shadow-sm transition-all duration-500 ${
              submitted ? 'opacity-0 scale-95 pointer-events-none' : 'opacity-100 scale-100'
            }`}
          >
            {/* Star rating */}
            <div className="flex flex-col items-center mb-10">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-4">Overall Satisfaction</label>
              <div className="flex gap-1.5">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button 
                    key={star} 
                    type="button"
                    onClick={() => setRating(star)}
                    className={`material-symbols-outlined text-3xl transition-colors ${
                      star <= rating ? 'text-cyan' : 'text-slate-200'
                    }`}
                    style={star <= rating ? { fontVariationSettings: "'FILL' 1" } : {}}
                  >
                    star
                  </button>
                ))}
              </div>
            </div>
            
            {/* Form fields */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 block">Full Name</label>
                <input required type="text" placeholder="John Doe" className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder:text-slate-300" />
              </div>
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 block">Email Address</label>
                <input required type="email" placeholder="john@example.com" className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder:text-slate-300" />
              </div>
            </div>
            
            <div className="mb-8">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 block">How can we improve?</label>
              <textarea required placeholder="Tell us about your experience and suggestions..." className="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 h-32 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none placeholder:text-slate-300"></textarea>
            </div>
            
            <button type="submit" className="w-full bg-blue-600 text-white font-semibold py-4 rounded-xl hover:bg-blue-700 transition-all text-sm shadow-lg shadow-blue-600/20">
              Submit Feedback
            </button>
          </form>

          {/* Success State */}
          {submitted && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-12 bg-white rounded-2xl border border-slate-200 shadow-sm">
              <div className="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mb-5">
                <span className="material-symbols-outlined text-success text-4xl" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              </div>
              <h3 className="font-headline text-2xl font-bold text-navy mb-3">Thank You!</h3>
              <p className="text-slate-500 text-sm max-w-sm">Thank you for your feedback! We appreciate your help in making SCMS better.</p>
              <button 
                type="button"
                onClick={() => setSubmitted(false)}
                className="mt-6 text-blue-600 font-semibold text-sm hover:underline"
              >
                Submit another response
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

// FOOTER COMPONENT
export interface FooterProps {
  readonly className?: string;
}
export const Footer: React.FC<FooterProps> = ({ className = '' }) => (
  <footer className={`bg-navy text-white ${className}`}>
    <div className="flex flex-col md:flex-row justify-between items-center px-8 md:px-12 py-10 max-w-[1200px] mx-auto">
      <div className="flex flex-col items-center md:items-start mb-6 md:mb-0">
        <div className="text-xl font-bold text-white font-headline mb-1">{footerData.logo}</div>
        <p className="text-xs text-slate-400">{footerData.copyright}</p>
      </div>
      <div className="flex gap-8">
        {footerData.links.map((link, idx) => (
          <a key={idx} href="#" className="text-[10px] font-bold text-slate-400 uppercase tracking-wider hover:text-white transition-colors">
            {link}
          </a>
        ))}
      </div>
    </div>
  </footer>
);

export default { Performance, Testimonials, Feedback, Footer };
