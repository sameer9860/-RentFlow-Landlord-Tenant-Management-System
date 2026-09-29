const features = [
  "Smart rent collection and payment tracking",
  "Tenant lifecycle and occupancy management",
  "Automated invoicing and due-date reminders",
  "Landlord and tenant dashboards in one place",
];

const cards = [
  {
    title: "Property Portfolio Overview",
    description: "Manage every property, unit, and room with a clear overview of occupancy, rent, and maintenance activity.",
    image:
      "https://images.unsplash.com/photo-1460317442991-0ec209397118?w=900&q=80",
  },
  {
    title: "Tenant Management",
    description: "Track tenancy details, agreements, and communication history while keeping each relationship organized.",
    image:
      "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=900&q=80",
  },
  {
    title: "Automated Billing",
    description: "Generate monthly rent invoices, monitor payments, and reduce late-payment delays with alert-driven workflows.",
    image:
      "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=900&q=80",
  },
  {
    title: "Role-Based Access",
    description: "Give landlords and tenants the right tools and visibility through separate, secure experiences.",
    image:
      "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=900&q=80",
  },
];

const faqs = [
  "Is RentFlow free to use?",
  "How do I manage rent collection?",
  "Can I track multiple properties in one dashboard?",
  "Is tenant data secure?",
  "Can I update tenant or property information later?",
];

