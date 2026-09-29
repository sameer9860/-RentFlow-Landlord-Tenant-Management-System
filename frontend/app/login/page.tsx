import Link from "next/link";

export default function LoginPage() {
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
              <Link href="/register" className="rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-slate-800">
                Create account
              </Link>
            </div>
          </div>
        </header>

        <section className="mx-auto grid max-w-6xl gap-8 py-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-16">
          <div className="hidden overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-sm lg:block">
            <img
              src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1200&q=80"
              alt="Apartment property"
              className="h-full min-h-[620px] w-full object-cover"
            />
          </div>

          <div className="rounded-[24px] border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
            <div className="mb-8">
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-sky-600">Welcome back</p>
              <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">Sign in to RentFlow</h1>
              <p className="mt-2 text-sm text-slate-600">Manage properties, payments, and tenant activity from one place.</p>
            </div>

            <form className="space-y-5">
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
                <div className="mb-1.5 flex items-center justify-between">
                  <label htmlFor="password" className="text-sm font-medium text-slate-700">
                    Password
                  </label>
                  <Link href="#" className="text-xs font-medium text-sky-600 transition hover:text-sky-700">
                    Forgot password?
                  </Link>
                </div>
                <input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  className="w-full rounded-md border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:bg-white"
                />
              </div>

              <div className="flex items-center justify-between gap-3 text-sm text-slate-600">
                <label className="flex items-center gap-2">
                  <input type="checkbox" className="h-4 w-4 rounded border-slate-300 text-sky-600 focus:ring-sky-500" />
                  Remember me
                </label>
                <Link href="/register" className="font-medium text-sky-600 hover:text-sky-700">
                  Need an account?
                </Link>
              </div>

              <button
                type="submit"
                className="w-full rounded-md bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800"
              >
                Sign in
              </button>
            </form>

            <div className="mt-6 border-t border-slate-200 pt-5 text-center text-sm text-slate-600">
              Don’t have an account? <Link href="/register" className="font-semibold text-sky-600 hover:text-sky-700">Create one</Link>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
