import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm z-10">
      <div className="flex items-center justify-between h-16 px-6">
        <h1 className="text-xl font-semibold text-gray-800">ML Trading System</h1>
        <div className="flex items-center space-x-4">
          {/* User profile, notifications, etc. */}
          <button className="p-1 rounded-full text-gray-600 hover:text-gray-900 focus:outline-none">
            <span className="sr-only">View notifications</span>
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 00-6-6H9a6 6 0 00-6 6v3.159c0 .538-.214 1.055-.595 1.436L1 17h5m0 0h6m-6 0v3m6-3v3" />
            </svg>
          </button>
          <div className="relative">
            <button className="flex items-center text-sm font-medium text-gray-700 rounded-full hover:text-gray-900 focus:outline-none">
              <span className="sr-only">Open user menu</span>
              <div className="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700">
                U
              </div>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
