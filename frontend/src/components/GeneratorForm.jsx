import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Loader2, Plus, X } from 'lucide-react';

const SKILLS = ["Python", "JavaScript", "React", "FastAPI", "Node.js", "Java", "C++", "SQL", "Docker", "AWS"];
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
    // Remove temporary field before submitting
    delete finalData.custom_goal;
    
    onSubmit(finalData);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="max-w-2xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl"
    >
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Skills */}
        <div className="space-y-3">
          <label className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Your Skills</label>
          <div className="flex flex-wrap gap-2 mb-3">
            {SKILLS.map(skill => (
              <button
                key={skill}
                type="button"
                onClick={() => toggleSelection('skills', skill)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  formData.skills.includes(skill)
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
              >
                {skill}
              </button>
            ))}
            {/* Display custom added skills */}
            {formData.skills.filter(s => !SKILLS.includes(s)).map(skill => (
              <button
                key={skill}
                type="button"
                onClick={() => toggleSelection('skills', skill)}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-all bg-indigo-600 text-white shadow-lg shadow-indigo-500/30 flex items-center gap-2"
              >
                {skill} <X size={14} />
              </button>
            ))}
          </div>
          {/* Custom Skill Input */}
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Add custom skill..."
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={customSkill}
              onChange={(e) => setCustomSkill(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem('skills', customSkill, setCustomSkill))}
            />
            <button
              type="button"
              onClick={() => addCustomItem('skills', customSkill, setCustomSkill)}
              className="bg-slate-700 hover:bg-slate-600 text-white p-2 rounded-lg transition-colors"
            >
              <Plus size={20} />
            </button>
          </div>
        </div>

        {/* Interests */}
        <div className="space-y-3">
          <label className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Interests</label>
          <div className="flex flex-wrap gap-2 mb-3">
            {INTERESTS.map(item => (
              <button
                key={item}
                type="button"
                onClick={() => toggleSelection('interests', item)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  formData.interests.includes(item)
                    ? 'bg-pink-600 text-white shadow-lg shadow-pink-500/30'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
              >
                {item}
              </button>
            ))}
             {/* Display custom added interests */}
             {formData.interests.filter(i => !INTERESTS.includes(i)).map(item => (
              <button
                key={item}
                type="button"
                onClick={() => toggleSelection('interests', item)}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-all bg-pink-600 text-white shadow-lg shadow-pink-500/30 flex items-center gap-2"
              >
                {item} <X size={14} />
              </button>
            ))}
          </div>
          {/* Custom Interest Input */}
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Add custom interest..."
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-pink-500"
              value={customInterest}
              onChange={(e) => setCustomInterest(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomItem('interests', customInterest, setCustomInterest))}
            />
            <button
              type="button"
              onClick={() => addCustomItem('interests', customInterest, setCustomInterest)}
              className="bg-slate-700 hover:bg-slate-600 text-white p-2 rounded-lg transition-colors"
            >
              <Plus size={20} />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-300">Experience Level</label>
            <select 
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-white"
              value={formData.experience_level}
              onChange={(e) => setFormData({...formData, experience_level: e.target.value})}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-300">Goal</label>
            <select 
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-white"
              value={formData.goal}
              onChange={(e) => setFormData({...formData, goal: e.target.value})}
            >
              {GOAL_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
              <option value="other">Other (Custom)</option>
            </select>
            
            {formData.goal === "other" && (
              <motion.input
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                type="text"
                placeholder="Describe your goal..."
                className="w-full mt-2 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-white"
                value={formData.custom_goal}
                onChange={(e) => setFormData({...formData, custom_goal: e.target.value})}
                required
              />
            )}
          </div>
        </div>
        
        <div className="space-y-2">
           <label className="text-sm font-semibold text-slate-300">Time Available</label>
           <div className="flex gap-4">
             <div className="flex-1">
               <select 
                 className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-white"
                 value={timeValue}
                 onChange={(e) => setTimeValue(e.target.value)}
               >
                 {/* Generate options based on unit */}
                 {Array.from({ length: 
                   timeUnit === 'Days' ? 31 : 
                   timeUnit === 'Weeks' ? 12 : 
                   timeUnit === 'Months' ? 24 : 
                   5 
                 }, (_, i) => i + 1).map(num => (
                   <option key={num} value={num}>{num}</option>
                 ))}
               </select>
             </div>
             <div className="flex-1">
               <select 
                 className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-white"
                 value={timeUnit}
                 onChange={(e) => {
                    setTimeUnit(e.target.value);
                    setTimeValue("1"); // Reset value when unit changes to avoid out of bounds
                 }}
               >
                 <option value="Days">Days</option>
                 <option value="Weeks">Weeks</option>
                 <option value="Months">Months</option>
                 <option value="Years">Years</option>
               </select>
             </div>
           </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || formData.skills.length === 0 || formData.interests.length === 0 || (formData.goal === "other" && !formData.custom_goal)}
          className="w-full bg-gradient-to-r from-indigo-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin" /> Generating Magic...
            </>
          ) : (
            <>
              Generate Project Plan <ArrowRight size={20} />
            </>
          )}
        </button>
      </form>
    </motion.div>
  );
}
