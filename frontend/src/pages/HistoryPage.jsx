import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { HiOutlineClock, HiOutlineTrash, HiOutlineExternalLink } from 'react-icons/hi';
import toast from 'react-hot-toast';
import { researchApi } from '../services/api';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const { data } = await researchApi.getHistory();
      setHistory(data);
    } catch (err) {
      toast.error('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    try {
      await researchApi.deleteById(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      toast.success('Deleted');
    } catch {
      toast.error('Delete failed');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Research History</h1>
        <p className="text-gray-500">View and manage your previous research results</p>
      </div>

      {/* History List */}
      {history.length === 0 ? (
        <div className="text-center py-20">
          <HiOutlineClock className="text-5xl text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-400 mb-2">No history yet</h3>
          <p className="text-gray-600">Your research results will appear here</p>
        </div>
      ) : (
        <div className="space-y-3">
          {history.map((item) => (
            <div
              key={item.id}
              onClick={() => navigate(`/result/${item.id}`)}
              className="glass-card p-5 cursor-pointer hover:bg-white/[0.08] transition-all duration-200 group"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="font-semibold text-white truncate">
                      {item.company_name || 'Unknown Company'}
                    </h3>
                    <HiOutlineExternalLink className="text-gray-600 group-hover:text-primary-400 transition-colors flex-shrink-0" />
                  </div>
                  <p className="text-sm text-gray-500 truncate">{item.target_url}</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {new Date(item.timestamp).toLocaleString()}
                  </p>
                </div>
                <button
                  onClick={(e) => handleDelete(item.id, e)}
                  className="p-2 text-gray-600 hover:text-red-400 transition-colors rounded-lg hover:bg-red-500/10 ml-4"
                >
                  <HiOutlineTrash />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
