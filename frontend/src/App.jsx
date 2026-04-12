import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import Hero from './components/Hero';
import GeneratorForm from './components/GeneratorForm';
import IdeaPicker from './components/IdeaPicker';
import FullPlan from './components/FullPlan';
import Layout from './components/Layout';
import { generateIdeas, expandIdea } from './services/api';

function App() {
  const [step, setStep] = useState('form'); // 'form', 'picker', 'plan'
  const [formData, setFormData] = useState(null);
  const [ideas, setIdeas] = useState([]);
  const [plan, setPlan] = useState(null);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateIdeas = async (data) => {
    setFormData(data);
    setLoading(true);
    setError(null);
    try {
      const result = await generateIdeas(data);
      setIdeas(result.ideas);
      setStep('picker');
      setTimeout(() => {
        document.getElementById('picker-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error(err);
      const message = err.response?.data?.detail || "Failed to generate ideas. Please try again or check your API key.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectIdea = async (selectedIdea) => {
    setLoading(true);
    setError(null);
    try {
      const result = await expandIdea(formData, selectedIdea);
      setPlan(result);
      setStep('plan');
      setTimeout(() => {
        document.getElementById('plan-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error(err);
      const message = err.response?.data?.detail || "Failed to generate plan. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleBackToForm = () => {
    setStep('form');
    setIdeas([]);
    setPlan(null);
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 pb-20">
        <AnimatePresence mode="wait">
          {step === 'form' && (
            <motion.div
              key="hero"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
              transition={{ duration: 0.3 }}
            >
               <Hero />
            </motion.div>
          )}
        </AnimatePresence>
        
        <AnimatePresence mode="wait">
          {step === 'form' && (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              <GeneratorForm onSubmit={handleGenerateIdeas} isLoading={loading} />
            </motion.div>
          )}

          {step === 'picker' && (
            <motion.div
              key="picker"
              id="picker-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="mt-10"
            >
              <IdeaPicker 
                ideas={ideas} 
                onSelect={handleSelectIdea} 
                onBack={handleBackToForm}
                isLoading={loading}
              />
            </motion.div>
          )}

          {step === 'plan' && plan && (
            <motion.div
              key="plan"
              id="plan-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
              className="mt-10"
            >
              <div className="mb-8 flex justify-center">
                <button
                  onClick={() => setStep('picker')}
                  className="text-slate-400 hover:text-white transition-colors flex items-center gap-2"
                >
                  <span className="text-xl">←</span> Back to Idea Selection
                </button>
              </div>
              <FullPlan plan={plan} />
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="max-w-2xl mx-auto mt-8 p-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-lg text-center"
          >
            {error}
          </motion.div>
        )}
      </div>
    </Layout>
  );
}

export default App;
