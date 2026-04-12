import { motion } from 'framer-motion';
import { Cpu } from 'lucide-react';

export default function Hero() {
  return (
    <div className="relative py-20 sm:py-32 flex flex-col items-center justify-center text-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10"
      >
        <div className="flex justify-center mb-10">
          <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl">
            <Cpu size={16} className="text-[#00f5ff]" />
            <span className="text-xs uppercase tracking-widest text-[#8b8d98] font-bold">Neural Core: Groq Llama 3.3</span>
          </div>
        </div>
        
        <h1 className="text-6xl sm:text-8xl font-black mb-8 text-cinematic tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-white/40 drop-shadow-2xl">
          Engineer the <br />
          <span className="gradient-text">Impossible.</span>
        </h1>
        
        <p className="text-xl sm:text-2xl text-[#8b8d98] max-w-2xl mx-auto mb-10 font-medium leading-relaxed">
          The ultimate intelligent architect. DevCraft calculates your optimal project vector and generates production-ready engineering blueprints instantly.
        </p>
      </motion.div>
    </div>
  );
}
