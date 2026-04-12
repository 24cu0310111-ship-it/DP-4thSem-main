export const navigationData = {
  logo: "SCMS",
  links: [
    { label: "Project info", href: "#obstacles", active: true },
    { label: "Team info", href: "#testimonials", active: false }
  ],
  ctaText: "Get Started"
};

export const heroData = {
  tagline: "Intelligent Infrastructure Management",
  titlePart1: "Smarter Complaint Management ",
  titlePart2: "Starts Here",
  description: "Transform how residential and commercial areas handle issues — from electricity and water to sanitation and maintenance. Automated, intelligent, seamless.",
  primaryCta: "Get Started",
  secondaryCta: "View Demo",
  stats: [
    { label: "Efficiency Increase", value: "84%" },
    { label: "Response Time", value: "-12h" },
    { label: "User Satisfaction", value: "4.9/5" }
  ],
  healthIndex: {
    label: "Strategic Health Index",
    value: "+12.5%"
  }
};

export const obstaclesData = {
  tagline: "The Obstacles",
  title: "Fragmented Systems, Silent Users",
  items: [
    {
      icon: "schedule",
      title: "Response Delays",
      description: "Manual logging creates bottlenecks that lead to days of unresolved utility outages."
    },
    {
      icon: "search_off",
      title: "Poor Tracking",
      description: "Users and admins lose track of status updates in a sea of emails and phone calls."
    },
    {
      icon: "inventory",
      title: "Manual Processes",
      description: "Paper trails and Excel sheets make reporting nearly impossible for facility managers."
    }
  ]
};

export const protocolData = {
  tagline: "The Protocol",
  title: "Introducing Smart Complaint Management",
  description: "Our AI-driven engine automatically categorizes incoming complaints using natural language processing, routing them to the correct department within seconds.",
  features: [
    "Neural Ticket Categorization",
    "Dynamic Resource Allocation",
    "Predictive Maintenance Alerts"
  ]
};

export const lifecycleData = {
  tagline: "Operational Flow",
  title: "The Resolution Lifecycle",
  steps: [
    { step: 1, title: "Submit", description: "Instant Logging" },
    { step: 2, title: "Process", description: "AI Analysis" },
    { step: 3, title: "Categorize", description: "Department Tagging" },
    { step: 4, title: "Assign", description: "Technician Dispatch" },
    { step: 5, title: "Resolve", description: "Final Verification" }
  ]
};

export const capabilitiesData = {
  title: "Core Capabilities",
  items: [
    {
      icon: "monitoring",
      title: "Real-time Tracking",
      description: "Visual transparency into every stage of a complaint's journey from submission to completion."
    },
    {
      icon: "psychology",
      title: "Smart Prioritization",
      description: "Urgent utility failures are automatically flagged and bumped to the top of technician queues."
    },
    {
      icon: "space_dashboard",
      title: "User Dashboard",
      description: "A centralized portal for residents to log issues, view history, and provide feedback."
    },
    {
      icon: "admin_panel_settings",
      title: "Admin Control Panel",
      description: "High-level analytics and resource management for facility administrators and municipal leads."
    },
    {
      icon: "notifications_active",
      title: "Notifications",
      description: "Automated SMS and Email alerts keeping all stakeholders informed at critical milestones."
    },
    {
      icon: "api",
      title: "API Integrations",
      description: "Seamlessly connect with existing ERPs, payment gateways, and billing systems."
    }
  ]
};

export const dashboardData = {
  tagline: "The Interface",
  title: "Command Your Infrastructure",
  stats: {
    activeIncidents: 24,
    avgResolutionTime: "2.4h"
  },
  incidents: [
    { id: "#LOG-2940", status: "PENDING", priority: "CRITICAL" },
    { id: "#LOG-2938", status: "ACTIVE", priority: "HIGH" },
    { id: "#LOG-2935", status: "RESOLVED", priority: "MEDIUM" }
  ]
};

export const performanceData = {
  title: "Built for Performance",
  items: [
    {
      tagline: "Frontend Engine",
      title: "React Next.js",
      description: "Edge-optimized responsiveness and real-time UI synchronization."
    },
    {
      tagline: "Backend Intelligence",
      title: "Python & FastAPI",
      description: "Robust AI processing pipelines and high-concurrency complaint handling."
    },
    {
      tagline: "Data Persistence",
      title: "PostgreSQL & Redis",
      description: "ACID-compliant storage paired with ultra-low latency caching."
    }
  ]
};

export const testimonialsData = {
  tagline: "Success Stories",
  title: "Trusted Across Sectors",
  items: [
    {
      quote: "I logged a water leakage at 8 AM and it was fixed by 10 AM. The tracking feature meant I didn't have to keep calling the office.",
      name: "Sarah Chen",
      role: "Resident, Skyview Towers",
      icon: "person"
    },
    {
      quote: "Management overhead has dropped by 40%. We no longer lose complaints in sticky notes or missed emails. Everything is central.",
      name: "Marcus Thorne",
      role: "Manager, Elite Estates",
      icon: "domain"
    },
    {
      quote: "The automated categorization saves hours of manual work. We can prioritize critical utility repairs before they become outages.",
      name: "Elena Rodriguez",
      role: "Facility Admin, Central Mall",
      icon: "engineering"
    }
  ]
};

export const feedbackData = {
  title: "Your Feedback Matters",
  description: "Help us refine the platform to better serve your management needs."
};

export const footerData = {
  logo: "SCMS",
  copyright: "@CopyRights",
  links: ["Privacy", "Terms", "Security", "Status"]
};
