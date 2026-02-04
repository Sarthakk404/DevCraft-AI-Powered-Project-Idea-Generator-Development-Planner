import { useState } from 'react';
import Hero from './components/Hero';
import GeneratorForm from './components/GeneratorForm';
import FullPlan from './components/FullPlan';
import Layout from './components/Layout';
import { generateFullPlan } from './services/api';

function App() {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      // In a real app we might generate ideas first, then let user pick
      // For this MVP we generate full plan directly
      const result = await generateFullPlan(formData);
      setPlan(result);
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error(err);
      const message = err.response?.data?.detail || "Failed to generate plan. Please try again or check your API key.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 pb-20">
        <Hero />
        
        <GeneratorForm onSubmit={handleGenerate} isLoading={loading} />

        {error && (
          <div className="max-w-2xl mx-auto mt-8 p-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-lg text-center">
            {error}
          </div>
        )}

        {/* Results Section */}
        {plan && (
          <div id="results-section" className="mt-32 pt-10 border-t border-white/5">
            <FullPlan plan={plan} />
          </div>
        )}
      </div>
    </Layout>
  );
}

export default App;
