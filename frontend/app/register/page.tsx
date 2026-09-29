import Link from "next/link";

export default function RegisterPage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto w-full max-w-7xl px-3 py-4 sm:px-5 lg:px-6">
        <header className="w-full border-b border-slate-200 bg-white/90 px-3 py-2.5 backdrop-blur-sm">
          <div className="flex items-center justify-between gap-3">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-sky-500 to-cyan-600 text-sm font-bold text-white shadow-sm shadow-sky-500/20">
                R
              </div>
              <div>
                <p className="text-base font-bold tracking-tight text-slate-900">RentFlow</p>
              </div>
            </Link>

            <nav className="hidden items-center gap-5 text-[10px] font-medium uppercase tracking-[0.12em] text-slate-600 md:flex">
              <Link href="/" className="transition hover:text-slate-900">Home</Link>
              <Link href="/#features" className="transition hover:text-slate-900">Features</Link>
              <Link href="/#faqs" className="transition hover:text-slate-900">FAQs</Link>
            </nav>

            <div className="flex items-center gap-2">
              <Link href="/login" className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-50">
                Sign in
              </Link>
            </div>
          </div>
        </header>

        <section className="mx-auto grid max-w-6xl gap-8 py-10 lg:grid-cols-[0.95fr_1.05fr] lg:items-center lg:py-16">
          <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
            <div className="mb-8">
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-sky-600">Get started</p>
              <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">Create your account</h1>
              <p className="mt-2 text-sm text-slate-600">Start managing your rental portfolio and tenant relationships with confidence.</p>
            </div>

            <form className="space-y-5">
              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="firstName" className="mb-1.5 block text-sm font-medium text-slate-700">
                    First name
                  </label>
                  <input
                    id="firstName"
                    type="text"
                    placeholder="Samir"
                    className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                  />
                </div>

                <div>
                  <label htmlFor="lastName" className="mb-1.5 block text-sm font-medium text-slate-700">
                    Last name
                  </label>
                  <input
                    id="lastName"
                    type="text"
                    placeholder="Khatiwada"
                    className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="role" className="mb-1.5 block text-sm font-medium text-slate-700">
                  Account type
                </label>
                <select
                  id="role"
                  className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                  defaultValue="landlord"
                >
                  <option value="landlord">Landlord</option>
                  <option value="tenant">Tenant</option>
                  <option value="manager">Property Manager</option>
                </select>
              </div>

              <div>
                <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-slate-700">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                />
              </div>

              <div>
                <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-slate-700">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  placeholder="Create a password"
                  className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                />
              </div>

              <div>
                <label htmlFor="confirmPassword" className="mb-1.5 block text-sm font-medium text-slate-700">
                  Confirm password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm your password"
                  className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                />
              </div>

              <button
                type="submit"
                className="w-full rounded-md bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800"
              >
                Create account
              </button>
            </form>

            <div className="mt-6 border-t border-slate-200 pt-5 text-center text-sm text-slate-600">
              Already have an account? <Link href="/login" className="font-semibold text-sky-600 hover:text-sky-700">Sign in</Link>
            </div>
          </div>

          <div className="hidden overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-sm lg:block">
            <img
              src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&q=80"
              alt="Team planning property management"
              className="h-full min-h-[720px] w-full object-cover"
            />
          </div>
        </section>
      </div>
    </main>
  );
}
