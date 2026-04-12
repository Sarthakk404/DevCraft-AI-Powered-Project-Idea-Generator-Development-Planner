import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Clock, BarChart3, ArrowRight, Loader2, ArrowLeft, Lightbulb, RefreshCw } from 'lucide-react';

const difficultyConfig = {
  beginner: { class: 'badge-beginner', label: 'Beginner', icon: '🌱' },
  intermediate: { class: 'badge-intermediate', label: 'Intermediate', icon: '⚡' },
  advanced: { class: 'badge-advanced', label: 'Advanced', icon: '🔥' },
};

function getDifficultyConfig(difficulty) {
  const key = difficulty?.toLowerCase() || 'intermediate';
  return difficultyConfig[key] || difficultyConfig.intermediate;
}

export default function IdeaPicker({ ideas, onSelect, onBack, isLoading }) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  const handleConfirm = () => {
    if (selectedIndex !== null) {
      onSelect(ideas[selectedIndex]);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-10">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/[0.08] border border-indigo-500/20 text-indigo-300 text-sm font-medium mb-4"
        >
          <Lightbulb size={14} className="text-amber-400" />
          <span>{ideas.length} ideas generated</span>
        </motion.div>
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-3">
          Pick your <span className="gradient-text">project</span>
        </h2>
        <p className="text-slate-400 text-base max-w-lg mx-auto">
          We crafted these ideas based on your profile. Choose the one that excites you most.
        </p>
      </div>

      {/* Ideas Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <AnimatePresence>
          {ideas.map((idea, index) => {
            const isSelected = selectedIndex === index;
            const diff = getDifficultyConfig(idea.difficulty);

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.4 }}
                onClick={() => setSelectedIndex(index)}
                className={`relative cursor-pointer rounded-2xl p-6 transition-all duration-300 group
                  ${isSelected
                    ? 'gradient-border active scale-[1.01]'
                    : 'glass hover:border-white/[0.12]'
                  }
                `}
                style={isSelected ? {
                  boxShadow: '0 0 40px rgba(99, 102, 241, 0.15), 0 0 80px rgba(236, 72, 153, 0.08)'
                } : {}}
              >
                {/* Selection indicator */}
                <AnimatePresence>
                  {isSelected && (
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      exit={{ scale: 0, opacity: 0 }}
                      className="absolute top-4 right-4 w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/30"
                    >
                      <Check size={14} className="text-white" strokeWidth={3} />
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Card number */}
                <div className="absolute top-4 left-4 w-7 h-7 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center text-xs font-bold text-slate-500">
                  {index + 1}
                </div>

                <div className="pt-6 space-y-4">
                  {/* Title */}
                  <h3 className={`text-lg font-bold leading-tight transition-colors ${
                    isSelected ? 'text-white' : 'text-slate-200 group-hover:text-white'
                  }`}>
                    {idea.title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm text-slate-400 leading-relaxed line-clamp-3">
                    {idea.description}
                  </p>

                  {/* Meta */}
                  <div className="flex items-center gap-3 flex-wrap">
                    <span className={`badge ${diff.class}`}>
                      {diff.icon} {diff.label}
                    </span>
                    <span className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                      <Clock size={12} />
                      {idea.estimated_time}
                    </span>
                  </div>

                  {/* Why suitable */}
                  <div className={`text-xs leading-relaxed pt-3 border-t transition-colors ${
                    isSelected
                      ? 'text-indigo-300/80 border-indigo-500/20'
                      : 'text-slate-500 border-white/[0.06]'
                  }`}>
                    💡 {idea.why_suitable}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex flex-col sm:flex-row items-center justify-between gap-4"
      >
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-300 transition-colors font-medium group"
        >
          <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
          Regenerate with different input
        </button>

        <AnimatePresence>
          {selectedIndex !== null && (
            <motion.button
              initial={{ opacity: 0, scale: 0.9, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              onClick={handleConfirm}
              disabled={isLoading}
              className="btn-gradient px-8 py-3.5 rounded-xl text-sm font-bold flex items-center gap-2.5 tracking-wide"
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin" size={18} />
                  Building your plan...
                </>
              ) : (
                <>
                  Build Full Plan
                  <ArrowRight size={18} />
                </>
              )}
            </motion.button>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}
