export default function ScanningLoader() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      {/* Scanning Animation */}
      <div className="relative w-32 h-32 mb-8">
        {/* Outer ring */}
        <div className="absolute inset-0 rounded-full border-2 border-primary-500/30 animate-ping" />
        {/* Middle ring */}
        <div className="absolute inset-4 rounded-full border-2 border-primary-400/50 animate-pulse" />
        {/* Inner dot */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-8 h-8 rounded-full bg-primary-500 animate-glow" />
        </div>
        {/* Scan line */}
        <div className="absolute inset-0 overflow-hidden rounded-full">
          <div className="w-full h-1 bg-gradient-to-r from-transparent via-primary-400 to-transparent scan-line" />
        </div>
      </div>

      {/* Text */}
      <h3 className="text-xl font-semibold text-primary-400 mb-2">
        Scanning Target...
      </h3>
      <p className="text-gray-500 text-sm max-w-xs text-center">
        Scraping website, analyzing content, and generating personalized outreach
      </p>

      {/* Progress Steps */}
      <div className="mt-8 space-y-3">
        {['Scraping website content...', 'Analyzing with AI...', 'Generating outreach email...'].map(
          (step, i) => (
            <div key={i} className="flex items-center gap-3 text-sm text-gray-400">
              <div
                className="w-2 h-2 rounded-full bg-primary-500 animate-pulse"
                style={{ animationDelay: `${i * 0.5}s` }}
              />
              {step}
            </div>
          )
        )}
      </div>
    </div>
  );
}
