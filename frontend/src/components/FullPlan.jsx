import { motion } from 'framer-motion';
import { CheckCircle2, Layers, Cpu, Map, BookOpen, ExternalLink, ArrowRight } from 'lucide-react';

export default function FullPlan({ plan }) {
  if (!plan) return null;

  const { idea, features, tech_stack, roadmap, learning_path } = plan;

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-12 pb-20"
    >
      {/* Header */}
      <motion.div variants={item} className="text-center space-y-4">
        <div className="inline-block px-4 py-1 rounded-full bg-green-500/10 text-green-400 text-sm font-medium border border-green-500/20">
          {idea.difficulty} • {idea.estimated_time}
        </div>
        <h2 className="text-4xl font-bold">{idea.title}</h2>
        <p className="text-xl text-slate-400 max-w-3xl mx-auto">{idea.description}</p>
      </motion.div>

      {/* Features Grid */}
      <motion.div variants={item} className="grid md:grid-cols-2 gap-8">
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center gap-3 text-indigo-400 mb-4">
            <Layers size={24} />
            <h3 className="text-xl font-bold">Core Features (MVP)</h3>
          </div>
          <ul className="space-y-4">
            {features.core_features.map((feature, idx) => (
              <li key={idx} className="flex gap-3">
                <CheckCircle2 className="text-indigo-500 shrink-0 mt-1" size={18} />
                <div>
                  <div className="font-semibold text-slate-200">{feature.name}</div>
                  <div className="text-sm text-slate-400">{feature.description}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center gap-3 text-pink-400 mb-4">
             <Layers size={24} />
            <h3 className="text-xl font-bold">Nice to Have</h3>
          </div>
          <ul className="space-y-4">
            {features.nice_to_have.map((feature, idx) => (
              <li key={idx} className="flex gap-3">
                <div className="w-5 h-5 rounded-full border border-pink-500/30 shrink-0 mt-1" />
                <div>
                  <div className="font-semibold text-slate-200">{feature.name}</div>
                  <div className="text-sm text-slate-400">{feature.description}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </motion.div>

      {/* Tech Stack */}
      <motion.div variants={item} className="glass-panel p-8 rounded-3xl">
        <div className="flex items-center gap-3 text-blue-400 mb-8">
          <Cpu size={24} />
          <h3 className="text-xl font-bold">Recommended Tech Stack</h3>
        </div>
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { label: 'Frontend', items: tech_stack.frontend },
            { label: 'Backend', items: tech_stack.backend },
            { label: 'Database', items: tech_stack.database },
            { label: 'Tools', items: tech_stack.tools }
          ].map((stack) => (
            <div key={stack.label} className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
              <div className="text-sm text-slate-500 uppercase tracking-widest font-semibold mb-3">{stack.label}</div>
              <div className="flex flex-wrap gap-2">
                {stack.items.map(tech => (
                  <span key={tech} className="px-3 py-1 bg-slate-800 rounded-md text-sm text-slate-300 border border-slate-700">
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
        {tech_stack.reasoning && (
           <p className="mt-6 text-slate-400 text-sm border-t border-slate-800 pt-4">
             💡 {tech_stack.reasoning}
           </p>
        )}
      </motion.div>

      {/* Roadmap */}
      <motion.div variants={item} className="space-y-6">
        <div className="flex items-center gap-3 text-indigo-400">
          <Map size={24} />
          <h3 className="text-xl font-bold">Development Roadmap</h3>
        </div>
        <div className="space-y-4">
          {roadmap.phases.map((phase, idx) => (
             <div key={idx} className="relative pl-8 border-l-2 border-slate-800 pb-8 last:pb-0">
               <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-slate-900 border-2 border-indigo-500" />
               <div className="glass-panel p-6 rounded-2xl">
                 <div className="flex justify-between items-start mb-4">
                   <h4 className="text-lg font-bold text-white">Phase {phase.phase_number}: {phase.title}</h4>
                   <span className="text-sm font-mono text-indigo-300 bg-indigo-500/10 px-3 py-1 rounded-full">{phase.duration}</span>
                 </div>
                 <div className="grid md:grid-cols-2 gap-8">
                   <div>
                     <div className="text-sm font-semibold text-slate-500 mb-2">Key Tasks</div>
                     <ul className="list-disc list-inside space-y-1 text-slate-300">
                       {phase.tasks.map((task, i) => <li key={i}>{task}</li>)}
                     </ul>
                   </div>
                   <div>
                     <div className="text-sm font-semibold text-slate-500 mb-2">Deliverables</div>
                     <ul className="space-y-1 text-slate-300">
                       {phase.deliverables.map((d, i) => (
                         <li key={i} className="flex items-center gap-2">
                           <CheckCircle2 size={14} className="text-green-500" /> {d}
                         </li>
                       ))}
                     </ul>
                   </div>
                 </div>
               </div>
             </div>
          ))}
        </div>
      </motion.div>

       {/* Learning Path */}
      {learning_path.new_technologies.length > 0 && (
        <motion.div variants={item} className="glass-panel p-8 rounded-3xl bg-gradient-to-br from-[#9d4edd]/10 to-[#00f5ff]/10">
          <div className="flex items-center gap-3 text-purple-400 mb-6">
            <BookOpen size={24} />
            <h3 className="text-xl font-bold">Learning Requirements</h3>
          </div>
          <div className="grid gap-6">
            {learning_path.resources.map((resource, idx) => (
              <a 
                key={idx} 
                href={resource.url || "#"} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg hover:bg-slate-800 transition-colors group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 font-bold text-lg">
                    {idx + 1}
                  </div>
                  <div>
                    <div className="font-semibold text-white group-hover:text-purple-300 transition-colors">{resource.title}</div>
                    <div className="text-sm text-slate-400 flex gap-2">
                      <span className="uppercase text-xs font-bold bg-slate-800 px-2 py-0.5 rounded text-slate-500">{resource.resource_type}</span>
                      <span>{resource.topic}</span>
                    </div>
                  </div>
                </div>
                <ExternalLink size={18} className="text-slate-600 group-hover:text-white transition-colors" />
              </a>
            ))}
          </div>
        </motion.div>
      )}

    </motion.div>
  );
}
