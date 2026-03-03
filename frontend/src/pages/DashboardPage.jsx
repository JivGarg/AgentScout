import { useState, useRef } from 'react';
import { HiOutlineGlobeAlt, HiOutlineStop, HiOutlineInformationCircle, HiOutlineCheckCircle, HiOutlineXCircle } from 'react-icons/hi';
import toast from 'react-hot-toast';
import { researchApi } from '../services/api';
import ScanningLoader from '../components/ScanningLoader';
import ResearchCard from '../components/ResearchCard';

export default function DashboardPage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const abortRef = useRef(null);

  const isLinkedIn = url.toLowerCase().includes('linkedin.com');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    // Basic URL validation
    let targetUrl = url.trim();
    if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
      targetUrl = 'https://' + targetUrl;
    }

    // Create AbortController for cancellation
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setResult(null);
    try {
      const { data } = await researchApi.analyze(targetUrl, controller.signal);
      setResult(data);
      toast.success('Research complete!');
    } catch (err) {
      if (err.code === 'ERR_CANCELED' || err.name === 'CanceledError') {
        toast('Analysis stopped', { icon: '🛑' });
      } else {
        toast.error(err.response?.data?.detail || 'Analysis failed. Try again.');
      }
    } finally {
      setLoading(false);
      abortRef.current = null;
    }
  };

  const handleStop = () => {
    if (abortRef.current) {
      abortRef.current.abort();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-white mb-2">
          Research a Company
        </h1>
        <p className="text-gray-500">
          Enter a company URL to get instant AI-powered research and a personalized outreach email
        </p>
      </div>

      {/* Search Bar – Glassmorphism Style */}
      <form onSubmit={handleAnalyze} className="mb-4">
        <div className="glass-card p-2 flex items-center gap-2">
          <div className="flex items-center gap-3 flex-1 px-4">
            <HiOutlineGlobeAlt className="text-2xl text-primary-400 flex-shrink-0" />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter company URL (e.g., stripe.com)"
              className="flex-1 bg-transparent text-lg text-white placeholder-gray-500 outline-none py-3"
              disabled={loading}
            />
          </div>
          {loading ? (
            <button
              type="button"
              onClick={handleStop}
              className="flex items-center gap-2 bg-red-600/90 hover:bg-red-500 text-white font-semibold
                px-8 py-4 rounded-xl transition-all duration-200 hover:shadow-lg hover:shadow-red-500/25
                active:scale-[0.98] flex-shrink-0"
            >
              <HiOutlineStop className="text-lg" />
              Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={!url.trim()}
              className="btn-primary flex-shrink-0"
            >
              Analyze
            </button>
          )}
        </div>
      </form>

      {/* LinkedIn Warning – shown only when a LinkedIn URL is detected */}
      {isLinkedIn && (
        <div className="mb-8 rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-4 space-y-3">
          <div className="flex items-center gap-2 text-yellow-400 font-semibold text-sm">
            <HiOutlineInformationCircle className="text-lg flex-shrink-0" />
            LinkedIn — Public Data Only (no account required)
          </div>
          <p className="text-xs text-gray-500 leading-relaxed">
            This tool scrapes LinkedIn <strong className="text-gray-400">without logging in</strong> to any account.
            No LinkedIn credentials are stored or used. Only publicly visible data is accessible.
          </p>
          <div className="grid grid-cols-2 gap-3 pt-1">
            <div>
              <p className="text-xs font-semibold text-emerald-400 mb-1.5 flex items-center gap-1">
                <HiOutlineCheckCircle /> What you'll get
              </p>
              <ul className="space-y-1">
                {[
                  'Company name & description',
                  'Industry, size & location',
                  'Company updates & posts',
                  'Public job listings',
                  'Headline / about section (partial)',
                ].map((item) => (
                  <li key={item} className="flex items-start gap-1.5 text-xs text-gray-400">
                    <span className="mt-1 w-1 h-1 rounded-full bg-emerald-500 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-xs font-semibold text-red-400 mb-1.5 flex items-center gap-1">
                <HiOutlineXCircle /> Not accessible without login
              </p>
              <ul className="space-y-1">
                {[
                  'Full work history & experience',
                  'Contact info & email addresses',
                  '2nd / 3rd degree connections',
                  'Private profiles',
                  'LinkedIn Sales Navigator data',
                ].map((item) => (
                  <li key={item} className="flex items-start gap-1.5 text-xs text-gray-400">
                    <span className="mt-1 w-1 h-1 rounded-full bg-red-500 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && <ScanningLoader />}

      {/* Results */}
      {!loading && result && <ResearchCard research={result} />}

      {/* Empty State */}
      {!loading && !result && (
        <div className="text-center py-20">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-primary-600/10 flex items-center justify-center">
            <HiOutlineGlobeAlt className="text-4xl text-primary-500" />
          </div>
          <h3 className="text-xl font-semibold text-gray-400 mb-2">
            Ready to Research
          </h3>
          <p className="text-gray-600 max-w-sm mx-auto">
            Enter any company URL above and let AI do the heavy lifting. Get a full company
            breakdown and outreach email in seconds.
          </p>
        </div>
      )}
    </div>
  );
}
