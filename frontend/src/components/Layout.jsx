import { Terminal, Github, Code2 } from 'lucide-react';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col relative z-10">
      {/* Floating Pill Navbar */}
      <div className="pt-6 px-4">
        <nav className="glass-panel mx-auto max-w-5xl rounded-full sticky top-6 z-50">
          <div className="px-6 h-14 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center border border-white/10">
                <Terminal size={16} className="text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight text-white mb-0.5">DevCraft</span>
            </div>
            
            <div className="flex gap-6 text-sm font-medium text-slate-400">
              <a href="https://github.com/Sarthakk404" target="_blank" rel="noopener noreferrer" className="hover:text-white flex items-center gap-2 transition-colors">
                <Github size={16} />
                <span className="hidden sm:inline">GitHub</span>
              </a>
            </div>
          </div>
        </nav>
      </div>

      <main className="flex-grow pt-10">
        {children}
      </main>

      {/* Ultra Minimal Footer */}
      <footer className="py-12 mt-20 border-t border-white/5 bg-transparent">
        <div className="container mx-auto px-4 text-center text-slate-600 flex flex-col items-center justify-center gap-3">
          <Code2 size={24} className="opacity-50" />
          <p className="text-xs uppercase tracking-[0.2em] font-semibold">Intelligence Engineered.</p>
        </div>
      </footer>
    </div>
  );
}
