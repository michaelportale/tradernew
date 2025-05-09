import React from 'react';

const DataExplorer: React.FC = () => {
  return (
    <div className="container mx-auto">
      <h2 className="text-2xl font-semibold text-gray-700 mb-6">Data Explorer</h2>
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Symbol
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              placeholder="AAPL"
              defaultValue="AAPL"
            />
            <button
              type="button"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Fetch Data
            </button>
          </div>
        </div>

        <div className="bg-gray-100 p-4 rounded-md mb-4">
          <p className="text-gray-500 text-sm italic">
            No data loaded. Please select a symbol and fetch data.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DataExplorer;
