import { Terminal, Github, Code2 } from 'lucide-react';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <nav className="border-b border-white/10 backdrop-blur-md sticky top-0 z-50 bg-slate-900/80">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 text-indigo-400">
            <Terminal size={24} />
            <span className="font-bold text-xl tracking-tight text-white">DevCraft</span>
          </div>
          <div className="flex gap-6 text-sm font-medium text-slate-300">
            <a href="https://github.com/Sarthakk404" target="_blank" rel="noopener noreferrer" className="hover:text-white flex items-center gap-2 transition-colors">
              <Github size={18} />
              GitHub
            </a>
          </div>
        </div>
      </nav>

      <main className="flex-grow">
        {children}
      </main>

      <footer className="border-t border-white/10 py-8 mt-20 bg-slate-950">
        <div className="container mx-auto px-4 text-center text-slate-500">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Code2 size={20} />
            <span className="font-semibold">DevCraft</span>
          </div>
          <p>© {new Date().getFullYear()} AI-Powered Project Generator. Built for developers.</p>
        </div>
      </footer>
    </div>
  );
}
