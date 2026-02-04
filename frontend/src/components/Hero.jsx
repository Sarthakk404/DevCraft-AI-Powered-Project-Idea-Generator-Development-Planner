import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

export default function Hero() {
  return (
    <div className="relative overflow-hidden py-20 sm:py-32">
      <div className="container mx-auto px-4 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-medium mb-8">
            <Sparkles size={16} />
            <span>Powered by Google Gemini AI</span>
          </div>
          
          <h1 className="text-5xl sm:text-7xl font-bold mb-6 tracking-tight">
            Build your next <span className="gradient-text">masterpiece</span>
          </h1>
          
          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10">
            Stop searching for ideas. DevCraft generates personalized project plans, 
            tech stacks, and roadmaps tailored to your skills and goals.
          </p>
        </motion.div>
      </div>
      
      {/* Background glow effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-600/20 rounded-full blur-3xl -z-10" />
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-pink-600/10 rounded-full blur-3xl -z-10" />
    </div>
  );
}
