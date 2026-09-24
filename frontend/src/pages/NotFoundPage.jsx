import { Link } from 'react-router-dom';
import { HiOutlineExclamationCircle } from 'react-icons/hi';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-card p-10 w-full max-w-md text-center">
        <HiOutlineExclamationCircle className="text-6xl text-primary-400 mx-auto mb-4" />
        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
          404
        </h1>
        <p className="text-gray-300 mt-3 text-lg">Page not found</p>
        <p className="text-gray-500 mt-2 text-sm">
          The page you're looking for doesn't exist or may have moved.
        </p>
        <Link to="/" className="btn-primary inline-block mt-8">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
}
