import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Loader2, Plus, X, Search } from 'lucide-react';

const SKILLS = ["Python", "JavaScript", "React", "FastAPI", "Node.js", "Java", "C++", "SQL", "AWS"];
const INTERESTS = ["AI/ML", "Web Dev", "Mobile", "Blockchain", "DevOps", "Game Dev", "Cybersecurity", "Data Science"];
const GOAL_OPTIONS = [
  { value: "learn", label: "Learn New Tech" },
  { value: "portfolio", label: "Build Portfolio" },
  { value: "startup", label: "Startup Idea" },
  { value: "hackathon", label: "Hackathon" },
];

export default function GeneratorForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    skills: [],
    interests: [],
    experience_level: "intermediate",
    goal: "portfolio",
    custom_goal: "",
    time_available: "1 month",
    preferences: ""
  });
  
  const [customSkill, setCustomSkill] = useState("");
  const [customInterest, setCustomInterest] = useState("");
  const [timeValue, setTimeValue] = useState("1");
  const [timeUnit, setTimeUnit] = useState("Months");

  const toggleSelection = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const addCustomItem = (field, value, setter) => {
    if (value.trim() && !formData[field].includes(value.trim())) {
      setFormData(prev => ({
        ...prev,
        [field]: [...prev[field], value.trim()]
      }));
      setter("");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const finalData = {
      ...formData,
      goal: formData.goal === "other" ? formData.custom_goal : formData.goal,
      time_available: `${timeValue} ${timeUnit}`
    };
    delete finalData.custom_goal;
    onSubmit(finalData);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="glass-panel rounded-3xl p-8 sm:p-12 relative overflow-hidden">
        {/* Ambient Top Glow in Panel */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-32 bg-[#9d4edd] opacity-10 blur-[80px] pointer-events-none" />

        <form onSubmit={handleSubmit} className="relative z-10 space-y-10">
          
          {/* Skills Section */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400">Technical Arsenal</h3>
            <div className="flex flex-wrap gap-2.5">
              {SKILLS.map(skill => (
                <button
                  key={skill}
                  type="button"
                  onClick={() => toggleSelection('skills', skill)}
                  className={`px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${
                    formData.skills.includes(skill)
                      ? 'bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.4)] scale-105'
                      : 'bg-[#12121a] text-slate-400 border border-white/5 hover:border-white/20 hover:text-white'
                  }`}
                >
                  {skill}
                </button>
              ))}
              {formData.skills.filter(s => !SKILLS.includes(s)).map(skill => (
                <button
                  key={skill}
                  type="button"
                  onClick={() => toggleSelection('skills', skill)}
                  className="px-5 py-2.5 rounded-full text-sm font-semibold bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.4)] scale-105 flex items-center gap-2 transition-all"
                >
                  {skill} <X size={14} className="opacity-60 hover:opacity-100" />
                </button>
              ))}
            </div>
            
            <div className="relative mt-2">
              <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
                <Search size={16} className="text-slate-500" />
              </div>
              <input
                type="text"
                placeholder="Search or add custom skills..."
                className="input-premium pl-10"
                value={customSkill}
                onChange={(e) => setCustomSkill(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem('skills', customSkill, setCustomSkill))}
              />
            </div>
          </div>

          {/* Interests Section */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-widest text-[#00f5ff]/70">Target Domains</h3>
            <div className="flex flex-wrap gap-2.5">
              {INTERESTS.map(item => (
                <button
                  key={item}
                  type="button"
                  onClick={() => toggleSelection('interests', item)}
                  className={`px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${
                    formData.interests.includes(item)
                      ? 'bg-[#00f5ff]/10 text-[#00f5ff] border border-[#00f5ff]/40 shadow-[0_0_20px_rgba(0,245,255,0.2)] scale-105'
                      : 'bg-[#12121a] text-slate-400 border border-white/5 hover:border-[#00f5ff]/20 hover:text-[#00f5ff]'
                  }`}
                >
                  {item}
                </button>
              ))}
              {formData.interests.filter(i => !INTERESTS.includes(i)).map(item => (
                <button
                  key={item}
                  type="button"
                  onClick={() => toggleSelection('interests', item)}
                  className="px-5 py-2.5 rounded-full text-sm font-semibold bg-[#00f5ff]/10 text-[#00f5ff] border border-[#00f5ff]/40 shadow-[0_0_20px_rgba(0,245,255,0.2)] scale-105 flex items-center gap-2 transition-all"
                >
                  {item} <X size={14} className="opacity-60 hover:opacity-100" />
                </button>
              ))}
            </div>
            <div className="relative mt-2">
              <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
                <Search size={16} className="text-slate-500" />
              </div>
              <input
                type="text"
                placeholder="Search or add custom domains..."
                className="input-premium pl-10"
                value={customInterest}
                onChange={(e) => setCustomInterest(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem('interests', customInterest, setCustomInterest))}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-4 border-t border-white/5">
            <div className="space-y-3">
              <label className="text-xs font-bold uppercase tracking-widest text-slate-400">Experience Tier</label>
              <select 
                className="input-premium"
                value={formData.experience_level}
                onChange={(e) => setFormData({...formData, experience_level: e.target.value})}
              >
                <option value="beginner">Initiate (Beginner)</option>
                <option value="intermediate">Operative (Intermediate)</option>
                <option value="advanced">Architect (Advanced)</option>
              </select>
            </div>

            <div className="space-y-3">
              <label className="text-xs font-bold uppercase tracking-widest text-slate-400">Primary Objective</label>
              <select 
                className="input-premium"
                value={formData.goal}
                onChange={(e) => setFormData({...formData, goal: e.target.value})}
              >
                {GOAL_OPTIONS.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
                <option value="other">Custom Initialization</option>
              </select>
              
              <AnimatePresence>
                {formData.goal === "other" && (
                  <motion.input
                    initial={{ opacity: 0, height: 0, marginTop: 0 }}
                    animate={{ opacity: 1, height: "auto", marginTop: 12 }}
                    exit={{ opacity: 0, height: 0, marginTop: 0 }}
                    type="text"
                    placeholder="Specify exact custom objective..."
                    className="input-premium"
                    value={formData.custom_goal}
                    onChange={(e) => setFormData({...formData, custom_goal: e.target.value})}
                    required
                  />
                )}
              </AnimatePresence>
            </div>
          </div>
          
          <div className="space-y-3">
             <label className="text-xs font-bold uppercase tracking-widest text-slate-400">Temporal Constraint (Timeboxing)</label>
             <div className="flex gap-4">
                 <select 
                   className="input-premium flex-1"
                   value={timeValue}
                   onChange={(e) => setTimeValue(e.target.value)}
                 >
                   {Array.from({ length: 
                     timeUnit === 'Days' ? 31 : 
                     timeUnit === 'Weeks' ? 12 : 
                     timeUnit === 'Months' ? 24 : 5 
                   }, (_, i) => i + 1).map(num => (
                     <option key={num} value={num}>{num}</option>
                   ))}
                 </select>
                 <select 
                   className="input-premium flex-1"
                   value={timeUnit}
                   onChange={(e) => {
                      setTimeUnit(e.target.value);
                      setTimeValue("1");
                   }}
                 >
                   <option value="Days">Days</option>
                   <option value="Weeks">Weeks</option>
                   <option value="Months">Months</option>
                   <option value="Years">Years</option>
                 </select>
             </div>
          </div>

          <div className="pt-6">
            <button
              type="submit"
              disabled={isLoading || formData.skills.length === 0 || formData.interests.length === 0 || (formData.goal === "other" && !formData.custom_goal)}
              className="btn-magic w-full flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin" size={20} /> SYNTHESIZING...
                </>
              ) : (
                <>
                  INITIALIZE GENERATION <ArrowRight size={20} />
                </>
              )}
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}
