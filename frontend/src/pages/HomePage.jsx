import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import FileUpload from '../components/common/FileUpload';
import TeamSelect from '../components/team/TeamSelect';
import ResultsList from '../components/common/ResultsList';

export default function HomePage() {
  const { user } = useAuth();
  const [results, setResults] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);

  const handleFileUpload = async (file) => {
    try {
      // TODO: Implement file processing logic
      // This will be implemented in Task 4
      console.log('Processing file:', file);
      // Mock results for now
      setResults([]);
    } catch (error) {
      console.error('Error processing file:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900">
                Problem Statement Finder
              </h1>
            </div>

            {/* Main Content */}
            <div className="space-y-6">
              {/* Top Controls */}
              <div className="flex flex-col sm:flex-row justify-between gap-4">
                <FileUpload onUpload={handleFileUpload} />
                <TeamSelect 
                  selectedTeam={selectedTeam} 
                  onSelect={setSelectedTeam} 
                />
              </div>

              {/* Results Section */}
              <div className="mt-8">
                <h2 className="text-lg font-semibold mb-4">
                  Top-10 Results, rank wise
                </h2>
                <div className="bg-white rounded-lg border border-gray-200">
                  <ResultsList results={results} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}