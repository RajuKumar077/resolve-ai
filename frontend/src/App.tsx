
import { Activity, BrainCircuit, Ticket, ShieldCheck } from "lucide-react";

function App() {
  return (
    <main className="min-h-screen bg-[#090d18] p-10 text-white">
      <h1 className="text-4xl font-bold">
        Resolve<span className="text-violet-400">AI</span>
      </h1>

      <p className="mt-3 text-gray-400">
        AI-Powered Customer Support Intelligence Platform
      </p>

      <div className="mt-10 grid grid-cols-1 gap-5 md:grid-cols-4">
        {[
          { name: "Total Tickets", value: "2,486", icon: Ticket },
          { name: "Resolved Tickets", value: "2,104", icon: ShieldCheck },
          { name: "SLA Breaches", value: "38", icon: Activity },
          { name: "AI Insights", value: "156", icon: BrainCircuit },
        ].map((item) => {
          const Icon = item.icon;

          return (
            <div key={item.name} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <Icon className="mb-5 text-violet-400" size={26} />
              <p className="text-sm text-gray-400">{item.name}</p>
              <h2 className="mt-2 text-3xl font-semibold">{item.value}</h2>
            </div>
          );
        })}
      </div>

      <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-8">
        <h2 className="text-xl font-semibold">Welcome to ResolveAI</h2>
        <p className="mt-3 text-gray-400">
          Your customer support intelligence workspace is ready for development.
        </p>
        <div className="mt-6 rounded-xl bg-violet-500/10 p-5 text-violet-300">
          AI Intelligence Engine: Initializing
        </div>
      </div>
    </main>
  );
}

export default App;
