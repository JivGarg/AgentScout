import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { HiOutlineSearch, HiOutlineClock, HiOutlineLogout, HiOutlineDocumentText } from 'react-icons/hi';

export default function Layout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex">
      {/* ── Sidebar ──────────────────────────────────────────── */}
      <aside className="w-64 bg-dark-900/50 border-r border-white/5 p-6 flex flex-col">
        {/* Logo */}
        <div className="mb-10">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
            AgentScout
          </h1>
          <p className="text-xs text-gray-500 mt-1">Deep Research Outreach</p>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 space-y-2">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-500/20'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <HiOutlineSearch className="text-xl" />
            <span className="font-medium">Research</span>
          </NavLink>

          <NavLink
            to="/history"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-500/20'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <HiOutlineClock className="text-xl" />
            <span className="font-medium">History</span>
          </NavLink>

          <NavLink
            to="/resume"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-500/20'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <HiOutlineDocumentText className="text-xl" />
            <span className="font-medium">Resume Tester</span>
          </NavLink>
        </nav>

        {/* User Section */}
        <div className="border-t border-white/5 pt-4">
          <div className="flex items-center justify-between">
            <div className="truncate">
              <p className="text-sm text-gray-300 truncate">{user?.email || 'User'}</p>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 text-gray-500 hover:text-red-400 transition-colors rounded-lg hover:bg-red-500/10"
              title="Logout"
            >
              <HiOutlineLogout className="text-xl" />
            </button>
          </div>
        </div>
      </aside>

      {/* ── Main Content ─────────────────────────────────────── */}
      <main className="flex-1 overflow-auto p-8">
        <Outlet />
      </main>
    </div>
  );
}
