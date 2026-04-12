import Navbar from '../components/layout/Navbar';
import Hero from '../components/sections/Hero';
import Obstacles from '../components/sections/Obstacles';
import Protocol from '../components/sections/Protocol';
import Lifecycle from '../components/sections/Lifecycle';
import Capabilities from '../components/sections/Capabilities';
import Dashboard from '../components/sections/Dashboard';
import { Performance, Testimonials, Feedback, Footer } from '../components/sections/RemainingSections';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-surface">
      <Navbar />
      <Hero />
      <Obstacles />
      <Protocol />
      <Lifecycle />
      <Capabilities />
      <Dashboard />
      <Performance />
      <Testimonials />
      <Feedback />
      <Footer />
    </div>
  );
}
