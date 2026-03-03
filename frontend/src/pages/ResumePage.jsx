import { useState } from 'react';
import {
  HiOutlineDocumentText,
  HiOutlineCheckCircle,
  HiOutlineXCircle,
  HiOutlineLightBulb,
  HiOutlineSparkles,
  HiOutlineRefresh,
} from 'react-icons/hi';
import toast from 'react-hot-toast';
import { resumeApi } from '../services/api';

// ── Score Ring ────────────────────────────────────────────────
function ScoreRing({ score, grade }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const gradeColors = {
    A: 'text-emerald-400',
    B: 'text-primary-400',
    C: 'text-yellow-400',
    D: 'text-orange-400',
    F: 'text-red-400',
  };
  const strokeColors = {
    A: '#34d399',
    B: '#818cf8',
    C: '#facc15',
    D: '#fb923c',
    F: '#f87171',
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="140" height="140" className="rotate-[-90deg]">
        <circle
          cx="70" cy="70" r={radius}
          fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="10"
        />
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke={strokeColors[grade] || '#818cf8'}
          strokeWidth="10"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
        />
      </svg>
      <div className="absolute flex flex-col items-center" style={{ marginTop: '40px' }}>
        <span className={`text-4xl font-black ${gradeColors[grade] || 'text-white'}`}>
          {score}
        </span>
        <span className="text-xs text-gray-500 font-semibold tracking-widest uppercase">/ 100</span>
      </div>
      <div className={`text-5xl font-black -mt-2 ${gradeColors[grade] || 'text-white'}`}>
        {grade}
      </div>
    </div>
  );
}

// ── Section Score Bar ─────────────────────────────────────────
function SectionBar({ section, score, feedback, suggestions }) {
  const [open, setOpen] = useState(false);
  const color =
    score >= 80 ? 'bg-emerald-500' :
    score >= 60 ? 'bg-primary-500' :
    score >= 40 ? 'bg-yellow-500' :
    'bg-red-500';

  return (
    <div
      className="glass-card p-4 cursor-pointer hover:border-white/10 transition-colors"
      onClick={() => setOpen((v) => !v)}
    >
      <div className="flex items-center gap-4">
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-gray-300">{section}</span>
            <span className="text-sm font-bold text-white">{score}/100</span>
          </div>
          <div className="h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              className={`h-full rounded-full ${color} transition-all duration-700`}
              style={{ width: `${score}%` }}
            />
          </div>
        </div>
      </div>

      {open && (
        <div className="mt-3 pt-3 border-t border-white/5 space-y-2">
          <p className="text-sm text-gray-400">{feedback}</p>
          {suggestions?.length > 0 && (
            <ul className="space-y-1">
              {suggestions.map((s, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-500">
                  <HiOutlineLightBulb className="text-yellow-400 flex-shrink-0 mt-0.5" />
                  {s}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

// ── Results Panel ─────────────────────────────────────────────
function ResumeResults({ result, onReset }) {
  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header row: score + summary */}
      <div className="glass-card p-8 flex flex-col md:flex-row items-center gap-8">
        <div className="relative flex flex-col items-center">
          <ScoreRing score={result.overall_score} grade={result.grade} />
        </div>
        <div className="flex-1">
          <h2 className="text-xl font-bold text-white mb-3">Overall Assessment</h2>
          <p className="text-gray-400 leading-relaxed">{result.summary}</p>
          <button
            onClick={onReset}
            className="mt-5 flex items-center gap-2 text-sm text-gray-500 hover:text-primary-400 transition-colors"
          >
            <HiOutlineRefresh />
            Test another resume
          </button>
        </div>
      </div>

      {/* Section Scores */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
          <HiOutlineDocumentText className="text-primary-400" />
          Section Breakdown
          <span className="text-xs text-gray-500 font-normal">(click a row to expand)</span>
        </h3>
        <div className="space-y-2">
          {result.section_scores?.map((s) => (
            <SectionBar key={s.section} {...s} />
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Red Flags */}
        {result.red_flags?.length > 0 && (
          <div className="glass-card p-5">
            <h3 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
              <HiOutlineXCircle className="text-lg" />
              Red Flags Detected
            </h3>
            <ul className="space-y-2">
              {result.red_flags.map((f, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-400">
                  <span className="mt-1 w-1.5 h-1.5 rounded-full bg-red-500 flex-shrink-0" />
                  <span>"{f}"</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Strong Points */}
        {result.strong_points?.length > 0 && (
          <div className="glass-card p-5">
            <h3 className="text-sm font-semibold text-emerald-400 mb-3 flex items-center gap-2">
              <HiOutlineCheckCircle className="text-lg" />
              Strong Points
            </h3>
            <ul className="space-y-2">
              {result.strong_points.map((p, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-400">
                  <span className="mt-1 w-1.5 h-1.5 rounded-full bg-emerald-500 flex-shrink-0" />
                  {p}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* XYZ Rewrites */}
      {result.rewritten_bullets?.length > 0 && (
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-primary-400 mb-3 flex items-center gap-2">
            <HiOutlineSparkles className="text-lg" />
            AI-Rewritten Bullets (XYZ Formula)
          </h3>
          <p className="text-xs text-gray-600 mb-3">
            Format: [Action Verb] + [Specific Task] + [Quantifiable Result]
          </p>
          <ul className="space-y-3">
            {result.rewritten_bullets.map((b, i) => (
              <li
                key={i}
                className="text-sm text-gray-300 bg-primary-600/10 border border-primary-500/20 rounded-xl px-4 py-3 leading-relaxed"
              >
                {b}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────
export default function ResumePage() {
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!resumeText.trim()) return;

    setLoading(true);
    setResult(null);
    try {
      const { data } = await resumeApi.analyze(resumeText);
      setResult(data);
      toast.success('Resume analyzed!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setResumeText('');
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-white mb-2">Resume Tester</h1>
        <p className="text-gray-500">
          Paste your resume text below. Our AI scores every section, flags weak language,
          and rewrites your worst bullets using the XYZ formula.
        </p>
      </div>

      {/* Input Form – hidden when results are shown */}
      {!result && (
        <form onSubmit={handleAnalyze} className="space-y-4">
          <div className="glass-card p-1">
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder={`Paste your full resume text here…\n\nExample bullet point that will be detected as weak:\n"Responsible for managing social media accounts"\n\nWill be rewritten to:\n"Orchestrated social media strategy across 4 platforms, growing engagement by 38% in Q2"`}
              rows={18}
              className="w-full bg-transparent text-gray-300 placeholder-gray-600 text-sm leading-relaxed
                         px-5 py-4 outline-none resize-none"
              disabled={loading}
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-600">
              {resumeText.length.toLocaleString()} / 15,000 characters
            </span>
            <button
              type="submit"
              disabled={loading || resumeText.trim().length < 50}
              className="btn-primary flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Analyzing…
                </>
              ) : (
                <>
                  <HiOutlineSparkles />
                  Analyze Resume
                </>
              )}
            </button>
          </div>
        </form>
      )}

      {/* Results */}
      {!loading && result && <ResumeResults result={result} onReset={handleReset} />}

      {/* Empty State */}
      {!loading && !result && resumeText.length === 0 && (
        <div className="mt-10 text-center py-12 border border-dashed border-white/5 rounded-2xl">
          <HiOutlineDocumentText className="text-5xl text-gray-700 mx-auto mb-4" />
          <p className="text-gray-600 text-sm max-w-xs mx-auto">
            Your analysis will appear here. Scores are based on recruiter best practices:
            measurable impact, strong action verbs, XYZ bullets, and clean structure.
          </p>
        </div>
      )}
    </div>
  );
}
