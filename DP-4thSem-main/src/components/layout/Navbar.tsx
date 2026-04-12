import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { navigationData } from '../../data/mockData';

export interface NavbarProps {
  readonly className?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ className = '' }) => {
  const [activeLink, setActiveLink] = useState<string>(navigationData.links[0].href);
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);

      const sections = navigationData.links
        .map(link => link.href.replace('#', ''))
        .filter(id => id);

      for (let i = sections.length - 1; i >= 0; i--) {
        const el = document.getElementById(sections[i]);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 120) {
            setActiveLink(`#${sections[i]}`);
            return;
          }
        }
      }
      setActiveLink(navigationData.links[0].href);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault();
    const targetId = href.replace('#', '');
    const el = document.getElementById(targetId);
    if (el) {
      const offsetTop = el.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: offsetTop, behavior: 'smooth' });
    }
    setActiveLink(href);
    setMobileOpen(false);
  };

  return (
    <>
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled
          ? 'glass border-b border-outline-variant/10'
          : 'bg-surface/80 backdrop-blur-md border-b border-outline-variant/5'
      } ${className}`}>
        <div className="flex justify-between items-center px-6 md:px-12 py-4 max-w-[1200px] mx-auto w-full">
          {/* Logo */}
          <a
            href="#"
            onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            className="flex items-center gap-2.5"
          >
            <span className="w-8 h-8 gradient-primary rounded-obsidian flex items-center justify-center text-on-primary text-xs font-bold font-headline">S</span>
            <span className="text-xl font-bold tracking-tight text-on-surface font-headline">{navigationData.logo}</span>
          </a>

          {/* Center links — desktop */}
          <div className="hidden md:flex gap-8 items-center">
            {navigationData.links.map((link, idx) => (
              <a
                key={idx}
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href)}
                className={`font-medium text-sm transition-all duration-200 ${
                  activeLink === link.href
                    ? 'text-primary-container'
                    : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                {link.label}
              </a>
            ))}
          </div>

          <div className="flex items-center gap-3">
            {/* CTA Button */}
            <button
              onClick={() => navigate('/login')}
              className="gradient-primary text-on-primary px-6 py-2.5 rounded-full text-sm font-semibold font-label uppercase tracking-wider transition-all duration-200 hover:scale-[1.02] hover:shadow-primary-glow"
            >
              {navigationData.ctaText}
            </button>

            {/* Mobile hamburger */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 text-on-surface-variant hover:text-on-surface rounded-obsidian hover:bg-surface-container transition-all"
            >
              <span className="material-symbols-outlined">{mobileOpen ? 'close' : 'menu'}</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-40 pt-[72px]">
          <div className="absolute inset-0 bg-black/60" onClick={() => setMobileOpen(false)} />
          <div className="relative bg-surface-container-low border-b border-outline-variant/10 p-6 space-y-1">
            {navigationData.links.map((link, idx) => (
              <a
                key={idx}
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href)}
                className={`block px-4 py-3 rounded-obsidian text-sm font-body transition-all ${
                  activeLink === link.href
                    ? 'bg-primary-container/15 text-primary-container'
                    : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
                }`}
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;