const footerGroups = {
  Product: [
    { label: "Dashboard", href: "#" },
    { label: "Properties", href: "#" },
    { label: "Invoices", href: "#" },
  ],
  Company: [
    { label: "About Us", href: "#" },
    { label: "Contact", href: "#" },
    { label: "Support", href: "#" },
  ],
  Resources: [
    { label: "FAQs", href: "#faqs" },
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
  ],
};

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <header className="rounded-full border border-slate-200 bg-white/80 px-5 py-3 shadow-sm backdrop-blur-sm">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-cyan-600 text-lg font-bold text-white shadow-lg shadow-sky-500/25">
                R
              </div>
              <div>
                <p className="text-lg font-bold tracking-tight text-slate-900">RentFlow</p>
              </div>
            </div>

            <nav className="hidden items-center gap-7 text-sm font-medium text-slate-600 md:flex">
              <a href="#features" className="transition hover:text-slate-900">Features</a>
              <a href="#solutions" className="transition hover:text-slate-900">Solutions</a>
              <a href="#faqs" className="transition hover:text-slate-900">FAQs</a>
            </nav>

            <div className="flex items-center gap-3">
              <a href="#" className="rounded-full px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100">
                Sign in
              </a>
              <a href="#" className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-slate-900/10 transition hover:bg-slate-800">
                Get started
              </a>
            </div>
          </div>
        </header>

        <section className="relative mt-8 overflow-hidden rounded-[30px] border border-sky-100 bg-gradient-to-br from-sky-50 via-white to-cyan-50 px-6 py-10 shadow-[0_20px_80px_-30px_rgba(14,116,144,0.35)] md:px-10 lg:px-14 lg:py-16">
          <div className="absolute -right-16 top-8 h-64 w-64 rounded-full bg-sky-200/60 blur-3xl" />
          <div className="absolute bottom-0 left-10 h-44 w-44 rounded-full bg-cyan-200/60 blur-3xl" />

          <div className="relative grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
            <div>
              <span className="inline-flex items-center rounded-full border border-sky-200 bg-white px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
                Smarter property management
              </span>
              <h1 className="mt-6 max-w-xl text-4xl font-black tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
                Keep rent, tenants, and property operations in sync.
              </h1>

              <p className="mt-5 max-w-xl text-lg leading-8 text-slate-600">
                RentFlow helps landlords and tenants manage properties, automate invoices, and stay on top of rent collection with a fast, modern workflow.
              </p>

              <div className="mt-8 flex flex-wrap items-center gap-4">
                <a href="#" className="inline-flex items-center justify-center rounded-full bg-sky-600 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-sky-500/30 transition hover:bg-sky-500">
                  Explore Platform
                </a>
                <a href="#" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 text-base font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
                  Create Account
                </a>
              </div>
            </div>

            <div className="relative">
              <div className="overflow-hidden rounded-[28px] border border-slate-200 bg-white p-3 shadow-2xl shadow-slate-200/80">
                <img
                  src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=900&q=80"
                  alt="Modern apartment exterior and property professionals"
                  className="h-[480px] w-full rounded-[20px] object-cover"
                />
              </div>

              <div className="absolute -left-5 bottom-8 w-56 rounded-2xl border border-slate-200 bg-white p-4 shadow-xl shadow-slate-200/60">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Portfolio health</p>
                <div className="mt-2 flex items-end justify-between">
                  <span className="text-3xl font-bold text-slate-900">96%</span>
                  <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-700">+12%</span>
                </div>
                <p className="mt-2 text-sm text-slate-500">On-time rent collection</p>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="mt-20">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-600">Why property managers choose RentFlow</p>
            <h2 className="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Everything you need to manage rental properties with confidence.
            </h2>
          </div>

          <div className="mt-10 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {features.map((feature) => (
              <div key={feature} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                  ✓
                </div>
                <p className="text-base font-medium leading-7 text-slate-700">{feature}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="solutions" className="mt-24">
          <div className="mb-10 text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-600">Everything you need</p>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Built for landlords, tenants, and growing rental businesses.
            </h2>
          </div>

          <div className="grid gap-7 lg:grid-cols-2">
            {cards.map((card, index) => (
              <div
                key={card.title}
                className={`overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-sm ${
                  index % 2 === 0 ? "lg:translate-y-6" : ""
                }`}
              >
                <img src={card.image} alt={card.title} className="h-64 w-full object-cover" />
                <div className="p-6">
                  <h3 className="text-2xl font-bold text-slate-900">{card.title}</h3>
                  <p className="mt-3 text-base leading-7 text-slate-600">{card.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-24 overflow-hidden rounded-[32px] bg-slate-900 px-6 py-10 text-white shadow-2xl shadow-slate-900/10 md:px-10 lg:px-14">
          <div className="grid items-center gap-10 lg:grid-cols-[1fr_0.9fr]">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-300">Ready to simplify operations</p>
              <h2 className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
                Make rent collection easier for everyone.
              </h2>
              <p className="mt-4 max-w-xl text-lg text-slate-300">
                Join RentFlow to manage properties, automate billing, and keep tenants informed without the paperwork hassle.
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
              <a href="#" className="inline-flex items-center justify-center rounded-full bg-sky-500 px-6 py-3 text-base font-semibold text-white transition hover:bg-sky-400">
                Get Started - It&apos;s Free
              </a>
              <a href="#" className="inline-flex items-center justify-center rounded-full border border-slate-700 bg-slate-800 px-6 py-3 text-base font-semibold text-slate-100 transition hover:bg-slate-700">
                Already have an account? Sign in
              </a>
            </div>
          </div>
        </section>

        <section id="faqs" className="mt-24">
          <div className="mb-8 text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-600">FAQs</p>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Frequently asked questions
            </h2>
          </div>

          <div className="mx-auto max-w-4xl space-y-4">
            {faqs.map((question, index) => (
              <details key={question} className="group rounded-2xl border border-slate-200 bg-white px-6 py-4 shadow-sm" open={index === 0}>
                <summary className="cursor-pointer list-none text-lg font-semibold text-slate-900 marker:content-none">
                  {question}
                </summary>
                <p className="mt-3 text-base leading-7 text-slate-600">
                  RentFlow is built to help landlords and tenants manage rental operations clearly, quickly, and securely.
                </p>
              </details>
            ))}
          </div>
        </section>
      </div>

      <footer className="mt-20 border-t border-slate-200 bg-white">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-12 sm:px-6 lg:grid-cols-[1.2fr_0.8fr_0.8fr_0.8fr] lg:px-8">
          <div>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-cyan-600 text-lg font-bold text-white">
                R
              </div>
              <span className="text-2xl font-bold tracking-tight text-slate-900">RentFlow</span>
            </div>
            <p className="mt-4 max-w-sm text-base leading-7 text-slate-600">
              RentFlow streamlines rent collection, tenant communication, and property management for better landlord-tenant relationships.
            </p>
            <div className="mt-5 flex items-center gap-4 text-slate-500">
              <a href="#" aria-label="GitHub" className="hover:text-slate-900">GitHub</a>
              <a href="#" aria-label="Website" className="hover:text-slate-900">Web</a>
              <a href="#" aria-label="LinkedIn" className="hover:text-slate-900">LinkedIn</a>
              <a href="mailto:samirkhatiwada68@gmail.com" aria-label="Email" className="hover:text-slate-900">Email</a>
            </div>
          </div>

          {Object.entries(footerGroups).map(([title, links]) => (
            <div key={title}>
              <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
              <ul className="mt-4 space-y-3 text-slate-600">
                {links.map((link) => (
                  <li key={link.label}>
                    <a href={link.href} className="transition hover:text-slate-900">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-slate-200">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-5 text-sm text-slate-500 sm:px-6 lg:px-8">
            <p>© 2026 RentFlow. All rights reserved.</p>
            <p>
              Developed by <a href="https://samirkhatiwada.com.np/" className="font-medium text-slate-700 hover:text-slate-900">Samir Khatiwada</a>
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
