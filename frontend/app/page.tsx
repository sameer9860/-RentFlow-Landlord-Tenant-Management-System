const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export default async function Home() {
  const summary = await fetchJson<{
    total_properties: number;
    total_rooms: number;
    active_tenancies: number;
    income: number;
    collected: number;
    expenses: number;
    due: number;
    monthly_income: number;
    monthly_expenses: number;
    monthly_due: number;
    net_profit: number;
  }>(`${API_BASE_URL}/dashboard/summary/`).catch(() => ({
    total_properties: 0,
    total_rooms: 0,
    active_tenancies: 0,
    income: 0,
    collected: 0,
    expenses: 0,
    due: 0,
    monthly_income: 0,
    monthly_expenses: 0,
    monthly_due: 0,
    net_profit: 0,
  }));

  const properties = await fetchJson<Array<{ id: number; name: string; address: string }>>(
    `${API_BASE_URL}/properties/`,
  ).catch(() => []);

  const invoices = await fetchJson<Array<{ id: number; tenant_name: string; amount: number; status: string }>>(
    `${API_BASE_URL}/invoices/`,
  ).catch(() => []);

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-900">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="rounded-2xl bg-slate-900 p-6 text-white shadow-sm">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-300">Landlord Management</p>
          <h1 className="mt-3 text-3xl font-bold">Dashboard Overview</h1>
        </header>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {[
            { label: "Properties", value: summary.total_properties },
            { label: "Rooms", value: summary.total_rooms },
            { label: "Active Tenancies", value: summary.active_tenancies },
            { label: "Net Profit", value: `NPR ${summary.net_profit.toFixed(2)}` },
          ].map((item) => (
            <div key={item.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">{item.label}</p>
              <p className="mt-3 text-3xl font-bold">{item.value}</p>
            </div>
          ))}
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="mb-4 text-xl font-semibold">Financial Snapshot</h2>
            <div className="space-y-3 text-sm text-slate-600">
              <div className="flex justify-between"><span>Income</span><strong className="text-slate-900">NPR {summary.income.toFixed(2)}</strong></div>
              <div className="flex justify-between"><span>Collected</span><strong className="text-slate-900">NPR {summary.collected.toFixed(2)}</strong></div>
              <div className="flex justify-between"><span>Expenses</span><strong className="text-slate-900">NPR {summary.expenses.toFixed(2)}</strong></div>
              <div className="flex justify-between"><span>Due</span><strong className="text-slate-900">NPR {summary.due.toFixed(2)}</strong></div>
              <div className="flex justify-between"><span>Monthly Revenue</span><strong className="text-slate-900">NPR {summary.monthly_income.toFixed(2)}</strong></div>
              <div className="flex justify-between"><span>Monthly Expense</span><strong className="text-slate-900">NPR {summary.monthly_expenses.toFixed(2)}</strong></div>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="mb-4 text-xl font-semibold">Properties</h2>
            <div className="space-y-3">
              {properties.length ? properties.slice(0, 5).map((property) => (
                <div key={property.id} className="rounded-xl bg-slate-50 p-3">
                  <p className="font-semibold">{property.name}</p>
                  <p className="text-sm text-slate-500">{property.address}</p>
                </div>
              )) : <p className="text-sm text-slate-500">No property data available yet.</p>}
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">Recent Invoices</h2>
          <div className="overflow-hidden rounded-xl border border-slate-200">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-slate-100 text-slate-700">
                <tr>
                  <th className="px-4 py-3 font-medium">Invoice</th>
                  <th className="px-4 py-3 font-medium">Tenant</th>
                  <th className="px-4 py-3 font-medium">Amount</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {invoices.length ? invoices.slice(0, 6).map((invoice) => (
                  <tr key={invoice.id} className="border-t border-slate-200">
                    <td className="px-4 py-3">#{invoice.id}</td>
                    <td className="px-4 py-3">{invoice.tenant_name}</td>
                    <td className="px-4 py-3">NPR {Number(invoice.amount).toFixed(2)}</td>
                    <td className="px-4 py-3">
                      <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-medium text-amber-700">
                        {invoice.status}
                      </span>
                    </td>
                  </tr>
                )) : <tr><td colSpan={4} className="px-4 py-6 text-center text-slate-500">No invoices found.</td></tr>}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}
